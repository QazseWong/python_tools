#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


def request_get(url, params=None, proxy=None, encoding=None, **kwargs):
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


def max_request_get(urls, max_pool=100, directory='data', show_log=True, headers=None, save_status_200 = True):
    """
    多线程读HTTP
    :param urls: dict {url:'http://xxx','name':'xxx',data:'data',method:"GET" }
    :param max_pool: 最大线程
    :param directory: 存储目录
    :param show_log: 显示日志
    :param headers:  请求头
    :save_status_200: 只保存返回为200的内容
    :return:
    """

    import aiohttp, asyncio
    from qazse import file

    file.mkdir(directory)

    async def main(pool):  # aiohttp必须放在异步函数中使用
        tasks = []
        sem = asyncio.Semaphore(pool)  # 限制同时请求的数量
        for url_info in urls:
            tasks.append(control_sem(sem, url_info))
        await asyncio.wait(tasks)

    async def control_sem(sem, url_info):  # 限制信号量
        async with sem:
            await fetch(url_info)

    async def fetch(url_info):
        async with aiohttp.request(url_info.get('method'), url_info.get('url'), data=url_info.get('data'),headers=headers) as resp:
            if show_log:
                print('Download', url_info.get('url'), url_info.get('method'), resp.status)
            if save_status_200:
                if resp.status == 200:
                    file.write_file(await resp.read(), file_path=directory + '/' + url_info.get('name'))
            else:
                file.write_file(await resp.read(), file_path=directory + '/' + url_info.get('name'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(pool=max_pool))
