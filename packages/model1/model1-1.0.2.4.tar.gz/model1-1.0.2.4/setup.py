#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="model1",
    version="1.0.2.4",
    keywords=("model1", "xxx"),
    description="model1 sdk",
    long_description="model1 sdk for python",
    license="MIT Licence",

    url="",
    author="skyeye",
    author_email="skyeye@gmail.com",

    packages=find_packages(exclude=['dist']),
    # packages=find_packages("model2"),
    # package_dir={'':'model2'},
    include_package_data=True,
    platforms="any",
    install_requires=['testext>=1.0.0.1'],
    data_files=[('model1/conf/validator', ['goods.json'])],

    scripts=[],
    # entry_points={
    #     'console_scripts': [
    #         'test = test.help:main'
    #     ]
    # }
)