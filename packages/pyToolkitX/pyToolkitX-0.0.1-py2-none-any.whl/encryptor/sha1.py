#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 10:54 AM
# @Author  : wangdongming
# @Site    : 
# @File    : sha1.py
# @Software: Hifive
from hashlib import sha1


def unique_hash_file(filepath, fast=True):
    """ Small function to generate a hash to uniquely generate
    a file. Inspired by MD5 version here:
    http://stackoverflow.com/a/1131255/712997

    Works with large files.
    """
    s = sha1()
    blocksize = 2 ** 20 if fast else -1
    with open(filepath, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            s.update(buf)
    return s.hexdigest().upper()