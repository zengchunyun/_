#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socket
import threading


def client(n):
    HOST = 'localhost'    # The remote host
    PORT = 8001           # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    # while True:
    # msg = bytes(input(">>:"),encoding="utf8")
    msg = bytes("hello{}".format(n), encoding="utf8")
    s.sendall(msg)
    data = s.recv(1024)
    #print(data)

    print('Received', repr(data))
    s.close()


t_list = []
for i in range(10000):
    t = threading.Thread(target=client, args=(i,))
    t.start()
    t_list.append(t)
for t in t_list:
    # t.start()
    t.join()