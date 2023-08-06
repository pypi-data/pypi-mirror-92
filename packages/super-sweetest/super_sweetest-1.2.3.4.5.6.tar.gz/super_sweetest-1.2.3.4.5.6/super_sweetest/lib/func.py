code = """
# coding:utf-8

# @Time: 2020/12/29 15:16
# @Auther: liyubin

import datetime
import random
import time
import json

# 本文件每次运行覆盖，请勿在此写自定义函数

def set_different_var(var_name='body_', num=1):
    # 通过使用此函数，在用例片段中可提取和设置body中不同的参数为变量
    return "<{}>".format(var_name + str(num))

char_name_file = './lib/char_num.json'  # 记录用例顺序生成随机参数文件
error_msg = "必填参数: char_type,  min_, max_, preset, char_name  对应： 字符类型， 最小长度， 最大长度， 正确预设值， 参数所在位置 如：'Login_009|1|3' / 'Login_009|2|3'  / 'Login_009|3|3'"


def func(char_type='随机', min_=1, max_=3, preset='预设值', char_name='demo_001|1|1'):
    # 自定义随机函数，api用例统一调用，传入关键字生成随机值
    # :param char_type: 字符类型 默认 随机 ，指定固定范围参数 中文|字母|特殊
    # :param min: 最小长度
    # :param max: 最大长度
    # :param preset: 正确预设值 参数组合
    # :param char_name: 参数所在位置  'Login_009|1|3' / 'Login_009|2|3'  / 'Login_009|3|3'
    # :return:
    try:
        if char_type == '随机':
            char_type_list = ['中文', '数字', '大写字母', '小写字母', '字母', '字母数字', '时间戳', '年月日', '特殊']
            # char_type_list = ['中文', '数字']
        else:
            char_type_list = char_type.split('|')

        # 按顺序递增替换变量 直到 = char_num_s
        if min_ and max_ and preset and char_name:
            preset_ = preset
            char_name_ = char_name.split('|')
            char_caseid = char_name_[0]
            char_num = int(char_name_[1])
            char_num_s = int(char_name_[2])

            CHAR_NAME_41 = read_random_char_num(char_caseid)  # 历史信息

            # 如果没有读取历史替换 char_caseid == 1
            if CHAR_NAME_41.get(char_caseid, {}).get('num', 0) == 0:
                CHAR_NAME_41[char_caseid]['num'] = 1
                with open(char_name_file, 'w')as fp:
                    json.dump(CHAR_NAME_41, fp)

            # 最新信息， 降低读写频率，上一个 if 条件成立时 说明写入了新的，再读， else = 上次读取内容
            CHAR_NAME_49 = read_random_char_num(char_caseid) if CHAR_NAME_41.get(char_caseid, {}).get('num', 0) == 0 else CHAR_NAME_41

            # 当所有的 char_type 循环完了再 +1 ，下次跑 +1 的下一个参数

            CHAR_TYPE_54 = CHAR_NAME_49.get(char_caseid).get('char_type')
            CHAR_TYPE = char_type_list[CHAR_TYPE_54] if CHAR_TYPE_54 <= len(char_type_list) - 1 else char_type_list[0]


            DATA = ''
            if CHAR_NAME_49.get(char_caseid).get('num') == char_num:
                random_str_new = random_str(CHAR_TYPE, min_, max_)  # 随机字符

                # char_type 的 index +1 ，下次使用下一个随机类型， 超过最大index 说明循环完 char_type = 0
                with open(char_name_file, 'w', encoding='utf8')as fp:
                    CHAR_NAME_49[char_caseid]['char_type'] = CHAR_NAME_49.get(char_caseid).get('char_type') + 1 if CHAR_NAME_49.get(char_caseid).get('char_type') < len(char_type_list) - 1 else 0
                    json.dump(CHAR_NAME_49, fp)

                # 返回随机字符类型
                DATA =  random_str_new
            # 返回前信息， 降低读写频率，上一个 if 条件成立时 说明写入了新的，再读， else = 上次读取内容
            CHAR_NAME_71 = read_random_char_num(char_caseid) if CHAR_NAME_49.get(char_caseid).get('num') == char_num else CHAR_NAME_49
            # 每次读完在写入，防止读到下次需要随机的参数，两个参数都随机
            if char_num == char_num_s and CHAR_NAME_71.get(char_caseid).get('char_type') == 0:  # 小于时递增，最大参数时归一,  char_type = 0 说明前面更新后超过最大index，循环完毕，就可以循环下一个参数的不同类型
                with open(char_name_file, 'w', encoding='utf8')as fp:
                    CHAR_NAME_71[char_caseid]['num'] = CHAR_NAME_71.get(char_caseid).get('num') + 1 if CHAR_NAME_71.get(char_caseid).get('num') < char_num_s else 1
                    json.dump(CHAR_NAME_71, fp)

            elif CHAR_NAME_71.get(char_caseid).get('num') == 0:
                return 0

            return preset_  if DATA == '' else DATA  # 预设值
        else:
            assert False, error_msg

    except:
        assert False, error_msg

def random_str(char_type, min_, max_):
    # char_type_list = ['中文', '数字', '大写字母', '小写字母', '字母', '字母数字', '时间戳', '年月日', '特殊']

    # 生成任意字符
    if '中文' == char_type:
        first_name = ["王", "李", "张", "刘", "赵", "蒋", "孟", "陈", "徐", "杨", "沈", "马", "高", "殷", "官", "钟",
                      "常", "伟", "华", "国", "洋", "刚", "里", "民", "牧", "陆", "路", "昕", "鑫", "兵", "硕", "宏",
                      "峰", "磊", "雷", "文", "浩", "光", "超", "军", "达"]
        zh = ''
        for i in range(random.randint(min_, max_)):
            zh = zh + random.choice(first_name)
        char = zh
    elif '数字' == char_type:
        num = ''
        for i in range(random.randint(min_, max_)):
            num += chr(random.randint(49, 57))  # 49-57对应字符0-9
        char = num
    elif '大写字母' == char_type:
        STR = ''
        for i in range(random.randint(min_, max_)):
            STR += chr(random.randint(66, 90))  # 65-91对应字符A-Z
        char = STR.replace('{', '').replace('}', '')
    elif '小写字母' == char_type:
        str_ = ''
        for i in range(random.randint(min_, max_)):
            str_ += chr(random.randint(97, 123))  # 97-123对应字符a-z
        char = str_.replace('{', '').replace('}', '')
    elif '字母' == char_type:  # 不区分大小写
        SRT_str_ = ''
        for i in range(random.randint(min_, max_)):
            code = random.randint(66, 90) if (i % 2) == 0 else random.randint(97, 123)
            SRT_str_ += chr(code)
        char = SRT_str_.replace('{', '').replace('}', '')
    elif '字母数字' == char_type:
        SRT_str_ = ''
        for i in range(random.randint(min_, max_)):
            code = random.randint(66, 90) if (i % 2) == 0 else random.randint(97, 123)
            SRT_str_ += chr(code)
        char = SRT_str_.replace('{', '').replace('}', '')[1:] + str(chr(random.randint(49, 57)))
    elif '正则' in char_type:
        from xeger import Xeger
        x = Xeger(limit=max_)
        string_or_regex = char_type.replace('正则:', '').replace('：','')
        char = x.xeger(string_or_regex)
    elif '时间戳' == char_type:
        char = time.time()
    elif '年月日' == char_type:
        char = datetime.datetime.now().strftime('%Y%m%d')
    elif '特殊' == char_type:
        first_name = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '_', '+', '=', '|', '[',
                      '{', '}', ']', ';', ':', '.', ',']
        teshu = ''
        for i in range(random.randint(min_, max_)):
            teshu = teshu + random.choice(first_name)
        char = teshu
    else:
        char = '没有生成符合的数据类型'

    return char


def read_random_char_num(char_caseid):
    # 读取写入的内容
    # from lib.char_num import random_char_num
    try:
        with open(char_name_file, 'r')as fp:
            random_char_ = json.load(fp)
            # 新的char_caseid 不存在时更新
            if char_caseid not in random_char_:
                with open(char_name_file, 'w')as fp:
                    random_char_[char_caseid] = {'num': 1, 'char_type': 0}
                    json.dump(random_char_, fp)
        return random_char_
    except:
        # 首次不存在或者内容读取错误时 写入， 而不是只判断文件存在
        # if not os.path.exists('./lib/char_num.json'):
        with open(char_name_file, 'w')as fp:
            json.dump({char_caseid: {'num': 1, 'char_type': 0}}, fp)
    # 报错写完 再读
    with open(char_name_file, 'r')as fp:
        random_char_ = json.load(fp)
    return random_char_

if __name__ == '__main__':
    min = r'(200[0-9]-14[5你好]-15[4]$18[0-9]17[a-z])(\d{8})'

    # for ii in range(1):
    #     min = 4
    #     data = func("数字", 2,2)
    #     print(data)

    # STR = '' [1-9]_[a_z]ssdsdsdsd_123123213
    # for i in range(random.randint(3, 18)):
    #     code = random.randint(66, 90) if (i % 2) == 0 else random.randint(97, 123)
    #     STR+=chr(code)
    # print(STR)

    ss1 = 'Login_009|1|4'
    ss2 = 'Login_009|2|4'
    ss3 = 'Login_009|3|4'
    ss4 = 'Login_009|4|4'

    for ss in [ss1, ss2, ss3, ss4]:
        data = func("年月日|特殊|正则:(200[0-9]-14[5你好]-15[4]$18[0-9]17[a-z])(\d{8})", 3, 12, '预设值' + ss, ss)
        print(data)
"""

