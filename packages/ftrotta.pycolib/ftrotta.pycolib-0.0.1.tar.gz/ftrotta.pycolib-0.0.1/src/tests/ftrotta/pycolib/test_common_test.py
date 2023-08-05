# pylint: disable=missing-docstring
# -*- coding: utf-8 -*-

import logging
import os
import pickle
from pathlib import Path
from multiprocessing.pool import Pool
import pytest
import numpy as np
from ftrotta.pycolib.common_tests import (
    CallableTest, CallableTestConfig, MultipleTypeArg, OptionalArg,
    OptionalMultipleTypeArg, MissingConfigurationError,
    CallableUnderTestNotTupleError, NotCallableError, MissingArgumentError,
    get_test_path
)
from ftrotta.pycolib import _amodule as am
from ftrotta.pycolib.log import get_configured_root_logger


_logger = get_configured_root_logger()
_temp = logging.getLogger(__name__)
_temp.setLevel(logging.DEBUG)


class TestModuleFunction(CallableTest):

    @pytest.fixture(scope="class")
    def callable_test_config(self) -> CallableTestConfig:
        return self.config_helper()

    @classmethod
    def config_helper(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.afunction,),
            default_arg_values_for_tests={
                'int_v': 5,
                'float_v': 1.0,
                'str_v': 'ciao',
                'dict_v': {},
                'other_v': am.AClass(3.),
                'int_or_dict_v': MultipleTypeArg(23, {'a': 23}),
                'optional_v': OptionalArg(1),
                'float_or_int_optional_v':
                    OptionalMultipleTypeArg(0.1, 12)
            },
            wrong_value_lists={
                'int_v': [-1],
                'float_v': [-1.0],
                'str_v': [],  # any string is valid
                'dict_v': [],  # any dictionary is valid
                'other_v': [],
                'int_or_dict_v': [-1],
                'optional_v': [],  # any int is valid,
                'float_or_int_optional_v': []
            }

        )
        return data

    # Adding some other types to the default ones.
    # (this is not strictly needed)
    @classmethod
    def get_some_types(cls):
        type_list = CallableTest.get_some_types()
        type_list.append(np.zeros([2, 2]))
        return type_list

    @pytest.mark.skip(reason="Demonstrating skipping")
    def test_skipped(self):
        pass


def _test_exception_helper(
        test_case: CallableTest,
        config: CallableTestConfig,
        expected_exception) -> None:
    with pytest.raises(expected_exception):
        test_case.test_input_types(config)
    with pytest.raises(expected_exception):
        test_case.test_input_values(config)


def test_missing_callable_under_test():
    test_case = TestModuleFunction()
    config = TestModuleFunction.config_helper()
    config.callable_under_test = None
    _test_exception_helper(test_case, config, MissingConfigurationError)


def test_wrong_callable_under_test_1():
    test_case = TestModuleFunction()
    config = TestModuleFunction.config_helper()
    config.callable_under_test = config.callable_under_test[0]
    _test_exception_helper(test_case, config, CallableUnderTestNotTupleError)


def test_wrong_callable_under_test_2():
    test_case = TestModuleFunction()
    config = TestModuleFunction.config_helper()
    config.callable_under_test = (1, )
    _test_exception_helper(test_case, config, NotCallableError)


def test_missing_default_arg_values_for_tests():
    test_case = TestModuleFunction()
    config = TestModuleFunction.config_helper()
    config.default_arg_values_for_tests = None
    _test_exception_helper(test_case, config, MissingConfigurationError)


def test_missing_wrong_value_lists():
    test_case = TestModuleFunction()
    config = TestModuleFunction.config_helper()
    config.wrong_value_lists = None
    _test_exception_helper(test_case, config, MissingConfigurationError)


def test_missing_argument():
    test_case = TestModuleFunction()
    config = TestModuleFunction.config_helper()
    config.wrong_value_lists.pop('int_v')
    with pytest.raises(MissingArgumentError):
        test_case.test_input_values(config)


def test_missing_expected_exception():
    obj = CallableTest()
    config = CallableTestConfig(
        callable_under_test=(am.do_not_perform_any_input_checking,),
        default_arg_values_for_tests={'par': 1},
        wrong_value_lists={'par': [-1]},
    )
    with pytest.raises(AssertionError):
        obj.test_input_types(config)
    with pytest.raises(AssertionError):
        obj.test_input_values(config)

    config = CallableTestConfig(
        callable_under_test=(am.raise_exception,),
        default_arg_values_for_tests={'par': 1},
        wrong_value_lists={'par': [-1]}, )
    with pytest.raises(AssertionError):
        obj.test_input_types(config)


def detect_src_path() -> str:
    pwd = os.getcwd()
    i = pwd.find('tests')
    if i > -1:
        ret = pwd[:i]
    else:
        ret = pwd
    return ret


