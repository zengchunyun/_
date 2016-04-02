#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
event_list = []  # 定义一个事件驱动列表,只有注册了该事件列表的对象都会被该事件方法处理


def run():
    for event in event_list:
        obj = event()
        obj.execute()  # 注册该事件的对象必须自己实现这个方法


class BaseHandler(object):
    """
    用户必须继承该类,从而规范所有类的方法,(类似接口功能)
    """
    def execute(self):
        raise Exception("you must overide execute method")

