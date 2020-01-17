#!/bin/env python
# -*- coding:utf-8 -*-

import sys

sys.path.append('..')
from utils import common


class Cacheing:
    log_rule_cache = None
    log_rule_req_num = 0

    log_event_cache = None
    log_event_req_num = 0

    @staticmethod
    def reloadLogRule():
        '''
        加载日志规则
        '''
        sql = '''select short_message, hash_id from log_report_rule
        where status=0 and hash_id>=0'''
        result = common.db1_handle().query(sql)
        rule_dict = {}
        for item in result:
            message = item['short_message']
            rule_dict[message] = dict(item)
        Cacheing.log_rule_cache = rule_dict

    @staticmethod
    def GetLogRule():
        if (Cacheing.log_rule_cache is None
                or Cacheing.log_rule_req_num > 1000):
            Cacheing.reloadLogRule()
            Cacheing.log_rule_req_num = 0
        Cacheing.log_rule_req_num = Cacheing.log_rule_req_num + 1
        return Cacheing.log_rule_cache

    @staticmethod
    def reloadLogEvent():
        sql = '''select  li.biz,biz_name,event,event_name,lie.note
        from log_id li, log_id_event lie where
        li.biz =lie.biz and li.status=0 and lie.status=0'''
        result = common.db2_handle().query(sql)
        event_dict = {}
        for item in result:
            biz_event = '{0}:{1}'.format(item['biz'], item['event'])
            event_dict[biz_event] = dict(item)

        Cacheing.log_event_cache = event_dict

    @staticmethod
    def GetLogEvent():
        if (Cacheing.log_event_cache is None
                or Cacheing.log_event_req_num > 100000):
            Cacheing.reloadLogEvent()
            Cacheing.log_event_req_num = 0
        Cacheing.log_event_req_num = Cacheing.log_event_req_num + 1
        return Cacheing.log_event_cache


if __name__ == '__main__':
    print(Cacheing.GetLogRule())
    # print(Cacheing.GetLogEvent())
