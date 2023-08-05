# pylint: disable=missing-docstring
# -*- coding: utf-8 -*-

from pathlib import Path
import pytest
import numpy as np
from ftrotta.pycolib.common_tests import (
    get_test_path,
)
from ftrotta.pycolib import input_checks as mut


def gtp(partial_path):
    return get_test_path(__name__, partial_path)


def test_check_type():
    with pytest.raises(TypeError):
        mut.check_type(5, 'par', float)

    mut.check_type(5, 'par', int)


def test_check_multiple_type():
    with pytest.raises(TypeError):
        mut.check_multiple_type(5, 'par', (float, bool))

    mut.check_multiple_type(5, 'par', (float, int))


def test_check_optional_type():
    with pytest.raises(TypeError):
        mut.check_noneable_type(5, 'par', float)

    mut.check_noneable_type(None, 'par', int)


def test_check_nonempty_str():
    wrong_value = ''
    wrong_type = 5
    correct_value = 'afunction'
    _test_helper(wrong_value=wrong_value,
                 wrong_type=wrong_type,
                 correct_value=correct_value,
                 func=mut.check_nonempty_str)


def test_check_isdir():
    wrong_value = gtp(Path('pippo/'))
    wrong_type = '/pippo'
    correct_value = gtp(Path('files/'))
    _test_helper(wrong_value=wrong_value,
                 wrong_type=wrong_type,
                 correct_value=correct_value,
                 func=mut.check_isdir)


def test_check_isfile():
    wrong_value = gtp(Path('ciao'))
    wrong_type = '/pippo'
    correct_value = gtp(Path('test_input_checks.py'))
    _test_helper(wrong_value=wrong_value,
                 wrong_type=wrong_type,
                 correct_value=correct_value,
                 func=mut.check_isfile)


def test_check_positiveint():
    wrong_value = 0
    wrong_type = 'pippo'
    correct_value = 1
    _test_helper(wrong_value=wrong_value,
                 wrong_type=wrong_type,
                 correct_value=correct_value,
                 func=mut.check_positiveint)


def test_check_positivefloat():
    wrong_value = 0.
    wrong_type = 'pippo'
    correct_value = 1.1
    _test_helper(wrong_value=wrong_value,
                 wrong_type=wrong_type,
                 correct_value=correct_value,
                 func=mut.check_positivefloat)


def test_check_nonnegativeint():
    wrong_value = -1
    wrong_type = 'pippo'
    correct_value = 0
    _test_helper(wrong_value=wrong_value,
                 wrong_type=wrong_type,
                 correct_value=correct_value,
                 func=mut.check_nonnegativeint)


def test_check_nonnegativefloat():
    wrong_value = -1.3
    wrong_type = 'pippo'
    correct_value = 0.
    _test_helper(wrong_value=wrong_value,
                 wrong_type=wrong_type,
                 correct_value=correct_value,
                 func=mut.check_nonnegativefloat)


def test_check_dict_has_key():
    mut.check_dict_has_key({'key': 1}, 'par', 'key')
    with pytest.raises(TypeError):
        mut.check_dict_has_key(1, 'par', 'key')
    with pytest.raises(ValueError):
        mut.check_dict_has_key({'key': 1}, 'par', 'ring')


def test_check_dict_has_key_with_type():
    mut.check_dict_has_key_with_type({'key': 1}, 'par', 'key', int)
    with pytest.raises(TypeError):
        mut.check_dict_has_key_with_type(1, 'par', 'key', int)
    with pytest.raises(ValueError):
        mut.check_dict_has_key_with_type({'key': 1}, 'par', 'ring', int)
    with pytest.raises(ValueError):
        mut.check_dict_has_key_with_type({'key': 1.}, 'par', 'key', int)


def test_check_ndarray_with_type():
    mut.check_ndarray_with_type(np.zeros([1, 1]), 'par', np.float)
    with pytest.raises(TypeError):
        mut.check_ndarray_with_type(2, 'par', np.float)
    with pytest.raises(ValueError):
        mut.check_ndarray_with_type(np.zeros([1, 1]), 'par', np.uint8)


def test_check_homogeneus_list():
    for value, tipo in [
        ([1, 2, 3], int),
        (['1', '2', '3'], str),
    ]:
        mut.check_homogeneous_list(value, 'v', tipo)

    for value in ['1', 2, None]:
        with pytest.raises(TypeError):
            mut.check_homogeneous_list(value, 'v', int)

    for value, tipo in [
        ([1, 2, '3'], int),
        ([2, 'a', 2], str),
        ([1., 2., 3], float),
    ]:
        with pytest.raises(ValueError):
            mut.check_homogeneous_list(value, 'v', tipo)


def _test_helper(wrong_value, wrong_type, correct_value, func):
    with pytest.raises(ValueError):
        func(wrong_value, 'par')
    with pytest.raises(TypeError):
        func(wrong_type, 'par')
    func(correct_value, 'par')


def test_check_in_range():
    for pars in [
        {
            'par': 1.,
            'par_name': 'p',
            'min_value': 1.,
            'max_value': 2,
            'include_min': True,
            'include_max': True,
        },
    ]:
        with pytest.raises(AssertionError):
            mut.check_in_range(**pars)

    for pars in [
        {
            'par': 1,
            'par_name': 'p',
            'min_value': 1.,
            'max_value': 2.,
            'include_min': True,
            'include_max': True,
        },
    ]:
        with pytest.raises(TypeError):
            mut.check_in_range(**pars)

    for pars in [
        {
            'par': 1.,
            'par_name': 'p',
            'min_value': 1.,
            'max_value': 2.,
            'include_min': False,
            'include_max': False,
        },
        {
            'par': 2.,
            'par_name': 'p',
            'min_value': 1.,
            'max_value': 2.,
            'include_min': False,
            'include_max': False,
        },
        {
            'par': 3.,
            'par_name': 'p',
            'min_value': 1.,
            'max_value': 2.,
            'include_min': False,
            'include_max': False,
        },
        {
            'par': 0.,
            'par_name': 'p',
            'min_value': 1.,
            'max_value': 2.,
            'include_min': False,
            'include_max': False,
        },
    ]:
        with pytest.raises(ValueError):
            mut.check_in_range(**pars)

    for pars in [
        {
            'par': 1.,
            'par_name': 'p',
            'min_value': 1.,
            'max_value': 2.,
            'include_min': True,
            'include_max': False,
        },
        {
            'par': 2.,
            'par_name': 'p',
            'min_value': 1.,
            'max_value': 2.,
            'include_min': False,
            'include_max': True,
        },
        {
            'par': 1.5,
            'par_name': 'p',
            'min_value': 1.,
            'max_value': 2.,
            'include_min': False,
            'include_max': False,
        },
    ]:
        mut.check_in_range(**pars)


def test_check_tuple_with_len():
    for length in ['0', 0, 0., 4., -1]:
        with pytest.raises(AssertionError):
            mut.check_tuple_with_len((1,), 'p', length)

    for tup, length in [
        ((1, 2, 3), 2),
        ((1, ), 2),
    ]:
        with pytest.raises(ValueError):
            mut.check_tuple_with_len(tup, 'p', length)

    for tup in []:
        with pytest.raises(TypeError):
            mut.check_tuple_with_len(tup, 'p', 2)

    for tup, length in [((1, 2, 3), 3), ((1,), 1), ]:
        mut.check_tuple_with_len(tup, 'p', length)
