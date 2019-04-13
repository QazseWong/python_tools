#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: text 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------
import re


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


def md5_str(text):
    """
    获取MD5
    :param text:
    :return:
    """
    from hashlib import md5

    return md5(str(text).encode()).hexdigest()

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

def remove_n_r(text):
    """
    删除空格。换行符
    :param text:
    :return:
    """
    return str(text).strip()
