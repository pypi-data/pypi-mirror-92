from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements/run.txt') as fh:
    install_requires = fh.read()

setup(
    name='ftrotta.pycolib',
    use_scm_version=True,
    project_urls={
        'Source Code': 'https://gitlab.com/ftrotta/pycolib',
        'Documentation': 'https://pycolib.readthedocs.io',
    },
    author='Francesco Trotta',
    description='A collection of tools of common usage in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src/'},
    packages=['ftrotta.pycolib'],
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
