# -*- coding: utf-8 -*-
"""A module with facilities to check the type and range of input parameters."""

import pathlib
from typing import Any, Type, Tuple
import numpy as np


def check_type(par: Any, par_name: str, expected_type: Type) -> None:
    """Check the parameters against a single type.

    Examples:

        >>> from ftrotta.pycolib import input_checks as ics
        >>>
        >>> def f(a):
        >>>     ics.check_type(a, 'a', int)
        >>>     pass

    Args:
        par:
        par_name:
        expected_type:

    Raises:
        TypeError
    """
    _check_type_helper(par, par_name, expected_type, TypeError)


def check_multiple_type(
        par: Any,
        par_name: str,
        expected_types: Tuple[Type, ...],
) -> None:
    """Check the parameter against a list of possible types.

    Examples:

        >>> from ftrotta.pycolib import input_checks as ics
        >>>
        >>> def f(a):
        >>>     ics.check_multiple_type(a, 'a', (int, double))
        >>>     pass

    Args:
        par:
        par_name:
        expected_types:

    Raises:
        TypeError
    """
    found = False
    for expected_type in expected_types:
        if isinstance(par, expected_type):
            found = True
            break
    if not found:
        msg = f'{par_name} should be of one of the types ' \
              f'{expected_types}, while it is of type {type(par)}.'
        raise TypeError(msg)


def check_noneable_type(par: Any, par_name: str, expected_type: Type) -> None:
    """Check the type of `par`, if it is not `None`.

    Args:
        par:
        par_name:
        expected_type:

    Raises:
        TypeError
    """
    if par is not None:
        check_type(par=par,
                   par_name=par_name,
                   expected_type=expected_type)


def check_noneable_multiple_type(
        par: Any,
        par_name: str,
        expected_type: Tuple[Type, ...]) -> None:
    """Check the parameter against a tuple of possible types, if not `None`.

    Examples:

        >>> from ftrotta.pycolib import input_checks as ics
        >>>
        >>> def f(a):
        >>>     ics.check_multiple_type(a, 'a', (int, double))
        >>>     pass

    Args:
        par:
        par_name:
        expected_type:

    Raises:
        TypeError
    """
    if par is not None:
        check_multiple_type(par=par,
                            par_name=par_name,
                            expected_types=expected_type)


def check_nonempty_str(par: Any, par_name: str) -> None:
    """

    Args:
        par (str):
        par_name (str):

    Raises:
        TypeError: if `par` is not a string.
        ValueError: if `par` is an empty string.
    """
    check_type(par, par_name, str)
    if not par:
        msg = f'{par_name} string cannot be empty.'
        raise ValueError(msg)


def check_isdir(par: Any, par_name: str) -> None:
    """Checks `par` to be a :class:`pathlib.Path` and an existing directory.

    Args:
        par (any):
        par_name (str):

    Raises:
        TypeError: if `par` type is not `pathlib.Path`.
        ValueError: if `par` value is not an existing directory.
    """
    check_type(par, par_name, pathlib.Path)
    if not par.is_dir():
        msg = f'\'{par_name}\' should be an existing directory, while \'' \
              f'{par.resolve()}\' does not exist or it is not a directory.'
        raise ValueError(msg)


def check_isfile(par: Any, par_name: str) -> None:
    """Checks `par` to be a :class:`pathlib.Path` and an existing file.

    Args:
        par:
        par_name:

    Raises:
        TypeError: if `par` type is not `:class:`pathlib.Path`.
        ValueError: if `par` value is not an existing file.
    """
    check_type(par, par_name, pathlib.Path)
    if not par.is_file():
        msg = f'\'{par_name}\' should be an existing file, while \'' \
              f'{par.resolve()}\' does not exist or it is not a file.'
        raise ValueError(msg)


def check_positiveint(par: Any, par_name: str) -> None:
    """Checks `par` to be `int` and positive.

    Args:
        par (any):
        par_name (str):

    Raises:
        TypeError: if `par` type if not ``int``.
        ValueError: if `par` value is not positive.
    """
    check_type(par, par_name, int)
    if not par > 0:
        msg = f'{par_name} should be positive, while it is {par}.'
        raise ValueError(msg)


def check_positivefloat(par: Any, par_name: str) -> None:
    """Check `par` to be `float` and positive.

    Args:
        par:
        par_name:

    Raises:
        TypeError: if `par` type if not `float`.
        ValueError: if `par` value is not positive.
    """
    check_type(par, par_name, float)
    if not par > 0:
        msg = f'{par_name} should be positive, while it is {par}.'
        raise ValueError(msg)


def check_nonnegativeint(par: Any, par_name: str) -> None:
    """Check `par` to be `int` and non-negative.

    Args:
        par:
        par_name:

    Raises:
        TypeError: if `par` type is not `int`.
        ValueError: if `par` value is not non-negative.
    """
    check_type(par, par_name, int)
    if not par >= 0:
        msg = f'{par_name} should be non-negative, while it is {par}.'
        raise ValueError(msg)


