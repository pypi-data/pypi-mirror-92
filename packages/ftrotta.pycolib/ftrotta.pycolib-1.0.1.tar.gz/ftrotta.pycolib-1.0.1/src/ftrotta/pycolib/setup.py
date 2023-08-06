"""Module with setup facilities.
"""
from pathlib import Path
from typing import (Tuple, Dict, List)
import setuptools
import ftrotta.pycolib.input_checks as ics


def infer_package_info(
        where: str,
        group: str,
        rtfd: bool,
) -> Tuple[str, Dict[str, str], List[str]]:
    """Infer package information from the filesystem.

    It assumes that there is only one main package, that is the object of the
    development of the repository.

    Such project package is assumed to be second-level subpackage.
    In particular a structure like `<group>.<project_package>`
    is assumed. This complies with `PEP423 Use single name`_.

    The first level package, namely `<group>` represents the author or
    the organization. It can a namespace package, in the form of either a
    `native namespace package`_, that has no `__init__.py` file in it, or a
    `pkgutil-style namespace package`_. Please recall that the strategy
    cannot be changed and all projects need to share the same method for the
    namespace package.

    .. _`PEP423 Use single name`:
        https://www.python.org/dev/peps/pep-0423/#use-a-single-name

    .. _`native namespace package`:
        https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages

    .. _`pkgutil-style namespace package`:
        https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages

    Args:
        where: Path where to look for packages, the source directory.

        group: The name of the author or organization.

        rtfd: Whether the documentation is hosted in ReadTheDocs.
            Alternatively, it is considered to be hosted in the Gitlab Pages of
            the project.

    Returns:
        (project_package, project_urls, pkg_list)

        * project_package: The name of the main package. It can be used for
          the `name` parameter of `setup.py`.

        * project_urls: The Source Code and Documentation URLs. A project
          hosted in Gitlab.com is assumed.

        * pkg_list: The list of packages to be installed.

    """
    ics.check_isdir(Path(where), 'where')
    ics.check_nonempty_str(group, 'group')
    ics.check_type(rtfd, 'rtfd_docs', bool)
    pkg_list = setuptools.find_namespace_packages(
        where,
        include=[f'{group}.*'],
    )

    nesting_levels = _check_nesting_levels(pkg_list)

    project_package = [name for name, level in nesting_levels if level == 2][0]
    temp = project_package.split('.')
    project_name = temp[1]

    if rtfd:
        documentation_url = f'https://{group}-{project_name}.readthedocs.io'
    else:
        documentation_url = f'https://{group}.gitlab.io/{project_name}'

    project_urls = {
        'Source Code': f'https://gitlab.com/{group}/{project_name}',
        'Documentation': documentation_url,
    }
    return project_package, project_urls, pkg_list


def _check_nesting_levels(pkg_list: List[str]) -> List[Tuple[str, int]]:
    nesting_levels = [(p, len(p.split('.'))) for p in pkg_list]

    def count_for_level(level):
        return len([p for p in nesting_levels if p[1] == level])

    if not count_for_level(2) == 1:
        msg = f'Unexpected number of level 2 packages: it ' \
              f'should be 1, while it is {count_for_level(2)}.'
        raise ValueError(msg)

    return nesting_levels
