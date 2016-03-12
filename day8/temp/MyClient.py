#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socket
import time

server_address = ("127.0.0.1", 8080)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_address)

while True:
    data = bytes(input(">> "), "utf8")
    # data = b"3333333333333333333"
    client.send(data)
    time.sleep(0.3)
    recvied = client.recv(14)
    if recvied:
        print("Server reply {}".format(recvied.decode()))
    else:
        break
client.close()