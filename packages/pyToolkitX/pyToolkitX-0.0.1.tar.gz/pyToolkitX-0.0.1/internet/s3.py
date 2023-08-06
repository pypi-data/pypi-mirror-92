#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 3:27 PM
# @Author  : wangdongming
# @Site    : 
# @File    : s3.py
# @Software: Hifive

import os
import boto3
import platform
from configparser import ConfigParser
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig


class LyS3(object):

    def __init__(self, **aws_config):
        self.client = boto3.client("s3", **aws_config)
        if not aws_config:
            self._region = self.get_region()

    @staticmethod
    def get_region():
        home_dir = os.environ.get("HOME") if \
            platform.system().lower() == 'linux' else \
            os.environ.get("USERPROFILE")
        if home_dir:
            region_file = os.path.join(home_dir, ".aws", "config")
            if os.path.exists(region_file):
                cfg = ConfigParser()
                try:
                    cfg.read(region_file)
                    region = cfg.get(cfg.sections()[0], "region")
                except Exception as e:
                    raise
                else:
                    return region
            else:
                raise FileNotFoundError(f"cannot found aws config:{home_dir}")
        else:
            raise NotADirectoryError(f"cannot found aws config directory:{home_dir}.")

    def list_buckets(self):
        """列出所有bucket"""
        bucket_list = self.client.list_buckets()
        return [bucket_info["Name"] for bucket_info in bucket_list["Buckets"]]

    def list_objects(self, bucket, prefix, size=100):
        """返回指定bucket下的所有对象"""
        return self.client.list_objects(Bucket=bucket, Prefix=prefix, MaxKeys=size)

    def create_bucket(self, bucket_name):
        """创建bucket

        :param bucket_name: 要创建的bucket名字
        :return: 布尔值。成功返回True, 否则返回False
        """
        try:
            s3_client = boto3.client('s3', region_name=self._region)
            location = {'LocationConstraint': self._region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
        except ClientError as e:
            raise e
        return True

    def delete_bucket(self, bucket_name):
        """
        删除存储桶.必须先删除存储桶中的所有对象(包括所有对象版本和删除标记),然后才能删除存储桶本身
        :param bucket_name: 桶名
        :return:
        """
        pass

    def get_object(self, bucket, key):
        """
        查看一个object的信息
        :param bucket: bucket的名字
        :param key: object的名字
        :return: object信息
        """
        object_info = self.client.get_object(Bucket=bucket, Key=key)
        return object_info

    def exists(self, bucket, keyname):
        try:
            obj = self.get_object(bucket, keyname)
            return True
        except ClientError as cerr:
            http_resp = cerr.response.get("ResponseMetadata")
            if http_resp is not None:
                code = http_resp.get('HTTPStatusCode', -1)
                if code == 404:
                    return False
            else:
                raise

    def delete_object(self, bucket, key):
        """
        删除bucket中的一个对象
        :param bucket: bucket的名字
        :param key: object的名字
        """
        self.client.delete_object(Bucket=bucket, Key=key)

    def upload_file(self, file_name, bucket, key):
        """
        上传文件
        :param file_name: 文件路径
        :param key: key 名
        :param bucket: 要上传的bucket
        """
        # TransferConfig类可以设置网络传输的配置
        # 当文件大小超过0.5GB时，启用多线程
        gb = 1024 ** 3
        config = TransferConfig(multipart_threshold=0.5 * gb)

        self.client.upload_file(file_name, bucket, key, Config=config)
        return True

    def download_file(self, bucket, key, path, replace=False):
        """
        下载文件
        :param replace:
        :param path: 文件名
        :param key: key名
        :param bucket: bucket名
        """
        # TransferConfig类可以设置网络传输的配置
        # 当文件大小超过0.5GB时，启用多线程
        gb = 1024 ** 3
        config = TransferConfig(multipart_threshold=0.5 * gb)

        if not os.path.isfile(path) or os.path.getsize(path) < 10 or replace:
            self.client.download_file(Bucket=bucket, Key=key, Filename=path, Config=config)

        return os.path.isfile(path)