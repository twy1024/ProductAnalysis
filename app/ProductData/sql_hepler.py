# !/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
from . import config
from . import log_helper
import pymysql

class SqlHelper(object):
    def __init__(self):
        self.conn = pymysql.connect(**config.productanalysis_db_config)
        self.cursor = self.conn.cursor()
        self.conn.select_db(config.productanalysis_db)

    def insert_json(self,data={},table_name = None):
        """
        以json数据插入
        :param data:
        :param table_name:
        :return:
        """
        try:
            keys = []
            vals = []
            for k,v in data.items():
                keys.append(k)
                vals.append(v)

            val_str = ','.join(['%s']*len(vals))
            key_str = ','.join(keys)

            sql = 'insert ignore into {table} ({keys}) values({values})'.\
                format(keys=key_str,values=val_str,table=table_name)

            self.cursor.execute(sql,tuple(vals))
            self.conn.commit()

            return self.cursor.lastrowid

        except Exception as e:
            log_helper.log(e,logging.WARNING)
            return -1

    def query_one(self,command,cursor_type = 'tuple'):
        try:
            cursor = None
            if cursor_type == 'dict':
                cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            else:
                cursor = self.cursor

            cursor.execute(command)
            data = cursor.fetchone()
            self.conn.commit()

            return data
        except Exception as e:
            log_helper.log(e,logging.WARNING)
            return None

    def close(self):
        """
        关闭操作
        :return:
        """
        self.cursor.close()
        self.conn.close()