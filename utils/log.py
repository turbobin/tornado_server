# -*- coding: utf-8  -*-
"""
发送日志到graylog

该文件中的接口尽可能都带上try:except, 以免影响到正常的逻辑;

        **上报内容可以丢,但不能抛出异常**
"""
import json
import sys
import traceback

from gelfclient import UdpClient
from urllib.parse import unquote, urlencode

# from utils.myBoomFilter import myBF
from utils import common

log_gelf_udp = UdpClient('127.0.0.1', port=52201)


def send_to_graylog_tornado(gelf_data, req=None, path=None, req_data=None):
    """
    发送日志到graylog
    """
    if 'source' in gelf_data or '_source' in gelf_data:
        return

    if 'short_message' not in gelf_data:
        return

    message = gelf_data['short_message'].replace(' ', '')
    import utils.myCache
    log_rule = utils.myCache.Cacheing.GetLogRule()
    if message not in log_rule:
        print("send log fail >>>> short_message not in log_rule table")
        return
    try:
        hash_id = int(log_rule[message]['hash_id'])
    except:
        hash_id = 0
    if req_data is None and req is None:
        data = "None"
    elif req_data is None and req is not None:
        data = req.arguments
    else:
        data = req_data
    if isinstance(data, dict):
        if '_user_id' not in gelf_data:
            user_id = common.my_int(
                data.get('user_id', [0])[0].decode('utf-8'))
            if user_id == '':
                user_id = 0
            if user_id > 10000:
                gelf_data['_user_id'] = user_id

        key_list = [
            'ver', 'phone_type', 'channel', 'os', 'package_name', 'source'
        ]
        for key in key_list:
            if key not in data:
                continue
            if '_{0}'.format(key) not in gelf_data:
                value = data.get(key, [''])[0].decode('utf-8')
                if key == 'source':
                    key = 'platform'
                if value:
                    gelf_data['_{0}'.format(key)] = value

        if '_uri' not in gelf_data:
            if not path:
                path = req.uri
            if path:
                gelf_data['_uri'] = path

    if hash_id > 0 and '_user_id' in gelf_data:
        user_id = int(gelf_data['_user_id'])
        if user_id % 100 >= hash_id:
            pass
            ## 非测试用户灰度上报,
            # is_test_user = True if user_id in myBF.getTestUserBF() else False
            # if not is_test_user:
            #    return

    if '_user_id' in gelf_data and '_tail_number' not in gelf_data:
        gelf_data['_tail_number'] = int(gelf_data['_user_id']) % 100
    if '_phone_type' in gelf_data:
        phone_type = gelf_data['_phone_type']
        if isinstance(phone_type, str) and phone_type:
            phone_type_arr = phone_type.split("_")
            if len(phone_type_arr) >= 3:
                gelf_data['_model'] = phone_type_arr[0]
                gelf_data['_phone'] = phone_type_arr[1]
                gelf_data['_os'] = str(phone_type_arr[2])
            elif 'iPhone' in phone_type:
                gelf_data['_model'] = 'iPhone'
                gelf_data['_phone'] = phone_type
        del gelf_data['_phone_type']

    if 'level' not in gelf_data:
        gelf_data['level'] = 7
    try:
        log_gelf_udp.log(gelf_data)
    except:
        send_try_except()


def send_event_log(biz_event_value,
                   user_id=0,
                   ver=None,
                   phone_type=None,
                   tornado_flag=0,
                   req=None):
    """
    事件相关日志发送
    """
    try:
        item = biz_event_value.split(':')
        if len(item) < 2:
            return
        biz, event = item[0], item[1]
        biz_event = '{0}:{1}'.format(biz, event)
        import utils.myCache
        log_event_dict = utils.myCache.Cacheing.GetLogEvent()
        if biz_event not in log_event_dict:
            return
        log_event = log_event_dict[biz_event]
        gelf_data = {
            'short_message': 'waterworld_event_log',
        }
        ### 判断是否是空字符串
        if user_id == '':
            user_id = 0
        if user_id > 10000:
            gelf_data['_user_id'] = user_id

        if not phone_type:
            gelf_data['_phone_type'] = phone_type
        if not ver:
            gelf_data['_ver'] = ver
        gelf_data['_biz'] = biz
        gelf_data['_biz_name'] = log_event['biz_name']
        gelf_data['_event'] = event
        gelf_data['_event_name'] = log_event['event_name']
        if log_event['note']:
            gelf_data['_event_note'] = log_event['note']
        if len(item) > 2:
            for i in range(2, min(len(item), 10)):
                try:
                    value = int(item[i])
                except:
                    value = 1
                gelf_data['_event_value{0}'.format(i - 1)] = value
        if tornado_flag == 1:
            send_to_graylog_tornado(gelf_data, req)
    except:
        send_try_except()


