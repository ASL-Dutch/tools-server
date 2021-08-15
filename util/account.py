# 获取物流信息需要用到的 第三方参数文件
import os

ups_conf = {
    # 'access_license_number': os.getenv('UPS_ACCESS_LICENSE_NUMBER'),
    'access_license_number': '8D5644C32FE8C868',
    'user_id': os.getenv('UPS_USER_ID'),
    'password': os.getenv('UPS_PASSWORD')
}

dpd_conf = {
    'username': os.getenv('DPD_LOGIN_USERNAME'),
    'password': os.getenv('DPD_LOGIN_PASSWORD')
}


def account():
    """
    获取 logistics 相关的账户信息
    :return:
    """
    return ups_conf, dpd_conf
