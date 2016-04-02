#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1"))
channel = connection.channel()

channel.queue_declare(queue="hello")  # 定义一个队列


def callback(ch, method, properties, body):
    print(" received {}".format(body))

channel.basic_consume(callback,
                      queue="hello",
                      no_ack=True)  # 定义接收的队列,当no_ack为True,当执行一个任务需要很长时间时,如果中间中断,可以不向服务端发送消费确认消息,如果为False,则最终会向服务端发送确认消息

print("waiting for message to exit press CTRL+C")
channel.start_consuming()  # 开始阻塞,直到有任务可取