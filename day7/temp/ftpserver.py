#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socketserver


class MyFTPServer(socketserver.StreamRequestHandler):
    def handle(self):
        pass

    def send_data(self, request, data):
        request.send(bytes(data, "utf8"))

    def recv_data(self, request, buffer=1024):
        data = request.recv(buffer)
        return str(data, "utf8")

    def exec_shell(self, cmd):
        import subprocess
        exec_result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        return exec_result.stdout.read()

    def get_length(self, strings):
        return len(strings)


def run_server(server_address, handleclass):
    try:
        ftp_server = socketserver.ThreadingTCPServer(server_address, handleclass)
        ftp_server.allow_reuse_address = True
        ftp_server.request_queue_size = 10
        ftp_server.serve_forever(1)
    except OSError:
        print(OSError)


if __name__ == "__main__":
    server_bind_address = ("0.0.0.0", 21)
    run_server(server_bind_address, MyFTPServer)


import socket
socket.CMSG_LEN()

class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)


f = open("myfile")
f.read()