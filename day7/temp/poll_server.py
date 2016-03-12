#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
Python Poll Server，Select升级版，无可监控事件数量限制，还是要轮询所有事件：
"""
import socket
import select
import queue
Queue=queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ("0.0.0.0", 9999)
server.bind(server_address)
server.listen(5)
print ("服务器启动成功，监听IP：" , server_address)
message_queues = {}
#超时，毫秒
timeout = 5000
#监听哪些事件
READ_ONLY = ( select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR)
READ_WRITE = (READ_ONLY|select.POLLOUT)
#新建轮询事件对象
poller = select.poll()
#注册本机监听socket到等待可读事件事件集合
poller.register(server,READ_ONLY)
#文件描述符到socket映射
fd_to_socket = {server.fileno():server,}
print(fd_to_socket)
print(server)
while True:
    print ("等待活动连接......")
    #轮询注册的事件集合
    events = poller.poll(timeout)
    print(events)
    if not events:
      print ("poll超时，无活动连接，重新poll......")
      continue
    print ("有" , len(events), "个新事件，开始处理......")
    for fd ,flag in events:
        print(fd)
        s = fd_to_socket[fd]
        #可读事件
        if flag & (select.POLLIN | select.POLLPRI) :
            if s is server :
                #如果socket是监听的server代表有新连接
                connection , client_address = s.accept()
                print ("新连接：" , client_address)
                connection.setblocking(False)
                print(connection.fileno())
                print(connection)

                fd_to_socket[connection.fileno()] = connection
                #加入到等待读事件集合
                poller.register(connection,READ_ONLY)
                print(READ_ONLY)
                message_queues[connection] = Queue.Queue()
                print(message_queues)
            else :
                #接收客户端发送的数据
                data = s.recv(1024)
                if data:
                    print ("收到数据：" , data , "客户端：" , s.getpeername())
                    message_queues[s].put(data)
                    #修改读取到消息的连接到等待写事件集合
                    poller.modify(s,READ_WRITE)
                else :
                    # Close the connection
                    print (" closing" , s.getpeername())
                    # Stop listening for input on the connection
                    poller.unregister(s)
                    s.close()
                    del message_queues[s]
        #连接关闭事件
        elif flag & select.POLLHUP :
            print (" Closing ", s.getpeername() ,"(HUP)")
            poller.unregister(s)
            s.close()
        #可写事件
        elif flag & select.POLLOUT :
            try:
                msg = message_queues[s].get_nowait()
            except Queue.Empty:
                print (s.getpeername() , " queue empty")
                poller.modify(s,READ_ONLY)
            else :
                print ("发送数据：" , data , "客户端：" , s.getpeername())
                s.send(msg)
        #异常事件
        elif flag & select.POLLERR:
            print (" exception on" , s.getpeername())
            poller.unregister(s)
            s.close()
            del message_queues[s]