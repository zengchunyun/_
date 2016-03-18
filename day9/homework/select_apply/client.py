#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

import socket
import sys
import threading


class MyClient(object):
    def __init__(self, server_address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.recv_buffer = 1024
        self.connect()

    def connect(self):
        self.socket.connect(self.server_address)
        sys.stdout.write("connecting to {} port {}\n".format(*self.socket.getpeername()))
        sys.stdout.flush()

    def client_forever(self, data=b""):
        while True:
            # data = bytes(input("请输入: "), "utf8")
            if type(data) is not bytes:
                data = bytes(str(data), "utf8")
            self.socket.send(data)
            received_data = self.socket.recv(self.recv_buffer)
            if received_data:
                sys.stdout.write("received {} from {} port {}\n".format(received_data, *self.socket.getpeername()))
                sys.stdout.flush()
                break
            else:
                sys.stdout.write("closing socket {} port {}\n".format(*self.socket.getpeername()))
                self.socket.close()


def run(data):
    server = ("127.0.0.1", 9999)
    clientmq = MyClient(server)
    clientmq.client_forever(data)


if __name__ == "__main__":
    for i in range(50000):
        t = threading.Thread(target=run, args=(i,))
        t.start()
        print("has been send {} times".format(i))
