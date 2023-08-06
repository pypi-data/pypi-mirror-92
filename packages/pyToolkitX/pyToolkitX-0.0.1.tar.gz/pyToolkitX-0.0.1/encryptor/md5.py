#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 3:07 PM
# @Author  : wangdongming
# @Site    : 
# @File    : md5.py
# @Software: Hifive
import hashlib


def md5(s):
    m = hashlib.md5()
    m.update(str(s).encode("utf8"))
    return m.hexdigest()


def md5_16(s) -> str:
    md5_str = md5(s)
    return ''.join([md5_str[i * 4: i * 4 + 2] for i in range(len(md5_str) // 4)])