# coding:utf-8

# @Time: 2020/12/29 15:16
# @Auther: liyubin

import datetime
import random
import time
import json

# 本文件每次运行覆盖，请勿在此写自定义函数

def set_different_var(var_name='body_', num=1):
    # 通过使用此函数，在用例片段中可提取和设置body中不同的参数为变量
    return "<{}>".format(var_name + str(num))

char_name_file = './lib/char_num.json'  # 记录用例顺序生成随机参数文件
error_msg = "必填参数: char_type,  min_, max_, preset, char_name  对应： 字符类型， 最小长度， 最大长度， 正确预设值， 参数所在位置 如：'Login_009|1|3' / 'Login_009|2|3'  / 'Login_009|3|3'"


def func(char_type='随机', min_=1, max_=3, preset='预设值', char_name='demo_001|1|1'):
    # 自定义随机函数，api用例统一调用，传入关键字生成随机值
    # :param char_type: 字符类型 默认 随机 ，指定固定范围参数 中文|字母|特殊
    # :param min: 最小长度
    # :param max: 最大长度
    # :param preset: 正确预设值 参数组合
    # :param char_name: 参数所在位置  'Login_009|1|3' / 'Login_009|2|3'  / 'Login_009|3|3'
    # :return:
    try:
        if char_type == '随机':
            char_type_list = ['中文', '数字', '大写字母', '小写字母', '字母', '字母数字', '时间戳', '年月日', '特殊']
            # char_type_list = ['中文', '数字']
        else:
            char_type_list = char_type.split('|')

        # 按顺序递增替换变量 直到 = char_num_s
        if min_ and max_ and preset and char_name:
            preset_ = preset
            char_name_ = char_name.split('|')
            char_caseid = char_name_[0]
            char_num = int(char_name_[1])
            char_num_s = int(char_name_[2])

            CHAR_NAME_41 = read_random_char_num(char_caseid)  # 历史信息

            # 如果没有读取历史替换 char_caseid == 1
            if CHAR_NAME_41.get(char_caseid, {}).get('num', 0) == 0:
                CHAR_NAME_41[char_caseid]['num'] = 1
                with open(char_name_file, 'w')as fp:
                    json.dump(CHAR_NAME_41, fp)

            # 最新信息， 降低读写频率，上一个 if 条件成立时 说明写入了新的，再读， else = 上次读取内容
            CHAR_NAME_49 = read_random_char_num(char_caseid) if CHAR_NAME_41.get(char_caseid, {}).get('num', 0) == 0 else CHAR_NAME_41

            # 当所有的 char_type 循环完了再 +1 ，下次跑 +1 的下一个参数

            CHAR_TYPE_54 = CHAR_NAME_49.get(char_caseid).get('char_type')
            CHAR_TYPE = char_type_list[CHAR_TYPE_54] if CHAR_TYPE_54 <= len(char_type_list) - 1 else char_type_list[0]


            DATA = ''
            if CHAR_NAME_49.get(char_caseid).get('num') == char_num:
                random_str_new = random_str(CHAR_TYPE, min_, max_)  # 随机字符

                # char_type 的 index +1 ，下次使用下一个随机类型， 超过最大index 说明循环完 char_type = 0
                with open(char_name_file, 'w', encoding='utf8')as fp:
                    CHAR_NAME_49[char_caseid]['char_type'] = CHAR_NAME_49.get(char_caseid).get('char_type') + 1 if CHAR_NAME_49.get(char_caseid).get('char_type') < len(char_type_list) - 1 else 0
                    json.dump(CHAR_NAME_49, fp)

                # 返回随机字符类型
                DATA =  random_str_new
            # 返回前信息， 降低读写频率，上一个 if 条件成立时 说明写入了新的，再读， else = 上次读取内容
            CHAR_NAME_71 = read_random_char_num(char_caseid) if CHAR_NAME_49.get(char_caseid).get('num') == char_num else CHAR_NAME_49
            # 每次读完在写入，防止读到下次需要随机的参数，两个参数都随机
            if char_num == char_num_s and CHAR_NAME_71.get(char_caseid).get('char_type') == 0:  # 小于时递增，最大参数时归一,  char_type = 0 说明前面更新后超过最大index，循环完毕，就可以循环下一个参数的不同类型
                with open(char_name_file, 'w', encoding='utf8')as fp:
                    CHAR_NAME_71[char_caseid]['num'] = CHAR_NAME_71.get(char_caseid).get('num') + 1 if CHAR_NAME_71.get(char_caseid).get('num') < char_num_s else 1
                    json.dump(CHAR_NAME_71, fp)

            elif CHAR_NAME_71.get(char_caseid).get('num') == 0:
                return 0

            return preset_  if DATA == '' else DATA  # 预设值
        else:
            assert False, error_msg

    except:
        assert False, error_msg

