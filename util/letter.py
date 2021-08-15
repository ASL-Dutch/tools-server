# 字符串工具
import random
import string


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    生成指定位数的字符串
    :param size:
    :param chars:  可指定在哪些字符中生成水机字符串
    :return:
    """
    return ''.join(random.choice(chars) for _ in range(size))


def transfer_content(content):
    """
    转义字符串中的单双引号
    :param content:
    :return:
    """
    if content is None:
        return None
    else:
        string = ""
        for c in content:
            if c == '"':
                string += '\\\"'
            elif c == "'":
                string += "\\\'"
            elif c == "\\":
                string += "\\\\"
            else:
                string += c
        return string
