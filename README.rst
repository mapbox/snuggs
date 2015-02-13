=======
parsnip
=======

Parsnip parses and evaluates lisp-like Numpy expressions.

It is based on several pyparsing examples.

Expression syntax
=================

Expressions have the following syntax:

.. code-block::

    expr: ( (op | func) operand* )
    operand: ( expr | name | number | string )

Formal grammar is a TODO. Meanwhile, see the examples below.

Examples
========

Add two numbers

.. code-block:: python

    import parsnip
    print parsnip.eval('(+ 1 2)')
    # Output:
    # 3

Add a number and an array

.. code-block:: python

    import numpy
    print parsnip.eval('(+ 2.5 foo)', foo=numpy.ones((2, 2)))
    # Output:
    # [[ 3.5  3.5]
    #  [ 3.5  3.5]]

Functions and operators
=======================

Arithmetic (``* + / -``) and logical (``< <= == != >= > & |``) operators are
available. Members of the ``numpy`` module such as ``mean()`` and ``where()``
are also available.

.. code-block:: python

    print parsnip.eval('(> (+ foo (mean foo)) 1)', foo=numpy.ones((2, 2)))
    # Output:
    # array([[ True,  True],
    #        [ True,  True]], dtype=bool)


.. code-block:: python

    print parsnip.eval('(where (& tt tf) 1 0)',
        tt=numpy.array([True, True]),
        tf=numpy.array([True, False]))
    # Output:
    # [1 0]

Performance notes
=================

Parsnip makes simple calculator programs possible. None of the optimizations
of, e.g., `numexpr <https://github.com/pydata/numexpr>`__ (multithreading,
elimination of temporary data, etc) exist.
