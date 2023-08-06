# -*- coding: utf-8 -*-
"""Write less test code; get more tests.

The module provides one main class, :class:`CallableTest`, and the module
function :func:`get_test_path`.
"""
import os
import logging
from copy import copy
from pathlib import Path
from typing import (Optional, Callable, Tuple, Any, Dict, List, Union)
import itertools as it
import attr
from . import input_checks as ics

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.WARNING)


def get_test_path(
        module_name: str,
        relative_path: Union[str, Path],
) -> Union[str, Path]:
    """Computes paths for testing.

    When running tests from the IDE, the working directory changes. This makes
    it difficult to define paths to files/directories, without knowing the
    project path, as it is the case when running in different environments.

    This function allows to define a path that will work for unittest and
    pytest regardless of the current working directory.

    Args:
        module_name: As obtained by `__name__`.

        relative_path: The path to file/dir relative to the test definition
            file.

    Returns:
        The absolute path to file/dir. It has the same type of `relative_path`.

    Examples:
        >>> import os
        >>> from typing import Union
        >>> from pathlib import Path
        >>> from ftrotta.pycolib.common_tests import get_test_path
        >>>
        >>>
        >>> def gtp(relative_path: Union[str, Path]) -> Union[str, Path]:
        >>>     return get_test_path(__name__, relative_path)
        >>>
        >>>
        >>> def test(self):
        >>>     fname = gtp(Path('files/')) / 'foo.png'
        >>>     fname = gtp('files/foo.png')
        >>>

    """
    ics.check_nonempty_str(module_name, 'module_name')
    return_str_type = True
    if isinstance(relative_path, Path):
        return_str_type = False
        relative_path = str(relative_path)
    elif isinstance(relative_path, str):
        ics.check_nonempty_str(relative_path, 'relative_path')
    else:
        msg = f'relative_path should either be str or pathlib.Path, ' \
              f'while it is {type(relative_path)}.'
        raise TypeError(msg)

    temp = module_name.replace('.', '/')
    test_base_path = os.path.dirname(temp)

    if relative_path[0] == '/':
        msg = f'partial_path cannot start with /, while it is \'' \
              f'{relative_path}\'. It should be the path relative to ' \
              f'\'{test_base_path}/\'.'
        raise ValueError(msg)

    test_path = os.path.join(test_base_path, relative_path)

    pwd = os.getcwd()

    non_overlapping_test_path = test_path
    i = non_overlapping_test_path.rfind('/')
    while i > -1:
        if pwd.endswith(non_overlapping_test_path[0:i]):
            non_overlapping_test_path = non_overlapping_test_path[i+1:]
            break
        i = non_overlapping_test_path.rfind('/', 0, i)

    ret = os.path.join(pwd, non_overlapping_test_path)

    if return_str_type:
        return ret

    return Path(ret)


# pylint: disable=too-few-public-methods
@attr.s(auto_attribs=True, kw_only=True)
class CallableTestConfig:
    """Configuration for test callable classes.

    Please refer to :class:`CallableTest`.

    Args:
        callable_under_test: Mind the syntax of the tuple: ``(callable,)``.
        default_arg_values_for_tests:
        wrong_value_lists:
        expected_output: defaults to None.
        skip_test_basic_behaviour: defaults to False.

    """
    callable_under_test: Tuple[Callable, ]
    """The callable under test.

    Mind the syntax of the tuple: ``(callable,)``.

    See also the examples of :class:`CallableTest`.
    """

    default_arg_values_for_tests: Dict[str, Any]
    """Every argument of the callable needs to be defined.

    :class:`OptionalArg`, :class:`MultipleTypeArg` and
    :class:`OptionalMultipleTypeArg` can be used.

    See also the examples of :class:`CallableTest`.
    """

    wrong_value_lists: Dict[str, List]
    """See also the examples of :class:`CallableTest`.
    """

    expected_output: Optional[Any] = None
    """See also :func:`CallableTest.test_basic_behaviour`.
    """

    skip_test_basic_behaviour: bool = False
    """See also :func:`CallableTest.test_basic_behaviour`.
    """


