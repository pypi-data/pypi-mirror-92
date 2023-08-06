#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="testext",
    version="1.0.1.1",
    keywords=("test", "ext"),
    description="ext sdk",
    long_description="ext sdk for python",
    license="MIT Licence",

    url="",
    author="skyeye",
    author_email="skyeye@gmail.com",

    packages=find_packages(exclude=['dist']),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'psycopg2==2.8.6',
        'sqlalchemy==1.3.22',
        'elasticsearch-dsl==7.3.0',
        'elasticsearch==7.9.1',
        'redis==3.5.3'
    ],

    scripts=[],
    # entry_points={
    #     'console_scripts': [
    #         'test = test.help:main'
    #     ]
    # }
)
