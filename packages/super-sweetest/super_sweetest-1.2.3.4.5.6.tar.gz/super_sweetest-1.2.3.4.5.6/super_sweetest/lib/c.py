# coding:utf-8

import datetime
import random


# write your function this file
def today():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d')


def common(char_type, min, max):
    """
    自定义随机函数，api用例统一调用，传入关键字生成随机值
    :param kwargs:
    :return:
    """
    if char_type in '中文':
        char = random.randint()
    elif char_type in '数字':
        char = random.randint(min, max)
    else:
        char = char_type

    return char

if __name__ == '__main__':
    data = common('数字', 100, 999)
    print(data)
    print(random.choice('i love python'))