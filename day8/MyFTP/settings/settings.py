#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import os
import logging


# 监听客户端地址,默认监听所有客户端
LISTEN = "0.0.0.0"

# 监听端口
PORT = 8500

# 匿名方式认证,启用为True,不启用为False
ENABLE_ANONYMOUS = False

# 设置当前程序的主目录
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

# 设置日志记录的日志位置
LOG_DIR = os.path.join(BASE_DIR, "logs")

# 设置用户数据存放位置
USER_DATA = os.path.join(BASE_DIR, "userdata")

# 设置每个用户的基本属性,可以定义磁盘配额大小,必须以用户名命名的配置文件,这里的配置优先
# 该功能目前尚未实现,只能通过下面的database控制用户大小,或使用全局配额控制配额
USER_CONF = os.path.join(BASE_DIR, "settings/conf")

#  为所有用户配置磁盘配额,匿名用户不生效,单位字节
QUTOTA_SIZE = 1000000

# 设置公共服务目录,一般只对匿名用户有效
PUBLIC_DATA = os.path.join(USER_DATA, "pub")

# 设置用户验证信息位置,这里采用shelve数据,所以数据文件名的后缀.db省略不写
database = os.path.join(BASE_DIR, "settings/database")

# 每次接收客户端数据大小,该值请勿随意修改,如果真的确定要修改,需要将客户端的buffer值改成与服务端一样,否则会出现粘包问题
RECV_BUFFER = 8000

# 设置输出日志到控制台,如果不想在控制台打印日志,设置为False,开启日志为True
OUTPUT_CONSOLE = True

# 设置日志记录的文件名,如果不记录日志,设置为None,或者False
LOG_FILE = None

# 设置编码格式
ENCODING = "utf8"

# 定义全局日志级别
LOG_LEVEL = logging.DEBUG

# 定义控制台输出级别
# CONSOLE_LOG_LEVEL = logging.DEBUG
CONSOLE_LOG_LEVEL = logging.INFO

# 定义记录到文本日志级别
FILE_LOG_LEVEL = logging.INFO

# 设置日志记录格式
FORMATTER = logging.Formatter("%(asctime)s  -  %(name)s   -  %(levelname)s  - %(message)s")






