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
        self.count = 0  # 初始化计数器
        self.open_file = None  # 初始化打开文件句柄名称
        self.cur_time = None  # 初始化时间字段
        self.start_time = None  # 初始化开始查询时间
        self.end_time = None  # 初始化结束查询时间
        self.match_list = []  # 初始化一个匹配条件列表

    def write_log(self, user=None, status=None, event=None, cur_time=None):  # 写入日志
        self.user = user
        self.status = status
        self.event = event
        self.cur_time = self.time.strftime("%Y-%m-%d %H:%M:%S", self.time.localtime())  # 获取当前时间
        if cur_time:
            self.cur_time = cur_time
        self.open_file = open(self.log_file, mode="a+")
        self.open_file.write("%s  %s %s %s\n" % (str(self.cur_time), str(self.user), str(self.status), str(self.event)))
        self.open_file.close()

    def search_count(self, user="", status="", content=None, print_log=False):  # 查询匹配,匹配成功返回1,否则返回0,可选打印
        self.count = 0
        self.user = str(user)
        self.status = str(status)
        if len(content) < 3:
            return self.count
        if self.user and self.status:
            if str(self.user) == content[2] and str(self.status) == content[3]:
                if print_log:
                    print(" ".join(content))
                self.count += 1
        elif self.user:
            if str(self.user) == content[2]:
                if print_log:
                    print(" ".join(content))
                self.count += 1
        elif self.status:
            if str(self.status) == content[3]:
                if print_log:
                    print(" ".join(content))
                self.count += 1
        else:
            if print_log:
                print(" ".join(content))
            self.count += 1
        return self.count

    def get_match_count(self, user="", status="", start_time=None, end_time=None):  # 返回匹配次数
        self.match_list = self.get_match_log(
            user=user, status=status, start_time=start_time, end_time=end_time)
        self.count = len(self.match_list)
        return self.count

    def get_match_log(self, user="", status="", start_time=None, end_time=None, print_log=False):  # 返回匹配列表
        self.user = user
        self.status = status
        self.start_time = str(start_time)
        self.end_time = str(end_time)
        self.match_list = []
        if self.start_time == str(None):
            self.start_time = self.time.strftime("%Y-%m-%d", self.time.localtime())
        if self.end_time == str(None):
            self.end_time = self.time.strftime("%Y-%m-%d", self.time.localtime())
        if len(self.start_time.split()) == 2:
            start_day = self.start_time.split()[0]
            start_hour = self.start_time.split()[1]
        else:
            start_day = self.start_time
            start_hour = "00:00:00"
        if len(self.end_time.split()) == 2:
            end_day = self.end_time.split()[0]
            end_hour = self.end_time.split()[1]
        else:
            end_day = self.end_time
            end_hour = "23:59:59"
        self.open_file = open(self.log_file, mode="a+")
        self.open_file.seek(0)
        for log in self.open_file.readlines():
            log_list = log.split()
            if len(log_list) > 3:
                if start_day < log_list[0] < end_day:
                    if self.search_count(user=self.user, status=self.status, content=log_list, print_log=print_log):
                        self.match_list.append(log.strip())
                elif start_day == log_list[0] < end_day:
                    if start_hour <= log_list[1]:
                        if self.search_count(user=self.user, status=self.status, content=log_list, print_log=print_log):
                            self.match_list.append(log.strip())
                elif start_day == log_list[0] == end_day:
                    if start_hour <= log_list[1] <= end_hour:
                        if self.search_count(user=self.user, status=self.status, content=log_list, print_log=print_log):
                            self.match_list.append(log.strip())
                elif start_day < log_list[0] == end_day:
                    if end_hour >= log_list[1]:
                        if self.search_count(user=self.user, status=self.status, content=log_list, print_log=print_log):
                            self.match_list.append(log.strip())
        self.open_file.close()
        return self.match_list
