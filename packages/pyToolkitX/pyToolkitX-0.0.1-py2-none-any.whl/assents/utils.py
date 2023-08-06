#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 2:37 PM
# @Author  : wangdongming
# @Site    : 
# @File    : utils.py
# @Software: Hifive
import os
import re
import pdb
import sys
import json
import types
import ctypes
import socket
import typing
import fnmatch
import platform
import warnings
import subprocess
from functools import reduce


def popen(command):
    if isinstance(command, str):
        command = command.split()
    p = subprocess.Popen(command, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p_out, p_err = p.communicate()
    return p.returncode, p_out, p_err


def mkdir(path):
    build_dirs = []

    def find_builds(_path):
        if not os.path.isdir(_path):
            build_dirs.append(_path)
            parent = os.path.dirname(_path)
            if parent:
                find_builds(parent)

    find_builds(path)
    while len(build_dirs) > 0:
        os.mkdir(build_dirs.pop())


def is_linuxos():
    return platform.system().lower() == 'linux'


def find_files(path, extensions):
    # Allow both with ".mp3" and without "mp3" to be used for extensions
    extensions = [e.replace(".", "") for e in extensions]

    for dirpath, dirnames, files in os.walk(path):
        for extension in extensions:
            for f in fnmatch.filter(files, "*.%s" % extension):
                if f.startswith('._'):
                    continue
                p = os.path.join(dirpath, f)
                yield (p, extension)


def _assert(boolean, data):
    """
    增强版assert，如果data是异常对象则直接抛出。
    :param boolean: True/False
    :param data: 异常或者描述信息
    """
    if not boolean:
        if isinstance(data, Exception):
            raise data
        raise AssertionError(data)


def overflow(val: int, btc: int) -> int:
    """
    对于超出字节长度的数字转换成负数
    :param val: 值
    :param btc: 字节长度
    """
    max_val = 2 ** (8 * btc - 1) - 1
    if not -max_val - 1 <= val <= max_val:
        val = (val + (max_val + 1)) % (2 * (max_val + 1)) - max_val - 1
    return val


def int_overflow(val: int) -> int:
    """
    类似js对于超过int范围的数转换成负数
    :param val: 值
    :return: 结果
    """
    return overflow(val, 4)


def unsigned_right_shift(n: int, i: int) -> int:
    """
    无符号右移python实现
    :param n: 值
    :param i: 移的位数
    :return: 结果
    """
    # 数字小于0，则转为32位无符号uint
    if n < 0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i < 0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)


def shift_left_for_js(num: int, count: int) -> int:
    """
    位运算左移js版
    :param num: 值
    :param count: 移的位数
    :return: 结果
    """
    return int_overflow(num << count)


def shift_right_for_js(num: int, count: int) -> int:
    """
    位运算右移js版
    :param num: 值
    :param count: 移的位数
    :return: 结果
    """
    return int_overflow(num >> count)


async def readexactly(stream, n: int) -> bytes:
    """
    asyncio stream read
    :param stream: 流
    :param n: 读取字节的长度
    :return:
    """
    if hasattr(stream, "_exception") and stream._exception is not None:
        raise stream._exception

    blocks = []
    while n > 0:
        block = await stream.read(n)
        if not block:
            break
        blocks.append(block)
        n -= len(block)

    return b''.join(blocks)


def find_ancestor(cls, root_define=None):
    """
    查找祖先，直到祖先为object或者祖先最早定义root_define这个属性时，返回当前类。
    :param cls:
    :param root_define:
    :return:
    """
    _mro = list(cls.__mro__)
    root = None

    while True:
        cls = _mro.pop(0)
        base = _mro[0]
        # 这里使用in cls.__dict__判断而不使用hasattr是因为hasattr
        # 会调用一个描述符属性的__get__，如果属性为cache_classproperty，
        # 会引发递归死循环。
        if not root_define or root_define and root_define in cls.__dict__:
            root = cls
        if base == object:
            break

    return root


def clear_cache(ins_or_cls, method_name):
    """
    删除缓存
    :param ins_or_cls:
    :param method_name:
    :return:
    """
    cache_key = "_" + method_name
    if hasattr(ins_or_cls, cache_key):
        delattr(ins_or_cls, cache_key)


def load_module(module_str: str):
    """
    返回字符串表示的模块
    :param module_str: 模块描述字符串，如: os.path
    :return: 模块，如: os.path
    """
    warnings.warn("load_function() is a deprecated alias since 1.7.19, "
                  "use load() instead.",
                  DeprecationWarning, 2)
    return __import__(module_str, fromlist=[module_str.split(".")[-1]])


