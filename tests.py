import numpy

import parsnip


def test_integer():
    assert list(parsnip.integer.parseString('1')) == [1]

def test_real():
    assert list(parsnip.real.parseString('1.1')) == [1.1]

def test_filename():
    assert list(parsnip.filename.parseString('tests/data/RGB.byte.tif')) == ['tests/data/RGB.byte.tif']

def test_shortname():
    assert list(parsnip.shortname.parseString('a')) == ['a']

def test_index():
    assert list(parsnip.index.parseString('1')) == [0]

def test_arr_filename():
    parsnip.sources.addSource('/foo/bar.tif', numpy.ones((2, 2)))
    r = parsnip.array.parseString('[/foo/bar.tif]')
    assert list(r[0].flatten()) == [1, 1, 1, 1]

def test_arr_shortname():
    parsnip.sources.addSource('f', numpy.ones((2, 2)))
    r = parsnip.array.parseString('[f]')
    assert list(r[0].flatten()) == [1, 1, 1, 1]

def test_arr_index():
    parsnip.sources.addSource('/foo/bar.tif', numpy.ones((2, 2)))
    r = parsnip.array.parseString('[1]')
    assert list(r[0].flatten()) == [1, 1, 1, 1]

def test_arr_slice():
    parsnip.sources.addSource('/foo/bar.tif', numpy.ones((2, 2)))
    r = parsnip.array.parseString('[1,1]')
    assert list(r[0].flatten()) == [1, 1]

def test_int_expr():
    assert parsnip.handleLine('(+ 1 2)') == 3

def test_real_expr():
    assert round(parsnip.handleLine('(* 0.1 0.2)'), 3) == 0.02

def test_int_real_expr():
    assert parsnip.handleLine('(+ 2 1.1)') == 3.1

def test_real_int_expr():
    assert parsnip.handleLine('(+ 1.1 2)') == 3.1

def test_int_arr_expr():
    parsnip.sources.addSource('foo', numpy.ones((2, 2)))
    result = parsnip.handleLine('(+ [1] 1)')
    assert list(result.flatten()) == [2, 2, 2, 2]

def test_int_arr_expr_by_name():
    parsnip.sources.addSource('foo', numpy.ones((2, 2)))
    result = parsnip.handleLine('(+ [foo] 1.5)')
    assert list(result.flatten()) == [2.5, 2.5, 2.5, 2.5]

def test_int_arr_slice_expr_by_name():
    parsnip.sources.addSource('foo', numpy.ones((2, 2)))
    result = parsnip.handleLine('(+ [foo,1] 1.5)')
    assert list(result.flatten()) == [2.5, 2.5]

def test_dstack():
    parsnip.sources.addSource('foo', numpy.ones((2, 2)))
    result = parsnip.handleLine('(dstack (+ [foo,1] 1.5) [foo,1])')
    assert list(result.flatten()) == [2.5, 1.0, 2.5, 1.0]
