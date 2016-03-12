#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socket
import select
import queue
import logging
import os
import sys


class MyFTPClient(object):
    buffer = 1000
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
        self.local_file = None
        self.remote_file = None

    def connect_server(self):
        """
        连接服务器
        :return:
        """
        try:
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
        """
        启动客户端
        :return:
        """
        while True:
            self.logger.info("等待连接服务器 ...")
            events = self.poll.poll(self.timeout)
            self.logger.debug("事件描述符[{}]".format(events))
            if not events:
                self.logger.info("当前客户端空闲 ...")
                self.logger.debug("准备向服务器发送请求socket[%s]" % self.socket)
                self.send_data()
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
                    data = self.recvall(sock)
                    if self.local_file:
                        self.writefile(self.local_file, data)
                    else:
                        self.message_queue[sock].put(data)
                        self.poll.modify(sock, self.wlist)  # 修改读取到消息的连接到等待写事件集合
                        try:
                            print(str(self.message_queue[sock].get(), "utf-8"))
                        except:
                            break
            else:
                self.shutdown_request(sock, "关闭 服务器: [{}]端口: [{}] (HUP)连接")

    def parse_command(self, data):
        if type(data) == bytes:
            data = str(data, "utf-8")
        if len(str(data).split()) > 1:
            remote_file = str(data).split(maxsplit=1)[1].strip("'")
            local_file = remote_file
            if len(str(remote_file).split()) > 1:
                remote_file, local_file = str(remote_file).split()
            if str(data).split()[0] == "put":
                remote_file, local_file = local_file, remote_file
                return local_file, remote_file
            elif str(data).split()[0] == "get":
                return local_file, remote_file

    def sendall(self, request, data):
        local_remote = self.parse_command(data)
        if local_remote:
            self.local_file, self.remote_file = local_remote
            message = "DATA_SIZE|{}|LOCAL_REMOTE|{}|{}".format(len(data), *local_remote)
        else:
            self.local_file = None
            message = "DATA_SIZE|{}".format(len(data))

        while True:
            respone_message = bytes(message, "utf8")
            request.send(respone_message)
            self.logger.debug("客户端socket[%s]发送请求消息[%s]" % (request, respone_message))
            client_ack = self.recv_data(request)
            if client_ack.decode() == 'CLIENT_READY_TO_RECV':
                self.logger.debug("客户端socket[%s]得到确认消息[%s]" % (request, client_ack))
                total_size = len(data)
                self.logger.debug("客户端socket[%s]开始发送消息,大小[%s]" % (request, total_size))
                while total_size > 0:
                    total_size -= request.send(data)
                self.logger.debug("客户端发送消息完成socket[%s]" % request)
                break

    def recvall(self, request):
        while True:
            server_respone_message = self.recv_data(request)
            self.logger.debug("收到服务器[{}]请求消息[{}]".format(request, server_respone_message))
            request_message = str(server_respone_message.decode()).split("|")
            if len(request_message) > 3:
                self.remote_file = request_message[3]
                self.local_file = request_message[4]
            if request_message[0] == "DATA_SIZE":
                cmd_res_size = int(request_message[1])
                self.logger.debug("向服务端[{}]发送确认消息".format(request))
                request.send(b"CLIENT_READY_TO_RECV")
                data = b''
                received_size = 0
                while received_size < cmd_res_size:
                    data += self.recv_data(request)
                    received_size = len(data)
                    self.logger.debug("收到服务器[{}] 消息[{}]".format(request, data))
                return data
            break

    def send_data(self):
        while True:
            if not self.is_send:
                get_command = str(input("ftp > "))
                self.is_send = get_command
            else:
                get_command = self.is_send
            if get_command:
                if "put" in get_command:
                    self.put(get_command)
                    break
                self.logger.debug("客户端socket[%s]准备向服务器发送请求" % self.socket)
                self.sendall(self.socket, bytes(get_command, "utf8"))
                self.logger.debug("客户端socket[%s]请求发送完成" % self.socket)
                self.is_send = None
                break

    def readfile(self, filename):
        total_size = os.path.getsize(filename)
        if total_size % 100 == 0:
            buffer = int(total_size / 100)
        else:
            buffer = int(total_size / 99)
        percent = 0
        while total_size > 0:
            percent += 1
            hashes = "#" * int(percent / 100.0 * 50)
            spaces = " " * (50 - len(hashes))
            sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent, hashes + spaces))
            sys.stdout.flush()
            with open(filename, "rb") as readdata:
                has_read = readdata.read(buffer)
                if has_read:
                    seek = readdata.tell()
                    total_size -= buffer
                    yield has_read, seek
                else:
                    readdata.close()

    def writefile(self, filename, data, seek=0, mode="a+b"):
        percent = 0
        while percent <= 100:
            hashes = "#" * int(percent / 100.0 * 50)
            spaces = " " * (50 - len(hashes))
            sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent, hashes + spaces))
            sys.stdout.flush()
            percent += 1
        with open(filename, mode) as writedata:
            writedata.write(data)
            writedata.flush()

    def put(self, cmd):
        self.local_file = str(cmd).split()[1]
        if os.path.isfile(self.local_file):
            get_file = os.path.abspath(self.local_file)
            for data in self.readfile(get_file):
                self.sendall(self.socket, data[0])

    def recv_data(self, request):
        return request.recv(self.buffer)

    def shutdown_request(self, request, message):
        self.logger.info(message.format(*request.getpeername()))
        self.poll.unregister(request)
        request.close()  # 停止监听该socket
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
        MyFTPClient.output_console = False
        connect_ftp = MyFTPClient(server_listen_address)
        connect_ftp.client_start()
    except KeyboardInterrupt:
        connect_ftp.logger.critical("客户端退出 ...")
