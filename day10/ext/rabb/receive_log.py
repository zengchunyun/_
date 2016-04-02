#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host="localhost"
))
channel = connection.channel()

channel.exchange_declare(exchange="logs",
                         type="fanout")  # 定义一个交换器名为logs,类型为广播

result = channel.queue_declare(exclusive=True)  # 当断开连接时,该随机队列会被删除
queue_name = result.method.queue  # 生成随机队列
channel.queue_bind(exchange="logs",
                   queue=queue_name)  # 将指定的交换器与我们定义的队列相关联,也可以说是交换器与队列绑定
print(" [*] Waiting for logs. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()
