# ups 物流信息的格式化工具类
import os
import sys
from datetime import datetime
from pathlib import Path
import traceback

import none

from util.image import base64_to_html
from util.letter import id_generator, transfer_content

env = (sys.argv[1] if len(sys.argv) > 2 else os.getenv("PYTHON_ENV")).upper()
# pod 保存路径
TMP_HTML_PATH = '/mnt/static/warehouse/pod'


# cut pod image command
HTML_TO_IMAGE_COMMAND = 'wkhtmltopdf --page-size A6 --enable-local-file-access HTML_PATH  PDF_PATH'


def format_one_logistics_info(tk, index, activity):
    """
    序列化一个 activity 节点,获取物流信息， 是否已签收，签收文件内容
    :param tk
    :param index 当前物流信息的数组下标
    :param activity: 当前物流信息的对象内容
    :return: (), has_pod, pod_base64
    """
    status = activity['Status']
    status_type = status['StatusType']['Code']
    status_description = transfer_content(status['StatusType']['Description'])
    address = activity['ActivityLocation']['Address']
    city = address['City'] if (address is not None and 'City' in address) else ''
    postal_code = address['PostalCode'] if (address is not None and 'PostalCode' in address) else ''
    country_code = address['CountryCode'] if (address is not None and 'CountryCode' in address) else ''
    status_code = status['StatusCode']['Code']

    signed_name = activity['ActivityLocation']['SignedForByName'] if 'D' == status_type else ''

    process = 1
    if status_type == 'M':
        process = 0

    pod_base64 = None
    has_pod = False
    if status_type == 'D':
        process = 2
        pod_base64 = activity['ActivityLocation']['PODLetter']['HTMLImage']
        has_pod = True

    return (tk, index, transfer_content(city), postal_code, country_code, signed_name, status_type, process,
            status_description,
            status_code, activity['Date'], activity['Time']), has_pod, pod_base64


def save_base64_pod_to_disk(log, base64, pod_path, tk):
    """
    将 base64 编码的pod 文件保存在磁盘中，并记录文件名及uri
    :param log: 日志log
    :param base64: pod_base64
    :param bill_id: tk 的bill_id
    :param tk:
    :return: pod_file_name,uri
    """

    # 检查路径是否存在，不存在则创建
    pod_save_dir = Path(pod_path)
    if not pod_save_dir.is_dir():
        pod_save_dir.mkdir()

    try:
        html_file_name = tk + '.html'
        base64_to_html(base64, TMP_HTML_PATH, html_file_name)
        # 生成截图
        pdf_file_name = tk + '-' + id_generator(5) + '-ups.pdf'
        html_path = "%s/%s" % (TMP_HTML_PATH, html_file_name)
        if Path(html_path).is_file():
            command = HTML_TO_IMAGE_COMMAND.replace('HTML_PATH', html_path) \
                .replace('PDF_PATH', "%s\\%s" % (pod_save_dir, pdf_file_name))
            print(command)
            print(pod_path)
            c_rel = os.system(command)
            print(c_rel)
            # 命令执行成功
            if c_rel == 0:
                if Path(html_path).exists():
                    os.remove(html_path)
                    return True
            else:
                log.error("Execute %s failed !!!!" % command)
        else:
            log.error("UPS %s pod html save failed, the html not exist !!!" % tk)
    except:
        log.error("UPS pod base64 str save to html file failed !!!!")
        log.error(traceback.format_exc())
        pass
    return False
