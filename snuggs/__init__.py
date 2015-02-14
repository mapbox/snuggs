"""
Snuggs are s-expressions for Numpy.
"""


import operator
import re
import sys

from pyparsing import (
    alphanums, ZeroOrMore, nums, oneOf, Word, Literal, Combine, QuotedString,
    ParseException, Forward, Group, CaselessLiteral, Optional, alphas)

import numpy


__all__ = ['eval']
__version__ = "1.0"

# Python 2-3 compatibility
string_types = (str,) if sys.version_info[0] >= 3 else (basestring,)


class Context(object):

    def __init__(self):
        self._data = {}

    def add(self, name, val):
        self._data[name] = val

    def get(self, name):
        return self._data[name]

    def lookup(self, index, subindex=None):
        s = list(self._data.values())[int(index)-1]
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
    '/': operator.truediv if sys.version_info[0] >= 3 else operator.div,
    '-': operator.sub,
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt,
    '&': operator.and_,
    '|': operator.or_
    }

func_map = {
    'asarray': lambda *args: numpy.asanyarray(args),
    'read': _ctx.lookup,
    'take': lambda a, idx: numpy.take(a, idx-1, axis=0),
    }

expr = Forward()

# Definition of the grammar.
decimal = Literal('.')
e = CaselessLiteral('E')
sign = Literal('+') | Literal('-')
number = Word(nums)
name = Word(alphas)

var = name.setParseAction(
    lambda s, l, t: _ctx.get(t[0]))

integer = Combine(
    Optional(sign) +
    number
    ).setParseAction(lambda s, l, t: int(t[0]))

real = Combine(
    integer +
    decimal + Optional(number) +
    Optional(e + integer)
    ).setParseAction(lambda s, l, t: float(t[0]))

string = QuotedString("'") | QuotedString('"')

lparen = Literal('(').suppress()
rparen = Literal(')').suppress()

op = oneOf(' '.join(op_map.keys())).setResultsName('op').setParseAction(
    lambda s, l, t: op_map[t[0]])

func = Word(alphanums + '_').setResultsName('func').setParseAction(
    lambda s, l, t: (
        func_map[t[0]] if t[0] in func_map else getattr(numpy, t[0])))

operand = expr | var | real | integer | string

expr << Group(
    lparen +
    (op | func) +
    operand +
    ZeroOrMore(operand) +
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
        return lst.func(*args)


def handleLine(line):
    result = expr.parseString(line)
    return processList(result[0])


def eval(source, **kwds):
    with ctx(**kwds):
        return handleLine(source)
