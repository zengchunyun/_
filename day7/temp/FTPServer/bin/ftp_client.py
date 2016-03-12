#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socket
import select
import queue
import logging
import time


class MyFTPClient(object):
    buffer = 100
    output_console = True  # 输出到屏幕
    logLevel = logging.DEBUG  # 日志输出级别
    logfile = None  # 日志文件名称
    encoding = "utf8"  # 编码格式
    timeout = 500  # 超时时间,单位毫秒
    formatter = logging.Formatter("%(asctime)s  -  %(name)s   -  %(levelname)s  - %(message)s")  # 日志记录格式

    def __init__(self, server_address):
        self.server_address = server_address  # 定义服务器IP和端口
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP连接socket
        self.message_queue = {}  # 创建消息队列
        self.rlist = (select.POLLIN or select.POLLHUP or select.POLLPRI or select.POLLERR)  # 可读事件
        self.wlist = (self.rlist or select.POLLOUT)  # 可写事件
        self.fd_socket = {}  # 将文件描述符与对应的socket放入字典
        self.poll = select.poll()  # 新建轮询事件对象
        self.logger = logging.getLogger(__name__)  # 创建日志对象
        if self.output_console:
            self.console_handler = logging.StreamHandler()  # 创建控制台日志输出对象
        if self.logfile:  # 当设置了文件名,则日志记录到文件
            self.file_handler = logging.FileHandler(filename=self.logfile, encoding=self.encoding)  # 创建日志文件对象
        self.set_log()  # 设置日志
        self.connect_server()
        self.is_send = None  # 如果请求发送成功,则结果为None,否则就请求赋值给改字段

    def connect_server(self):
        try:
            # self.socket.settimeout(5)
            self.socket.connect(self.server_address)
            self.logger.debug("客户端socket[%s]" % self.socket)
            self.poll.register(self.socket.fileno(), self.rlist)  # 注册本机监听socket到等待可读事件事件集合
            self.logger.debug("客户端注册文件描述符[%s]" % self.socket.fileno())
            self.fd_socket = {self.socket.fileno(): self.socket}  # 将与服务器建立连接的套接字及文件描述符放入字典
        except OSError:
            self.logger.info("连接服务器异常,重新建立socket")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP连接socket
            self.logger.debug("客户端socket[%s]" % self.socket)

    def client_start(self):
        while True:
            self.logger.info("等待连接服务器 ...")
            events = self.poll.poll(self.timeout)
            self.logger.debug("事件描述符[{}]".format(events))
            if not events:
                self.logger.info("当前客户端空闲 ...")
                self.logger.debug("准备向服务器发送请求socket[%s]" % self.socket)
                self.socket.setblocking(True)
                self.send_data()
                self.socket.setblocking(False)
            else:
                self.logger.info("有{}个新事件，开始处理......".format(len(events)))
                self.handle_request(events)

    def handle_request(self, events):
        for fd, flag in events:
            if self.fd_socket.get(fd):
                sock = self.fd_socket[fd]  # 获取文件描述符对应的socket
                if sock == self.socket:  # 获取的socket等于server端的socket,说明有新的连接请求
                    self.logger.info("已连接：服务器: [{}]端口: [{}]".format(*sock.getpeername()))
                    self.fd_socket[sock.fileno()] = sock  # 将新的socket请求加入到字典
                    self.poll.register(sock, self.rlist)  # 加入到等待读事件集合
                    self.message_queue[sock] = queue.Queue()
                    self.recvall(sock)
            else:
                self.recvall(self.socket)
                self.shutdown_request(sock, "关闭 服务器: [{}]端口: [{}] (HUP)连接")

    def sendall(self, request, data):
        while True:
            respone_message = bytes("CMD_RESULT_SIZE|%s" % len(data), "utf8")
            self.logger.debug("客户端socket[%s]\n发送请求消息[%s]" % (request, respone_message))
            request.send(respone_message)
            # events = self.poll.poll(self.timeout)
            # self.logger.debug("获取[{}]事件".format(events))
            client_ack = self.recv_data(request)
            self.logger.debug("客户端socket[%s]确认消息" % request)
            if client_ack.decode() == 'CLIENT_READY_TO_RECV':
                total_size = len(data)
                self.logger.debug("客户端socket[%s]\n开始发送消息,大小[%s]" % (request, total_size))
                time.sleep(2)
                while total_size > 0:
                    total_size -= request.send(data)
                self.logger.debug("客户端发送消息完成socket[%s]" % request)
                time.sleep(3)
                break

    def recvall(self, request):
        while True:
            server_respone_message = self.recv_data(request)
            request_message = str(server_respone_message.decode()).split("|")
            print("server response:", request_message)
            if request_message[0] == "CMD_RESULT_SIZE":
                cmd_res_size = int(request_message[1])
                self.poll.poll(self.timeout)
                request.send(b"CLIENT_READY_TO_RECV")
                data = b''
                received_size = 0
                while received_size < cmd_res_size:
                    data += self.recv_data(request)
                    received_size = len(data)
                self.logger.debug("收到数据：{} 服务器：[{}]端口: [{}]".format(data, *request.getpeername()))
                self.message_queue[request].put(data)
                self.poll.modify(request, self.wlist)  # 修改读取到消息的连接到等待写事件集合
                print(str(self.message_queue[request].get(), "utf-8"))
            break

    def send_data(self):
        while True:
            if not self.is_send:
                get_command = str(input("ftp > "))
                self.is_send = get_command
            else:
                get_command = self.is_send
            if get_command:
                self.logger.debug("客户端socket[%s]\n准备向服务器发送请求" % self.socket)
                self.sendall(self.socket, bytes(get_command, "utf8"))
                self.logger.debug("客户端socket[%s]\n请求发送完成" % self.socket)
                self.is_send = None
                break

    def recv_data(self, request):
        self.logger.debug("客户端socket[%s]\n接收到新消息" % self.socket)
        return request.recv(self.buffer)

    def shutdown_request(self, request, message):
        self.logger.info(message.format(*request.getpeername()))
        self.poll.unregister(request)
        request.close()  # 停止监听该客户
        del self.message_queue[request]

    def set_log(self):
        self.logger.setLevel(self.logLevel)  # 设置日志记录级别
        if self.output_console:  # 当设置了输出屏幕日志,则启用该日志打印屏幕功能,默认开启
            self.console_handler.setLevel(self.logLevel)
            self.console_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.console_handler)
        if self.logfile:  # 当设置了文件名,则启用记录日志文件功能,默认关闭
            self.file_handler.setLevel(self.logLevel)
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)


if __name__ == "__main__":
    try:
        server_listen_address = ("127.0.0.1", 9999)
        # MyFTPClient.output_console = False
        connect_ftp = MyFTPClient(server_listen_address)
        connect_ftp.client_start()
    except KeyboardInterrupt:
        connect_ftp.logger.critical("客户端退出 ...")
