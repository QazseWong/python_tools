#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: __init__.py 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
