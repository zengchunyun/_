#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database,提供数据连接方式

DATABASES = {
    'default': {
        'ENGINE': 'mysql',
        'NAME': 'day11',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123',
    }
}

# 命令行参数,只有这里注册的参数,命令行才能使用
subcommands = {
    1: 'create_users',  # 创建主机用户
    2: 'create_groups',  # 创建堡垒机组
    3: 'create_hosts',  # 创建主机
    4: 'bind_host_user',  # 主机绑定到对应的登录系统用户
    5: 'bind_user_group',  # 绑定堡垒机用户到组
    6: 'makemigrations',  # 初始化数据库
    7: 'create_fort_user',  # 创建堡垒机认证用户
    8: 'bind_host_group',  # 将组与主机关联
    9: 'runserver',  # 启动服务
}
