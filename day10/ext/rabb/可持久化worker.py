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
                      )  # 这里我们需要告诉rabbitMQ这个回调函数会从我们的hello队列接收消息,我们使用消息回执机制,当任务执行完,则向服务器发送确认
# 完成消息,这时服务器从将任务从队列删除,否则只要客户端执行任务出现异常,而服务端没有得到消息确认,服务器不会删除该任务,但是如果服务器挂了,该任务还是会丢失

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()  # 我们这里进入了一个永不终止的循环等待数据状态
