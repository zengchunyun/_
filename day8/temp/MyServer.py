#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socketserver


class MyRequestHandle(socketserver.BaseRequestHandler):
    def handle(self):
        print("New Connection from[{}][{}]".format(*self.client_address))
        while True:
            data = self.request.recv(1024)
            print("data {}".format(data))
            if len(data) > 0:
                print("Client say {}".format(data.decode()))
            else:
                print("Cleint broken {}{}".format(*self.client_address))
                break
            self.request.send(data)
        self.request.close()


if __name__ == "__main__":
    server_address = ("0.0.0.0", 9999)
    server = socketserver.ThreadingTCPServer(server_address, MyRequestHandle)
    server.serve_forever()
