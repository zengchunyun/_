#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import threading
import socket
import selectors
import socketserver
socketserver.TCPServer
Selector = selectors.SelectSelector


class MyServer(object):
    request_queue_size = 5  # 请求连接数
    allow_reuse_address = False  # 是否允许地址复用
    daemon_thread = False  # 是否设置为后台线程
    all_user_list = []

    def __init__(self, server_address):
        """
        :param server_address: 服务器IP,端口
        :return:
        """
        self.server_address = server_address  # 设置服务器IP和端口
        self.__shutdown = threading.Event()  # 线程事件
        self.__shutdown_request = False  # 设置事件为阻塞状态
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_bind()
            self.socket.listen(self.request_queue_size)
        except OSError:
            self.socket.close()

    def server_bind(self):
        """绑定监听地址
        :return:
        """
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 设置地址复用
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def server_start(self, interval=0.4):
        """
        :param interval: 设置select的阻塞间隔时间,
        :return:
        """
        self.__shutdown.clear()  # 将事件机制设置为False阻塞状态
        try:
            with Selector() as selector:
                selector.register(self, selectors.EVENT_READ)
                while not self.__shutdown_request:
                    ready = selector.select(interval)
                    if ready:
                        self.handle_request()
        finally:
            self.__shutdown_request = False
            self.__shutdown.set()  # 将线程事件设置为不阻塞

    def handle_request(self):
        """如果有新连接请求,则调用socket的accept()方法处理连接
        :return:
        """
        try:
            request, client_address = self.socket.accept()
            self.all_user_list.append(request)
        except OSError:
            return
        try:
            self.process_request(request, client_address)
        except OSError:
            self.shutdown_request(request)

    def process_request_thread(self, request, client_address):
        """
        :param request: 已建立请求连接的socket
        :param client_address: 客户端的IP端口信息
        :return:
        """
        try:
            self.handle(request, client_address)
            self.shutdown_request(request)
        except OSError:
            self.shutdown_request(request)

    def process_request(self, request, client_address):
        """启用线程功能,对每一个新请求启用一个线程
        :param request:
        :param client_address:
        :return:
        """
        thread = threading.Thread(target=self.process_request_thread, args=(request, client_address))
        thread.daemon = self.daemon_thread
        thread.start()

    def shutdown_request(self, request):
        """关闭连接请求
        :param request:
        :return:
        """
        try:
            request.shutdown(socket.SHUT_WR)
            request.close()
        except OSError:
            pass
        request.close()

    def fileno(self):
        return self.socket.fileno()  # selector会获取该套接字文件描述符

    def handle(self, request, client_address):
        """当有新请求过来,会通过该方法进行处理请求连接
        :param request:
        :param client_address:
        :return:
        """
        rbufsize = -1
        wbufsize = 0
        rfile = request.makefile("rb", rbufsize)
        wfile = request.makefile("wb", wbufsize)
        try:
            self.define_handle(request, client_address)
        finally:
            if not wfile.closed:
                try:
                    wfile.flush()
                except socket.error:
                    wfile.close()
                    rfile.close()

    def define_handle(self, request, client_address):
        """自定义事件处理,通过继承,可以覆盖该类方法,进行自定义操作
        :return:
        """
        pass
