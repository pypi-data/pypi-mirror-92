#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 11:36 AM
# @Author  : wangdongming
# @Site    : 
# @File    : __init__.py.py
# @Software: Hifive
import time
import inspect
import traceback


def free_namedtuple(func):
    """
    根据一个类及其参数创建一个类namedtuple class，
    但不同之处在于创建实例成功后可以自由赋值，初时化时指定的值决定其Hash和eq结果
    :param func:
    :return:
    """
    cls_tmpl = """
class {}(object):
    def __init__(self, {}):
        {}
    def __hash__(self):
        return {}
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return {}
"""

    args = inspect.getargspec(func).args
    if args and args[0] in ["self", "cls"]:
        args.pop(0)

    class_name = func.__name__.capitalize()
    init_arg = ", ".join(args + "=None" for args in args) if args else ""
    init_body = "".join(
        "self.{%s} = {%s}\n        " % (
            index, index) for index in range(len(args))).format(*args) if args else "pass"
    hash_body = " + ".join("hash(self.{})".format(arg) for arg in args) if args else "0"
    eq_body = " and ".join("self.{0} == other.{0}".format(arg) for arg in args) if args else "True"
    namespace = dict(__name__='entries_%s' % class_name)
    class_str = cls_tmpl.format(class_name, init_arg, init_body, hash_body, eq_body)
    exec(class_str, namespace)
    return namespace[class_name]


class classproperty(object):
    """
    property只能用于实例方法到实例属性的转换，使用classproperty来支持类方法到类属性的转换
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func(owner)


class NotImplementedProp(object):
    """
    用来对子类需要实现的类属性进行占位
    """

    def __get__(self, instance, owner):
        return NotImplemented


class Blocker(object):
    """
    有的时候我们需要将线程停止一段时间，通常我们选择调用time.sleep(..)，
    当我们需要sleep很长一段时间，比如一分钟以上时，如果这时我们选择关闭程序，
    而我们通过singal注册了关闭信号的监听器，用来改变当时程序的状态，
    如果置self.alive = False,由于time.sleep阻塞导致我们的程序当前线程无法获知alive状态，
    难以被关闭，通过使用Blocker，我们可以避免上述情况发生。
    eg:
    if Blocker(sleep_time).wait_timeout_or_notify(notify=lambda: time.time() > 1000000):
        `返回true, 我们知道是被唤醒了，而不是时间到了`
        ....
    """
    def __init__(self, block_time):
        """
        :param block_time: 需要阻塞的时长
        这个对象会被传递给notify回调函数
        """
        self.block_time = block_time
        self.interval = 0.5

    def wait_timeout_or_notify(self, notify=lambda: False):
        start_time = time.time()
        is_notified = False
        while time.time() - start_time < self.block_time:
            is_notified = notify()
            if is_notified:
                break
            time.sleep(self.interval)
        return is_notified