def ApiGraylog(user_id, msg_type, path, desc="_", extra_desc="_", req=None):
    """
    发送日志
    """
    try:
        gelf_data = {}
        gelf_data['short_message'] = msg_type
        gelf_data['_path'] = path
        gelf_data['_user_id'] = user_id
        gelf_data['_detail'] = desc[0:4096]
        gelf_data['_extra_detail'] = extra_desc[0:4096]
        send_to_graylog_tornado(gelf_data, req)
    except:
        send_try_except()


def send_try_except(req=None):
    """
    发送异常
    """
    try:
        gelf_data = {}
        filename = sys._getframe().f_back.f_code.co_filename
        trace_stack = "".join(traceback.format_stack()[-10:-1])
        gelf_data['short_message'] = 'waterworld_try_except'
        gelf_data['_filename'] = filename
        gelf_data['_detail'] = traceback.format_exc()
        gelf_data['_extra_detail'] = trace_stack
        send_to_graylog_tornado(gelf_data, req)
    except:
        pass


def ApiGrayUserlog_tornado(user_id, response, req, is_normal_response):
    """
    发送返回日志
    """
    try:
        is_test_user = 0
        path = req.uri
        # 大请求,抽样2%上报
        from configs import not_need_log
        if (user_id % 100 not in [0, 1] and path in not_need_log.reqs
                and not is_test_user):
            return
        req_data = req.arguments
        cur_req_data = req_data.copy()
        req_ts = req.request_time()
        ip = req.headers.get('X-Forwarded-For', req.remote_ip)
        if ip.find(",") > 0:
            ip = ip.split(",")[0]
        device_id = req_data.get('device_id,', '')

        key_list = [
            'sign',
            'device_id',
            'screen_density',
            'screen_width',
            'screen_densityDpi',
            'mac',
            'client_user_id',
            'screen_height',
            'language',
            'locale',
            'timezone',
            'sdk',
            'device_id_type',
            'phone_type',
            'ver',
            'channel',
            'yd_network_status',
            'package_name',
            'source',
            'os',
        ]
        if not is_normal_response:  # 为了定位问题,非正常请求字段不剔除
            key_list = []
        # 为了安全考虑,xyy,sign不外传, 同时节省存储,删除部分字段上报
        # 内部测试用户，除了xyy，其他字段不隐藏.
        for key in key_list:
            if key in req_data.keys():
                if not is_test_user:
                    req_data.pop(key)
        request = unquote(urlencode(req_data, 'utf-8'))
        gelf_data = {}
        gelf_data['short_message'] = 'waterworld_api_log'
        gelf_data['_user_id'] = user_id
        gelf_data['_device_id'] = device_id
        gelf_data['_ip'] = ip
        gelf_data['_uri'] = path
        need_more_key_list = [
            'day_id',
            'oper_type',
            'index',
            'circle_id',
            'step',
            'kind_id',
            'steps',
            'topic_id',
            'group_run_id',
            'order_id',
        ]
        for key in need_more_key_list:
            if key in req_data.keys():
                gelf_data['_{0}'.format(key)] = req_data.get(key, 0)

        if is_test_user:
            req_len = 16384
        else:
            req_len = 2048
        gelf_data['_request'] = request[0:req_len]
        if isinstance(response, dict):
            response = json.dumps(response, indent=4, ensure_ascii=False)

        gelf_data['_response'] = response[0:req_len]
        gelf_data['_response_time'] = round(req_ts * 1000.0, 2)
        send_to_graylog_tornado(gelf_data, req=req, req_data=cur_req_data)
    except:
        send_try_except()


if __name__ == '__main__':
    pass
