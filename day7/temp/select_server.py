#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import select
import socket
import queue
Queue=queue

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setblocking(False)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
server_address= ('0.0.0.0',8082)
server.bind(server_address)
server.listen(10)

#select轮询等待读socket集合
inputs = [server]
#select轮询等待写socket集合
outputs = []
message_queues = {}
#select超时时间
timeout = 20

while True:
    print ("等待活动连接......")
    readable , writable , exceptional = select.select(inputs, outputs, inputs, timeout)

    if not (readable or writable or exceptional) :
        print ("select超时无活动连接，重新select...... ")
        continue;
    #循环可读事件
    for s in readable :
        #如果是server监听的socket
        if s is server:
            #同意连接
            connection, client_address = s.accept()
            print ("新连接： ", client_address)
            connection.setblocking(0)
            #将连接加入到select可读事件队列
            inputs.append(connection)
            #新建连接为key的字典，写回读取到的消息
            message_queues[connection] = Queue.Queue()
        else:
            #不是本机监听就是客户端发来的消息
            data = s.recv(1024)
            if data :
                print ("收到数据：" , data , "客户端：",s.getpeername())
                message_queues[s].put(data)
                if s not in outputs:
                    #将读取到的socket加入到可写事件队列
                    outputs.append(s)
            else:
                #空白消息，关闭连接
                print ("关闭连接：", client_address)
                if s in outputs :
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]
    for s in writable:
        try:
            msg = message_queues[s].get_nowait()
        except Queue.Empty:
            print ("连接：" , s.getpeername() , '消息队列为空')
            outputs.remove(s)
        else:
            print ("发送数据：" , msg , "到", s.getpeername())
            s.send(msg)

    for s in exceptional:
        print ("异常连接：", s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]