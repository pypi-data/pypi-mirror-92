"""
Classes for Python course for beginners.

The classes in this module comes from introcs package by Dr. Walker M. White,
and have been adopted and modified under MIT License.
"""


# ----- object <= Employee <= Executive -------------
class Employee:
    """
    A class representing an employee with a salary.

    INSTANCE ATTRIBUTES:
        _name:   Employee's name [string, not empty]
        _start:  Year hired      [int > 1970; -1 if undefined]
        _salary: Salary          [int or float >= 0]
    """

    # GETTERS/SETTERS
    def get_name(self):
        """
        :returns: the employee's name.
        """
        return self._name

    def set_name(self, value):
        """
        Sets the employee's name to to the given value

        :param value: the new name
        :precondition: value is a nonempty string
        """
        assert type(value) == str and value != '', \
            repr(value) + ' is an invalid name'
        self._name = value

    def get_start(self):
        """
        :returns: the year hired.
        """
        return self._start

    def set_start(self, value):
        """
        Sets the year hired to the given value.

        :param value: the new year
        :precondition: valus is an int > 1970, or -1 if undefined.
        """
        assert type(value) == int, repr(value) + ' is not an int'
        assert value > 1970 or value == -1, \
            repr(value) + ' is an invalid start date'
        self._start = value

    def get_salary(self):
        """
        :returns: the annual salary
        """
        return self._salary

    def set_salary(self, value):
        """
        Sets the annual salary to the given value.

        :param value: the new salary
        :precondition: value is a number (int or float) >= 0.
        """
        assert type(value) == int or type(value) == float, \
            repr(value) + ' is not a number'
        assert value >= 0, repr(value) + ' is negative'
        self._salary = value

    def get_compensation(self):
        """
        :returns: the annual compensation (will be overridden).
        """
        return self._salary

    # INITIALIZER
    def __init__(self, n, d=-1, s=50000.0):
        """
        Initializer: Creates an Employee with name n, year hired d, salary s

        :param n: the employee name
        :precondition: n is a nonempty string

        :param d: the employee start date (optional)
        :precondition: d is an int > 1970 or -1 if undefined (default)

        :param s: the employee salary (optional)
        :precondition: s is an int or float >= 0 (50000.0 default)
        """
        # LET THE SETTERS ENFORCE THE PRECONDITIONS
        self.set_name(n)
        self.set_start(d)
        self.set_salary(s)

    # OPERATIONS
    def __str__(self):
        """
        :returns: The string representation of this Employee
        """
        return (self._name + ', year ' + str(self._start) +
                ', salary ' + str(self._salary))

    def __repr__(self):
        """
        :returns: The unambiguous representation of this Employee
        """
        return str(self.__class__) + '[' + str(self) + ']'


# SUBCLASS
class Executive(Employee):
    """
    A class representing an Employee with a bonus.

    INSTANCE ATTRIBUTES:
        _bonus: annual bonus [float >= 0]
    """

    # GETTERS/SETTERS
    def get_bonus(self):
        """
        :returns: the annual bonus.
        """
        return self._bonus

    def set_bonus(self, value):
        """
        Sets the annual bonus salary to the give value

        :param value: the new bonus
        :precondition: value is a number (int or float) >= 0.
        """
        assert type(value) == int or type(value) == float, \
            repr(value) + ' is not a number'
        assert value >= 0, repr(value) + ' is negative'
        self._bonus = value

    def get_compensation(self):
        """
        :returns: the annual compensation (will be overridden).
        """
        return self._salary + self._bonus

    # INITIALIZER
    def __init__(self, n, d, b=0.0):
        """
        Initializer: Creates an Executive w/ name n, year hired d, and bonus b

        The default salary of an executive is 50k

        :param n: the executive name
        :precondition: n is a nonempty string

        :param d: the executive start date (optional)
        :precondition: d is an int > 1970 or -1 if undefined (default)

        :param b: the executive bonus (optional)
        :precondition: b is an int or float >= 0 (0.0 default)
        """
        # Asserts precondition for n and d
        super().__init__(n, d)
        self.set_bonus(b)

    # OPERATIONS
    def __str__(self):
        """
        :returns: a string representation of this Executive
        """
        # Add on to the string representation of the base class.
        return super().__str__() + ', bonus ' + str(self._bonus)

