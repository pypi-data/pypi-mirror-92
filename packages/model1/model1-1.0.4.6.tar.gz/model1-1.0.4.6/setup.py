#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="model1",
    version="1.0.4.6",
    keywords=("model1", "xxx"),
    description="model1 sdk",
    long_description="model1 sdk for python",
    license="MIT Licence",

    url="",
    author="skyeye",
    author_email="skyeye@gmail.com",

    packages=find_packages(exclude=['dist']),
    include_package_data=True,
    platforms="any",
    install_requires=['skyext>=1.0.2.5'],
    data_files=[('conf/api/model1', ['model1/conf/api/goods.json', 'model1/conf/api/order.json']),
                ('conf/api', ['model1/validators.json'])],

    scripts=[],
    # entry_points={
    #     'console_scripts': [
    #         'test = test.help:main'
    #     ]
    # }
)