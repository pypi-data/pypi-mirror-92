from setuptools import setup
from ftrotta.pycolib.setup import infer_package_info

SRC_PATH = 'src/'


name, project_urls, packages = infer_package_info(
    where=SRC_PATH, group='ftrotta', rtfd=True)

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements/run.txt') as fh:
    install_requires = fh.read()

setup(
    name=name,
    use_scm_version=True,
    project_urls=project_urls,
    author='Francesco Trotta',
    description='A collection of tools of common usage in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': SRC_PATH},
    packages=packages,
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=install_requires,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
