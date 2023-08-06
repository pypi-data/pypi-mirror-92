#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 3:01 PM
# @Author  : wangdongming
# @Site    : 
# @File    : http.py
# @Software: Hifive

import os
import json
import random
import requests
from urllib.parse import urlparse


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
]
DEFAULT_HEADERS = {
        'Accept-Language': 'en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Connection': 'Keep-Alive',
}


def simple_save(response, filepath):
    success = False
    if response.status_code == requests.codes.ok:
        with open(filepath, 'wb') as f:
            f.write(response.content)
            success = True
    return success


def http_request(url, method='GET', headers=None, cookies=None, data=None, timeout=10):
    _headers = DEFAULT_HEADERS
    if headers and isinstance(headers, dict):
        _headers.update(headers)
    method = method.upper()
    if data and method != "GET" and 'json' in _headers.get('Content-Type', ''):
        data = json.dumps(data)
    _headers['User-Agent'] = random.choice(USER_AGENTS)
    if method == 'GET':
        res = requests.get(url, data, headers=_headers, cookies=cookies, timeout=timeout)
    elif method == 'PUT':
        res = requests.put(url, data, headers=_headers, cookies=cookies, timeout=timeout)
    elif method == 'DELETE':
        res = requests.delete(url, headers=_headers, cookies=cookies, timeout=timeout)
    elif method == 'OPTIONS':
        data = data if isinstance(data, dict) else {}
        res = requests.options(url, **data)
    else:
        res = requests.post(url, data, headers=_headers, cookies=cookies, timeout=timeout)
    return res


def download_file(url, local_path, data=None, headers=None, cookies=None,
                  method='GET', retry=3, safe=False, replace=True, timeout=10):
    retry = retry if retry > 1 and retry < 10 else 3
    if not replace and os.path.isfile(local_path):
        return True
    exception = None
    for times in range(retry):
        try:
            response = http_request(url, method, data=data, headers=headers,
                                    cookies=cookies, timeout=timeout)
            if response.ok and simple_save(response, local_path):
                return True
        except Exception as ex:
            exception = ex
    if not safe and exception:
        raise exception
    return False


def download2folder(url, folder, filename=None, hashname=True, safe=False):
    if not filename:
        path = urlparse(url).path
        if not hashname:
            filename = os.path.basename(path)
        else:
            _, ex = os.path.splitext(path)
            filename = hash(url) + ex

    dst_path = os.path.join(folder, filename)
    if download_file(url, dst_path, safe=safe):
        return dst_path
