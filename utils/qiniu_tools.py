# -*- coding: utf-8 -*-
"""
七牛通用方法
"""
import math
import random
import string
import time
from qiniu import Auth, put_file
from configs import config


def get_up_token(bucket_name, key):
    q = Auth(config.QINIU_ACCESS_KEY, config.QINIU_SECRET_KEY)
    token = q.upload_token(bucket_name, key, 3600)
    return token


def get_key_by_uid(uid):
    ms = int(time.time() * 1000)
    key = str(uid) + '-' + str(ms)
    return key


def get_bucket(qiniu_source):
    if qiniu_source == 'config':
        bucket = 'global-pubpic'
    else:
        bucket = None
    return bucket


def get_bucket_host(bucket_name):
    if bucket_name == 'global-pubpic':
        host = 'https://global-pubpic.51yund.com/'
    else:
        host = None
    return host


def upload_file(bucket_name, upload_key, filepath):
    """上传文件"""
    auth = Auth(config.QINIU_ACCESS_KEY, config.QINIU_SECRET_KEY)
    token = auth.upload_token(bucket_name, upload_key)
    ret, info = put_file(token, upload_key, filepath)
    hash_value = ret.get('hash', '')
    key_value = ret.get('key', '')
    return hash_value, key_value


def get_random_filename():
    """
    获取随机文件名
    """
    filename = ""
    day_id = int(time.strftime("%Y%m%d", time.localtime(time.time())))
    origin = string.ascii_letters + string.digits
    for index in range(8):
        filename += random.choice(origin)
    filename = str(day_id) + filename + str(
        math.ceil(float(time.time() * 1000)))
    return filename
