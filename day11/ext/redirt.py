#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
'/Users/zengchunyun/Documents/PycharmProjects/s12/day11/myfort/bin/myfort.py'  # 目标模块
'/Users/zengchunyun/Documents/PycharmProjects/s12/day11/ext/redirt.py'  # 执行模块

# from ..myfort.core.shortcuts import runserver
# 通过加入path变量后,

str1 = "myfort.core.shortcuts"
package = __import__(str1)  # 导入shortcuts模块,并执行模块
if hasattr(package, 'core'):  # 由于是非同级目录,package只导入了myfort.core,并执行了shortcuts
    module = getattr(package, 'core')  # 我们需要执行的是指定的函数,所以需要再获取一次,首先获取core目录下的所有模块
    func = getattr(module, 'shortcuts')  # 然后在core目录下找shortcuts模块
    func.runserver()  # 执行shortcuts模块的函数
