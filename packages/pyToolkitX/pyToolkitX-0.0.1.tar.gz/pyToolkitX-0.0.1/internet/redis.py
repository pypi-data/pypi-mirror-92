#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 3:20 PM
# @Author  : wangdongming
# @Site    : 
# @File    : redis.py
# @Software: Hifive
import json
import redis
import socket


class RedisClient(object):

    def __init__(self, host='localhost', port=6379,
                 db=0, password=None, socket_timeout=None,
                 socket_connect_timeout=None):
        self._default_client = self.get_db(
            host, port, db, password, socket_timeout, socket_connect_timeout)

    @property
    def client(self):
        return self._default_client

    def get_db(self, host='localhost', port=6379, db=0,
               password=None, socket_timeout=None, socket_connect_timeout=None):
        return redis.Redis(
            host, port, db, password, socket_timeout, socket_connect_timeout)

    def del_key(self, keynames, redis_db=None):
        client = self.client or redis_db
        if isinstance(keynames, str):
            keynames = [keynames]
        return client.delete(*keynames)

    def exists(self, keyname, redis_db=None):
        client = self.client or redis_db
        return client.exists(keyname)

    def serialize(self, data):
        if not isinstance(data, (str, bytes)):
            return json.dumps(data)
        return data

    def deserialize(self, data):
        if not isinstance(data, (str, bytes)):
            return data
        try:
            s = json.loads(data)
        except:
            s = data
        return s

    def insert(self, keyname, value, expire_sec=None, redis_db=None):
        """
        简单插入操作，将对象以字符串的方式存储在REIDS。
        :param keyname:
        :param value:
        :param expire_sec:
        :param redis_db:
        :return:
        """
        client = self.client or redis_db
        data = self.serialize(value)
        return client.set(keyname, data, ex=expire_sec)

    def get(self, keyname, redis_db=None):
        '''
        简单提取操作，获取以字符串的方式存储的对象。
        :param keyname:
        :param redis_db:
        :return:
        '''
        client = self.client or redis_db
        data = client.get(keyname)
        return self.deserialize(data)


class AliveRedisClient(RedisClient):
    """
    连接keep alive
    os: linux
    version: 大于2.4
    """

    def get_db(self, host='localhost', port=6379, db=0,
               password=None, socket_timeout=None, socket_connect_timeout=None):
        socket_potions = {
            # socket.TCP_KEEPIDLE: 60,
            socket.TCP_KEEPINTVL: 30,
            socket.TCP_KEEPCNT: 3
        }
        pool = redis.ConnectionPool(host=host, port=port, password=password,
                                    db=db, socket_connect_timeout=socket_connect_timeout,
                                    socket_timeout=socket_timeout, socket_keepalive=True,
                                    socket_keepalive_options=socket_potions)
        return redis.Redis(connection_pool=pool)