# pylint: disable=missing-docstring, too-many-arguments
# pylint: disable=unused-argument, invalid-name
# -*- coding: utf-8 -*-
"""This is just a helper module, used to show the functionality."""

from multiprocessing.pool import Pool
from . import input_checks as ics


def afunction(int_v,
              float_v,
              str_v,
              dict_v,
              other_v,
              int_or_dict_v,
              optional_v=None,
              float_or_int_optional_v=None):
    ics.check_type(int_v, 'int_v', int)
    ics.check_type(float_v, 'float_v', float)
    ics.check_type(str_v, 'str_v', str)
    ics.check_type(dict_v, 'dict_v', dict)
    ics.check_type(other_v, 'other_v', AClass)
    ics.check_multiple_type(int_or_dict_v, 'int_or_dict_v', (int, dict))
    ics.check_noneable_type(optional_v, 'optional_v', int)
    ics.check_noneable_multiple_type(float_or_int_optional_v,
                                     'float_or_int_optional_v',
                                     (float, int),
                                     )
    if isinstance(int_or_dict_v, int) and int_or_dict_v < 0.5:
        raise ValueError()
    if int_v < 0:
        raise ValueError()
    if float_v < 0.0:
        raise ValueError()


def double_float(value):
    ics.check_type(value, 'value', float)
    return 2*value


def double_int_if_given(value=2):
    ics.check_type(value, 'value', int)
    return 2*value


def fun_with_noneable(value=None):
    ics.check_noneable_type(value, 'value', int)
    if value is not None:
        return 2*value
    return None


def fun_with_two_optionals(str_or_int, a=3, b=4.):
    ics.check_multiple_type(str_or_int, 'str_or_int', (str, int))
    if isinstance(str_or_int, str):
        ics.check_nonempty_str(str_or_int, 'str_or_int')
    if isinstance(str_or_int, int):
        ics.check_nonnegativeint(str_or_int, 'str_or_int')
    ics.check_positiveint(a, 'a')
    ics.check_positivefloat(b, 'b')


def function_non_pickleable_optional_input(pool=None):
    ics.check_noneable_type(pool, 'pool', Pool)


def do_not_perform_any_input_checking(par):
    """
    This function does not perform any type/value checking.
    Therefore expected exceptions are not raised.

    Args:
        par:

    Returns:

    """
    return


def raise_exception(par):
    """Raise a generic exception

    Args:
        par:

    Raises:
        Exception: always
    """
    raise Exception


def optional_different_from_none(a=5):
    """
    This function has an optional parameter, that is expected to be different
    from None.

    Args:
        a (int, optional): defaults to 5.

    Returns:
        (int) 5 / a
    """
    ics.check_positiveint(a, 'a')
    return 5 / a


class AClass:

    def __init__(self, in_value):
        ics.check_nonnegativefloat(in_value, "in_value")
        self.in_value = in_value

    def a_method(self, arg):
        ics.check_nonnegativefloat(arg, "arg")
        return self.in_value + arg

    @classmethod
    def a_class_method(cls, value):
        ics.check_positiveint(value, "value")
        return value ** 0.5
