#
#  Copyright (c) 2019 by Hyoung Bok Min, All rights reserved.
#
#  File       : zoo.py
#  Written on : Feb. 10, 2019
#  Author     : Hyoung Bok Min (min.skku@gmail.com)
#
"""Miscellaneous functions for a Python course."""


# ----- Keyword arguments and Unpacking
def add121(x, y, z):
    """Add 3 numbers by weights of 1:2:1, i.e., x+2*y+z.

    :returns: the added number, x+2*y+z
    """
    return x + y + y + z


def argprint(*args, **kwargs):
    """Print positional arguments and keyword arguments.

    :param args: positional arguments
    :param kwargs: keyword arguments

    Note: All arguments are printed one at a line.
    """
    for value in args:
        print('arg:', value)
    for key in kwargs:
        print(key, '::', kwargs[key])


def addall(*args):
    """Add all the positional arguments.

    :returns: sum of all the positional arguments.
    :note: We use ``sum(args)``
    """
    return sum(args)


def add(x, y, z):
    """Add given 3 numbers.

    :returns: sum of 3 arguments, i.e., returns x+y+z.
    """
    return x + y + z


def unpacking(*args, **kwargs):
    """Unpacking positional and keyword arguments.

    (1) Unpacking positional arguments to call addall().
            print(addall(*args))
    (2) Unpacking 1st 3 positional argument to call add()
            if len(args) >= 3: print(add(*args[0:3]))
    (3) Unpacking keyword arguments to call argprint()
            argprint(**kwargs)
    """
    print(addall(*args))
    if len(args) >= 3:
        print(add(*args[0:3]))
    argprint(**kwargs)


# ----- A function decorator
def print_inside(fn):
    """A function decorator

    :param fn: function to be decorated by using this decorator function
    :type fn:  callable class such as <class function>
    """
    def inner(*args, **kwargs):
        print('Decorator "print_inside" at', __name__, 'module')
        return fn(*args, **kwargs)
    return inner

# -- end of zoo.py