class TestGetTestPath(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(get_test_path, ),
            default_arg_values_for_tests={
                'module_name': __name__,
                'relative_path': MultipleTypeArg('files/', Path('files/')),
            },
            wrong_value_lists={
                'module_name': [''],
                'relative_path': ['', '/files/'],
            },
        )
        return data

    def test_pytest_like_call(self, callable_test_config):
        """
        When run in pytest the module name is always complete, regardless
        of the current working directory.
        """

        src_path = detect_src_path()
        expected_output = os.path.join(
            src_path, 'tests/ftrotta/pycolib/files/')
        pwd = os.getcwd()

        for working_dir in [
            '',
            'tests/',
            'tests/ftrotta',
            'tests/ftrotta/pycolib',
        ]:
            os.chdir(os.path.join(src_path, working_dir))
            cur = self._get_cut(callable_test_config)(
                'tests.ftrotta.pycolib.test_common_test', 'files/')
            assert expected_output == cur

        os.chdir(pwd)


class TestInstanceMethod(CallableTest):

    @classmethod
    @pytest.fixture(scope="function")
    def callable_test_config(cls) -> CallableTestConfig:
        ainstance = am.AClass(3.)
        data = CallableTestConfig(
            callable_under_test=(ainstance.a_method,),
            default_arg_values_for_tests={
                "arg": 2.
            },
            wrong_value_lists={
                "arg": [-1.]
            },
        )
        return data


class TestConstructor(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.AClass,),
            default_arg_values_for_tests={
                "in_value": 2.
            },
            wrong_value_lists={
                "in_value": [-1.]
            },
        )
        return data


class TestBasicBehaviour(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.double_float,),
            default_arg_values_for_tests={
                "value": 2.
            },
            wrong_value_lists={
                "value": []
            },
        )
        return data


class TestBasicBehaviourOptional(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.double_int_if_given,),
            default_arg_values_for_tests={
                "value": OptionalArg(2)
            },
            wrong_value_lists={
                "value": []
            },
        )
        return data


class TestBasicBehaviourOptionalWithOutput(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.double_int_if_given,),
            default_arg_values_for_tests={
                "value": OptionalArg(2)
            },
            wrong_value_lists={
                "value": []
            },
            expected_output=4,
        )
        return data


class TestBehaviourWithTwoOptional(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.fun_with_two_optionals,),
            default_arg_values_for_tests={
                "str_or_int": MultipleTypeArg('pippo', 3),
                "a": OptionalArg(3),
                "b": OptionalArg(7.)
            },
            wrong_value_lists={
                "str_or_int": ['', -1],
                "a": [-1, 0],
                "b": [-1., 0.],
            },
        )
        return data


class TestBasicBehaviourNoneableSingle(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.fun_with_noneable,),
            default_arg_values_for_tests={
                "value": MultipleTypeArg(None, 2)
            },
            wrong_value_lists={
                "value": []
            },
        )
        return data


# pylint: disable=missing-docstring
def is_picklable(obj):
    try:
        pickle.dumps(obj)
    except (pickle.PicklingError, NotImplementedError):
        return False
    return True


class TestBasicBehaviourOptionalNonPickleable(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.function_non_pickleable_optional_input,),
            default_arg_values_for_tests={
                "pool": OptionalArg(Pool())
            },
            wrong_value_lists={
                "pool": []
            },
        )
        return data

    # pylint: disable=no-self-use
    def test(self):
        assert not is_picklable(Pool())


class TestSkipTestBasicBehaviour(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.double_float,),
            default_arg_values_for_tests={
                "value": 2.
            },
            wrong_value_lists={
                "value": []
            },
            skip_test_basic_behaviour=True,
        )
        return data


class TestOutputValue(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.double_float,),
            default_arg_values_for_tests={
                "value": 2.
            },
            wrong_value_lists={
                "value": []
            },
            expected_output=4.0,
        )
        return data


class TestClassMethod(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.AClass.a_class_method,),
            default_arg_values_for_tests={
                "value": 2
            },
            wrong_value_lists={
                "value": [-1]
            },
        )
        return data

    @pytest.mark.skip(reason="Demonstrating skipping")
    def test_skipped(self, config):
        pass


# pylint: disable=too-few-public-methods
class TestSkipped:

    @pytest.mark.skip(reason="Demonstrating skipping")
    def test_skipped(self):
        pass


class TestOptionalParameterDifferentFromNone(CallableTest):

    @classmethod
    @pytest.fixture(scope="class")
    def callable_test_config(cls) -> CallableTestConfig:
        data = CallableTestConfig(
            callable_under_test=(am.optional_different_from_none,),
            default_arg_values_for_tests={
                "a": OptionalArg(10)
            },
            wrong_value_lists={
                "a": [-1, 0]
            },
            expected_output=2.,
        )
        return data