def check_nonnegativefloat(par: Any, par_name: str) -> None:
    """Check `par` to be `float` and non-negative.

    Args:
        par:
        par_name:

    Raises:
        TypeError: if `par` type is not `float`.
        ValueError: if `par` value is not non-negative.
    """
    check_type(par, par_name, float)
    if not par >= 0:
        msg = f'{par_name} should be non-negative, while it is {par}.'
        raise ValueError(msg)


def check_dict_has_key(par: Any, par_name: str, key: Any) -> None:
    """Check par to be a dictionary that includes a given key.

    Args:
        par:
        par_name:
        key:

    Raises:
        TypeError: if `par` type is not ``dict``.
        ValueError: if `par` has not the key.
    """
    check_type(par, par_name, dict)
    if key not in par:
        msg = f"No key {key} in {par_name}"
        raise ValueError(msg)


def check_dict_has_key_with_type(
        par: Any,
        par_name: str,
        key: Any,
        key_type: Type) -> None:
    """Check par to be a dictionary that includes a given key of a given type.

    Args:
        par:
        par_name:
        key:
        key_type:

    Raises:
        TypeError: if `par` type is not ``dict``.
        ValueError: if `par` has not the `key` or the `key` type is not
            `key_type`.
    """
    check_dict_has_key(par, par_name, key)
    if not isinstance(par[key], key_type):
        msg = f"{par_name}[{key}] should be {key_type}, while it has type" \
              f"{type(par[key])}."
        raise ValueError(msg)


def check_ndarray_with_type(
        par: Any,
        par_name: str,
        np_type: np.dtype) -> None:
    """Check that par is a ndarray whose type is np_type.

    Args:
        par:
        par_name:
        np_type:

    Raises:
        TypeError: if `par` type is not `ndarray`.
        ValueError: if the type of the elements of `par` is not `np_type`.
    """
    check_type(par, par_name, np.ndarray)
    if not par.dtype == np_type:
        message = f'{par_name}.dtype should be {np_type} while it is' \
                  f'{par.dtype}.'
        raise ValueError(message)


def check_homogeneous_list(
        par: Any,
        par_name: str,
        expected_type: Type) -> None:
    """Check that all elements have same type.

    Args:
        par:
        par_name:
        expected_type:

    Raises:
         TypeError: if `par` is not a list.
         ValueError: if at least one element has not type `expected_type`.
    """
    check_type(par, par_name, list)
    # pylint: disable=consider-using-enumerate
    for i in range(len(par)):
        if not isinstance(par[i], expected_type):
            msg = f"All elements of {par_name} should by of type" \
                  f"{expected_type}, while element {i} has type {type(par[i])}"
            raise ValueError(msg)


# pylint: disable=too-many-arguments
def check_in_range(
        par: Any,
        par_name: str,
        min_value: Any,
        max_value: Any,
        include_min: bool,
        include_max: bool,
) -> None:
    """Check par to be within (min_value, max_value).

    Args:
        par: Same type as `value_min`.
        par_name:
        min_value: Same type as `value_max`, less than it.
        max_value: Same type as `value_min`, grater than it.
        include_min:
        include_max:

    Raises:
        AssertionError: If input pars different from `par` do not have
          the right type/value.
        TypeError: If `not isinstance(par, type(min_value))`.
        ValueError: If par is not within the range.
    """
    if not isinstance(min_value, type(max_value)):
        msg = f'{min_value} and {max_value} should have the same type, ' \
              f'while {type(min_value)} != {type(max_value)}.'
        raise AssertionError(msg)
    check_type(par, par_name, type(min_value))

    if not min_value < max_value:
        msg = f'_min_value ({min_value}) should be less than max_va' \
              f'lue ({max_value}).'
        raise AssertionError(msg)

    _check_type_helper(include_min, 'include_min', bool, AssertionError)

    _check_type_helper(include_max, 'include_max', bool, AssertionError)

    if not ((par > min_value or (include_min and par == min_value)) and
            (par < max_value or (include_max and par == max_value))):
        msg = f"{par_name} should be in {'[' if include_min else ']'}" \
              f"{min_value},{max_value}{']' if include_min else '['}, " \
              f"while it is {par}."
        raise ValueError(msg)


def _check_type_helper(par, par_name, expected_type, raise_type):
    if not isinstance(par, expected_type):
        msg = f'{par_name} should be of type {expected_type}, while it is ' \
              f'{type(par)}.'
        raise raise_type(msg)


def check_tuple_with_len(
        par: Any,
        par_name: str,
        length: int,
) -> None:
    """Check par to be a tuple with given length.

    Args:
        par:
        par_name:
        length: positive.

    Raises:
        AssertionError: if length is not positive int.
        TypeError: if par is not a tuple.
        ValueError: if `len(par) != length`.
    """
    _check_type_helper(length, 'length', int, AssertionError)
    if not length > 0:
        msg = f'length should be positive, while it is {length}.'
        raise AssertionError(msg)
    check_type(par, par_name, tuple)
    if len(par) != length:
        msg = f'len({par_name}) should be {length}, while it is {len(par)}.'
        raise ValueError(msg)
