#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

client.send(bytes("hello", "utf8"))


while True:
    received = client.recv(1024)
    while True:
        user_input = str(input(">>: "))
        if not user_input:
            continue
        else:
            break
    client.send(bytes(user_input, "utf8"))
    print("received: %s" % str(received, "utf8"))
client.close()