# end----- object <= Employee <= Executive -------------


# ----- object <= Worker -------------
class Worker:
    """
    A class to represent a worker in a certain organization

    INSTANCE ATTRIBUTES:
       lname: Last name.  [str]
       rrn:   Resident registration no. [int in 0..9999999]
       boss:  The worker's boss. [Worker, or None if no boss]
    """

    def __init__(self, lname, rrn, boss):
        """
        Initializer: Creates an instance with last name n,
                     resident registration number r, and boss b.

        :param lname: The worker's last name
        :precondition: lname is a string

        :param rrn: The worker's social security number
        :precondition: rrn is an int in 0..999999999

        :param boss: The worker's boss
        :precondition: boss is another Worker object or None
        """
        self.lname = lname
        self.rrn = rrn
        self.boss = boss

    def __str__(self):
        """
        :returns: text representation of this Worker
        """
        return ('Worker ' + self.lname +
                '. Resi reg XXXXXX-XXX' + str(self.rrn % 10000) +
                ('.' if self.boss is None else '. boss: ' + self.boss.lname))

    def __eq__(self, other):
        """
        :returns: True if self and other has the same attributes.
        """
        assert type(other) == Worker

        return (self.lname == other.lname and
                self.rrn == other.rrn and
                self.boss is other.boss)

# end----- object <= Worker -------------


