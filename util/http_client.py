import json
import os
import traceback
from pathlib import Path

import requests


def get_request(url):
    """
    发起get 请求
    :param url:
    :return:
    """
    response = requests.request("GET", url)
    return response.text


def post_request(url, payload):
    """
    发起 post 请求
    :param url:
    :param payload: json str(json.dumps)
    :return:
    """
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response


def post_request_by_xml(url, payload):
    """
    通过 xml 发起的数据请求
    :param url:
    :param payload:
    :return:
    """
    headers = {
        'Content-Type': 'application/xml'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    return response.text


def get_cookie_of_dpd(url, payload):
    """
    通过登录接口返回 header中的 set-cookie作为请求凭证
    :param url:
    :param payload:
    :return:
    """
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.headers['Set-Cookie']


def download_file_url_to_path(file_url, cookie, save_path, pod_name):
    """
    保存未见到指定路径
    :param file_url:
    :param cookie
    :param save_path:
    :return:
    """
    # 检查路径是否存在，不存在则创建
    pod_save_dir = Path(save_path)
    if not pod_save_dir.is_dir():
        pod_save_dir.mkdir()

    headers = {
        'Cookie': cookie
    }
    try:
        r = requests.get(file_url, headers=headers)
        file_type = r.headers['Content-type'].split('/')[1] or 'pdf'

        save_path = save_path + pod_name
        save_path = '%s.%s' % (save_path, file_type)

        print("Download file, file save path:", save_path)
        with open(save_path, 'wb') as f:
            f.write(r.content)
        return True
    except:
        print(traceback.format_exc())
        pass
    return False


if __name__ == '__main__':
    url = 'https://tracking.dpd.de/rest/documents/v2/documents?documentKey=2kfDho6p3Bn0mXXMIMn%2FXRchAF%2BQPsSquTaIEg7rRmVKUru6C3iG%2FEtY7RiQOtlgtZrrBlB%2F88sFhQkivD3gGicGKid1CL3z4rP%2By1DXVyLTJW2VNP6dZV1lcGIymdrlMVtciXr3HEgXHAGwm7XnY1WI%2BvDvWWd9uSeqZKhFiHSoudSqUOi2i1XVRvP9yqIl&messageLanguage=en_US'
    cookie = 'ntrack=s%3ApivMKhd2oHLQusT_fRXh0FGxat5J3mrt.AssXFKg9r0XgJymNiNUlPB7GsPVc9APA9ZrOfBUvhsE; Path=/'
    download_file_url_to_path(url, cookie, './test.tif', '')
