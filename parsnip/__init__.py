import logging
import operator
import re
import sys

from pyparsing import (
    alphanums, OneOrMore, nums, oneOf, Word, Literal, Suppress, Combine,
    ParseException, Forward, Group, CaselessLiteral, Optional, alphas, Regex)

import numpy

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger('calc')


class Sources(object):

    def __init__(self):
        self._sources = {}

    def addSource(self, name, val):
        self._sources[name] = val

    def getSource(self, index):
        parts = index.split(',')
        index = parts.pop(0)
        subindex = parts.pop(0) if parts else None
        if index in self._sources:
            s = self._sources[index]
        else:
            s = self._sources.values()[int(index)-1]
        if subindex:
            return s[subindex]
        else:
            return s

sources = Sources()

op_map = {
    '*': operator.mul,
    '+': operator.add,
    '/': operator.div,
    '-': operator.sub}

expr = Forward()

# Definition of the grammar.
decimal = Literal('.')
e = CaselessLiteral('E')
sign = Literal('+') | Literal('-')
number = Word(nums)

integer = Combine(
    Optional(sign) +
    number
    ).setParseAction(lambda s, l, t: int(t[0]))

real = Combine(
    integer +
    Optional(decimal + Optional(number)) +
    Optional(e + integer)
    ).setParseAction(lambda s, l, t: float(t[0]))

filename = Word(alphanums + "/-_. ")
shortname = Word(alphas)
index = Word(nums).setParseAction(lambda s, l, t: int(t[0])-1)

lbracket = Literal('[').suppress()
rbracket = Literal(']').suppress()

array = Combine(
    lbracket +
    (filename | shortname | index) +
    Optional(Literal(',') + index) +
    rbracket
    ).setParseAction(lambda s, l, t: sources.getSource(t[0]))

lparen = Literal('(').suppress()
rparen = Literal(')').suppress()

op = oneOf('+ - * /').setResultsName('op').setParseAction(
    lambda s, l, t: op_map[t[0]])

func = Word(alphanums).setResultsName('func').setParseAction(
    lambda s, l, t: getattr(numpy, t[0]))

operand = expr | array | real | integer

expr << Group(lparen + (op | func) + operand + OneOrMore(operand) + rparen)


def processArg(arg):
    if isinstance(arg, (int, float, numpy.ndarray)):
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
