import numpy
import pytest

import parsnip

# Fixtures follow the tests. See the end of the file.


def test_integer():
    assert list(parsnip.integer.parseString('1')) == [1]


def test_real():
    assert list(parsnip.real.parseString('1.1')) == [1.1]


def test_int_expr():
    assert parsnip.eval('(+ 1 2)') == 3


def test_real_expr():
    assert round(parsnip.eval('(* 0.1 0.2)'), 3) == 0.02


def test_int_real_expr():
    assert parsnip.eval('(+ 2 1.1)') == 3.1


def test_real_int_expr():
    assert parsnip.eval('(+ 1.1 2)') == 3.1


def test_arr_var(ones):
    r = parsnip.eval('(+ foo 0)', foo=ones)
    assert list(r.flatten()) == [1, 1, 1, 1]


def test_arr_lookup(ones):
    r = parsnip.eval('(read 1)', foo=ones)
    assert list(r.flatten()) == [1, 1, 1, 1]


def test_arr_lookup_2(ones):
    r = parsnip.eval('(read 1 1)', foo=ones)
    assert list(r.flatten()) == [1, 1]


def test_arr_take(ones):
    r = parsnip.eval('(take foo 1)', foo=ones)
    assert list(r.flatten()) == [1, 1]
    r = parsnip.eval('(take foo 2)', foo=ones)
    assert list(r.flatten()) == [1, 1]


def test_int_arr_expr(ones):
    result = parsnip.eval('(+ foo 1)', foo=ones)
    assert list(result.flatten()) == [2, 2, 2, 2]


def test_int_arr_expr_by_name(ones):
    result = parsnip.eval('(+ (read 1) 1.5)', foo=ones)
    assert list(result.flatten()) == [2.5, 2.5, 2.5, 2.5]


def test_int_arr_read(ones):
    result = parsnip.eval('(+ (read 1 1) 1.5)', foo=ones)
    assert list(result.flatten()) == [2.5, 2.5]


def test_list(ones):
    result = parsnip.eval(
        '(asarray (take foo 1) (take foo 1) (take bar 1) (take bar 1))',
        foo=ones, bar=ones)
    assert list(result.flatten()) == [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


def test_eq(ones):
    ones[0][0] = 2
    result = parsnip.eval('(== foo 1)', foo=ones)
    assert list(result.flatten()) == [False, True, True, True]


def test_or(truetrue, truefalse):
    result = parsnip.eval(
        '(| foo bar)', foo=truetrue, bar=truefalse)
    assert list(result.flatten()) == [True, True]


def test_and(truetrue, truefalse):
    result = parsnip.eval(
        '(& foo bar)', foo=truetrue, bar=truefalse)
    assert list(result.flatten()) == [True, False]


def test_ones_like(truefalse):
    result = parsnip.eval("(ones_like foo 'uint8')", foo=truefalse)
    assert list(result.flatten()) == [1.0, 1.0]


def test_full_like(truefalse):
    result = parsnip.eval("(full_like foo 3.14 'float64')", foo=truefalse)
    assert list(result.flatten()) == [3.14, 3.14]
    result = parsnip.eval('(full_like foo 3.14 "float64")', foo=truefalse)
    assert list(result.flatten()) == [3.14, 3.14]


def test_ufunc(truetrue, truefalse):
    result = parsnip.eval(
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
