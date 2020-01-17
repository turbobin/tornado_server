#!/usr/bin/env python
# coding:utf8
"""
校验签名
"""
import binascii
import hashlib
import hmac
import urllib.parse


def mk_source(method, url_path, params):
    source = '%s&%s&%s' % (method.upper(), urllib.parse.quote(url_path, ''),
                           params)
    return source


def hmac_sha1_sig(method, url_path, params, secret):
    """
    生成签名
    """
    sign_list = []
    if 'sign' in params.keys():
        params.pop("sign")
    if 'xyy' in params.keys():
        params.pop("xyy")

    param_list = set()
    param_list.add(
        urllib.parse.quote("&".join(
            k + "=" + urllib.parse.quote(str(params[k]))
            for k in sorted(params.keys()) if str(params[k]) != ''), ''))
    param_list.add(
        urllib.parse.quote("&".join(k + "=" + str(params[k])
                                    for k in sorted(params.keys())
                                    if str(params[k]) != ''), ''))
    param_list.add(
        urllib.parse.quote("&".join(
            k + "=" + urllib.parse.quote(str(params[k]))
            for k in sorted(params.keys())), ''))
    param_list.add(
        urllib.parse.quote("&".join(
            k + "=" + str(params[k]) for k in sorted(params.keys())), ''))
    key_list = [
        'content', 'feeling', 'nick', 'alipay_name', 'content_extra',
        'extra_configs'
    ]
    flag = False
    for key in key_list:
        if key in params.keys():
            flag = True
            params.pop(key)
    if flag:
        param_list.add(urllib.parse.quote("&".join(
            k + "=" + urllib.parse.quote(str(params[k])) for k in sorted(params.keys()) if str(params[k]) != ''), ''))
        param_list.add(urllib.parse.quote(
            "&".join(k + "=" + str(params[k]) for k in sorted(params.keys()) if str(params[k]) != ''), ''))
        param_list.add(
            urllib.parse.quote("&".join(k + "=" + urllib.parse.quote(str(params[k])) for k in sorted(params.keys())),
                               ''))
        param_list.add(urllib.parse.quote("&".join(k + "=" + str(params[k]) for k in sorted(params.keys())), ''))
    for params in param_list:
        source = mk_source(method, url_path, params)
        hashed = hmac.new(
            bytes(secret, 'utf-8'), bytes(source, 'utf-8'), hashlib.sha1)
        sign = binascii.b2a_base64(hashed.digest())[:-1]
        if sign not in sign_list:
            sign_list.append(sign.decode())
    return sign_list
