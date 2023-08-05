"""
Classes for representing points.

Points have position, but they do not have magnitude or direction.
Use the vector classes if you want direction.

:author:  Walker M. White (wmw2)
:version: July 13, 2018

Note by Min: This code comes from introcs, but much simplified.
"""

import math


class Point2:
    """
    An instance is a point in 2D space.
    """
    EPSILON = 1.0e-10

    # BUILT_IN METHODS
    def __init__(self, x=0, y=0):
        """
        All attribute values are 0.0 by default.

        :param x: initial x value
        :type x:  ``int`` or ``float``

        :param y: initial y value
        :type y:  ``int`` or ``float``
        """
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        """
        :return: A string representation of this object.
        :rtype:  ``str``
        """
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __repr__(self):
        """
        :return: An unambiguous string representation of this object.
        :rtype:  ``str``
        """
        return "%s%s" % (self.__class__.__name__, self.__str__())

    def _allclose(self, list1, list2):
        """Check if all numbers in the two lists are close enough.

        The package introcs uses numpy for this feature, and it is desiable,
        but, we do want to use numpy though the result is not good.
        """
        for number1, number2 in zip(list1, list2):
            if isinstance(number1, int) and isinstance(number2, int):
                if number1 != number2:
                    return False
            elif abs(number1-number2) > self.EPSILON:
                return False
        return True

    # COMPARISON
    def __eq__(self, other):
        """
        Compares this object with ``other``

        It does not require exact equality for floats.

        :param other: The object to check

        :return: True if ``self`` and ``other`` are equivalent
        :rtype:  ``bool``
        """
        return (type(other) == type(self) and
                self._allclose(self.list(), other.list()))

    def __ne__(self, other):
        """
        Compares this object with ``other``

        :param other: The object to check

        :return: False if ``self`` and ``other`` are equivalent objects.
        :rtype:  ``bool``
        """
        return not self == other

    def __lt__(self, other):
        """
        Compares the lexicographic ordering of ``self`` and ``other``.

        Lexicographic ordering checks the x-coordinate first, and then y.

        :param other: The object to check
        :type other:  ``type(self)``

        :return: True if ``self`` is lexicographic kess than ``other``
        :rtype:  ``float``
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __bool__(self):
        """
        Computes the boolean value of this tuple.

        :return: True if this object is 'close enough' to the origin;
                 False otherwise
        :rtype:  ``bool``
        """
        return not self.isZero()

    def isZero(self):
        """
        Determines whether or not this object is 'close enough' to the origin.

        :return: True if this object is 'close enough' to the origin;
                 False otherwise
        :rtype:  ``bool``
        """
        return self._allclose([self.x, self.y], [0, 0])

    def __neg__(self):
        """
        Negates this tuple, producing a new object.

        The value returned has the same type as ``self``
        (so if ``self`` is an instance of a subclass, it uses that
        object instead of the original class. The contents of
        this object are not altered.

        :return: the negation of this tuple
        :rtype:  ``type(self)``
        """
        result = self.copy()
        result.x = -result.x
        result.y = -result.y
        return result

    def __pos__(self):
        """
        Positivizes this tuple, producing a new object.

        The value returned has the same type as ``self``
        (so if ``self`` is an instance of a subclass, it uses that
        object instead of the original class. The contents of
        this object are not altered.

        :return: a copy of this tuple
        :rtype:  ``type(self)``
        """
        return self.copy()

    def __abs__(self):
        """
        Creates a copy where each component of this point is
        its absolute value.

        :return: the absolute value of this tuple
        :rtype:  ``type(self)``
        """
        self.x = abs(self.x)
        self.y = abs(self.y)
        return self

    def __add__(self, other):
        """
        Adds the odject to another, producing a new object

        The value returned has the same type as ``self``
        (so if ``self`` is an instance of a subclass, it uses that
        object instead of the original class. The contents of
        this object are not altered.

        :param other: object to add
        :type other:  ``type(self)``

        :return: the sum of this object and ``other``.
        :rtype:  ``type(self)``
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        result = self.copy()
        result.x += other.x
        result.y += other.y
        return result

    def __iadd__(self, other):
        """
        Adds ``other`` to this object in place.

        This method will modify the attributes of this oject.
        This method returns this object for chaining.

        :param other: tuple value to add
        :type other:  ``type(self)``

        :return: This object, newly modified
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        """
        Subtracts ``other`` from this object, producing a new object.

        The value returned has the same type as ``self``
        (so if ``self`` is an instance of a subclass, it uses that
        object instead of the original class. The contents of
        this object are not altered.

        :param other: object to subtract
        :type other:  ``type(self)``

        :return: the difference of this object and ``other``.
        :rtype:  ``type(self)``
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        result = self.copy()
        result.x -= other.x
        result.y -= other.y
        return result

    def __isub__(self, other):
        """
        Subtracts ``other`` from this object in place

        This method will modify the attributes of this oject.
        This method returns this object for chaining.

        :param other: object to subtract
        :type other:  ``type(self)``

        :return: This object, newly modified
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        self.x -= other.x
        self.y -= other.y
        return self

    def interpolate(self, other, alpha):
        """
        Interpolates this object with another in place

        This method will modify the attributes of this oject.
        The new attributes will be equivalent to::

            alpha*self+(1-alpha)*other

        according to the rules of addition and scalar multiplication.

        This method returns this object for chaining.

        :param other: object to interpolate with
        :type other:  ``type(self)``

        :param alpha: scalar to interpolate by
        :type alpha:  ``int`` or ``float``

        :return: This object, newly modified
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        assert (type(alpha) in [int, float]), \
            "%s is not a number" % repr(alpha)
        result = self.copy()
        result.x = alpha*result.x + (1-alpha)*other.x
        result.y = alpha*result.y + (1-alpha)*other.y
        return result

    # ADDITIONAL METHODS
    def copy(self):
        """
        :return: A copy of this tuple
        :rtype:  ``type(self)``
        """
        import copy
        return copy.copy(self)

    def list(self):
        """
        :return: A python list with the contents of this tuple.
        :rtype:  ``list``
        """
        return [self.x, self.y]

    def clamp(self, low, high):
        """
        Clamps this tuple to the range [``low``, ``high``].

        Any value in this tuple less than ``low`` is set to ``low``.
        Any value greater than ``high`` is set to ``high``.

        This method returns this object for chaining.

        :param low: The low range of the clamp
        :type low:  ``int`` or ``float``

        :param high: The high range of the clamp
        :type high:  ``int`` or ``float``

        :return: This object, newly modified
        :rtype:  ``type(self)``
        """
        assert (type(low) in [int, float]), \
            "%s is not a number" % repr(scalar)
        assert (type(high) in [int, float]), \
            "%s is not a number" % repr(scalar)
        self.x = max(low, min(high, self.x))
        self.y = max(low, min(high, self.y))
        return self

    # PUBLIC METHODS
    def midpoint(self, other):
        """
        Computes the midpoint between self and ``other``.

        This method treats ``self`` and ``other`` as a line segment,
        so they must both be points.

        :param other: the other end of the line segment
        :type other:  ``Point2``

        :return: the midpoint between this point and ``other``
        :rtype:  ``Point2``
        """
        return self.interpolate(other, 0.5)

    def distance(self, other):
        """
        Computes the Euclidean between two points

        :param other: value to compare against
        :type other:  ``Point2``

        :return: the Euclidean distance from this point to ``other``
        :rtype:  ``float``
        """
        assert (isinstance(other, Point2)), \
            "%s is not a 2-d point" % repr(other)
        return math.sqrt((self.x-other.x) * (self.x-other.x) +
                         (self.y-other.y) * (self.y-other.y))

    def distance2(self, other):
        """
        Computes the squared Euclidean between two points

        This method is slightly faster than :meth:`distance`.

        :param other: value to compare against
        :type other:  ``Point2``

        :return: the squared Euclidean distance from this point to ``other``
        :rtype:  ``float``
        """
        assert (isinstance(other, Point2)), \
            "%s is not a 2-d point" % repr(other)
        return ((self.x-other.x) * (self.x-other.x) +
                (self.y-other.y) * (self.y-other.y))


class Point3:
    """
    An instance is a point in 3D space.
    """
    EPSILON = 1.0e-10

    # BUILT_IN METHODS
    def __init__(self, x=0, y=0, z=0):
        """
        All attribute values are 0.0 by default.

        :param x: initial x value
        :type x:  ``int`` or ``float``

        :param y: initial y value
        :type y:  ``int`` or ``float``

        :param z: initial z value
        :type z:  ``int`` or ``float``
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        """
        :return: A string representation of this object.
        :rtype:  ``str``
        """
        return ('(' + str(self.x) + ', ' + str(self.y) + ', '
                + str(self.z) + ')')

    def __repr__(self):
        """
        :return: An unambiguous string representation of this object.
        :rtype:  ``str``
        """
        return "%s%s" % (self.__class__.__name__, self.__str__())

    def _allclose(self, list1, list2):
        """Check if all numbers in the two lists are close enough.

        The package introcs uses numpy for this feature, and it is desiable,
        but, we do want to use numpy though the result is not good.
        """
        for number1, number2 in zip(list1, list2):
            if isinstance(number1, int) and isinstance(number2, int):
                if number1 != number2:
                    return False
            elif abs(number1-number2) > self.EPSILON:
                return False
        return True

    # COMPARISON
    def __eq__(self, other):
        """
        Compares this object with ``other``

        It does not require exact equality for floats.

        :param other: The object to check

        :return: True if ``self`` and ``other`` are equivalent
        :rtype:  ``bool``
        """
        return (type(other) == type(self) and
                self._allclose(self.list(), other.list()))

    def __ne__(self, other):
        """
        Compares this object with ``other``

        :param other: The object to check

        :return: False if ``self`` and ``other`` are equivalent objects.
        :rtype:  ``bool``
        """
        return not self == other

    def __lt__(self, other):
        """
        Compares the lexicographic ordering of ``self`` and ``other``.

        Lexicographic ordering checks the x-coordinate first, and then y.

        :param other: The object to check
        :type other:  ``type(self)``

        :return: True if ``self`` is lexicographic kess than ``other``
        :rtype:  ``float``
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        if self.x == other.x:
            if self.y == other.y:
                return self.z < other.z
            return self.y < other.y
        return self.x < other.x

    def __bool__(self):
        """
        Computes the boolean value of this tuple.

        :return: True if this object is 'close enough' to the origin;
                 False otherwise
        :rtype:  ``bool``
        """
        return not self.isZero()

    def isZero(self):
        """
        Determines whether or not this object is 'close enough' to the origin.

        :return: True if this object is 'close enough' to the origin;
                 False otherwise
        :rtype:  ``bool``
        """
        return self._allclose([self.x, self.y, self.z], [0, 0, 0])

    def __neg__(self):
        """
        Negates this tuple, producing a new object.

        The value returned has the same type as ``self``
        (so if ``self`` is an instance of a subclass, it uses that
        object instead of the original class. The contents of
        this object are not altered.

        :return: the negation of this tuple
        :rtype:  ``type(self)``
        """
        result = self.copy()
        result.x = -result.x
        result.y = -result.y
        result.z = -result.z
        return result

    def __pos__(self):
        """
        Positivizes this tuple, producing a new object.

        The value returned has the same type as ``self``
        (so if ``self`` is an instance of a subclass, it uses that
        object instead of the original class. The contents of
        this object are not altered.

        :return: a copy of this tuple
        :rtype:  ``type(self)``
        """
        return self.copy()

    def __abs__(self):
        """
        Creates a copy where each component of this point is
        its absolute value.

        :return: the absolute value of this tuple
        :rtype:  ``type(self)``
        """
        self.x = abs(self.x)
        self.y = abs(self.y)
        self.z = abs(self.z)
        return self

    def __add__(self, other):
        """
        Adds the odject to another, producing a new object

        The value returned has the same type as ``self``
        (so if ``self`` is an instance of a subclass, it uses that
        object instead of the original class. The contents of
        this object are not altered.

        :param other: object to add
        :type other:  ``type(self)``

        :return: the sum of this object and ``other``.
        :rtype:  ``type(self)``
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        result = self.copy()
        result.x += other.x
        result.y += other.y
        result.z += other.z
        return result

    def __iadd__(self, other):
        """
        Adds ``other`` to this object in place.

        This method will modify the attributes of this oject.
        This method returns this object for chaining.

        :param other: tuple value to add
        :type other:  ``type(self)``

        :return: This object, newly modified
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other):
        """
        Subtracts ``other`` from this object, producing a new object.

        The value returned has the same type as ``self``
        (so if ``self`` is an instance of a subclass, it uses that
        object instead of the original class. The contents of
        this object are not altered.

        :param other: object to subtract
        :type other:  ``type(self)``

        :return: the difference of this object and ``other``.
        :rtype:  ``type(self)``
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        result = self.copy()
        result.x -= other.x
        result.y -= other.y
        result.z -= other.z
        return result

    def __isub__(self, other):
        """
        Subtracts ``other`` from this object in place

        This method will modify the attributes of this oject.
        This method returns this object for chaining.

        :param other: object to subtract
        :type other:  ``type(self)``

        :return: This object, newly modified
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def interpolate(self, other, alpha):
        """
        Interpolates this object with another in place

        This method will modify the attributes of this oject.
        The new attributes will be equivalent to::

            alpha*self+(1-alpha)*other

        according to the rules of addition and scalar multiplication.

        This method returns this object for chaining.

        :param other: object to interpolate with
        :type other:  ``type(self)``

        :param alpha: scalar to interpolate by
        :type alpha:  ``int`` or ``float``

        :return: This object, newly modified
        """
        assert isinstance(other, type(self)), \
            "%s is not of type %s" % (repr(other), repr(type(self)))
        assert (type(alpha) in [int, float]), \
            "%s is not a number" % repr(alpha)
        result = self.copy()
        result.x = alpha*result.x + (1-alpha)*other.x
        result.y = alpha*result.y + (1-alpha)*other.y
        result.z = alpha*result.z + (1-alpha)*other.z
        return result

    # ADDITIONAL METHODS
    def copy(self):
        """
        :return: A copy of this tuple
        :rtype:  ``type(self)``
        """
        import copy
        return copy.copy(self)

    def list(self):
        """
        :return: A python list with the contents of this tuple.
        :rtype:  ``list``
        """
        return [self.x, self.y, self.z]

    def clamp(self, low, high):
        """
        Clamps this tuple to the range [``low``, ``high``].

        Any value in this tuple less than ``low`` is set to ``low``.
        Any value greater than ``high`` is set to ``high``.

        This method returns this object for chaining.

        :param low: The low range of the clamp
        :type low:  ``int`` or ``float``

        :param high: The high range of the clamp
        :type high:  ``int`` or ``float``

        :return: This object, newly modified
        :rtype:  ``type(self)``
        """
        assert (type(low) in [int, float]), \
            "%s is not a number" % repr(scalar)
        assert (type(high) in [int, float]), \
            "%s is not a number" % repr(scalar)
        self.x = max(low, min(high, self.x))
        self.y = max(low, min(high, self.y))
        self.z = max(low, min(high, self.z))
        return self

    # PUBLIC METHODS
    def midpoint(self, other):
        """
        Computes the midpoint between self and ``other``.

        This method treats ``self`` and ``other`` as a line segment,
        so they must both be points.

        :param other: the other end of the line segment
        :type other:  ``Point3``

        :return: the midpoint between this point and ``other``
        :rtype:  ``Point3``
        """
        return self.interpolate(other, 0.5)

    def distance(self, other):
        """
        Computes the Euclidean between two points

        :param other: value to compare against
        :type other:  ``Point3``

        :return: the Euclidean distance from this point to ``other``
        :rtype:  ``float``
        """
        assert (isinstance(other, Point3)), \
            "%s is not a 3-d point" % repr(other)
        return math.sqrt((self.x-other.x) * (self.x-other.x) +
                         (self.y-other.y) * (self.y-other.y) +
                         (self.z-other.z) * (self.z-other.z))

    def distance2(self, other):
        """
        Computes the squared Euclidean between two points

        This method is slightly faster than :meth:`distance`.

        :param other: value to compare against
        :type other:  ``Point3``

        :return: the squared Euclidean distance from this point to ``other``
        :rtype:  ``float``
        """
        assert (isinstance(other, Point3)), \
            "%s is not a 3-d point" % repr(other)
        return ((self.x-other.x) * (self.x-other.x) +
                (self.y-other.y) * (self.y-other.y) +
                (self.z-other.z) * (self.z-other.z))


# Make 3-dimensions the default
Point = Point3