def load(prop_str: str):
    """
    返回字符串表示的模块、函数、类、若类的属性等
    :param prop_str: 函数、类、类属性、模块描述字符串，如: module1.class.function....
    :return: 函数、类、模块等。
    """
    attr_list = []
    # 每次循环将prop_str当模块路径查找，成功则返回，
    # 失败则将模块路径回退一级，将回退的部分转换成属性
    # 至到加载模块成功后依次从模块中提取属性。
    ex = None
    while prop_str:
        try:
            obj = __import__(prop_str, fromlist=[prop_str.split(".")[-1]])
            for attr in attr_list:
                obj = getattr(obj, attr)
            return obj
        except (AttributeError, ImportError) as e:
            prop_str, _sep, attr_str = prop_str.rpartition('.')
            attr_list.insert(0, attr_str)
            raise ImportError(f"cannot load model:{prop_str}.")
    else:
        if ex is not None:
            raise ex
        else:
            raise ImportError("Empty path!")


def free_port() -> int:
    """
    找到一个可用端口
    :return 端口号
    """
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind(('0.0.0.0', 0))
    free_socket.listen(5)
    port = free_socket.getsockname()[1]
    free_socket.close()
    return port


def get_ip() -> str:
    """
    获取局域网ip
    :return: 局域网ip
    """
    try:
        import psutil
    except ImportError:
        warnings.warn(
            "get_ip function depends on psutil, try: pip install psutil. ")
        raise
    netcard_info = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and not item[1] == '127.0.0.1':
                netcard_info.append((k, item[1]))

    if netcard_info:
        return netcard_info[0][1]


def strip(value, chars: typing.AnyStr = None):
    """
    安全strip，如果不是字符串类型，直接返回。
    :param value: 要strip的值
    :param chars: 需要去掉的字符
    :return: 结果
    """
    if isinstance(value, (bytes, str)):
        return value.strip(chars)
    return value


def decode(value, encoding: str = "utf-8"):
    """
    decode字段
    :param value: 要decode的值
    :param encoding: 编码
    :return: 结果
    """
    return value.decode(encoding)


def encode(value, encoding: str = "utf-8"):
    """
    encode字段
    :param value: 要encode的值
    :param encoding: 编码
    :return: 结果
    """
    return value.encode(encoding)


def rid(value: typing.AnyStr,
        old: typing.Union[typing.AnyStr, typing.Pattern[typing.AnyStr]],
        new: typing.AnyStr) -> typing.AnyStr:
    """
    去掉匹配成功的字段
    :param value: 要被处理的字符串
    :param old: 被替换的内容，可以为正则表达示或字符串
    :param new: 替换的字符串
    :return: 结果
    """
    if hasattr(old, "sub"):
        return old.sub(new, value)
    else:
        return value.replace(old, new)


def wrap_key(json_str: str,
             key_pattern: typing.Pattern[str] = re.compile(r"([a-zA-Z_]\w*)[\s]*:")
             ) -> str:
    """
    将javascript 对象字串串形式的key转换成被双字符包裹的格式如{a: 1} => {"a": 1}
    :param json_str: 要处理的json字符串
    :param key_pattern: 用来处理的正则表达式
    :return: 结果
    """
    return key_pattern.sub('"\g<1>":', json_str)


def safely_json_loads(json_str: typing.AnyStr,
                      defaulttype: typing.Any = dict,
                      escape: bool = True):
    """
    返回安全的json类型
    :param json_str: 要被loads的字符串
    :param defaulttype: 若load失败希望得到的对象类型
    :param escape: 是否将单引号变成双引号
    :return: 结果
    """
    if not json_str:
        return defaulttype()
    elif escape:
        data = replace_quote(json_str)
        return json.loads(data)
    else:
        return json.loads(json_str)


def chain_all(iter: typing.Iterable) -> typing.Union[typing.Collection]:
    """
    连接多个序列或字典
    :param iter: 字典或列表的列表
    :return: 结果
    """
    iter = list(iter)

    if not iter:
        return []

    if isinstance(iter[0], dict):
        result = {}
        for i in iter:
            result.update(i)
    else:
        result = reduce(lambda x, y: list(x) + list(y), iter)
    return result


def replace_quote(json_str: str) -> str:
    """
    将要被json.loads的字符串的单引号转换成双引号，
    如果该单引号是元素主体，而不是用来修饰字符串的。则不对其进行操作。
    :param json_str: json字符串
    :return: 结果
    """
    if not isinstance(json_str, str):
        return json_str

    double_quote = []
    new_lst = []

    for index, val in enumerate(json_str):
        if val == '"' and not len(_get_last_backslash(json_str[:index])) % 2:
            if double_quote:
                double_quote.pop(0)
            else:
                double_quote.append(val)

        if val == "'" and not len(_get_last_backslash(json_str[:index])) % 2:
            if not double_quote:
                val = '"'
        new_lst.append(val)
    return "".join(new_lst)


