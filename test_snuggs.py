import numpy
import pytest

import snuggs

# Fixtures follow the tests. See the end of the file.


def test_integer():
    assert list(snuggs.integer.parseString('1')) == [1]


def test_real():
    assert list(snuggs.real.parseString('1.1')) == [1.1]


def test_int_expr():
    assert snuggs.eval('(+ 1 2)') == 3


def test_real_expr():
    assert round(snuggs.eval('(* 0.1 0.2)'), 3) == 0.02


def test_int_real_expr():
    assert snuggs.eval('(+ 2 1.1)') == 3.1


def test_real_int_expr():
    assert snuggs.eval('(+ 1.1 2)') == 3.1


def test_arr_var(ones):
    r = snuggs.eval('(+ foo 0)', foo=ones)
    assert list(r.flatten()) == [1, 1, 1, 1]


def test_arr_lookup(ones):
    r = snuggs.eval('(read 1)', foo=ones)
    assert list(r.flatten()) == [1, 1, 1, 1]


def test_arr_lookup_2(ones):
    r = snuggs.eval('(read 1 1)', foo=ones)
    assert list(r.flatten()) == [1, 1]


def test_arr_take(ones):
    r = snuggs.eval('(take foo 1)', foo=ones)
    assert list(r.flatten()) == [1, 1]
    r = snuggs.eval('(take foo 2)', foo=ones)
    assert list(r.flatten()) == [1, 1]


def test_int_arr_expr(ones):
    result = snuggs.eval('(+ foo 1)', foo=ones)
    assert list(result.flatten()) == [2, 2, 2, 2]


def test_int_arr_expr_by_name(ones):
    result = snuggs.eval('(+ (read 1) 1.5)', foo=ones)
    assert list(result.flatten()) == [2.5, 2.5, 2.5, 2.5]


def test_int_arr_read(ones):
    result = snuggs.eval('(+ (read 1 1) 1.5)', foo=ones)
    assert list(result.flatten()) == [2.5, 2.5]


def test_list(ones):
    result = snuggs.eval(
        '(asarray (take foo 1) (take foo 1) (take bar 1) (take bar 1))',
        foo=ones, bar=ones)
    assert list(result.flatten()) == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def test_eq(ones):
    ones[0][0] = 2
    result = snuggs.eval('(== foo 1)', foo=ones)
    assert list(result.flatten()) == [False, True, True, True]


def test_or(truetrue, truefalse):
    result = snuggs.eval(
        '(| foo bar)', foo=truetrue, bar=truefalse)
    assert list(result.flatten()) == [True, True]


def test_and(truetrue, truefalse):
    result = snuggs.eval(
        '(& foo bar)', foo=truetrue, bar=truefalse)
    assert list(result.flatten()) == [True, False]


def test_ones_like(truefalse):
    result = snuggs.eval("(ones_like foo 'uint8')", foo=truefalse)
    assert list(result.flatten()) == [1.0, 1.0]


def test_full_like(truefalse):
    result = snuggs.eval("(full_like foo 3.14 'float64')", foo=truefalse)
    assert list(result.flatten()) == [3.14, 3.14]
    result = snuggs.eval('(full_like foo 3.14 "float64")', foo=truefalse)
    assert list(result.flatten()) == [3.14, 3.14]


def test_ufunc(truetrue, truefalse):
    result = snuggs.eval(
        '(where (& foo bar) 1 0)', foo=truetrue, bar=truefalse)
    assert list(result.flatten()) == [1.0, 0.0]


# Fixtures.
@pytest.fixture
def ones():
    return numpy.ones((2, 2))


@pytest.fixture
def truetrue():
    return numpy.array([True, True])


@pytest.fixture
def truefalse():
    return numpy.array([True, False])
