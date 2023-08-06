# -*- coding: utf-8 -*-
"""unicategories setuptools script."""
"""
unicategories
=============

Unicode category database.

More details on project `README.md` and
`repository <https://gitlub.com/ergoithz/unicategories/>`_.

License
-------
MIT (see LICENSE file).
"""

import io
import re

from setuptools import find_packages, setup

from unicategories_setup import Distribution

from unicategories_tools.cache import generate_and_cache


with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()


with io.open('unicategories/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='unicategories',
    version=version,
    url='https://gitlab.com/ergoithz/unicategories',
    license='MIT',
    author='Felipe A. Hernandez',
    author_email='ergoithz@gmail.com',
    description='Unicode category database',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    keywords=['unicode'],
    extras_require={
        'codestyle': [
            'flake8',
            'flake8-blind-except',
            'flake8-bugbear',
            'flake8-builtins',
            'flake8-commas',
            'flake8-docstrings',
            'flake8-import-order',
            'flake8-logging-format',
            'flake8-rst-docstrings',
            ],
        'coverage': [
            'coverage',
            ],
        'tests': [
            'coverage',
            ],
        },
    py_modules=['unicategories'],
    packages=find_packages('.', exclude=['unicategories_setup', 'tests']),
    package_content={
        'unicategories': {
            'database.pickle': generate_and_cache,
            },
        },
    install_requires=['appdirs'],
    test_suite='tests',
    distclass=Distribution,
    zip_safe=True,
    platforms='any',
    )
