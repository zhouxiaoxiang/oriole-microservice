from setuptools import find_packages, setup

install_requires = [
    "nameko==2.11.0",
    "oriole>=16.1.0",
]

setup(
    name='oriole-service',
    version='26.1.0',
    description='Rapidly create services.',
    long_description=open('README.rst').read(),
    author='Eric.Zhou',
    author_email='xiaoxiang.cn@gmail.com',
    url='https://github.com/zhouxiaoxiang/oriole-service',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'o=oriole_service.cli:main',
        ],
    },
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ])
