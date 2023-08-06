#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 3:26 PM
# @Author  : wangdongming
# @Site    : 
# @File    : mongodb.py
# @Software: Hifive
import pymongo


class MongoClient(object):

    def __init__(self, addr=None, db=None, port=None, user=None, passwd=None):
        config = self.get_mongo_config(addr, db, port, user, passwd)
        client = pymongo.MongoClient(config['host'])
        self.client = client
        self.active_db = self.use_database(config.get('name'))

    def use_database(self, database_name):
        if not database_name:
            return None
        self.active_db = self.client[database_name]
        return self.active_db

    def get_mongo_config(self, addr=None, db=None, port=None, user=None, passwd=None):
        if user and passwd:
            host = "mongodb://{}:{}@{}:{}/{}".format(user, passwd, addr, port, db)
        else:
            host = "mongodb://{}:{}".format(addr, port)
        return {
            'host': host,
            'maxPoolSize': 1000,
            'tz_aware': True,
            'socketTimeoutMS': None,
            'connectTimeoutMS': 1000,
            'w': 1,
            'wtimeout': 10000,
            'j': False,
            'name': db
        }

    def collections(self, database_name):
        db = self.client.use_database(database_name)
        return [(name, db[name]) for name in db.collection_names()]

    def close(self):
        self.client.close()