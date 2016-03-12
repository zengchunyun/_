#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

import socket
server_address = ("0.0.0.0", 9999)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(server_address)

server.listen(5)

while True:
    request, client_address = server.accept()
    print(request, client_address)
    while True:
        data = request.recv(1000)
        if len(data) > 0:
            print("收到数据[{}]".format(data.decode()))
        else:
            continue
        send_data = bytes(input("请应答:"), "utf8")
        send_size = request.send(send_data)
        print("发送数据[{}]发送大小[{}]".format(send_data.decode(), send_size))
    request.close()
server.close()
