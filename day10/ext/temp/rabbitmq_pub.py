#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1"))
channel = connection.channel()

channel.queue_declare(queue="hello")  # 定义一个队列,当消费者先启动,防止队列不存在报错,存在则忽略

channel.basic_publish(exchange="",
                      routing_key="hello",
                      body="hello world")  # 发送消息到交换器,交换器再通过路由KEY路由到队列
print("sent hello world")
connection.close()


