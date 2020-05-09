#!/bin/env python
# -*- coding: utf-8 -*-
from configs import db_config
import records


class DBMySql(object):
    db_mysql = {}

    @staticmethod
    def reloadMySql(dbname):
        mysql_dict = db_config.config.get(dbname)
        if mysql_dict:
            database_url = "mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}".format(
                **mysql_dict)
            # 设置连接池的失效时间，解决"MySQL server has gone away"
            DBMySql.db_mysql[dbname] = records.Database(database_url, pool_recycle=60*50)

    @staticmethod
    def GetMySql(dbname):
        if not DBMySql.db_mysql.get(dbname):
            DBMySql.reloadMySql(dbname)
        return DBMySql.db_mysql.get(dbname)