def random_str(char_type, min_, max_):
    # char_type_list = ['中文', '数字', '大写字母', '小写字母', '字母', '字母数字', '时间戳', '年月日', '特殊']

    # 生成任意字符
    if '中文' == char_type:
        first_name = ["王", "李", "张", "刘", "赵", "蒋", "孟", "陈", "徐", "杨", "沈", "马", "高", "殷", "官", "钟",
                      "常", "伟", "华", "国", "洋", "刚", "里", "民", "牧", "陆", "路", "昕", "鑫", "兵", "硕", "宏",
                      "峰", "磊", "雷", "文", "浩", "光", "超", "军", "达"]
        zh = ''
        for i in range(random.randint(min_, max_)):
            zh = zh + random.choice(first_name)
        char = zh
    elif '数字' == char_type:
        num = ''
        for i in range(random.randint(min_, max_)):
            num += chr(random.randint(49, 57))  # 49-57对应字符0-9
        char = num
    elif '大写字母' == char_type:
        STR = ''
        for i in range(random.randint(min_, max_)):
            STR += chr(random.randint(66, 90))  # 65-91对应字符A-Z
        char = STR.replace('{', '').replace('}', '')
    elif '小写字母' == char_type:
        str_ = ''
        for i in range(random.randint(min_, max_)):
            str_ += chr(random.randint(97, 123))  # 97-123对应字符a-z
        char = str_.replace('{', '').replace('}', '')
    elif '字母' == char_type:  # 不区分大小写
        SRT_str_ = ''
        for i in range(random.randint(min_, max_)):
            code = random.randint(66, 90) if (i % 2) == 0 else random.randint(97, 123)
            SRT_str_ += chr(code)
        char = SRT_str_.replace('{', '').replace('}', '')
    elif '字母数字' == char_type:
        SRT_str_ = ''
        for i in range(random.randint(min_, max_)):
            code = random.randint(66, 90) if (i % 2) == 0 else random.randint(97, 123)
            SRT_str_ += chr(code)
        char = SRT_str_.replace('{', '').replace('}', '')[1:] + str(chr(random.randint(49, 57)))
    elif '正则' in char_type:
        from xeger import Xeger
        x = Xeger(limit=max_)
        string_or_regex = char_type.replace('正则:', '').replace('：','')
        char = x.xeger(string_or_regex)
    elif '时间戳' == char_type:
        char = time.time()
    elif '年月日' == char_type:
        char = datetime.datetime.now().strftime('%Y%m%d')
    elif '特殊' == char_type:
        first_name = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '_', '+', '=', '|', '[',
                      '{', '}', ']', ';', ':', '.', ',']
        teshu = ''
        for i in range(random.randint(min_, max_)):
            teshu = teshu + random.choice(first_name)
        char = teshu
    else:
        char = '没有生成符合的数据类型'

    return char


