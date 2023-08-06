#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 10:47 AM
# @Author  : wangdongming
# @Site    : 
# @File    : restful_api.py
# @Software: Hifive
import os
import abc
import tornado.web
import tornado.httpserver
import logging as logger
from future.backports.http.client import BAD_REQUEST, NOT_FOUND, INTERNAL_SERVER_ERROR, OK


class ApiBaseHandler(tornado.web.RequestHandler, metaclass=abc.ABCMeta):

    def __init__(self, t, obj, *argment_keys, **default_argments):
        allKeys = list(argment_keys)
        self.defaultKeys = dict(default_argments)
        allKeys.extend(self.defaultKeys.keys())
        self.allKeys = set(allKeys)
        super(ApiBaseHandler, self).__init__(t, obj)
        if not os.path.isdir('temp'):
            os.mkdir('temp')

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')

    def find_default_val(self, keyname):
        return self.defaultKeys.get(keyname)

    def convert_arg_type(self, key, value):
        return value

    def parse_argments(self):
        argments = {}
        for key in self.allKeys:
            arg = self.get_argument(key, None)
            if not arg:
                arg = self.find_default_val(key)
                if arg is None:
                    raise KeyError(f"[invalid request]not find the key in request: {key}.")
            argments[key] = self.convert_arg_type(key, arg)

        return argments

    @abc.abstractmethod
    def do(self, response, argments):
        raise NotImplementedError

    def request_handler(self):
        response = {
            "code": OK,
            "msg": 'ok',
            "data": {}
        }
        self.temporal_files = []
        separators = "===" * 20
        logger.info(separators)
        logger.info('recieve response.')
        try:
            argments = self.parse_argments()
            logger.info('argments:{}.'.format(
                "&".join(("=".join((k, str(v))) for k, v in argments.items()))
            ))
            self.do(response, argments)
        except KeyError as keyErr:
            if str(keyErr).find("[invalid request]"):
                response['code'] = BAD_REQUEST
                response['msg'] = str(keyErr)
                logger.error(response['msg'])
            else:
                raise keyErr
        except FileNotFoundError as fileErr:
            response['code'] = NOT_FOUND
            response['msg'] = str(fileErr)
            logger.error(response['msg'])
        except Exception as error:
            response['code'] = INTERNAL_SERVER_ERROR
            response['msg'] = f'interna server error[{error}]'
            logger.error(response['msg'])
        finally:
            for f in self.temporal_files:
                try:
                    os.remove(f)
                except Exception:
                    continue
            self.temporal_files = []
            logger.info(separators)
        self.write(response)
        self.finish()

    def post(self, *args, **kwargs):
        self.request_handler()

    def get(self, *args, **kwargs):
        self.request_handler()



