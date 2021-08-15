# -*- coding:utf-8 -*-
import os

env = os.getenv("SPRING_ENV").upper()
# 数据库配置
data_options = {
    'host': os.getenv("%s_DB_HOST" % env),
    'username': os.getenv("%s_DB_USERNAME" % env),
    'password': os.getenv("%s_DB_PASSWORD" % env),
    'port': os.getenv("%s_DB_PORT" % env),
    'database': os.getenv("%s_DB_DATABASE" % env),
}
