#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue="task_queue", durable=True)  # 为了确保服务器崩溃或关闭,队列消息持久化,我们需要将durable标记为True,
# rabbitmq不允许我们重新定义一个已存在的队列,所以如果是要创建一个可持久化队列,需要重新定义不存在的队列名
message = " ".join(sys.argv[1:]) or "Hello world!"
channel.basic_publish(exchange="",
                      routing_key="task_queue",
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                      ))

print(" [x] Sent %r " % message)
connection.close()