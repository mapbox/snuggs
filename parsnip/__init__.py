import operator
import re
import sys

from pyparsing import (
    alphanums, ZeroOrMore, nums, oneOf, Word, Literal, Combine,
    ParseException, Forward, Group, CaselessLiteral, Optional, alphas)

import numpy


# Python 2-3 compatibility
string_types = (str,) if sys.version_info[0] >= 3 else (basestring,)


class Context(object):

    def __init__(self):
        self._data = {}

    def add(self, name, val):
        self._data[name] = val

    def get(self, args):
        index = args.pop(0)
        subindex = args.pop(0) if args else None
        if index in self._data:
            s = self._data[index]
        else:
            s = self._data.values()[int(index)-1]
        if subindex:
            return s[int(subindex)-1]
        else:
            return s

    def clear(self):
        self._data = {}

_ctx = Context()


class ctx(object):

    def __init__(self, **kwds):
        self.kwds = kwds

    def __enter__(self):
        _ctx.clear()
        for k, v in self.kwds.items():
            _ctx.add(k, v)
        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.kwds = None
        _ctx.clear()


op_map = {
    '*': operator.mul,
    '+': operator.add,
    '/': operator.div,
    '-': operator.sub
    }

func_map = {
    'list': numpy.asanyarray,
    'ra': _ctx.get
    }

expr = Forward()

# Definition of the grammar.
decimal = Literal('.')
e = CaselessLiteral('E')
sign = Literal('+') | Literal('-')
number = Word(nums)
name = Word(alphas)

integer = Combine(
    Optional(sign) +
    number
    ).setParseAction(lambda s, l, t: int(t[0]))

real = Combine(
    integer +
    decimal + Optional(number) +
    Optional(e + integer)
    ).setParseAction(lambda s, l, t: float(t[0]))

lparen = Literal('(').suppress()
rparen = Literal(')').suppress()

op = oneOf('+ - * /').setResultsName('op').setParseAction(
    lambda s, l, t: op_map[t[0]])

func = Word(alphanums).setResultsName('func').setParseAction(
    lambda s, l, t: func_map[t[0]])

operand = expr | name | real | integer

expr << Group(
    lparen +
    (op | func) +
    operand +
    Optional(operand) +
    ZeroOrMore(expr) +
    rparen)


def processArg(arg):
    if isinstance(arg, string_types + (int, float, numpy.ndarray)):
        return arg
    else:
        return processList(arg)


def processList(lst):
    args = [processArg(x) for x in lst[1:]]
    if lst.op:
        return lst.op(*args)
    if lst.func:
        return lst.func(args)


def handleLine(line):
    result = expr.parseString(line)
    return processList(result[0])
