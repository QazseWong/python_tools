#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: db 
#       作者  : Qazse 
#       时间  : 2019/4/18
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------
import redis

class redis_db():

    def __init__(self,host='192.168.1.10',port=6379,db=0,password=''):
        self.r = redis.Redis(host=host, port=port, db=db,password=password)


    def list_to_set(self,list,name='discharge'):
        """
        写list 到 set
        :param list:
        :param name:
        :return:
        """
        for data in list:
            self.r.sadd(name,data)

    def val_to_set(self,val,name='discharge'):
        """
        写值到set
        :param val:
        :param name:
        :return: 失败 返回 0
        """
        return self.r.sadd(name,val)

if __name__ == '__main__':
    r = redis_db(host='192.168.1.10',port=6633,db=3,password='wang1997')
    import qazse
    datas = qazse.file.read_file_list('urls.txt')
    r.list_to_set(datas,'cyb')