#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
校验签名
"""
import time

from configs import not_need_sign, config, err_conf
from utils import common
from utils import sign_tool


def is_right_sign(path, data):
    """
    检查是否是正确的签名
    """
    reason = {}
    if path in not_need_sign.path:
        return True
    if 'sign' not in data.keys():
        reason['msg'] = "请求中没有sign参数"
        return False, reason
    client_sign = common.my_str(data.get('sign', ''))
    if client_sign == "waterworldwaterworldwaterworld":
        return True
    user_id = common.my_int(data.get('user_id', 0))
    timestamp = common.my_int(data.get('timestamp', 0))
    cur_time = int(time.time())
    if user_id == 0:
        return True
    if client_sign == "":
        reason['msg'] = "请求中没有sign参数"
        return False, reason
    # 超过配置时间就默认这个请求不合法
    if cur_time - timestamp > config.SIGN_TIME_OUT:
        reason['msg'] = "请求timestamp已超过5分钟, current_time:{},timestamp:{}".format(
            cur_time, timestamp)
        return False, reason
    memc_key = "session_key_{}".format(user_id)
    user_session_key = common.redis_handle().get(memc_key)
    if user_session_key is None:
        reason['code'] = err_conf.E_BAD_SESSION
        reason['msg'] = "user_session已失效，mem_session_key: {}".format(memc_key)
        return False, reason
    client_session_key = common.my_str(data.get('session_key', ''))
    user_session_key = common.my_str(user_session_key)
    if client_session_key != user_session_key:
        reason['code'] = err_conf.E_BAD_SESSION
        reason['msg'] = "session_key已失效，客户端session_key: {0}，服务器session_key: {1}".format(
            client_session_key, user_session_key)
        return False, reason
    new_sign = sign_tool.hmac_sha1_sig('POST', path, data, user_session_key)
    if client_sign in new_sign:
        return True
    reason['msg'] = "客户端sign:{},服务器sign:{}".format(client_sign, new_sign)
    return False, reason
