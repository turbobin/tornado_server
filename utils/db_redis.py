#!/bin/env python
# -*- coding: utf-8 -*-
import redis
from configs import config


class DBRedis(object):
    db_redis = None

    @staticmethod
    def reloadRedis():
        pool = redis.ConnectionPool(
            host=config.REDIS_HOST,
            port=6379,
            db=0,
            password=config.REDIS_PASSWD,
            socket_timeout=2)
        DBRedis.db_redis = redis.StrictRedis(connection_pool=pool, decode_responses=True)

    @staticmethod
    def GetRedis():
        if not DBRedis.db_redis:
            DBRedis.reloadRedis()
        return DBRedis.db_redis
