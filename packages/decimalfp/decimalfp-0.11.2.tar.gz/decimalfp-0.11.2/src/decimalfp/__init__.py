# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        decimalfp (package)
# Purpose:     Decimal fixed-point arithmetic
#
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2014 Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source: src/decimalfp/__init__.py $
# $Revision: 2021-01-24T22:03:22+01:00 $


# noinspection PyUnresolvedReferences
"""
The package `decimalfp` provides a :class:`Decimal` number type which can
represent decimal numbers of (nearly) arbitrary magnitude and very large
precision, i.e. with a very large number of fractional digits.

Usage
=====

:class:`decimalfp.Decimal` instances are created by giving a `value` (default:
0) and a `precision` (i.e the number of fractional digits, default: None).

    >>> Decimal()
    Decimal(0)

If `precision` is given, it must be of type `int` and >= 0.

    >>> Decimal(5, 3)
    Decimal(5, 3)
    >>> Decimal(5555, -3)
    ValueError: Precision must be >= 0.

If `value` is given, it must either be a string, an instance of
`numbers.Integral`, `number.Rational` (for example `fractions.Fraction`),
`decimal.Decimal`, a finite instance of `numbers.Real` (for example `float`)
or be convertable to a `float` or an `int`.

The value is always adjusted to the given precision or the precision is
calculated from the given value, if no precision is given.

    >>> Decimal(b'12.345')
    Decimal('12.345')
    >>> Decimal(u'12.345')
    Decimal('12.345')
    >>> Decimal(u'12.345', 5)
    Decimal('12.345', 5)
    >>> Decimal(15, 4)
    Decimal(15, 4)
    >>> Decimal(10 ** 23)
    Decimal(100000000000000000000000)
    >>> Decimal(10 ** 48)
    Decimal(1000000000000000000000000000000000000000000000000)
    >>> Decimal(2 ** 48)
    Decimal(281474976710656)
    >>> Decimal(2 ** 98)
    Decimal(316912650057057350374175801344)
    >>> Decimal(Fraction(7, 56))
    Decimal('0.125')
    >>> Decimal(Fraction(8106479329266893, 4503599627370496), 7)
    Decimal('1.8', 7)
    >>> Decimal(1.8, 7)
    Decimal('1.8', 7)
    >>> Decimal(decimal.Decimal('-19.26', 5), 3)
    Decimal('-19.26', 3)

When the given `precision` is lower than the precision of the given `value`,
the result is rounded, according to the current default rounding mode (which
itself defaults to ROUND_HALF_EVEN).

    >>> Decimal(u'12.345', 2)
    Decimal('12.34')
    >>> Decimal(u'12.3456', 3)
    Decimal('12.346')
    >>> Decimal(0.2, 3)
    Decimal('0.2', 3)
    >>> Decimal(0.2, 17)
    Decimal('0.20000000000000001')
    >>> Decimal(0.2, 55)
    Decimal('0.200000000000000011102230246251565404236316680908203125', 55)

When no `precision` is given and the given `value` is a `float` or a
`numbers.Rational` (but no :class:`Decimal`), the :class:`Decimal` constructor
tries to convert `value` exactly. But this is done only up a fixed limit of
fractional digits (imposed by the implementation, currently 65535). If `value`
can not be represented as a :class:`Decimal` within this limit, an exception
is raised.

    >>> Decimal(Fraction(1, 7))
    ValueError: Can't convert Fraction(1, 7) exactly to Decimal.

:class:`Decimal` does not deal with infinity, division by 0 always raises a
`ZeroDivisionError`. Likewise, infinite instances of type `float` or
`decimal.Decimal` can not be converted to :class:`Decimal` instances. The same
is true for the 'not a number' instances of these types.

Computations
============

When importing `decimalfp`, its :class:`Decimal` type is registered in Pythons
numerical stack as `number.Rational`. It supports all operations defined for
that base class and its instances can be mixed in computations with instances
of all numeric types mentioned above.

All numerical operations give an exact result, i.e. they are not automatically
constraint to the precision of the operands or to a number of significant
digits (like the floating-point `Decimal` type from the standard module
`decimal`). When the result can not exactly be represented by a
:class:`Decimal` instance within the limit of fractional digits, an instance
of `fractions.Fraction` is returned.

Addition and subtraction
------------------------

Adding or subtracting :class:`Decimal` instances results in a :class:`Decimal`
instance with a precision equal to the maximum of the precisions of the
operands.

    >>> Decimal('7.3') + Decimal('8.275')
    Decimal('15.575')
    >>> Decimal('-7.3', 4) + Decimal('8.275')
    Decimal('0.975', 4)

In operations with other numerical types the precision of the result is at
least equal to the precision of the involved :class:`Decimal` instance, but
may be greater, if neccessary. If the needed precision exceeds the limit of
fractional digits, an instance of `fractions.Fraction` is returned.

    >>> 0.25 + Decimal(3)
    Decimal('3.25')
    >>> 0.25 - Decimal(-3, 5)
    Decimal('3.25', 5)
    >>> 0.725 + Decimal('3')
    Decimal('3.72499999999999997779553950749686919152736663818359375')
    >>> Decimal('3') + Fraction(1, 7)
    Fraction(22, 7)

Multiplication and division
---------------------------

Multiplying :class:`Decimal` instances results in a :class:`Decimal` instance
with precision equal to the sum of the precisions of the operands.

    >>> Decimal('5.000') * Decimal('2.5')
    Decimal('12.5', 4)

Dividing :class:`Decimal` instances results in a :class:`Decimal` instance
with precision at least equal to max(0, numerator.precision -
denominator.precision), but may be greater, if needed.

    >>> Decimal('5.2000') / Decimal('2.5')
    Decimal('2.08', 3)
    >>> Decimal('5.2003') / Decimal('2.5')
    Decimal('2.08012')

In operations with other numerical types the precision of the result is at
least equal to the precision of the involved :class:`Decimal` instance, but
may be greater, if neccessary. If the needed precision exceeds the limit of
fractional digits, an instance of `fractions.Fraction` is returned.

    >>> 3 * Decimal('7.5')
    Decimal('22.5')
    >>> Decimal(5) * 0.25
    Decimal('1.25')
    >>> Decimal('3') * Fraction(1, 7)
    Fraction(3, 7)

Rounding
--------

:class:`Decimal` supports rounding via the built-in function `round`.

.. note::
    In Python 3.x the function `round` uses the rounding mode ROUND_HALF_EVEN
    and returns an `int` when called with one argument, otherwise the same
    type as the number to be rounded.

    >>> round(Decimal('12.345'))
    12
    >>> round(Decimal('12.345'), 2)
    Decimal('12.34')
    >>> round(Decimal('1234.5'), -2)
    Decimal(1200)

In addition, via the method :meth:`adjusted` a :class:`Decimal` with a
different precision can be derived, supporting all rounding modes defined by
the standard library module `decimal`.

The rounding modes defined in `decimal` are wrapped into the Enum
:class:`ROUNDING`.

    >>> d = Decimal('12.345')
    >>> d.adjusted(2)           # default rounding mode is ROUND_HALF_EVEN !
    Decimal('12.34')
    >>> d.adjusted(2, ROUNDING.ROUND_HALF_UP)
    Decimal('12.35')
    >>> d.adjusted(1, ROUNDING.ROUND_UP)
    Decimal('12.4')

For the details of the different rounding modes see the documentation of the
standard library module `decimal`.

`round` and `adjusted` only allow to round to a quantum that's a power to 10.
The method :meth:`quantize` can be used to round to any quantum and it does
also support all rounding modes mentioned above.

    >>> d = Decimal('12.345')
    >>># equivalent to round(d, 2) or d.adjusted(2)
    >>># (default rounding mode ROUNDING.ROUND_HALF_EVEN):
    >>> d.quantize(Decimal('0.01'))
    Decimal('12.34')
    >>> d.quantize(Decimal('0.05'))
    Decimal('12.35')
    >>> d.quantize('0.6')
    Decimal('12.6')
    >>> d.quantize(4)
    Decimal('12')
"""

__version__ = 0, 11, 2

# Under PyPy the C implementation is slower than the Python
# implementation, so we force to import the latter.
# In addition, the import of the Python implementation can be forced by
# setting the environment variable DECIMALFP_FORCE_PYTHON_IMPL
import platform  # noqa: I100, I202
_impl = platform.python_implementation()
del platform

import os  # noqa: I100, I202
_force_python_impl = os.getenv('DECIMALFP_FORCE_PYTHON_IMPL')
del os

if _impl == 'PyPy' or _force_python_impl:
    from ._pydecimalfp import (
        Decimal, get_dflt_rounding_mode, ROUNDING, set_dflt_rounding_mode,
    )
else:  # pragma: no cover
    try:
        # C implementation available?
        from ._cdecimalfp import (
            Decimal, get_dflt_rounding_mode, ROUNDING, set_dflt_rounding_mode,
        )
    except ImportError:
        from ._pydecimalfp import (
            Decimal, get_dflt_rounding_mode, ROUNDING, set_dflt_rounding_mode,
        )

# define public namespace
__all__ = [
    'Decimal',
    'ROUNDING',
    'get_dflt_rounding_mode',
    'set_dflt_rounding_mode',
]
