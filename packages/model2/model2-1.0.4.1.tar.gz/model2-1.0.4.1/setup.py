#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="model2",
    version="1.0.4.1",
    keywords=("model2", "xxx"),
    description="model2 sdk",
    long_description="model2 sdk for python",
    license="MIT Licence",

    url="",
    author="skyeye",
    author_email="skyeye@gmail.com",

    packages=find_packages(exclude=['dist']),
    include_package_data=True,
    platforms="any",
    install_requires=['skyext>=1.0.1.4'],
    data_files=[('conf/api/model2', ['model2/conf/api/role.json','model2/conf/api/user.json'])],

    scripts=[],
    # entry_points={
    #     'console_scripts': [
    #         'test = test.help:main'
    #     ]
    # }
)