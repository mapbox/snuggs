import numpy

import parsnip


def test_integer():
    assert list(parsnip.integer.parseString('1')) == [1]

def test_real():
    assert list(parsnip.real.parseString('1.1')) == [1.1]

def test_shortname():
    assert list(parsnip.name.parseString('a')) == ['a']

def test_arr_shortname():
    parsnip.ctx.add('foo', numpy.ones((2, 2)))
    r = parsnip.handleLine('(ra foo)')
    assert list(r.flatten()) == [1, 1, 1, 1]

def test_arr_index():
    parsnip.ctx.add('foo', numpy.ones((2, 2)))
    r = parsnip.handleLine('(ra 1)')
    assert list(r.flatten()) == [1, 1, 1, 1]

def test_arr_slice():
    parsnip.ctx.add('foo', numpy.ones((2, 2)))
    r = parsnip.handleLine('(ra 1 1)')
    assert list(r.flatten()) == [1, 1]

def test_int_expr():
    assert parsnip.handleLine('(+ 1 2)') == 3

def test_real_expr():
    assert round(parsnip.handleLine('(* 0.1 0.2)'), 3) == 0.02

def test_int_real_expr():
    assert parsnip.handleLine('(+ 2 1.1)') == 3.1

def test_real_int_expr():
    assert parsnip.handleLine('(+ 1.1 2)') == 3.1

def test_int_arr_expr():
    parsnip.ctx.add('foo', numpy.ones((2, 2)))
    result = parsnip.handleLine('(+ (ra 1) 1)')
    assert list(result.flatten()) == [2, 2, 2, 2]

def test_int_arr_expr_by_name():
    parsnip.ctx.add('foo', numpy.ones((2, 2)))
    result = parsnip.handleLine('(+ (ra foo) 1.5)')
    assert list(result.flatten()) == [2.5, 2.5, 2.5, 2.5]

def test_int_arr_slice_expr_by_name():
    parsnip.ctx.add('foo', numpy.ones((2, 2)))
    result = parsnip.handleLine('(+ (ra foo 1) 1.5)')
    assert list(result.flatten()) == [2.5, 2.5]

def test_list():
    parsnip.ctx.add('foo', numpy.ones((2, 2)))
    result = parsnip.handleLine('(list (ra foo 1) (ra foo 1) (ra foo 1) (ra foo 1))')
    assert list(result.flatten()) == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
