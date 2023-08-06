#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 10:38 AM
# @Author  : wangdongming
# @Site    : 
# @File    : obs.py
# @Software: Hifive
import os
from assents.utils import mkdir
from urllib.parse import urlparse
from obs import ObsClient
from obs import StorageClass
from obs import HeadPermission
from obs import CreateBucketHeader
from obs import RestoreTier

# install obs sdk command:
# pip install esdk-obs-python --trusted-host pypi.org


class LyObs(object):

    def __init__(self, ak, sk, host):
        self.ak = ak
        self.sk = sk
        self.host = host
        self.client = ObsClient(
            access_key_id=ak,
            secret_access_key=sk,
            server=host
        )

    def create_bucket_header(self, headPermission, storageClass):
        if not isinstance(headPermission, HeadPermission) \
                or not isinstance(storageClass, StorageClass):
            raise TypeError('headPermission or storageClass type error.')
        header = CreateBucketHeader()
        header.aclControl = headPermission
        header.storageClass = storageClass
        return header

    def create_bucket(self, bucket_name, header=None, location=None):
        resp = self.client.createBucket(bucket_name, header=header, location=location)
        return resp.status < 300

    def list_bucket(self, isQueryLocation=True):
        resp = self.client.listBuckets(isQueryLocation)
        if resp.status < 300:
            return resp.body.buckets
        else:
            raise Exception('errorCode:%s,errorMessage:%s' % (resp.errorCode, resp.errorMessage))

    def del_bucket(self, bucket_name):
        resp = self.client.deleteBucket(bucket_name)
        return resp.status < 300

    def upload(self, bucket_name, src_path, keyname):
        resp = self.client.putFile(bucket_name, keyname, file_path=src_path)
        return resp.status < 300

    def download(self, bucket_name, keyname, dst_path):
        dirname = os.path.dirname(dst_path)
        if dirname and not os.path.isdir(dirname):
            os.mkdir(dirname)
        resp = self.client.getObject(bucket_name, keyname, downloadPath=dst_path)
        return resp.status < 300

    def ls(self, bucket_name, prefix):
        '''
        迭代枚举最大1000个
        :param bucket_name:
        :param prefix:
        :return:
        '''
        resp = self.client.listObjects(bucket_name, prefix=prefix)
        if resp.status < 300:
            return resp.body.contents
        else:
            raise Exception('errorCode:%s,errorMessage:%s' % (resp.errorCode, resp.errorMessage))

    def listall(self, bucket_name, prefix):
        max_keys = 100
        marker = None
        while True:
            resp = self.client.listObjects(bucket_name, prefix=prefix, max_keys=max_keys, marker=marker)
            if resp.status < 300:
                for content in resp.body.contents:
                    yield content
                if not resp.body.is_truncated:
                    break
                marker = resp.body.next_marker
            else:
                raise Exception(f'Obs response error, errorCode:{resp.errorCode}.\n msg:{resp.errorMessage}')

    def delete(self, bucket_name, keyname):
        resp = self.client.deleteObject(bucket_name, keyname)
        return resp.status < 300

    def get_key(self, bucket_name, keyname):
        resp = self.client.getObjectMetadata(bucket_name, keyname)
        if resp.status < 300:
            item = {}
            item['requestId'] = resp.requestId
            item['contentType'] = resp.body.contentType
            item['contentLength'] = resp.body.contentLength
            item['property'] = dict(resp.header).get('property')
            return item
        else:
            raise Exception('errorCode:%s,errorMessage:%s' % (resp.errorCode, resp.errorMessage))

    def signature_url(self, method, bucket_name=None, keyname=None, specialParam=None,
                      expires=300, headers=None, queryParams=None):
        resp = self.client.createSignedUrl(
            method, bucket_name, keyname, specialParam, expires, headers, queryParams)
        if resp.status < 300:
            return resp['signedUrl']

    def signature_obj_url(self, bucket_name=None, keyname=None, expires=300):
        return self.signature_url('GET', bucket_name, keyname, expires=expires)

    def restore(self, bucket_name, keyname, days=1):
        resp = self.client.restoreObject(bucket_name, keyname, days=days, tier=RestoreTier.EXPEDITED)
        return resp.status < 300


class Obs(object):
    default_config = {
        "bucket_name": 'BucketName',
        "connection": ['ak', 'sk'],  # ak,sk
        "extra": {
            "host":  'obs.cn-north-1.myhuaweicloud.com',
            "is_secure": False,
            "domain_mode": False,

        }
    }

    def __init__(self, bucket, ak, sk, host=None):
        HK_HOST = 'obs.ap-southeast-1.myhuaweicloud.com'
        if not ak or not sk:
            ak, sk = self.default_config['connection']
        host = host or self.default_config['extra']['host']
        if str(bucket).startswith('hk'):
            host = HK_HOST
        self.obs = LyObs(ak, sk, host)
        self.bukect = bucket or self.default_config["bucket_name"]
        buckets = [b.name for b in self.obs.list_bucket()]
        if self.bukect not in buckets:
            self.obs.create_bucket(self.bukect)

    @property
    def conn(self):
        return self.obs.client

    def walk(self, prefix=None):
        for obj in self.obs.listall(self.bukect, prefix):
            yield obj.key, obj

    def exists(self, key_name, bukect=None):
        bukect = bukect or self.bukect
        try:
            meta = self.obs.get_key(bukect, key_name)
            if meta.get('contentLength'):
                return True
        except:
            return False

    def upload(self, key_name, src_path, replace=True, bukect=None):
        bukect = bukect or self.bukect
        if not replace:
            if self.exists(key_name, bukect):
                return True

        return self.obs.upload(bukect, src_path, key_name)

    def download(self, key_name, dst_path):
        '''
        support multi key download,usage:key_name="key1,key2,key3...".
        :param key_name: single file or multi files.
        :param dst_path:
        :return:
        '''
        keys = key_name.split(',')
        if not os.path.isdir(os.path.dirname(dst_path)):
            mkdir(os.path.dirname(dst_path))
        self.restore_obj(key_name)
        return self.obs.download(self.bukect, key_name, dst_path)

    def download2temp(self, key_name, filename=None):
        basename = filename or os.path.basename(key_name)
        # dst_path = os.path.join(TEMP_FOLDER, basename)
        dst_path = os.path.join('temp', basename)
        if os.path.isfile(dst_path) or self.download(key_name, dst_path):
            return dst_path

    def access_obj_url(self, bucket_name, key_name, expires=300, public_read=False):
        if not public_read:
            return self.obs.signature_obj_url(bucket_name, key_name, expires)
        else:
            url = self.access_obj_url(bucket_name, key_name)
            components = urlparse(url)
            return "%s://%s%s" % (
                components.scheme, components.netloc, components.path)

    def restore_obj(self, keyname, bucket_name=None, days=1):
        bucket_name = bucket_name or self.bukect
        return self.obs.restore(bucket_name, keyname, days)

