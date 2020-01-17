#!/bin/env python
# -*- coding: utf-8 -*-
"""
布隆过滤器装载数据
"""
import sys

sys.path.append('..')
import time
import pybloomfilter
from utils import db_tools


class myBF:
    robot_bloom_filter = {}
    robot_last_ts = {}

    @staticmethod
    def reloadRobotUser(mode):
        sql = '''select user_id from user_robot_info where user_id%100={0}
        '''.format(mode)
        query_results = db_tools.db_midware('waterworld').query(sql)
        sbf = pybloomfilter.BloomFilter(
            capacity=len(query_results), error_rate=0.001)
        [sbf.add(int(item['user_id'])) for item in query_results]
        myBF.robot_last_ts[mode] = time.time()
        myBF.robot_bloom_filter[mode] = sbf

    @staticmethod
    def getRobotBF(mode):
        # return {}
        try:
            # 防止重启服务导致的雪崩,分散reload, 每秒只reload 1%的数据
            if (mode not in myBF.robot_bloom_filter
                    and mode != int(time.time()) % 100):
                return {}

            if (mode not in myBF.robot_bloom_filter
                    or mode not in myBF.robot_last_ts or
                    time.time() - myBF.robot_last_ts[mode] > 3600 + mode * 10):
                myBF.reloadRobotUser(mode)
            return myBF.robot_bloom_filter[mode]
        except:
            pass

    test_user_bloom_filter = {}
    test_user_last_ts = 0

    @staticmethod
    def reloadTestUser():
        sql = '''select user_id from test_user where status=0
        UNION DISTINCT select user_id from user_evil where kind='test'
        and update_ts>now()- interval 2 day '''
        query_results = db_tools.db_midware('waterworld').query(sql)
        sbf = pybloomfilter.BloomFilter(len(query_results), 0.001)
        [sbf.add(int(item['user_id'])) for item in query_results]
        myBF.test_user_last_ts = time.time()
        myBF.test_user_bloom_filter = sbf

    @staticmethod
    def getTestUserBF():
        try:
            if (not myBF.test_user_bloom_filter
                    or time.time() - myBF.test_user_last_ts > 600):
                myBF.reloadTestUser()
            return myBF.test_user_bloom_filter
        except:
            pass


if __name__ == '__main__':
    a = time.time()
    myBF.reloadRobotUser(1)
