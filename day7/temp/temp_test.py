#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
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
import subprocess
import re


class FTPServer(object):
    allow_reuse_address = True  # 允许地址复用
    request_queue_size = 5  # 允许最大连接数
    output_console = True  # 输出到屏幕
    logLevel = logging.DEBUG  # 日志输出级别
    logfile = None  # 日志文件名称
    encoding = "utf8"  # 编码格式
    timeout = 10000  # 超时时间,单位毫秒
    buffer = 1024
    formatter = logging.Formatter("%(asctime)s  -  %(name)s   -  %(levelname)s  - %(message)s")  # 日志记录格式

    def __init__(self, server_address):
        self.server_address = server_address  # 定义服务器IP和端口
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP连接socket
        self.__setblock = False  # 设置阻塞状态为不阻塞
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
        self.bind()  # 开始绑定IP和端口

    def bind(self):
        self.socket.setblocking(self.__setblock)  # 设置为不阻塞
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        self.socket.listen(self.request_queue_size)
        self.server_address = self.socket.getsockname()
        self.logger.info("服务器启动成功,监听IP[{}] 端口:[{}]".format(*self.server_address))

    def server_start(self):
        self.poll.register(self.fileno(), self.rlist)  # 注册本机监听socket到等待可读事件事件集合
        self.fd_socket = {self.socket.fileno(): self.socket}  # 将文件描述符与对应的socket放入字典
        while not self.__setblock:
            self.logger.info("等待活动连接 ...")
            events = self.poll.poll(self.timeout)  # 轮询注册的事件集合
            if not events:
                self.logger.info("轮询超时，无活动连接，重新轮询......")
                continue
            self.logger.info("有{}个新事件，开始处理......".format(len(events)))
            self.handle_request(events)

    def handle_request(self, events):
        for fd, flag in events:
            sock = self.fd_socket[fd]  # 获取文件描述符对应的socket
            if sock == self.socket:  # 获取的socket等于server端的socket,说明有新的连接请求
                request, client_address = self.socket.accept()
                self.logger.info("新连接：客户端: [{}]端口: [{}]".format(*client_address))
                request.setblocking(self.__setblock)
                self.fd_socket[request.fileno()] = request  # 将新的socket请求加入到字典
                self.poll.register(request, self.rlist)  # 加入到等待读事件集合
                self.message_queue[request] = queue.Queue()
            else:
                data = sock.recv(self.buffer)  # 接收客户端发送的数据
                if data:
                    self.logger.info("收到数据：{} 客户端：[{}]端口: [{}]".format(data, *sock.getpeername()))
                    self.message_queue[sock].put(data)
                    self.poll.modify(sock, self.wlist)  # 修改读取到消息的连接到等待写事件集合
                    cmd = self.message_queue[sock].get()
                    self.handle(sock, cmd)
                else:
                    self.shutdown_request(sock, "关闭 客户端: [{}]端口: [{}] (HUP)")

    def shutdown_request(self, request, message):
        self.logger.info(message.format(*request.getpeername()))
        self.poll.unregister(request)
        request.close()  # 停止监听该客户端
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

    def fileno(self):
        return self.socket.fileno()

    def handle(self, request, data):
        request.send(data)
        pass


class FTPController(FTPServer):
    def __init__(self, server_address, anonymous=False):
        super(FTPController, self).__init__(server_address)
        self.request = None
        self.anonymous = anonymous
        self.has_login = False

    def handle(self, request, command):
        self.request = request
        command = str(command, "utf-8")
        if len(command.split()) > 1:
            attr = command.split()[0]
        else:
            attr = command

        if hasattr(self, attr):
            attr = getattr(self, attr)
            attr(command)

    def bye(self):
        print("bye")

    def cd(self):
        pass

    def chmod(self):
        pass

    def close(self):
        pass

    def delete(self):
        pass

    def dir(self, cmd):
        if sys.platform.startswith("win32"):
            stdout = subprocess.Popen("dir", shell=True, stdout=subprocess.PIPE)
            self.request.send(stdout.stdout.read())
        else:
            cmd = str(cmd).replace("dir", "ls")
            self.ls(cmd)

    def disconnection(self):
        pass

    def get(self):
        pass

    def help(self):
        pass

    def lcd(self):
        pass

    def ls(self, cmd):
        if sys.platform.startswith("win32"):
            self.dir(cmd)
        else:
            stdout = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = stdout.stderr.read()
            if not result:
                result = stdout.stdout.read()
            while True:
                ack_msg = bytes("CMD_RESULT_SIZE|%s" % len(result), "utf8")
                self.request.send(ack_msg)
                client_ack = self.message_queue[self.request].get()
                # if client_ack.decode() == 'CLIENT_READY_TO_RECV':
                self.request.send(result)

    def mdelete(self):
        pass

    def mdir(self):
        pass

    def mget(self):
        pass

    def mkdir(self):
        pass

    def mput(self):
        pass

    def open(self):
        pass

    def put(self):
        pass

    def pwd(self):
        pass

    def quit(self):
        pass

    def rename(self):
        pass

    def rmdir(self):
        pass

    def user(self):
        pass

    def send_data(self, data):
        self.request.send(data)

    def recv_data(self):
        return self.request.recv(self.buffer)


if __name__ == "__main__":
    try:
        server = ("0.0.0.0", 9999)
        ftp = FTPController(server)
        ftp.server_start()
    except KeyboardInterrupt:
        ftp.logger.critical("服务器退出")
