#
#  Copyright (c) 2019-2021 by Hyoung Bok Min, All rights reserved.
#
#  File        : __init__.py
#  Written on  : Feb. 10, 2019
#  Last updated: Jan. 20, 2021
#  Author      : Hyoung Bok Min (min.skku@gmail.com)
#
"""This package is used in a Python course for beginners.

This package is intended to be used in a Python course. Most of the
classes and functions come from introcs package of Dr. Walker White
under MIT license. But, more classes and functions are added by Min
to augment our Python course. The followings are summaries.

point : classes Point3 and Point2
art   : classes for our Python course such as
        Employee, Executive, Worker, Fraction, BinaryFraction,
        PFraction, and BinaryPFraction.
test  : helper functions for unit testing of homeworks.
        einput(), option_exists(), get_exc_info(), test_function(),
        test_equal(), and more.
zoo   : helpful small functions such as
        add121(), argprint(), addall(), add(), unpacking(),
        print_inside() and more.
cat   : Simple version of UNIX utility cat
        Use the following command to learn how to use this program.
        python -m eepy.cat -h
"""

__version__ = '0.3.55'

from .art import *
from .point import *
from .test import *
from .zoo import *

