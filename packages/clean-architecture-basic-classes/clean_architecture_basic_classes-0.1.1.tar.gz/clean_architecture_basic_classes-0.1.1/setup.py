#!/usr/bin/env python

"""The setup script."""
from requirements import *
from setuptools import setup, find_packages

with open('README.rst', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name='clean_architecture_basic_classes',
    version='0.1.1',
    author="Anselmo Lira (https://github.com/aberriel)",
    author_email='anselmo.lira1@gmail.com',
    description="Classes to implement a Clean Architecture Python Framework",
    url='https://github.com/aberriel/clean_architecture_basic_classes',
    packages=find_packages(include=['clean_architecture_basic_classes', 'clean_architecture_basic_classes.*']),
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'clean_architecture_basic_classes=clean_architecture_basic_classes.cli:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='clean_architecture_basic_classes',
    test_suite='tests',
    zip_safe=False,
)
