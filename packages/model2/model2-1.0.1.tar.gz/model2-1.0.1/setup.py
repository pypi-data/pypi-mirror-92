#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="model2",
    version="1.0.1",
    keywords=("model2", "xxx"),
    description="model2 sdk",
    long_description="model2 sdk for python",
    license="MIT Licence",

    url="",
    author="skyeye",
    author_email="skyeye@gmail.com",

    packages=find_packages(exclude=['dist']),
    # packages=find_packages("model2"),
    # package_dir={'':'model2'},
    include_package_data=True,
    platforms="any",
    install_requires=['testdb>=1.0.0.1'],

    scripts=[],
    # entry_points={
    #     'console_scripts': [
    #         'test = test.help:main'
    #     ]
    # }
)