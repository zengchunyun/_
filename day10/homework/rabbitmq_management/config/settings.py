#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import os
import logging


# 监听客户端地址,默认监听所有客户端
server = "localhost"

# 监听端口
port = 5672

# 设置每个任务最大超时时间,避免无期限等待
timeout = 15

# 设置服务器角色ID,该名称方便标识处理任务的主机,如果为空,则以服务器IP作为唯一ID
host_id = ""

# 该配置仅针对客户端有效,用于绑定指定队列,接收不同的任务,如果不填,则默认监听所有
# 如果队列的binding key使用"#",则这个队列会接收所有的消息,会忽略routing key,就像fanout交换器
# 如果以字符*开始,且没有使用#绑定队列,则这个交换器行为与direct类似
# 注意,该keys 支持控制台直接参数传入,优先级最高
binding_keys = ["remote.call"]

# 设置当前程序的主目录
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

# 设置日志记录的日志位置
log_dir = os.path.join(BASE_DIR, "logs")


# 设置用户验证信息位置,这里采用shelve数据,所以数据文件名的后缀.db省略不写
database = os.path.join(BASE_DIR, "settings/database")


# 设置输出日志到控制台,如果不想在控制台打印日志,设置为False,开启日志为True
output_console = True

# 设置日志记录的文件名,如果不记录日志,设置为None,或者False
log_file = "{}/rabbitmq.log".format(log_dir)

# 设置编码格式
encoding = "utf8"

# 定义全局日志级别
log_level = logging.DEBUG

# 定义控制台输出级别
# CONSOLE_LOG_LEVEL = logging.DEBUG
console_log_level = logging.DEBUG

# 定义记录到文本日志级别
file_log_level = logging.INFO

# 设置日志记录格式
formatter = logging.Formatter("%(asctime)s  -  %(name)s   -  %(levelname)s  - %(message)s")






