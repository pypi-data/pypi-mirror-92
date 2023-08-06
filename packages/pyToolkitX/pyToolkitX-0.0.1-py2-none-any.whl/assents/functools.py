#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 11:37 AM
# @Author  : wangdongming
# @Site    : 
# @File    : functools.py
# @Software: Hifive
import types
import typing
from assents import classproperty
from assents.decorators import _classproperty_cache_for
from functools import wraps, reduce

__version__ = '0.0.5'


class Compose(object):
    """
    函数聚合器
    """

    def __init__(self, *functions: typing.Tuple[types.FunctionType],
                 is_pipe: bool = False, aggregation: types.FunctionType = None):
        """
        连续调用多个函数, 如果is_pipe=True，依次连接所有函数的输出到输入。
        否则，返回所有函数结果集列表将传aggregation中进行聚合。
        :param functions: 需要连接的函数
        :param is_pipe: 是否建立管道
        :param aggregation: 聚合函数
        """
        self.functions = functions
        self.is_pipe = is_pipe
        if aggregation:
            self.aggregation = aggregation

    @staticmethod
    def aggregation(iterable: typing.Iterable) -> bool:
        """
        对所有运算结果进行逻辑与
        :param iterable: 所有运算结果集合
        :return: 运算结果True/False
        """
        return reduce(lambda x, y: x and y, iterable)

    def __call__(self, *args: typing.Tuple[typing.Any],
                 **kwargs: typing.Dict[typing.AnyStr, typing.AnyStr]):
        result_set = []
        for index, func in enumerate(self.functions):
            if not index or not self.is_pipe:
                result_set.append(func(*args, **kwargs))
            else:
                result_set[0] = func(result_set[0])
        return self.aggregation(
            result_set or [0, 0]) if len(result_set) != 1 else result_set[0]


def duplicate(iterable: typing.Iterable,
              keep: types.FunctionType = lambda x: x,
              key: types.FunctionType = lambda x: x,
              reverse: bool = False) -> list:
    """
    保序去重
    :param iterable: 需要去重的列表
    :param keep: 去重的同时要对element做的操作
    :param key: 使用哪一部分去重
    :param reverse: 是否反向去重
    :return:
    """
    result = list()
    duplicator = list()
    if reverse:
        iterable = reversed(iterable)

    for i in iterable:
        keep_field = keep(i)
        key_words = key(i)
        if key_words not in duplicator:
            result.append(keep_field)
            duplicator.append(key_words)
    return list(reversed(result)) if reverse else result


def global_cache_classproperty(func: types.FunctionType):
    """
    全局类缓存性
    :param func:
    :return:
    """
    return classproperty(_classproperty_cache_for(all=True)(func))


def cache_classproperty(func: types.FunctionType):
    """
    类缓存属性
    :param func:
    :return:
    """
    return classproperty(_classproperty_cache_for(all=False)(func))


def cache_property(func):
    """
    缓存属性
    :param func:
    :return:
    """
    return property(_property_cache(func))


def _property_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        prop_name = "_" + func.__name__
        if prop_name not in args[0].__dict__:
            args[0].__dict__[prop_name] = func(*args, **kwargs)
        return args[0].__dict__[prop_name]

    return wrapper












