#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""


class Logger(object):
    def __init__(self, log_file):  # 传入一个文件名
        import time
        self.time = time
        self.log_file = log_file  # 定义日志文件名
        self.user = None  # 初始化记录操作用户名称
        self.status = None  # 初始化记录日志状态
        self.event = None  # 初始化记录事情内容字段
        self.is_day_time = True  # 查询条件是否为按天查询
        self.count = 0  # 初始化计数器
        self.open_file = None  # 初始化打开文件句柄名称
        self.cur_time = None  # 初始化时间字段

    def write_log(self, user=None, status=None, event=None, cur_time=None):
        self.user = user
        self.status = status
        self.event = event
        self.cur_time = self.time.strftime("%Y-%m-%d %H:%M:%S", self.time.localtime())  # 获取当前时间
        if cur_time:
            self.cur_time = cur_time
        self.open_file = open(self.log_file, mode="a+")
        self.open_file.write("%s  %s %s %s\n" % (str(self.cur_time), str(self.user), str(self.status), str(self.event)))
        self.open_file.close()

    def read_log(self, user=None, status=None, search_time=None):
        self.user = user
        self.status = status
        self.cur_time = search_time
        self.count = 0
        if str(self.cur_time).__contains__(":"):
            self.is_day_time = False
        self.open_file = open(self.log_file, mode="a+")
        self.open_file.seek(0)
        for log in self.open_file.readlines():
            log_list = log.split()
            if len(log_list) > 3:
                try:
                    if self.is_day_time:
                        self.time.strptime(log_list[0], "%Y-%m-%d")  # 判断日志时间格式
                        record_time = log_list[0]
                    else:
                        self.time.strptime(log_list[1], "%H:%M:%S")
                        record_time = log_list[1]
                except ValueError:
                    record_time = self.time.strftime("%Y-%m-%d", self.time.localtime())  # 默认取当天日期
                user_name = log_list[2]
                user_status = log_list[3]
                if user_name == str(self.user):
                    if self.status and self.cur_time:
                        if len(str(self.cur_time).split("-")) > 2:
                            if record_time == str(self.cur_time) and user_status == str(self.status):
                                self.count += 1
                        elif len(str(self.cur_time).split(":")) > 2:
                            if record_time == str(self.cur_time) and user_status == str(self.status):
                                self.count += 1
                    elif self.status:
                        if user_status == str(self.status):
                            self.count += 1
                    elif self.cur_time:
                        if len(str(self.cur_time).split("-")) > 2:
                            if record_time == str(self.cur_time):
                                self.count += 1
                        elif len(str(self.cur_time).split(":")) > 2:
                            if record_time == str(self.cur_time):
                                self.count += 1
        self.open_file.close()
        return self.count  # 返回查询条件次数
