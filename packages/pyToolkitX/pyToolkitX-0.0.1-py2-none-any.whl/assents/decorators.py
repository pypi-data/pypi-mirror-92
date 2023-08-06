#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 2:30 PM
# @Author  : wangdongming
# @Site    : 
# @File    : decorators.py
# @Software: Hifive
import typing
import time
import types
import signal
import math
from functools import wraps
from assents import free_namedtuple
from assents.utils import find_ancestor, debugger


def cache_for(timeout: typing.Union[float, int] = 10):
    """
    缓存属性，指定缓存失效时间
    :param timeout: 缓存失效时间 second
    """

    def outer(func):
        @property
        @wraps(func)
        def inner(*args, **kwargs):
            prop_name = "_" + func.__name__
            prop_start_name = "%s_cache_start_time" % prop_name
            if time.time() - args[0].__dict__.get(prop_start_name, 0) > timeout:
                args[0].__dict__[prop_name] = func(*args, **kwargs)
                args[0].__dict__["%s_cache_start_time" % prop_name] = time.time()
            return args[0].__dict__[prop_name]

        return inner

    return outer


def cache_method(timeout: int = 10):
    """
    缓存一个方法的调用结果，持续一定时长，
    根据不同的调用参数来缓存不同的结果，调用参数必须是可hash的，
    该方法调用失败时，希望抛出异常，此时缓存会失败。
    :param timeout: 缓存时长 :s
    """

    def cache(func):
        entry_class = free_namedtuple(func)
        data = dict()

        @wraps(func)
        def inner(*args, **kwargs):
            for k in data.copy().keys():
                if time.time() - timeout > data[k].ts:
                    del data[k]

            entry = entry_class(*args[1:], **kwargs)
            entry.ts = time.time()
            stored = data.get(entry, entry)
            if entry not in data or time.time() - timeout > stored.ts:
                entry.result = func(*args, **kwargs)
                data[entry] = entry
                return entry.result
            else:
                return stored.result

        return inner

    return cache


def cache_method_for_update(func: types.FunctionType):
    """
    缓存方法调用结果直到实例的updated返回True，与cache_method类似。
    @param func: 要缓存的方法
    """
    entry_class = free_namedtuple(func)
    data = dict()

    @wraps(func)
    def inner(*args, **kwargs):
        self = args[0]
        # 没有更新方法(直接使用子类，而不通过cache)，不进行缓存操作
        if not self.updated:
            return func(*args, **kwargs)
        # 如果已更新，则清除所有缓存
        if self.updated():
            data.clear()
        entry = entry_class(*args[1:], **kwargs)
        stored = data.get(entry, entry)

        if entry not in data:
            entry.result = func(*args, **kwargs)
            if entry.result:
                data[entry] = entry
            return entry.result
        else:
            return stored.result

    return inner


def _classproperty_cache_for(all=False):
    """
    缓存类属性，只计算一次，如果all=True，子类和父类共用
    :param all:
    :return:
    """

    def outer(func: types.FunctionType):

        @wraps(func)
        def inner(*args, **kwargs):
            if all:
                base = find_ancestor(args[0], func.__name__)
            else:
                base = args[0]

            prop_name = "_" + func.__name__
            if prop_name not in base.__dict__:
                setattr(base, prop_name, func(*args, **kwargs))
            return base.__dict__[prop_name]

        return inner

    return outer


def thread_safe(lock):
    """
    对指定函数进行线程安全包装，需要提供锁
    :param lock: 锁
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorate


def thread_safe_for_method(func):
    """
    对类中的方法进行线程安全包装
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        with args[0].lock:
            return func(*args, **kwargs)

    return wrapper


def call_later(callback: str,
               call_args: typing.Tuple = tuple(),
               immediately: bool = True,
               interval: typing.Union[float, int] = 1):
    """
    应用场景：
    被装饰的方法需要大量调用，随后需要调用保存方法，
    但是因为被装饰的方法访问量很高，而保存方法开销很大
    所以设计在装饰方法持续调用一定间隔后，再调用保存方法。
    规定间隔内，无论调用多少次被装饰方法，保存方法只会
    调用一次，除非immediately=True
    :param callback: 随后需要调用的方法名
    :param call_args: 随后需要调用的方法所需要的参数
    :param immediately: 是否立即调用
    :param interval: 调用间隔
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            try:
                return func(*args, **kwargs)
            finally:
                if immediately:
                    getattr(self, callback)(*call_args)
                else:
                    now = time.time()
                    if now - self.__dict__.get("last_call_time", 0) > interval:
                        getattr(self, callback)(*call_args)
                        self.__dict__["last_call_time"] = now

        return wrapper

    return decorate


def retry_wrapper(
        retry_times: int,
        exception: type = Exception,
        error_handler: types.FunctionType = None,
        interval: float = 0.1):
    """
    函数出错时用来重试的装饰器
    :param retry_times: 重试次数
    :param exception: 需要重试的异常
    :param error_handler: 出错时的回调函数
    :param interval: 重试间隔时间
    """

    def out_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    count += 1
                    if error_handler:
                        result = error_handler(
                            func.__name__, count, e, *args, **kwargs)
                        if result:
                            count -= 1
                    if count >= retry_times:
                        raise
                    time.sleep(interval)

        return wrapper

    return out_wrapper


def timeout(timeout_time: int, default):
    """
    装饰一个方法，用来限制其执行时间，超时后返回default，只能在主线程使用。
    :param timeout_time: 超时时间
    :param default: 超时后的返回
    """

    class DecoratorTimeout(Exception):
        pass

    def timeout_function(f):
        def f2(*args):
            def timeout_handler(signum, frame):
                raise DecoratorTimeout()

            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout_time)
            try:
                retval = f(*args)
            except DecoratorTimeout:
                return default
            finally:
                signal.signal(signal.SIGALRM, old_handler)
            signal.alarm(0)
            return retval

        return f2

    return timeout_function


def print_exec_time():

    def wrapper(func):
        @wraps(func)
        def handler(*args, **kwargs):
            st = time.time()
            r = func(*args, **kwargs)
            if debugger(False):
                func_name = func.__name__
                exec_time = math.ceil(time.time() - st)
                print(f"[DEBUG]function <{func_name}> :expend {exec_time} sec")
            return r
        return handler
    return wrapper


def insert_arguments(**arguments):
    """装饰器，为类方法增加参数
    （主要用于类的__init__方法）
    """
    def actual_decorator(func):
        def new_func(self, *args, **kwargs):
            for k, v in arguments.items():
                if k in kwargs:
                    v = kwargs.pop(k)
                setattr(self, k, v)
            return func(self, *args, **kwargs)

        return new_func

    return actual_decorator


def delete_arguments(*arguments):
    """装饰器，为类方法删除参数
    （主要用于类的__init__方法）
    """
    def actual_decorator(func):
        def new_func(self, *args, **kwargs):
            for k in arguments:
                if k in kwargs:
                    raise TypeError(
                        '%s got an unexpected keyword argument \'%s\'' %
                        (self.__class__.__name__, k)
                    )
            return func(self, *args, **kwargs)

        return new_func

    return actual_decorator

