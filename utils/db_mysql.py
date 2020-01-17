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
            DBMySql.db_mysql[dbname] = records.Database(database_url)

    @staticmethod
    def GetMySql(dbname):
        if not DBMySql.db_mysql.get(dbname):
            DBMySql.reloadMySql(dbname)
        return DBMySql.db_mysql.get(dbname)
