#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   GoogleTranslate.py

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/5/25           Joker      1.0         数据库连接操作库

pip3 install googletrans
'''

import os
import sys
import mysql.connector

# 获取对应的环境变量
env = (sys.argv[1] if len(sys.argv) > 2 else os.getenv("SPRING_ENV")).upper()

if env not in ['PRO', 'DEV']:
    print("%s is  not legal ." % env)
    exit(1)

print(os.getenv("DEV_DB_HOST"))
# 数据库参数
db_properties = {
    'host': os.getenv("%s_DB_HOST" % env),
    'username': os.getenv("%s_DB_USERNAME" % env),
    'password': os.getenv("%s_DB_PASSWORD" % env),
    'port': os.getenv("%s_DB_PORT" % env),
    'database': os.getenv("%s_DB_DATABASE" % env),
}


def execute_query(sql):
    """
    执行查询的语句
    """
    conn = mysql.connector.connect(
        host=db_properties['host'],
        user=db_properties['username'],
        passwd=db_properties['password'],
        port=db_properties['port'],
        database=db_properties['database'],
    )
    # 获取指针
    cursor = conn.cursor()
    cursor.execute(sql)
    rel = cursor.fetchall()
    # 释放资源
    cursor.close()
    conn.close()
    return rel


def execute_change_sql(sql):
    """
    执行 修改数据的sql
    :param sql:
    :return:
    """
    conn = mysql.connector.connect(
        host=db_properties['host'],
        user=db_properties['username'],
        passwd=db_properties['password'],
        port=db_properties['port'],
        database=db_properties['database'],
    )
    # 获取指针
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    row_count = cursor.rowcount

    cursor.close()
    conn.close()
    return row_count


def execute_delete_sql(sql):
    """
    执行 删除数据的sql
    :param sql:
    :return: 返回删除的行数
    """
    conn = mysql.connector.connect(
        host=db_properties['host'],
        user=db_properties['username'],
        passwd=db_properties['password'],
        port=db_properties['port'],
        database=db_properties['database'],
    )
    # 获取指针
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    del_rows = cursor.rowcount

    cursor.close()
    conn.close()
    return del_rows
