"""
Snuggs are s-expressions for Numpy.
"""

import functools
import itertools
import operator
import re
import sys

from pyparsing import (
    alphanums, ZeroOrMore, nums, oneOf, Word, Literal, Combine, QuotedString,
    ParseException, Forward, Group, CaselessLiteral, Optional, alphas,
    OneOrMore, ParseResults)

import numpy


__all__ = ['eval']
__version__ = "1.1.0"

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

def asarray(*args):
    if len(args) == 1 and hasattr(args[0], '__iter__'):
        return numpy.asanyarray(list(args[0]))
    else:
        return numpy.asanyarray(list(args))

func_map = {
    'asarray': asarray,
    'read': _ctx.lookup,
    'take': lambda a, idx: numpy.take(a, idx-1, axis=0),
    }

higher_func_map = {
    'map': map if sys.version_info[0] >= 3 else itertools.imap,
    'partial': functools.partial,
    }

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

op = oneOf(' '.join(op_map.keys())).setParseAction(
    lambda s, l, t: op_map[t[0]])

func = Word(alphanums + '_').setParseAction(
    lambda s, l, t: (
        func_map[t[0]] if t[0] in func_map else getattr(numpy, t[0])))

higher_func = oneOf('map partial').setParseAction(
    lambda s, l, t: higher_func_map[t[0]])

func_expr = Forward()
higher_func_expr = Forward()
expr = higher_func_expr | func_expr

operand = higher_func_expr | func_expr | var | real | integer | string

func_expr << Group(
    lparen +
    (higher_func_expr | op | func ) +
    operand +
    ZeroOrMore(operand) +
    rparen)

higher_func_expr << Group(
    lparen +
    higher_func +
    (higher_func_expr | op | func) +
    ZeroOrMore(operand) +
    rparen)


def processArg(arg):
    if not isinstance(arg, ParseResults):
        return arg
    else:
        return processList(arg)


def processList(lst):
    args = [processArg(x) for x in lst[1:]]
    func = processArg(lst[0])
    return func(*args)


def handleLine(line):
    result = expr.parseString(line)
    return processList(result[0])


def eval(source, **kwds):
    with ctx(**kwds):
        return handleLine(source)
