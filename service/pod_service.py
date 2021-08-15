# -*- coding:utf-8 -*-
import datetime
import os
import random
import string
import sys
import time

from util.database import execute_change_sql
from util.excelUtil import read_excel_pandas_by_byte
from service.dpd_pod import DpdPod
from service.ups_pod import UpsPod

# 根据环境变量设置日志
env = (sys.argv[1] if len(sys.argv) > 2 else os.getenv("PYTHON_ENV")).upper()

POD_PATH = '/mnt/static/warehouse/pod/YEAR/PATH/'
BODY_PATH = '/home/tools-server/ups-body.xml' if 'DEV' == env else '/data/tools-server/ups-body.xml'
ZIP_CMD = 'zip -jr /mnt/static/warehouse/pod/YEAR/PATH/FILENAME.zip /mnt/static/warehouse/pod/YEAR/PATH/'
ZIP_PATH = '/mnt/static/warehouse/pod/YEAR/PATH/FILENAME.zip'
POD_FILE_URI_HOST = 'http://resource.y-clouds.com/' if env == 'DEV' \
    else 'http://resource.sysafari.com/'

year = datetime.datetime.now().year
today = time.strftime("%y%m%d%H%m%s", time.localtime())


def async_pull_pod(file, log, remark, cid):
    file_first = file[0]
    file_byte = file_first.body

    # # 读取表格数据
    data = read_excel_pandas_by_byte(file_byte)

    ups = []
    dpd = []
    for one in data:
        print('one', one)
        if one[1] == 'UPS':
            ups.append(one[0])
        else:
            dpd.append(one[0])

    p_path = POD_PATH.replace('YEAR', str(year)).replace('PATH', str(cid) + '_' + str(today))
    print(p_path)

    # 各自拉取pod
    dpd_pull = DpdPod(dpd, log, p_path)
    dpd_res = dpd_pull.pull_pod()

    ups_pull = UpsPod(ups, log, BODY_PATH, p_path)
    ups_res = ups_pull.pull_pod()

    # 拉取完毕 执行压缩命令
    filename = 'POD_' + time.strftime("%y%m%d", time.localtime()) + ''.join(random.sample(string.ascii_letters, 6))
    print('filename', filename)
    print('year', year)
    cmd = ZIP_CMD.replace('YEAR', str(year)) \
        .replace('PATH', str(cid) + '_' + str(today)) \
        .replace('FILENAME', filename)
    print('cmd', cmd)
    cmd_res = os.system(cmd)
    zip_path = ZIP_PATH.replace('/mnt/static/', POD_FILE_URI_HOST) \
        .replace('YEAR', str(year)) \
        .replace('PATH', str(cid) + '_' + str(today)) \
        .replace('FILENAME', filename)
    if cmd_res:
        # 保存zip 到db
        in_sql = "insert into tools_pod_log(pod_Id, remark, url) values ('%s', '%s', '%s')" % (
            filename, remark, zip_path)
        print('sql', in_sql)
        u_rows = execute_change_sql(in_sql)
        if u_rows != 1:
            log.error("%s generate zip failed." % remark)
    else:
        log.error("%s generate zip failed." % remark)
    return dpd_res + ups_res
