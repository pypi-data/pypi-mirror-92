#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="model1",
    version="1.0.2.7",
    keywords=("model1", "xxx"),
    description="model1 sdk",
    long_description="model1 sdk for python",
    license="MIT Licence",

    url="",
    author="skyeye",
    author_email="skyeye@gmail.com",

    packages=find_packages(exclude=['dist']),
    package_data={'model1/conf': ['validator/*.json']},
    include_package_data=True,
    platforms="any",
    install_requires=['skyext>=1.0.1.4'],
    # data_files=[('model1/conf/validator', ['goods.json'])],
    # data_files=[('model1/conf/validator', ['model1/conf/validator/*.json'])],

    scripts=[],
    # entry_points={
    #     'console_scripts': [
    #         'test = test.help:main'
    #     ]
    # }
)