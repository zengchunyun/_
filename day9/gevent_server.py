#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
# from gevent import monkey; monkey.patch_all()
# import gevent
# from  urllib.request import urlopen
#
# def f(url):
#     print('GET: %s' % url)
#     resp = urlopen(url)
#     data = resp.read()
#     print('%d bytes received from %s.' % (len(data), url))
#
# gevent.joinall([
#         gevent.spawn(f, 'https://www.python.org/'),
#         gevent.spawn(f, 'https://www.yahoo.com/'),
#         gevent.spawn(f, 'https://github.com/'),
# ])



import sys
import socket
import time
import gevent

from gevent import socket,monkey
monkey.patch_all()
def server(port):
    s = socket.socket()
    s.bind(('0.0.0.0', port))
    s.listen(500)
    while True:
        cli, addr = s.accept()
        gevent.spawn(handle_request, cli)
def handle_request(s):
    try:
        while True:
            data = s.recv(1024)
            print("recv:", data)
            s.send(data)
            if not data:
                s.shutdown(socket.SHUT_WR)

    except Exception as  ex:
        print(ex)
    finally:

        s.close()
if __name__ == '__main__':
    server(8001)