def read_random_char_num(char_caseid):
    # 读取写入的内容
    # from lib.char_num import random_char_num
    try:
        with open(char_name_file, 'r')as fp:
            random_char_ = json.load(fp)
            # 新的char_caseid 不存在时更新
            if char_caseid not in random_char_:
                with open(char_name_file, 'w')as fp:
                    random_char_[char_caseid] = {'num': 1, 'char_type': 0}
                    json.dump(random_char_, fp)
        return random_char_
    except:
        # 首次不存在或者内容读取错误时 写入， 而不是只判断文件存在
        # if not os.path.exists('./lib/char_num.json'):
        with open(char_name_file, 'w')as fp:
            json.dump({char_caseid: {'num': 1, 'char_type': 0}}, fp)
    # 报错写完 再读
    with open(char_name_file, 'r')as fp:
        random_char_ = json.load(fp)
    return random_char_

if __name__ == '__main__':
    min = r'(200[0-9]-14[5你好]-15[4]$18[0-9]17[a-z])(\d{8})'

    # for ii in range(1):
    #     min = 4
    #     data = func("数字", 2,2)
    #     print(data)

    # STR = '' [1-9]_[a_z]ssdsdsdsd_123123213
    # for i in range(random.randint(3, 18)):
    #     code = random.randint(66, 90) if (i % 2) == 0 else random.randint(97, 123)
    #     STR+=chr(code)
    # print(STR)

    ss1 = 'Login_009|1|4'
    ss2 = 'Login_009|2|4'
    ss3 = 'Login_009|3|4'
    ss4 = 'Login_009|4|4'

    for ss in [ss1, ss2, ss3, ss4]:
        data = func("年月日|特殊|正则:(200[0-9]-14[5你好]-15[4]$18[0-9]17[a-z])(\d{8})", 3, 12, '预设值' + ss, ss)
        print(data)