"""Module with setup facilities.
"""
from pathlib import Path
from typing import (Tuple, Dict, List)
from urllib.parse import urlparse
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


# pylint: disable=too-many-locals
def get_install_requires(fname: str, schema: str) -> List[str]:
    """Get the `install_requires` list from `requirements.txt` file.

    The main goal is to manage the git+ requirements, such as
    `git+https://gitlab.com/foo/bar.git`. Such a requirement is accepted in
    `requirements.txt, but not in `install_requires` of `setup.py`. For this to
    happen it must be converted to `<package>@git+<url>`. Please refer to
    https://stackoverflow.com/questions/55385900/pip3-setup-py-install-requires-pep-508-git-url-for-private-repo.

    The function also parses files included via the '-r' syntax. It ignores
    the comment and empty lines.

    Args:
        fname:
        schema: only 'gitlab' is accepted. It converts
            `git+https://gitlab.com/foo/bar.git` to
            `foo.bar@git+https://gitlab.com/foo/bar.git`.

    Returns:
        The list of requirements to be used as `install_requires` in
        `setup.py`.
    """
    ics.check_nonempty_str(fname, 'fname')
    fname = Path(fname)
    ics.check_isfile(fname, 'fname')
    ics.check_nonempty_str(schema, 'schema')

    if fname.is_absolute():
        base_path = fname.parent
    else:
        base_path = Path.cwd() / fname.parent

    res: List[str] = list()

    if schema == 'gitlab':
        with open(fname, 'r') as req_file:
            lines = req_file.readlines()

        for line in lines:
            if line.endswith('\n'):
                line = line[:-1]

            if not line or line.startswith('#'):
                continue

            if line.startswith('-r'):
                included_fname = str(base_path / line[3:])
                included_reqs = get_install_requires(included_fname, schema)
                res = res + included_reqs
            elif line.startswith('git+'):
                parse_url = urlparse(line[4:])
                temp = parse_url.path.split('/')
                if not len(temp) == 3:
                    msg = f'The URL or the git repository should be like ' \
                          f'http://gitlab.com/<group>/<project>.git, ' \
                          f'while it is {line}.'
                    raise ValueError(msg)
                group = temp[1]
                i = temp[2].find('.git')
                package = temp[2][:i]
                req = f'{group}.{package}@{line}'
                res.append(req)
            else:
                res.append(line)
    else:
        raise ValueError(f'Unexpected schema: {schema}.')
    return res
