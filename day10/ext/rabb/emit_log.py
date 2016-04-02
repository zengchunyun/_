#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host="localhost"
))
channel = connection.channel()

channel.exchange_declare(exchange="logs",
                         type="fanout")  # 定义一个交换器名为logs,类型为广播

message = " ".join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange="logs",
                      routing_key="",  # 在fanout类型的交换器里,routing_key会被忽略
                      body=message)
print(" [x] Sent %r" % message)
connection.close()