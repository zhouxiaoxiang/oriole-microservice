import os
from setuptools import find_packages, setup

install_requires = [
    "oriole>=7.2.0",
    "nameko>=2.8.4",
]

setup(
    name='oriole-service',
    version='12.4.0',
    description='Rapidly create services.',
    long_description=open('README.md').read(),
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
