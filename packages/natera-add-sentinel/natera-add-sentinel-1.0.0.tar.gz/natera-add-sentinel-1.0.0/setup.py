#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open
from os import path
import sentinel

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='natera-add-sentinel',
    version=sentinel.__version__,
    description='Natera sentinel',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sergey Tyurin',
    author_email='styurin@natera.com',
    packages=find_packages(exclude=["*.tests", "tests.*", "tests"]),
    entry_points={
        'console_scripts': [
            'sentinel=sentinel.entrypoint:main',
        ],
    },
    install_requires=[
        'dxpy==0.288.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 2'
    ],
    python_requires='>=2.7'
)
