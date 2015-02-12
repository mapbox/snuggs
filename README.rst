=======
parsnip
=======

Parsnip parses and evaluates lisp-like Numpy expressions.

It is based on several pyparsing examples.

Expression syntax
=================

Expressions have the following syntax:

.. code-block::

    expr: ( (op | func) operand operand* )
    operand: ( expr | name | number )

Formal grammar is a TODO. Meanwhile, see the examples below.

Examples
========

Add two numbers.

.. code-block:: python

    import parsnip
    print parsnip.handleLine('(+ 1 2)')
    # Output:
    # 3

Add two arrays.

.. code-block:: python

    import numpy
    import parsnip
    parsnip.ctx.add('foo', numpy.ones((2, 2)))
    parsnip.ctx.add('bar', numpy.ones((2, 2)))
    print parsnip.handleLine('(+ (ra foo) (* 2.5 (ra bar)))')
    # Output:
    # [[ 3.5  3.5]
    #  [ 3.5  3.5]]
