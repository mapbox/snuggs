=======
parsnip
=======

Parsnip parses and evaluates lisp-like Numpy expressions.

It is based on several pyparsing examples.

Expression syntax
=================

Expressions have the following syntax:

.. code-block::

    expr: ( op operand operand* )
    operand: ( number | array | expr )

Formal grammar is a TODO. Meanwhile, see the examples below.

Examples
========

.. code-block:: python

    import parsnip
    print npcalc.handleLine('(+ 1 2)')
    # Output:
    # 3

.. code-block:: python

    import numpy
    import parsnip
    parsnip.sources.addSource('foo', numpy.ones((2, 2)))
    parsnip.sources.addSource('bar', numpy.ones((2, 2)))
    print parsnip.handleLine('(+ [foo] (* 2.5 [bar]))')
    # Output:
    # [[ 3.5  3.5]
    #  [ 3.5  3.5]]
