# -*- coding:utf-8 -*-
import json
import os
import sys
import traceback

import xmltodict as xmltodict

from util.UPSFormatter import format_one_logistics_info, save_base64_pod_to_disk
from util.account import account
from util.http_client import post_request_by_xml
from util.logger import Logger

# ups 请求获取物流信息的接口
post_request_api = 'https://onlinetools.ups.com/ups.app/xml/Track'

ups, dpd = account()


class UpsPod:
    def __init__(self, data, log, body_file, save_path):
        self.data = data
        self.log = log
        self.body_file = body_file
        self.save_path = save_path

    def pull_pod(self):
        """
        保存物流信息，并更新相关数据表的状态
        :return:
        """
        data, log = self.data, self.log
        count = 0
        for tk in data:
            # http 请求物流信息
            res_dic = self.request_ups_logistics_info(tk)
            # 保存结果
            if res_dic is not None:
                d_res = self.download_pod(res_dic, tk)
                if d_res:
                    count += 1
            else:
                log.error("%s download pod failed!" % tk)
        return count

    def request_ups_logistics_info(self, tk):
        """
        请求 ups 物流信息
        :return:
        """
        log, body_file = self.log, self.body_file
        try:
            with open(body_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content is not None:
                    print(ups)
                    body = content.replace('ACCESS_LICENSE_NUMBER', '8D5644C32FE8C868') \
                        .replace('USER_ID', 'asldutch2018').replace('PASSWORD', 'Asldutch888$') \
                        .replace('TRACKING_NUMBER', tk)
                    res = post_request_by_xml(post_request_api, body)
                    dic = xmltodict.parse(res, encoding='utf-8')
                    return json.dumps(dic)
        except:
            log.error("%s UPS rquest logistics info failed !!!!" % tk)
            log.error(traceback.format_exc())
            pass

    def download_pod(self, dic, tk):
        """
        格式化 物流信息的返回内容，方便后续业务中的数据操作
        :param dic:
        :return: 返回物流信息列表，如果有pod列表中同样还应该包含pod file_id
        """
        log = self.log
        save_path = self.save_path
        json_i = json.loads(dic)
        print(json_i)
        try:
            activity_list = json_i['TrackResponse']['Shipment']['Package']['Activity']
            if type(activity_list) == list:
                for i in range(0, len(activity_list)):
                    activity = activity_list[i]
                    one_ac, has_pod, pod_base64 = format_one_logistics_info(tk, i, activity)
                    if has_pod:
                        return save_base64_pod_to_disk(log, pod_base64, save_path, tk)

            else:
                one_ac, has_pod, pod_base64 = format_one_logistics_info(tk, 0, activity_list)
                return save_base64_pod_to_disk(log, pod_base64, save_path, tk)
        except:
            log.error("Get track activities failed !!")
            log.error("Ups request res: %s " % json_i)
            log.error(traceback.format_exc())
            pass


if __name__ == '__main__':
    LOG_PATH = '/var/log/py/tools_server.log'
    LOG_LEVEL = os.getenv("PYTHON_LOG_LEVEL") or 'debug'
    ups = UpsPod(['1Z44F6F26836010983'], Logger(LOG_PATH, LOG_LEVEL, 'MIDNIGHT', 5).logger,
                 '../ups-body.xml', 'C:\\mnt\\static\\warehouse\\pod')
    ups.pull_pod()
