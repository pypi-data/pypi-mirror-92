#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/22 5:16 PM
# @Author  : wangdongming
# @Site    : 
# @File    : setup.py
# @Software: Hifive
# coding: utf-8
from setuptools import setup, find_packages

requires = []
with open("requirements.txt") as f:
    for line in f:
        requires.append(line.strip())

version = '0.0.1'

setup(
    name='pyToolkitX',
    version=version,
    description="python tools repository.",
    long_description="""
pyToolkitX
=======================

Python Toolkit for XingzeAI & HifiveAI.

""",
    keywords='pyToolkitX',
    author='wangdongming',
    author_email='wangdongming@hifive.ai',
    url='https://gitlab.ilongyuan.cn/pyhifive/toolkit',
    license='MIT',
    packages=find_packages(),
    install_requires=requires,

)