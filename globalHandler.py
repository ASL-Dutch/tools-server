# -*- coding:utf-8 -*-

import os
import threading

from concurrent.futures import ThreadPoolExecutor

from py_eureka_client import eureka_client
from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
import tornado.options
import tornado.gen
from service.pod_service import async_pull_pod
from util.logger import Logger
import sys

# 根据环境变量设置日志
env = os.getenv("PYTHON_ENV").upper()

LOG_PATH = '/var/log/py/tools_server.log'
LOG_LEVEL = os.getenv("PYTHON_LOG_LEVEL") or 'debug'
log = Logger(LOG_PATH, LOG_LEVEL, 'MIDNIGHT', 5).logger
EUREKA_HOST = os.getenv('EUREKA_HOST', '')

# 定义变量
tornado.options.options.define("port", default=14001, type=int, help="server port")
# 起线程池，由当前RequestHandler持有
executor = ThreadPoolExecutor(20)


class IndexHandler(RequestHandler):
    def get(self):
        self.write('First')


class UploadHandler(RequestHandler):
    def post(self):
        files = self.request.files
        remark = self.get_argument('remark')
        up_headers = self.request.headers
        cid = up_headers.get('cid')

        file_list = files['file']
        # 异步进行pod拉取
        pod_thread = threading.Thread(target=async_pull_pod, args=(file_list, log, remark))
        pod_thread.start()
        self.write("request success.")


if __name__ == '__main__':
    app = Application([(r'/', IndexHandler),
                       (r'/upload', UploadHandler)])
    tornado.options.parse_command_line()
    print('EUREKA_HOST', EUREKA_HOST)

    eureka_client.init(eureka_server=EUREKA_HOST,
                       app_name='py-tools-server',
                       instance_port=14001)

    http_server = HTTPServer(app)
    http_server.bind(tornado.options.options.port)
    http_server.start(1)
    print('tools-server start ..')
    # 启动IOLoop轮循监听
    IOLoop.instance().start()
