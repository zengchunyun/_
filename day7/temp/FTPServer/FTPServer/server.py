#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socket
import select
import queue
import logging
import sys
import subprocess


class FTPServer(object):
    allow_reuse_address = True  # 允许地址复用
    request_queue_size = 5  # 允许最大连接数
    output_console = True  # 输出到屏幕
    logLevel = logging.DEBUG  # 日志输出级别
    logfile = None  # 日志文件名称
    encoding = "utf8"  # 编码格式
    timeout = 20000  # 超时时间,单位毫秒
    buffer = 1024
    formatter = logging.Formatter("%(asctime)s  -  %(name)s   -  %(levelname)s  - %(message)s")  # 日志记录格式

    def __init__(self, server_address):
        """初始化日志,socket实例化
        :param server_address:
        :return:
        """
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
        """
        绑定服务器IP地址端口
        :return:
        """
        self.socket.setblocking(self.__setblock)  # 设置为不阻塞
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        self.socket.listen(self.request_queue_size)
        self.logger.debug("服务器socket[%s]" % self.socket)
        self.logger.debug("服务器socket描述符[%s]" % self.socket.fileno())
        self.server_address = self.socket.getsockname()
        self.logger.info("服务器启动成功,监听IP[{}] 端口:[{}]".format(*self.server_address))

    def server_start(self):
        """
        启动服务器
        :return:
        """
        self.poll.register(self.fileno(), self.rlist)  # 注册本机监听socket到等待可读事件事件集合
        self.fd_socket = {self.socket.fileno(): self.socket}  # 将文件描述符与对应的socket放入字典
        while not self.__setblock:
            self.logger.info("等待活动连接 ...")
            events = self.poll_event()  # 监听事件消息
            if not events:
                self.logger.info("轮询超时，无活动连接，重新轮询......")
                continue
            self.logger.info("有{}个新事件，开始处理......".format(len(events)))
            self.handle_request(events)

    def poll_event(self):
        """
        轮询已注册的事件集合
        :return:
        """
        return self.poll.poll(self.timeout)

    def respone_client(self, request, data):
        """
        响应客户端请求
        :param request: 客户端与服务器建立的socket
        :param data: 客户端发过来的请求数据
        :return:
        """
        self.logger.info("收到数据：{} 客户端：[{}]端口: [{}]".format(data, *request.getpeername()))
        self.message_queue[request].put(data)
        self.poll.modify(request, self.wlist)  # 修改读取到消息的连接到等待写事件集合

    def get_request(self, request):
        """
        获取用户发过来的请求数据
        :param request: 客户端与服务端建立的socket
        :return:
        """
        self.logger.debug("服务端收到socket[%s]请求" % request)
        data = self.recvall(request)  # 接收客户端发送的数据
        if data:
            self.respone_client(request, data)  # 响应客户端,将客户端请求放入队列
            self.handle(request)
        else:
            self.shutdown_request(request, "关闭 客户端: [{}]端口: [{}] (HUP)")

    def handle_request(self, events):
        """
        处理已注册的事件
        :param events: 已注册的事件请求
        :return:
        """
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
                self.get_request(sock)

    def recvall(self, request):
        return request.recv(self.buffer)

    def shutdown_request(self, request, message):
        """
        关闭客户端连接请求
        :param request: 已建立的socket
        :param message: 记录日志消息
        :return:
        """
        self.logger.info(message.format(*request.getpeername()))
        self.poll.unregister(request)
        request.close()  # 停止监听该客户端
        del self.message_queue[request]

    def set_log(self):
        """
        设置日志输出
        :return:
        """
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
        """
        :return: 生存套接字描述符,为轮询事件调用
        """
        return self.socket.fileno()

    def handle(self, request):
        """
        自定义方法,通过继承方式可以覆盖该方法,默认已将客户请求添加到消息队列,通过request即可获得对应的消息请求
        :param request: 已建立的socket
        :return:
        """
        command = self.message_queue[request].get()
        request.send(command)


class FTPController(FTPServer):
    """
    继承FTPServer
    重构handle方法,自定义一些操作
    """
    def __init__(self, server_address, anonymous=False):
        super(FTPController, self).__init__(server_address)
        self.anonymous = anonymous
        self.has_login = False

    def handle(self, request):
        self.logger.info("处理客户端：[{}]端口: [{}]请求".format(*request.getpeername()))
        command = self.message_queue[request].get()  # 通过消息队列,获取用户请求
        print(command)
        command = self.message_queue[request].get()  # 通过消息队列,获取用户请求
        print(command)
        command = str(command, "utf-8")
        if len(command.split()) > 1:
            attr = command.split()[0]
        else:
            attr = command

        if hasattr(self, attr):  # 如果用户请求合理,则返回用户请求
            attr = getattr(self, attr)
            attr(request, command)
        else:  # 否则响应客户请求失败
            self.send_data(request, bytes("request error", "utf8"))

    def dir(self, request, cmd):
        if sys.platform.startswith("win32"):
            stdout = subprocess.Popen("dir", shell=True, stdout=subprocess.PIPE)
            self.sendall(request, stdout.stdout.read())
        else:
            cmd = str(cmd).replace("dir", "ls")
            self.ls(request, cmd)

    def ls(self, request, cmd):
        if sys.platform.startswith("win32"):
            self.dir(request, cmd)
        else:
            stdout = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = stdout.stderr.read()
            if not result:
                result = stdout.stdout.read()
            self.sendall(request, result)

    def send_data(self, request, data):
        return request.send(data)

    def recv_data(self, request):
        self.logger.debug("服务端开始接收数据来自socket[%s]" % request)
        return request.recv(self.buffer)

    def sendall(self, request, data):
        while True:
            respone_message = bytes("CMD_RESULT_SIZE|%s" % len(data), "utf8")
            self.send_data(request, respone_message)
            self.poll_event()
            client_ack = self.recv_data(request)
            if client_ack.decode() == 'CLIENT_READY_TO_RECV':
                total_size = len(data)
                while total_size > 0:
                    total_size -= self.send_data(request, data)
                break

    def recvall(self, request):
        self.logger.debug("服务端接收socket[%s]\n所有信息" % request)
        while True:
            client_respone_message = self.recv_data(request)
            self.logger.debug("服务端收到socket[{}]响应信息[{}]".format(request, client_respone_message))
            request_message = str(client_respone_message.decode()).split("|")
            print("server response:", request_message)
            if request_message[0] == "CMD_RESULT_SIZE":
                cmd_res_size = int(request_message[1])
                request.send(b"CLIENT_READY_TO_RECV")
                self.logger.debug("服务器回应客户端socket[%s]" % request)
                data = b''
                received_size = 0
                self.logger.debug("服务端准备接收socket[%s]消息" % request)
                while received_size < cmd_res_size:
                    data += self.recv_data(request)
                    self.logger.debug("服务端收到socket[%s]\n消息大小为[%s]" % (request, received_size))
                    received_size = len(data)
                self.logger.debug("服务器接收消息完成socket[%s]" % request)
                return data
            break

if __name__ == "__main__":
    try:
        server = ("0.0.0.0", 9999)
        ftp = FTPController(server)
        ftp.server_start()
    except KeyboardInterrupt:
        ftp.logger.critical("服务器退出")
