#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: requser 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------
import requests


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


def request_get(url, params=None, proxy=None,encoding = None,**kwargs):
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
        if encoding:
            response.encoding = encoding
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return None
