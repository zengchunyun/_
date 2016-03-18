#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socket
import select
import queue
import sys
import time


class MyServer(object):
    def __init__(self, server_address):
        """
        初始化服务器配置
        :param server_address:
        :return:
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP socket
        self.socket.setblocking(False)  # 设置非阻塞
        self.server_address = server_address  # 设置服务器IP端口

        self.readlist = []  # 生成可读列表,当有可接收消息时,说明有可连接请求发送消息到此服务器
        self.writelist = []  # 生成可写列表,当该队列含有对象时,说明可以向该对象发送消息,
        self.message_queue = {}  # 生成消息队列字典,以socket:queue.Queue形式存储接收的请求信息
        self.recv_buffer = 1024  # 设置接收的缓冲区大小
        self.bind()  # 服务器绑定IP端口

    def bind(self):
        """
        绑定服务器IP端口,最大监听5个队列
        :return:
        """
        self.socket.bind(self.server_address)
        sys.stdout.write("starting up on {} port {}\n".format(*self.server_address))
        sys.stdout.flush()
        self.socket.listen(5)
        self.readlist.append(self.socket)  # 将服务器socket实例添加到可读事件列表

    def serve_forever(self, interval=0.5):
        """
        开始轮询事件
        :param interval: 轮询超时时间,单位s
        :return:
        """
        while self.readlist:  # 由于绑定服务器端口时已加入元素,所以该条件成立
            try:
                #  每次都轮询下面事件列表,当有事件触发时,则继续执行,否则一直阻塞,如果设置了超时时间,则超时后,继续执行
                readlist, writelist, exceptionlist = select.select(self.readlist, self.writelist, self.readlist, interval)
            except ValueError:  # 出现该错误 filedescriptor out of range in select(),说明文件句柄已耗尽
                time.sleep(10)
                continue
            if not (readlist, writelist, exceptionlist):  # 如果没有事件被触发,三个列表都是空的
                continue  # 当三个事件列表都没有被触发都为空,则不继续往下执行
            for sock in readlist:  # 轮询可读列表,开始接收客户端发来对消息
                if sock is self.socket:
                    request, client_address = sock.accept()  # 当服务器本身实例可读时,说明有新连接请求接入
                    sys.stdout.write("new connection from {} port {}\n".format(*client_address))
                    sys.stdout.flush()
                    request.setblocking(False)  # 设置非阻塞模式
                    self.readlist.append(request)  # 将新的socket连接请求实例加入到可读列表,下次该客户端发送消息时,由select轮询处理
                    self.message_queue[request] = queue.Queue()  # 以socket实例命名生成一个队列实例,存储该客户端发来的消息
                else:  # 只有之前建立过连接的客户端才不会触发服务器自身的socket对象,即该对象不是服务器自身socket对象,而是新连接生成对的对象
                    data = sock.recv(self.recv_buffer)  # 如果可读事件不等于服务器本身socket实例,则说明有客户端发送消息过来了
                    if data:  # 如果接收到新消息,则说明客户端发送消息过来了
                        sys.stdout.write("received [{}] from {} port {}\n".format(data, *sock.getpeername()))
                        sys.stdout.flush()
                        self.message_queue[sock].put(data)  # 将客户端发来的消息放入它对应的队列里
                        if sock not in self.writelist:  # 并且,如果它没有被放进可写列表,则先添加到该列表,然后接下来统一处理该列表
                            self.writelist.append(sock)  # 当收到该客户端消息,不进行立即回复,先加入到可写事件列表
                    else:  # 如果没有消息,说明客户端断开连接了
                        sys.stdout.write("closing client {} port {}\n".format(*sock.getpeername()))  # 由于收到空消息,说明客户端已断开
                        sys.stdout.flush()
                        if sock in self.writelist:  # 由于客户端断开连接,则需要清除该socket实例,避免发送异常
                            self.writelist.remove(sock)  # 将该客户端从可写列表移除,避免回复客户端时由于断开了,造成阻塞
                        self.readlist.remove(sock)  # 从可读事件列表移除不存在的客户端
                        sock.close()  # 关闭该连接
                        del self.message_queue[sock]  # 删除该客户端的消息队列

            for sock in writelist:  # 轮询可写列表,该列表仅存储还没有对客户端请求回复的对象
                try:
                    get_msg = self.message_queue[sock].get_nowait()  # 开始获取客户端发来的数据,由于数据队列可能为空,避免阻塞使用nowait()方法
                except queue.Empty:  # 如果队列为空,可能会触发队列空异常,需要处理该异常,避免影响其他客户端连接
                    sys.stdout.write("queue is empty\n")
                    sys.stdout.flush()
                    self.writelist.remove(sock)  # 将该客户端从可写事件移除,即不需要对该客户端发送消息了
                except KeyError:  # 并发时,可能出现此问题
                    pass
                else:  # 表示没有异常,则说明获取到队列消息了
                    sys.stdout.write("beginning send message to client {} port {}\n".format(*sock.getpeername()))
                    sys.stdout.flush()
                    sock.send(get_msg)  # 直接将用户发来的消息返回给客户端

            for sock in exceptionlist:  # 轮询异常事件列表
                sys.stdout.write("handling exception condition from {} port {}\n".format(*sock.getpeername()))
                sys.stdout.flush()
                self.readlist.remove(sock)  # 移除异常列表对象
                if sock in self.writelist:  # 由于客户端异常,所以如果还未对客户端回复消息,则不需要再进行回复了,直接移除该客户端
                    self.writelist.remove(sock)
                sock.close()  # 关闭该客户端连接
                del self.message_queue[sock]  # 删除该客户端的消息队列


if __name__ == "__main__":
    server = ("0.0.0.0", 9999)
    servermq = MyServer(server)
    servermq.serve_forever()
