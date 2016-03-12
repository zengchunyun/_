#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

import socket

server_address = ("127.0.0.1", 9999)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)

while True:
    send_data = bytes(input("请输入请求:"), "utf8")
    send_size = client.send(send_data)
    print("发送数据[{}]发送大小[{}]".format(send_data.decode(), send_size))
    data = client.recv(1000)
    if len(data):
        print("收到数据[{}]".format(data.decode()))
    else:
        continue
client.close()