# ----- object <= Fraction <= BinaryFraction -------------
class Fraction:
    """
    A class to represent a fraction n/d

    INSTANCE ATTRIBUTES (hidden):
        _numerator:   The fraction numerator   [int]
        _denominator: The fraction denomenator [int > 0]

    Note: This class does not use property() for getters and setters.
    """

    # GETTER AND SETTERS
    def get_numerator(self):
        """
        :returns: The fraction numerator.
        """
        return self._numerator   # returns the attribute

    def set_numerator(self, value):
        """
        Sets the numerator to value.

        :param value: the new numerator
        :precondition: value is an int
        """
        # enforce invariant
        assert isinstance(value, int), repr(value) + ' is not an int'
        # assign to attribute
        self._numerator = value

    def get_denominator(self):
        """
        :returns: The fraction denominator.
        """
        return self._denominator   # returns the attribute

    def set_denominator(self, value):
        """
        Sets the numerator to value.

        :param value: the new denominator
        :precondition: value is an int > 0
        """
        # enforce invariant
        assert isinstance(value, int), repr(value) + ' is not an int'
        assert value > 0, repr(value) + ' is not positive'
        # assign to field
        self._denominator = value

    # INITIALIZER
    def __init__(self, n=0, d=1):
        """
        Initializer: Creates a new Fraction n/d

        :param n: the numerator (default is 0)
        :precondition: n is an int (or optional)

        :param d: the denomenator (default is 1)
        :precondition: d is an int > 0 (or optional)
        """
        # No need for asserts; setters handle everything
        self.set_numerator(n)
        self.set_denominator(d)

    def __str__(self):
        """
        :returns: this Fraction as a string 'n/d'
        """
        return repr(self._numerator) + '/' + repr(self._denominator)

    def __repr__(self):
        """
        :returns: The unambiguous representation of Fraction
        """
        return str(self.__class__) + '[' + str(self) + ']'

    # MATH METHODS
    def __mul__(self, other):
        """
        :returns: The product of self and other as a new Fraction

        This method does not modify the contents of self or other

        :param other: the value to multiply on the right
        :precondition: other is a Fraction or an int
        """
        assert isinstance(other, Fraction) or isinstance(other, int), \
            repr(other) + ' is not a valid operand'
        if type(other) == int:
            return self._multiply_int(other)
        return self._multiply_fraction(other)

    # Private helper to multiply fractions
    def _multiply_fraction(self, other):
        """
        :returns: The product of self and other as a new Fraction

        This method does not modify the contents of self or other

        :param other: the fraction to multiply on the right
        :precondition: other is a Fraction
        """
        # No need to enforce preconditions on a hidden method
        top = self.get_numerator() * other.get_numerator()
        bot = self.get_denominator() * other.get_denominator()
        return Fraction(top, bot)

    # Private helper to multiply ints
    def _multiply_int(self, x):
        """
        :returns: The product of self and other as a new Fraction

        This method does not modify the contents of self or other

        :param other: the value to multiply on the right
        :precondition: other is a int
        """
        # No need to enforce preconditions on a hidden method
        top = self.get_numerator() * x
        bot = self.get_denominator()
        return Fraction(top, bot)

    def __add__(self, other):
        """
        :returns: The sum of self and other as a new Fraction

        This method does not modify the contents of self or other

        :param other: the value to add on the right
        :precondition: other is a Fraction or an int
        """
        assert isinstance(other, Fraction) or isinstance(other, int), \
            repr(other) + ' is not a valid operand'
        if type(other) == int:
            return self._add_int(other)
        return self._add_fraction(other)

    # Private helper to multiply fractions
    def _add_fraction(self, other):
        """
        :returns: The sum of self and other as a new Fraction

        This method does not modify the contents of self or other

        :param other: the fraction to add on the right
        :precondition: other is a Fraction
        """
        # No need to enforce preconditions on a hidden method
        bot = self.get_denominator() * other.get_denominator()
        top = (self.get_numerator() * other.get_denominator() +
               self.get_denominator() * other.get_numerator())
        return Fraction(top, bot)

    # Private helper to multiply ints
    def _add_int(self, x):
        """
        :returns: The sum of self and other as a new Fraction

        This method does not modify the contents of self or other

        :param other: the value to add on the right
        :precondition: other is an int
        """
        # No need to enforce preconditions on a hidden method
        bot = self.get_denominator()
        top = (self.get_numerator() + self.get_denominator() * x)
        return Fraction(top, bot)

    # COMPARISONS
    def __eq__(self, other):
        """
        :returns: True if self, other are equal Fractions.

        It returns False if they are not equal, or other is not a Fraction

        :param other: value to compare to this fraction
        :precondition: NONE
        """
        if not isinstance(other, Fraction) and not isinstance(other, int):
            return False

        if isinstance(other, int):
            return self.get_numerator() == other*self.get_denominator()

        # Cross multiply
        left = self.get_numerator() * other.get_denominator()
        rght = self.get_denominator() * other.get_numerator()
        return left == rght

    def __lt__(self, other):
        """
        :returns: True if self < other, False otherwise

        This method is used to implement all strict comparison operations.
        Both < and > are determined automatically from this method.

        :param other: value to compare to this fraction
        :precondition: other is a Fraction
        """
        assert isinstance(other, Fraction) or isinstance(other, int), \
            repr(other) + ' is not a valid operand'

        if isinstance(other, int):
            return self.get_numerator() < other*self.get_denominator()

        # Cross multiply
        left = self.get_numerator() * other.get_denominator()
        rght = self.get_denominator() * other.get_numerator()
        return left < rght

    def __le__(self, other):
        """
        :returns: True if self < other, False otherwise

        This method is used to implement all inclusive comparison operations.
        Both <= and >= are determined automatically from this method.

        :param other: value to compare to this fraction
        :precondition: other is a Fraction
        """
        assert isinstance(other, Fraction) or isinstance(other, int), \
            repr(other) + ' is not a valid operand'

        if isinstance(other, int):
            return self.get_numerator() <= other*self.get_denominator()

        # Cross multiply
        left = self.get_numerator() * other.get_denominator()
        rght = self.get_denominator() * other.get_numerator()
        return left <= rght

    @staticmethod
    def _gcd(a, b):
        """
        :returns: Greatest common divisor of x and y.

        :precondition: x and y are integers.
        """
        assert type(a) == int, repr(x) + ' is not an int'
        assert type(b) == int, repr(y) + ' is not an int'
        while b != 0:
            t = b
            b = a % b
            a = t
        return a

    def reduce(self):
        """
        Normalizes this fraction into simplest form.

        Normalization ensures that the numerator and denominator have no
        common divisors.
        """
        g = self._gcd(self.get_numerator(), self.get_denominator())
        self.set_numerator(self.get_numerator()//g)
        self.set_denominator(self.get_denominator()//g)


class BinaryFraction(Fraction):
    """
    A class to represent are fractions that are k/2n

    INSTANCE ATTRIBUTES are the same, but:
        numerator:   [int]: top
        denominator  [= 2n, n ≥ 0]: bottom """

    def __init__(self, k, n):
        """
        Initializer: Creates a fraction k/2n

        :param k: The numerator
        :precondition: k is an int

        :param n: The exponent for binary fraction 2 ** n
        :precondition: n is an int >= 0
        """
        assert type(n) == int and n >= 0
        super().__init__(k, 2 ** n)

# end----- object <= Fraction <= BinaryFraction -------------


# ----- object <= PFraction <= BinaryPFraction -------------
class PFraction:
    """
    A class to represent a fraction n/d

    INSTANCE ATTRIBUTES (hidden):
        _numerator:   The fraction numerator   [int]
        _denominator: The fraction denomenator [int > 0]

    Note: This class use property() for getters and setters.
    """

    # GETTER AND SETTERS
    @property
    def numerator(self):
        """
        :returns: The fraction numerator.
        """
        return self._numerator    # returns the attribute

    @numerator.setter
    def numerator(self, value):
        """
        Sets the numerator to value.

        :param value: the new numerator
        :precondition: value is an int
        """
        # enforce invariant
        assert isinstance(value, int), repr(value) + ' is not an int'
        # assign to attribute
        self._numerator = value

    @property
    def denominator(self):
        """
        :returns: The fraction denominator.
        """
        return self._denominator   # returns the attribute

    @denominator.setter
    def denominator(self, value):
        """
        Sets the numerator to value.

        :param value: the new denominator
        :precondition: value is an int > 0
        """
        # enforce invariant
        assert isinstance(value, int), repr(value) + ' is not an int'
        assert value > 0, repr(value) + ' is not positive'
        # assign to field
        self._denominator = value

    # INITIALIZER
    def __init__(self, n=0, d=1):
        """
        Initializer: Creates a new PFraction n/d

        :param n: the numerator (default is 0)
        :precondition: n is an int (or optional)

        :param d: the denomenator (default is 1)
        :precondition: d is an int > 0 (or optional)
        """
        # No need for asserts; setters handle everything
        self._numerator = n
        self._denominator = d

    def __str__(self):
        """
        :returns: this PFraction as a string 'n/d'
        """
        return repr(self._numerator) + '/' + repr(self._denominator)

    def __repr__(self):
        """
        :returns: The unambiguous representation of PFraction
        """
        return str(self.__class__) + '[' + str(self) + ']'

    # MATH METHODS
    def __mul__(self, other):
        """
        :returns: The product of self and other as a new PFraction

        This method does not modify the contents of self or other

        :param other: the value to multiply on the right
        :precondition: other is a PFraction or an int
        """
        assert isinstance(other, PFraction) or isinstance(other, int), \
            repr(other) + ' is not a valid operand'
        if type(other) == int:
            return self._multiply_int(other)
        return self._multiply_fraction(other)

    # Private helper to multiply fractions
    def _multiply_fraction(self, other):
        """
        :returns: The product of self and other as a new PFraction

        This method does not modify the contents of self or other

        :param other: the fraction to multiply on the right
        :precondition: other is a PFraction
        """
        # No need to enforce preconditions on a hidden method
        top = self._numerator * other._numerator
        bot = self._denominator * other._denominator
        return PFraction(top, bot)

    # Private helper to multiply ints
    def _multiply_int(self, x):
        """
        :returns: The product of self and other as a new PFraction

        This method does not modify the contents of self or other

        :param other: the value to multiply on the right
        :precondition: other is a int
        """
        # No need to enforce preconditions on a hidden method
        top = self._numerator * x
        bot = self._denominator
        return PFraction(top, bot)

    def __add__(self, other):
        """
        :returns: The sum of self and other as a new PFraction

        This method does not modify the contents of self or other

        :param other: the value to add on the right
        :precondition: other is a PFraction or an int
        """
        assert isinstance(other, PFraction) or isinstance(other, int), \
            repr(other) + ' is not a valid operand'
        if type(other) == int:
            return self._add_int(other)
        return self._add_fraction(other)

    # Private helper to multiply fractions
    def _add_fraction(self, other):
        """
        :returns: The sum of self and other as a new PFraction

        This method does not modify the contents of self or other

        :param other: the fraction to add on the right
        :precondition: other is a PFraction
        """
        # No need to enforce preconditions on a hidden method
        bot = self._denominator * other._denominator
        top = (self._numerator * other._denominator +
               self._denominator * other._numerator)
        return PFraction(top, bot)

    # Private helper to multiply ints
    def _add_int(self, x):
        """
        :returns: The sum of self and other as a new PFraction

        This method does not modify the contents of self or other

        :param other: the value to add on the right
        :precondition: other is an int
        """
        # No need to enforce preconditions on a hidden method
        bot = self._denominator
        top = (self._numerator + self._denominator * x)
        return PFraction(top, bot)

    # COMPARISONS
    def __eq__(self, other):
        """
        :returns: True if self, other are equal PFractions.

        It returns False if they are not equal, or other is not a PFraction

        :param other: value to compare to this fraction
        :precondition: NONE
        """
        if not isinstance(other, PFraction) and not isinstance(other, int):
            return False

        if isinstance(other, int):
            return self._numerator == other*self._denominator

        # Cross multiply
        left = self._numerator * other._denominator
        rght = self._denominator * other._numerator
        return left == rght

    def __lt__(self, other):
        """
        :returns: True if self < other, False otherwise

        This method is used to implement all strict comparison operations.
        Both < and > are determined automatically from this method.

        :param other: value to compare to this fraction
        :precondition: other is a PFraction
        """
        assert isinstance(other, PFraction) or isinstance(other, int), \
            repr(other) + ' is not a valid operand'

        if isinstance(other, int):
            return self._numerator < other*self._denominator

        # Cross multiply
        left = self._numerator * other._denominator
        rght = self._denominator * other._numerator
        return left < rght

    def __le__(self, other):
        """
        :returns: True if self < other, False otherwise

        This method is used to implement all inclusive comparison operations.
        Both <= and >= are determined automatically from this method.

        :param other: value to compare to this fraction
        :precondition: other is a PFraction
        """
        assert isinstance(other, PFraction) or isinstance(other, int), \
            repr(other) + ' is not a valid operand'

        if isinstance(other, int):
            return self._numerator <= other*self._denominator

        # Cross multiply
        left = self._numerator * other._denominator
        rght = self._denominator * other._numerator
        return left <= rght

    @staticmethod
    def _gcd(a, b):
        """
        :returns: Greatest common divisor of x and y.

        :precondition: x and y are integers.
        """
        assert type(a) == int, repr(x) + ' is not an int'
        assert type(b) == int, repr(y) + ' is not an int'
        while b != 0:
            t = b
            b = a % b
            a = t
        return a

    def reduce(self):
        """
        Normalizes this fraction into simplest form.

        Normalization ensures that the numerator and denominator have no
        common divisors.
        """
        g = self._gcd(self._numerator, self._denominator)
        self._numerator = self._numerator//g
        self._denominator = self._denominator//g


class BinaryPFraction(PFraction):
    """
    A class to represent are fractions that are k/2n

    INSTANCE ATTRIBUTES are the same, but:
        numerator:   [int]:         top
        denominator  [= 2n, n ≥ 0]: bottom """

    def __init__(self, k, n):
        """
        Initializer: Creates a fraction k/2n

        :param k: The numerator
        :precondition: k is an int

        :param n: The exponent for binary fraction 2 ** n
        :precondition: n is an int >= 0
        """
        assert type(n) == int and n >= 0
        super().__init__(k, 2 ** n)

# -- end of art.py
