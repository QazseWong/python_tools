#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ---------------------------------------------------
#       项目名: ins_spider   
#       文件名: qazse 
#       作者  : Qazse 
#       时间  : 2019/3/31
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------


# 日志系统
import io
import logging
import os
import re
import sys
import time

import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


# logging.disable(logging.CRITICAL)   # 禁止输出日志
def log(logger_name='log-log', log_file=os.path.join(BASE_DIR, 'log', 'log.log'), level=logging.DEBUG,
        console_level=logging.DEBUG):
    try:
        os.mkdir('log')
    except:
        pass
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)  # 添加日志等级

    # 创建控制台 console handler
    ch = logging.StreamHandler()
    # 设置控制台输出时的日志等级
    ch.setLevel(console_level)

    # 创建文件 handler
    fh = logging.FileHandler(filename=log_file, encoding='utf-8')
    # 设置写入文件的日志等级
    fh.setLevel(logging.DEBUG)
    # 创建 formatter
    formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(name)s %(levelname)s %(message)s')

    # 添加formatter
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # 把ch fh 添加到logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


def read_file_list(file_path, encoding='utf8'):
    """
    读取文件返回列表
    :param file: 文件目录
    :return:
    """
    file_list = []
    files = open(file_path, 'r', encoding=encoding)
    for file in files:
        file_list.append(file.strip())
    files.close()
    return file_list


def write_sql(sql, file_path='sql.sql', encoding='utf8'):
    """
    写sql
    :param sql: sql语句
    :param file_path: 写到目录
    :return:
    """
    with open(file_path, 'a+', encoding=encoding) as f:
        if not '\n' in sql:
            sql = sql + '\n'
        f.write(sql)

def write_text(sql, file_path='text.txt', encoding='utf8'):
    """
    写text
    :param sql: sql语句
    :param file_path: 写到目录
    :return:
    """
    with open(file_path, 'a+', encoding=encoding) as f:
        if not '\n' in sql:
            sql = sql + '\n'
        f.write(sql)

def remove_emoji(text):
    """
    删除emoji
    :param text:
    :return:
    """
    try:
        data = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        data = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return data.sub(u'', text)


def baidu_weight(text):
    """
    获取百度权重
    :param text:
    :return:
    """
    from bs4 import BeautifulSoup
    import difflib

    url = "https://www.baidu.com/s"
    querystring = {"wd": text}
    headers = {
        'accept': "application/json, text/javascript",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'content-type': "application/x-www-form-urlencoded",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        'x-requested-with': "XMLHttpRequest",
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    max_index = 0
    h3_list = soup.find_all('em')
    for h3 in h3_list:
        s1 = h3.text
        index = difflib.SequenceMatcher(None, text, s1).quick_ratio()
        if max_index <= index:
            max_index = index
    return max_index


def md5_str(text):
    """
    获取MD5
    :param text:
    :return:
    """
    from hashlib import md5

    return md5(str(text).encode()).hexdigest()


def timestamp(timestamp=time.time(), thirteen=False):
    """
    获取时间戳
    :param timestamp: 时间戳
    :param thirteen: 取三十位
    :return:
    """
    if thirteen:
        return int(timestamp)
    else:
        return int(timestamp * 1000)


def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    """
    将时间转化为时间戳
    :param date:
    :param format_string:
    :return:
    """
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    """
    将时间戳转换为时间
    :param time_stamp:
    :param format_string:
    :return:
    """
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


def useragent(device=0):
    """
    返回一个头
    :param device:
    :return:
    """
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        'cache-control': "no-cache",
    }
    return headers


def request_get(url, params=None, proxy=None, **kwargs):
    """
    get参数
    :param url:
    :param params:
    :param proxy:
    :param kwargs:
    :return:
    """
    from requests.adapters import HTTPAdapter
    if proxy:
        proxies = {
            'http': 'http://%s' % proxy,
            'https': 'https://%s' % proxy
        }
    else:
        proxies = {
            'http': None,
            'https': None
        }
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    try:
        response = requests.get(url, params, proxies=proxies, headers=useragent(), **kwargs)
        response.encoding = 'utf-8'
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def remove_n_r(text):
    """
    删除空格。换行符
    :param text:
    :return:
    """
    return str(text).strip()

def remove_keyword(text,keywords):
    """
    删除指定关键字,支持正则
    :param text:
    :param keyword:
    :return:
    """
    import re
    for keyword in keywords:
        # text = str(text).replace(keyword,'')
        text = re.sub(keyword,'',text)
    return remove_n_r(text)

# class thread():
#     """
#     线程框架
#     """
#     todo
#     class threads(threading.Thread):
#
#         def __init__(self):
#
#     def __init__(self, function, Threads=100, is_lock=False, data =()):
#         threading.Thread.__init__(self)
#         self.data = data
#         self.function = function
#         self.Threads = Threads
#         self.is_lock = is_lock
#
#         self.queueLock = threading.Lock()
#         self.workQueue = queue.Queue()
#
#         for t in range(Threads):
#
#
#     def run(self):
#         pass
