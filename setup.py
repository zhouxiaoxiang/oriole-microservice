import os
from setuptools import find_packages, setup

install_requires = [
    "oriole==7.0.0",
    "nameko==2.8.4",
]

with open('README.md') as readme:
    readme = readme.read()

setup(
    name='oriole-service',
    version='12.0.1',
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