def _get_last_backslash(strings, regex=re.compile(r"\\*$")):
    mth = regex.search(strings)
    if mth:
        return mth.group()
    return ""


def format_html_string(html: str) -> str:
    """
    格式化html, 去掉多余的字符，类，script等。这个函数性能可能会较差。
    :param html: 传入的html字符串
    :return: 处理完的html
    """
    trims = [(r'\n', ''),
             (r'\t', ''),
             (r'\r', ''),
             (r'  ', ''),
             (r'\u2018', "'"),
             (r'\u2019', "'"),
             (r'\ufeff', ''),
             (r'\u2022', ":"),
             (r"<([a-z][a-z0-9]*)\ [^>]*>", '<\g<1>>'),
             (r'<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', ''),
             (r"</?a.*?>", '')]
    return reduce(lambda string, replacement:
                  re.sub(replacement[0], replacement[1], string), trims, html)


def urldecode(query: str) -> dict:
    """
    与urlencode相反，不过没有unquote
    :param query: url查询字符串
    :return: 查询字符串的字典
    """
    if not query.strip():
        return dict()

    return dict(x.split("=", 1) for x in query.strip().split("&"))


def re_search(regex: typing.Union[typing.Pattern[str], str],
              text: typing.AnyStr,
              dotall: bool = True,
              default: str = "") -> str:
    """
    抽取正则规则的第一组元素
    :param regex: 正则对象或字符串
    :param text: 被查找的字符串
    :param dotall: 正则.是否匹配所有字符
    :param default: 找不到时的默认值
    :return: 抽取正则规则的第一组
    """
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    if not isinstance(regex, list):
        regex = [regex]
    for rex in regex:
        rex = (re.compile(rex, re.DOTALL)
               if dotall else re.compile(rex)) if isinstance(rex, str) else rex
        match_obj = rex.search(text)
        if match_obj is not None:
            t = match_obj.group(1).replace('\n', '')
            return t
    return default


def custom_re(regex: typing.Pattern[typing.AnyStr], text: typing.AnyStr) -> list:
    """
    模仿selector.re
    :param regex: 正则表达式对象
    :param text: 被查询的字符串
    :return:
    """
    return re.findall(regex, text)


def replace_dot(data: dict) -> dict:
    """
    mongodb不支持key中带有"."，该函数用来将"."转换成"_"
    :param data: 要处理的字典
    :return: 返回的字典
    """
    return dict((k.replace(".", "_"), v) for k, v in data.items())


def groupby(it: typing.Iterable, key: types.FunctionType) -> dict:
    """
    自实现groupby，itertool的groupby不能合并不连续但是相同的组, 且返回值是iter
    :param it: 一个列表套字典的结构
    :param key: 从字典从取值的函数，作为group_by后的key
    :return: 字典对象
    """
    groups = dict()
    for item in it:
        groups.setdefault(key(item), []).append(item)
    return groups


def parse_cookie(string: str,
                 regex: typing.Pattern[str] = re.compile(r'([^=]+)=([^\;]+);?\s?')
                 ) -> dict:
    """
    解析cookie
    :param string: cookie字符串
    :param regex: 解析cookie的正则表达式
    :return: cookie字典
    """
    return dict((k, v) for k, v in regex.findall(string))


def test_prepare(search_paths: typing.List[str] = None):
    """
    单元测试时，动态添加PYTHONPATH。
    :param search_paths: 要将哪个路径加入PYTHONPATH
    """
    if not search_paths:
        search_paths = [".."]

    for search_path in search_paths:
        sys.path.insert(0, os.path.abspath(search_path))
    del sys.modules["toolkit"]


def debugger(set_break=True):
    '''
        pdb的简单封装，在debug=False和set_break=False的情况下，不会打断点
    :param set_break: 该值设置True且处于debug环境时，立即设置PDB断点;设置为FALSE时判断当前是否处于debug环境。
    :return: set_break=False时返回debug状态否则返回none.
    '''
    try:
        debug = bool(eval(os.environ.get("DEBUG", "0").lower().capitalize()))
    except Exception:
        debug = False
    if set_break:
        if debug:
            d = pdb.Pdb()
            d.set_trace(sys._getframe().f_back)
    else:
        return debug


def arg_to_iter(arg: typing.Any) -> typing.List[typing.Any]:
    """
    将非可迭代对象转换成可迭代对象
    :param arg: 任意对象
    :return: 列表对象
    """
    if arg is None:
        return []
    elif not isinstance(arg, (dict, str, bytes)) and hasattr(arg, '__iter__'):
        return arg
    else:
        return [arg]

