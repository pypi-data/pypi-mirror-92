#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 3:41 PM
# @Author  : wangdongming
# @Site    : 
# @File    : timer.py
# @Software: Hifive
import abc
from threading import Event, Thread, Lock


class Timer(Thread):
    """
    定时器，每隔一段时间触发调用do_work.
    """

    def __init__(self, interval, args=None, kwargs=None):
        Thread.__init__(self)
        self.interval = interval
        self.args = args or []
        self.kwargs = kwargs or {}
        self.finished = Event()
        self.lock = Lock()

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def run(self):
        while not self.finished.isSet():
            self.finished.wait(self.interval)
            if not self.finished.is_set():
                self.do_work(*self.args, **self.kwargs)
        # self.finished.set()

    @abc.abstractmethod
    def do_work(self, *args, **kwargs):
        pass