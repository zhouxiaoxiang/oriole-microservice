#!/usr/bin/env python

import os
import re
import sys
from codecs import open
from ast import literal_eval
from setuptools import find_packages, setup

if sys.version_info[:2] < (3, 6):
    raise RuntimeError('Error: Python < 3.6')

_ver = re.compile(r'__version__\s+=\s+(.+)')
with open('oriole_service/__init__.py', 'rb') as f:
    version = str(literal_eval(_ver.search(f.read().decode()).group(1)))

install_requires = [
    "oriole>=5.5.0",
    "nameko==2.7.0",
    "mogo==0.4.0",
    "redis==2.10.6",
]

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), 'r', 'utf-8') as handle:
    readme = handle.read()

setup(
    name='oriole-service',
    version=version,
    description='Rapidly create services.',
    long_description=readme,
    author='Eric.Zhou',
    author_email='xiaoxiang.cn@gmail.com',
    url='https://github.com/zhouxiaoxiang/oriole-service',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'oriole=oriole_service.cli:main',
            'o=oriole_service.cli:main',
        ],
    },
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ])
