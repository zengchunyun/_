#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

import getpass
import paramiko
import os

user = input('username:')
pwd = getpass.getpass('password')
if user == 'alex' and pwd == '123':
    print('登陆成功')
else:
    print('登陆失败')

dic = {
    'alex': [
        '127.0.0.1',
        'c10.puppet.com',
        'c11.puppet.com',
    ],
    'eric': [
        'c100.puppet.com',
    ]
}

host_list = dic['alex']

print('please select:')
for index, item in enumerate(host_list, 1):
    print(index, item)

inp = input('your select (No):')
inp = int(inp)
hostname = host_list[inp-1]
port = 22

tran = paramiko.Transport((hostname, port,))
tran.start_client()
# default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
# key = paramiko.RSAKey.from_private_key_file(default_path)
# tran.auth_publickey('zengchunyun', " ")
tran.connect(username="zengchunyun", password=" ")
# 打开一个通道
chan = tran.open_session()
# 获取一个终端
chan.get_pty()
# 激活器
chan.invoke_shell()

#########
# 利用sys.stdin,肆意妄为执行操作
# 用户在终端输入内容，并将内容发送至远程服务器
# 远程服务器执行命令，并将结果返回
# 用户终端显示内容
#########

chan.close()
tran.close()