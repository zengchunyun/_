#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="hello")  # 为了确保每次订阅的队列都存在,我们先声明一个队列

# 接收队列消息需要通过回调函数来接收


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(3)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback,
                      queue="hello",
                      no_ack=True)  # 这里我们需要告诉rabbitMQ这个回调函数会从我们的hello队列接收消息,关闭消息确认标记,
# 那么当worker工作中异常,如没有完成任务就关闭了连接,可能会丢失任务,使用no_ack=True默认只要rabbit分配任务给该worker了,就会将任务从队列删除

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()  # 我们这里进入了一个永不终止的循环等待数据状态
