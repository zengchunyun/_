#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))
server.listen(5)


while True:
    print("waiting connection ...")
    request, client_address = server.accept()
    received = request.recv(1024)
    print("received :%s" % str(received, "utf8"))
    request.send(bytes("don't say english", "utf8"))
    while True:
        try:
            received = request.recv(1024)
            if not received:
                break
            print("received :%s" % str(received, "utf8"))
            request.send(bytes("don't say english", "utf8"))
        except ConnectionResetError:
            break
    request.close()

server.close()