class CallableTest:
    """Base class that provides facilities to test a single callable.

    This class allows automated input type and value checking for any callable,
    being it:

    + a module function, or
    + an instance method, or
    + a class method, or
    + a class constructor.

    Warnings:
        A new test case is needed for every function/method. A single
        case can test only one function/method, the so-called "callable
        under test" (CUT).

    The CUT is automatically tested for:

    + correct checking of input types (see :func:`test_input_types`);

    + correct checking of input values (see :func:`test_input_values`);

    + correct functioning of basic behaviour (see
      :func:`test_basic_behaviour`).

    A fixture `callable_test_config` method that returns a
    :class:`CallableTestConfig` must be implemented in the derived test
    case, as shown in the following examples.

    Examples:

        >>> from apackage import amodule as mut
        >>> from ftrotta.pycolib.common_tests import (
        >>>     CallableTest,
        >>>     MultipleTypeArg, OptionalArg, OptionalMultipleTypeArg
        >>> )
        >>> from ftrotta.pycolib.log import get_configured_root_logger
        >>>
        >>> _logger = get_configured_root_logger()
        >>>
        >>> class TestModuleFunction(CallableTest):
        >>>
        >>>     @classmethod
        >>>     @pytest.fixture(scope="class")
        >>>     def callable_test_config(cls):
        >>>         config = CallableTestConfig(
        >>>             callable_under_test=(mut.afunction,), # MIND THE COMMA!
        >>>             default_arg_values_for_tests={
        >>>                 'str_or_int': 5,
        >>>                 'f': 1.0,
        >>>                 's': 'ciao',
        >>>                 'd': {},
        >>>                 'int_or_dict': MultipleTypeArg(23,  {'a': 23}),
        >>>                 'optional': OptionalArg(1),
        >>>                 'float_or_int_optional':
        >>>                     OptionalMultipleTypeArg(0.1, 12),
        >>>             },
        >>>             wrong_value_lists = {
        >>>                 'str_or_int': [-1],
        >>>                 'f': [-1.0],
        >>>                 's': [],  # any string is valid
        >>>                 'd': [],  # any dictionary is valid
        >>>                 'int_or_dict': [-1],
        >>>                 'optional': [],  # any int is valid,
        >>>                 'float_or_int_optional': [],
        >>>             },
        >>>         )
        >>>         return config
        >>>
        >>>     # test_input_types is automatically provided by
        >>>     # CallableTest
        >>>
        >>>     # test_input_values is automatically provided by
        >>>     # CallableTest
        >>>
        >>>     # test_basic_behaviour is automatically provided by
        >>>     # CallableTest


        >>>  class TestModuleFunctionWithOutput(CallableTest):
        >>>
        >>>     @classmethod
        >>>     @pytest.fixture(scope="class")
        >>>     def callable_test_config(cls):
        >>>         config = CallableTestConfig(
        >>>              callable_under_test=(am.double_float,),
        >>>              default_arg_values_for_tests={
        >>>                  "value": 2.
        >>>              },
        >>>              wrong_value_lists = {
        >>>                  "value": []
        >>>              },
        >>>              # By setting expected_output, the corresponding
        >>>              # verification is triggered. This is applicable
        >>>              # only in case of no multiple/optional arguments are
        >>>              # are present.
        >>>              expected_output=4.0,
        >>>         )
        >>>         return config



        >>> class TestInstanceMethod(CallableTest):
        >>>
        >>>     @classmethod
        >>>     @pytest.fixture(scope="class")
        >>>     def callable_test_config(cls):
        >>>         # The same as config above, but for the scope.
        >>>         # Remark: function scope is used (rather than
        >>>         #  class) in order to have a fresh object for each
        >>>         #  test.
        >>>         an_instance = mut.AClass()
        >>>         config = CallableTestConfig(
        >>>              callable_under_test=\\
        >>>                  (an_instance.a_method,),  # MIND THE COMMA!
        >>>              ...
        >>>          )
        >>>          return config
        >>>


        >>> class TestConstructor(CallableTest):
        >>>
        >>>     @classmethod
        >>>     @pytest.fixture(scope="class")
        >>>     def callable_test_config(cls):
        >>>         # The same as config above, but for the scope.
        >>>         # Remark: function scope is used (rather than
        >>>         #  class) in order to have a fresh object for each
        >>>         #  test.
        >>>         config = CallableTestConfig(
        >>>              callable_under_test=\\
        >>>                  (mut.AClass,),  # MIND THE COMMA!
        >>>              ...
        >>>          )
        >>>          return config
        >>>


        >>> class TestClassMethod(CallableTest):
        >>>
        >>>     @classmethod
        >>>     @pytest.fixture(scope="class")
        >>>     def callable_test_config(cls):
        >>>         # The same as config above, but for the scope.
        >>>         # Remark: function scope is used (rather than
        >>>         #  class) in order to have a fresh object for each
        >>>         #  test.
        >>>         config = CallableTestConfig(
        >>>              callable_under_test=\\
        >>>                  (mut.AClass.a_class_method,),  # MIND THE COMMA!
        >>>              ...
        >>>          )
        >>>          return config

    """

    @classmethod
    def _get_kwargs(cls, names: List[str], values: Tuple) -> Dict[str, Any]:
        """Creates kwargs dictionary from two lists, skipping the optionals.

        Args:
            names: List of argument names
            values: List of argument values

        Returns:
            Dictionary with input arguments. Optional
            arguments have been removed.
        """
        kwargs: Dict[str, Any] = {}
        for key, value in zip(names, values):
            if not isinstance(value, OptionalArg):
                kwargs[key] = value
        return kwargs

    @classmethod
    def _make_other_correct_values_dict(
            cls,
            default_dict: Dict[str, Any],
            current_arg_name: str,
    ) -> Dict[str, Any]:
        """

        Args:
            default_dict:
            current_arg_name:

        Returns:
            A dictionary that has value `[None]` for the
            current argument and the list of correct values for all the
            other arguments.
        """
        new_dict: Dict[str, Any] = {}
        for arg in default_dict:
            if arg == current_arg_name:
                new_dict[arg] = [None]
            else:
                if isinstance(default_dict[arg],
                              OptionalArg):
                    new_dict[arg] = [OptionalArg(), default_dict[arg].value]
                elif isinstance(default_dict[arg],
                                MultipleTypeArg):
                    new_dict[arg] = default_dict[arg].values
                elif isinstance(default_dict[arg],
                                OptionalMultipleTypeArg):
                    new_dict[arg] = [OptionalArg()] + default_dict[arg].values
                else:
                    new_dict[arg] = [default_dict[arg]]

        return new_dict

    def _create_arg_combinations(
            self, other_correct_dict: Dict[str, List]) -> List[Dict[str, Any]]:
        """Create the combinations of inputs.

        Args:
            other_correct_dict: A dict returned by
                :func:`_make_other_correct_values_dict`

        Returns:
            A list of dictionaries that can be used as input arguments.
        """
        result: List[Dict[str, Any]] = []
        arg_names = sorted(other_correct_dict)
        combinations = it.product(
            *(other_correct_dict[name] for name in arg_names))
        for arg_values in combinations:
            result.append(self._get_kwargs(arg_names, arg_values))
        return result

    @classmethod
    def get_some_types(cls) -> List:
        """

        Returns:
            List of items with different types for :func:`test_input_types`.

            It can be overridden by the child class, to provide different
            types to check against.

        Examples:

            >>>  @classmethod
            >>>  def get_some_types(self):
            >>>     l = CallableTest.get_some_types()
            >>>     l.append(np.zeros([2, 2]))
            >>>     return l
        """
        return [1, 2.0, {}, [], lambda x: x, 'str']       # pragma: no cover

    @classmethod
    def _get_cut(
            cls, callable_test_config: CallableTestConfig) -> Callable:
        """Get callable under test.
        """
        if not isinstance(callable_test_config.callable_under_test, tuple):
            raise CallableUnderTestNotTupleError(
                f"callable_under_test must be a tuple which contains a "
                f"callable. It is instead "
                f"{type(callable_test_config.callable_under_test)}"
            )
        if not callable(callable_test_config.callable_under_test[0]):
            raise NotCallableError(
                "The callable_under_test[0] must be a callable python"
                " object")
        return callable_test_config.callable_under_test[0]

    @classmethod
    def _check_configuration(
            cls, callable_test_config: CallableTestConfig) -> None:
        for name in ['callable_under_test',
                     'default_arg_values_for_tests',
                     'wrong_value_lists',
                     ]:
            if callable_test_config.__getattribute__(name) is None:
                raise MissingConfigurationError(
                    name + ' is missing')

    def _test_input_types(
            self, callable_test_config: CallableTestConfig) -> None:
        """Test that Callable Under Test raises TypeErrors correctly.

        The input for such tests is created from
        :obj:`callable_test_config.default_arg_values_for_tests` and
        :obj:`get_some_types`. For each
        argument all the values returned by :obj:`get_some_types` are used,
        except for the (only) one that has the same type of the argument.

        This method only allows for checking each argument of the Callable
        Under Test by itself. Cross-checks that involve more than one argument
        together need to be written explicitly. In this case, this method
        can be used via :func:`super`.
        """
        self._check_configuration(callable_test_config)

        wrong_type_lists: Dict[str, list] = {}
        for arg_name, arg in \
                callable_test_config.default_arg_values_for_tests.items():
            if isinstance(arg, OptionalArg):
                # pylint: disable=no-member
                arg_type = type(arg.value)
                temp = [a for a in self.get_some_types()
                        if not isinstance(a, arg_type) and a is not None]
                wrong_type_lists[arg_name] = temp
            elif isinstance(arg, MultipleTypeArg):
                # pylint: disable=no-member
                arg_types = tuple([type(a) for a in arg.values])
                temp = [a for a in self.get_some_types()
                        if not isinstance(a, arg_types)]
                wrong_type_lists[arg_name] = temp

            elif isinstance(arg, OptionalMultipleTypeArg):
                # pylint: disable=no-member
                arg_types = tuple([type(a) for a in arg.values])
                temp = [a for a in self.get_some_types()
                        if not isinstance(a, arg_types)]
                wrong_type_lists[arg_name] = temp

            else:
                temp = [a for a in self.get_some_types()
                        if not isinstance(a, type(arg))]
                wrong_type_lists[arg_name] = temp
        _logger.debug('wrong_type_list created')
        _logger.debug('Starting testing for input types')
        self._input_test_helper(callable_test_config=callable_test_config,
                                args_lists=wrong_type_lists,
                                expected_exception=TypeError)

    def _test_input_values(
            self, callable_test_config: CallableTestConfig) -> None:
        """Test that Callable Under Test raises ValueErrors correctly.

        This method only allows for checking each argument of the Callable
        Under Test by itself. Cross-checks that involve more than one argument
        together need to be written explicitly. In this case, this method
        can be used via :func:`super`.
        """
        self._check_configuration(callable_test_config)

        _logger.debug('Starting testing for input values')
        self._input_test_helper(
            callable_test_config=callable_test_config,
            args_lists=callable_test_config.wrong_value_lists,
            expected_exception=ValueError)

    def _input_test_helper(
            self,
            callable_test_config: CallableTestConfig,
            args_lists: Dict[str, list],
            expected_exception: type,
    ) -> None:
        self._check_input_test_configuration(args_lists, callable_test_config)

        fut = self._get_cut(callable_test_config)
        for arg_name in args_lists:
            values = args_lists[arg_name]

            current_none_others_correct = \
                self._make_other_correct_values_dict(
                    callable_test_config.default_arg_values_for_tests,
                    arg_name)

            input_list = self._create_arg_combinations(
                current_none_others_correct)

            for current_args in input_list:
                for val in values:
                    current_args[arg_name] = val
                    expected_exception_raised = False
                    try:
                        fut(**current_args)
                    except Exception as e:  # pylint: disable=broad-except
                        if isinstance(e, expected_exception):
                            expected_exception_raised = True
                        else:
                            msg = f'Expecting exception {expected_exception}' \
                                  f' for arg \'{arg_name}\' with value' \
                                  f' {val}, while {type(e)} was ' \
                                  f'raised. Description: {str(e)}'
                            raise AssertionError(msg)  # pylint: disable=W0707

                    if not expected_exception_raised:
                        msg = f'Expected exception {expected_exception} not ' \
                              f'raised for arg \'{arg_name}\' with value ' \
                              f'{val}.'
                        raise AssertionError(msg)

    @classmethod
    def _check_input_test_configuration(
            cls,
            args_lists: Dict[str, list],
            callable_test_config: CallableTestConfig,
    ):
        ics.check_type(args_lists, 'args_list', dict)
        for arg_name in args_lists:
            ics.check_type(args_lists[arg_name], arg_name, list)
        ics.check_type(
            callable_test_config.default_arg_values_for_tests,
            'default_arg_values_for_tests', dict)
        ics.check_type(
            callable_test_config.wrong_value_lists,
            'wrong_value_lists', dict)
        for arg_name, _ in \
                callable_test_config.default_arg_values_for_tests.items():
            if arg_name not in args_lists:
                raise MissingArgumentError(
                    f'Argument {arg_name} is not in \'args_list\'. Each '
                    f'argument present in default_arg_values_for_tests '
                    f'should be defined. If you do not want to provide any '
                    f'value to check, please assign an empty list to the '
                    f'argument')

    def test_input_types(self, callable_test_config: CallableTestConfig):
        """Check that the callable raises a :obj:`TypeError` when an input
        with type different from that in :any:`default_arg_values_for_tests`
        is given.

        The values that are used as wrong type values can be managed in
        :func:`get_some_types`.
        """
        self._test_input_types(callable_test_config)

    def test_input_values(self, callable_test_config: CallableTestConfig):
        """Check that the callable raises a :obj:`ValueError` when an input
        with value defined in :any:`wrong_value_lists` is given.
        """
        self._test_input_values(callable_test_config)

    def test_basic_behaviour(self, callable_test_config: CallableTestConfig):
        """Check that no exception is raised when the callable is invoked
        with inputs defined in :any:`default_arg_values_for_tests`.

        Warnings:
            In case :obj:`OptionalArg` or :obj:`MultipleTypeArg` or
            :obj:`OptionalMultipleTypeArg` are used, this leads to multiple
            effective inputs to be checked. In doing so, no copies of the
            inputs are created. This means that any **side effect** of the
            callable on any of its inputs could impair the test.

            If your callable under test has side effects that could influence
            the output, please: (1) skip this test by setting
            :any:`skip_test_basic_behaviour` to `True`; and (2) **perform
            custom behavioural testing**, by implementing your test functions.

        If :any:`CallableTestConfig.expected_output` is not None, output
        checking is triggered.
        """

        self._check_configuration(callable_test_config)

        if not callable_test_config.skip_test_basic_behaviour:
            _logger.info(
                "Performing test_basic_behaviour for %s...",
                self._get_cut(callable_test_config).__name__
            )

            input_list = self._unroll_kwargs_dict(
                callable_test_config.default_arg_values_for_tests)

            if len(input_list) > 1:
                if callable_test_config.expected_output is not None:
                    msg = f"expected_output is not None for " \
                      f"{self._get_cut(callable_test_config).__name__}," \
                      f" but no verification can be performed, given " \
                      f"that {len(input_list)} input combinations need " \
                      f"to be used. expected_output should be set to None."
                    _logger.warning(msg)

                # Multiple inputs combinations need to be checked
                for i in input_list:
                    fun_name = self._get_cut(callable_test_config).__name__
                    _logger.info(
                        "Checking %s against %s should not raise any "
                        "exception...",
                        fun_name,
                        i)
                    self._get_cut(callable_test_config)(
                        **i,
                    )
            else:
                # Single input combination: output check can be done.
                ans = self._get_cut(callable_test_config)(
                    **input_list[0],
                )
                fun_name = self._get_cut(callable_test_config).__name__
                if callable_test_config.expected_output is not None:
                    msg = f"Verifying expected output for {fun_name} " \
                          f"against {input_list[0]}..."
                    _logger.info(msg)
                    expected = callable_test_config.expected_output
                    if expected != ans:
                        msg = f'Actual output differs from expectation. ' \
                              f'Actual: {ans}. Expected: {expected}.'
                        raise ValueError(msg)
                else:
                    _logger.info("No output verification for %s",
                                 fun_name)
            _logger.info(
                "test_basic_behaviour for %s done",
                self._get_cut(callable_test_config).__name__
            )
        else:
            _logger.info(
                "Skipping test_basic_behaviour for %s",
                self._get_cut(callable_test_config).__name__
            )

    # pylint: disable=too-many-branches
    @classmethod
    def _unroll_kwargs_dict(
            cls, kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Unroll kwargs dict into the list of all possible kwargs.

        Args:
            kwargs: A kwargs dictionary that could contain *Arg objects, i.e.
                :class:`OptionalArg`, class:`MultipleTypeArg` or
                class:`OptionalMultipleTypeArg`.

        Returns:
            List of kwargs dictionaries corresponding to the "unrolling" of
            *Arg objects.
        """
        kwargs_list = list()
        for arg_name, arg_value in kwargs.items():
            value_list = cls._get_extended_value_list(arg_value)

            if not kwargs_list:
                # Handling the first argument
                for value in value_list:
                    new_kwargs = {arg_name: value}
                    kwargs_list.append(new_kwargs)
            else:
                # Every kwargs in the list needs to be "multiplied" by each
                # value of the current argument
                new_kwargs_list = list()
                for kwa in kwargs_list:
                    for value in value_list:
                        new_kwargs = copy(kwa)
                        new_kwargs[arg_name] = value
                        new_kwargs_list.append(new_kwargs)
                kwargs_list = new_kwargs_list

        cls._remove_optional_args(kwargs_list)
        return kwargs_list

    @classmethod
    def _remove_optional_args(cls, kwargs_list) -> None:
        """Remove the :class:`OptionalArg`s from the kwargs.

        Args:
            kwargs_list:

        """
        for kwargs in kwargs_list:
            args_to_be_removed = []
            for arg_name, arg_value in kwargs.items():
                if isinstance(arg_value, OptionalArg):
                    args_to_be_removed.append(arg_name)
            for par in args_to_be_removed:
                del kwargs[par]

    @classmethod
    def _get_extended_value_list(cls, arg_value: Any) -> List:
        """Create a list of values with :class:`OptionalArg`.

        An optional argument is an argument that can be assigned no value.
        An empty :class:`OptionalArg` object is used to model this.

        Args:
            arg_value: can be anything or *Arg type,
                i.e. :class:`OptionalArg`, class:`MultipleTypeArg` or
                class:`OptionalMultipleTypeArg`

        Returns:
            The extended list of values that contains an empty
            :class:`OptionalArg`, if `arg_value`has type Optional*Arg.
        """
        if isinstance(arg_value, OptionalArg):
            value_list = [arg_value.value, OptionalArg()]
        elif isinstance(arg_value, MultipleTypeArg):
            value_list = arg_value.values
        elif isinstance(arg_value, OptionalMultipleTypeArg):
            value_list = arg_value.values + [OptionalArg()]
        else:
            value_list = [arg_value]
        return value_list


class CommonTestsException(Exception):
    """Base class for exceptions."""


# pylint: disable=missing-docstring
class CallableUnderTestNotTupleError(CommonTestsException):
    pass


# pylint: disable=missing-docstring
class NotCallableError(CommonTestsException):
    pass


# pylint: disable=missing-docstring
class MissingArgumentError(CommonTestsException):
    pass


# pylint: disable=missing-docstring
class MissingConfigurationError(CommonTestsException):
    pass


# pylint: disable=too-few-public-methods
class MultipleTypeArg:
    def __init__(self, *args):
        """A parameter that allows multiple types.

        Args:
            *args: any number of arguments of different types.
        """
        self.values = list(args)


# pylint: disable=too-few-public-methods
class OptionalArg:
    def __init__(self, arg=None):
        """An optional parameter.

        An optional parameter has a default value, regardless of such default
        value. Indeed it can have a default value to `None` or a default
        value to any other value.

        A parameter that needs to be specified and can take `None` value,
        as well as another value, is not an optional parameter. It is a
        :obj:`MultipleTypeArg`.


        Args:
            arg: The value that the argument will take when it will be
                specified.
        """
        self.value = arg


# pylint: disable=too-few-public-methods
class OptionalMultipleTypeArg:
    def __init__(self, *args):
        """An optional parameter with multiple types.

        Please refer to :obj:`OptionalArg` for considerations on optional
        parameters.

        Args:
            *args: any number of arguments of different types.
        """
        self.values = list(args)
