#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="testdb",
    version="1.0.0.2",
    keywords=("test", "xxx"),
    description="db sdk",
    long_description="db sdk for python",
    license="MIT Licence",

    url="",
    author="skyeye",
    author_email="skyeye@gmail.com",

    packages=find_packages(exclude=['dist']),
    include_package_data=True,
    platforms="any",
    install_requires=['psycopg2>=2.8.6','sqlalchemy==1.3.22'],

    scripts=[],
    # entry_points={
    #     'console_scripts': [
    #         'test = test.help:main'
    #     ]
    # }
)
