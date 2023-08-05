# pylint: disable=missing-docstring
# -*- coding: utf-8 -*-

import logging
from typing import Union
from pathlib import Path
import pytest
from ftrotta.pycolib.log import get_configured_root_logger
from ftrotta.pycolib.common_tests import (
    CallableTest, CallableTestConfig, get_test_path)
from ftrotta.pycolib import setup as mut

_logger = get_configured_root_logger()
_temp = logging.getLogger(mut.__name__)
_temp.setLevel(logging.INFO)


def gtp(partial_path: Union[str, Path]) -> Union[str, Path]:
    return get_test_path(__name__, partial_path)


class TestInferPackageInfoInput(CallableTest):

    @classmethod
    @pytest.fixture
    def callable_test_config(cls):
        config = CallableTestConfig(
            callable_under_test=(mut.infer_package_info, ),
            default_arg_values_for_tests={
                'where': str(gtp('files/native/src')),
                'group': 'group',
                'rtfd': True,
            },
            wrong_value_lists={
                'where': ['/foo'],
                'group': ['bar', ''],
                'rtfd': [],
            },
        )
        return config


@pytest.mark.parametrize("namespace_style", ["native", "pkgutil"])
@pytest.mark.parametrize("rtfd, documentation_url", [
    (True, 'https://group-project.readthedocs.io'),
    (False, 'https://group.gitlab.io/project'),
])
def test_infer_package_info_project(namespace_style, rtfd, documentation_url):
    pkg_name, project_urls, pkg_list = mut.infer_package_info(
        str(gtp(f'files/{namespace_style}/src')),
        'group',
        rtfd,
    )
    assert pkg_name == 'group.project'
    assert project_urls == \
           {
               'Source Code': 'https://gitlab.com/group/project',
               'Documentation': documentation_url,
           }
    assert ['group.project'] == pkg_list


def test_infer_package_info_multiple_l2():
    with pytest.raises(ValueError) as exinfo:
        mut.infer_package_info(
            str(gtp('files/pkgutil/src')), 'multiple', True)
    exception_msg = exinfo.value.args[0]
    assert exception_msg == 'Unexpected number of level 2 packages: it ' \
                            'should be 1, while it is 2.'
