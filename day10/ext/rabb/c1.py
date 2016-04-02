#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="hello")  # 在发送之前,我们要确保这个队列存在,如果我们发送一个消息到不存在的队列,rabbitmq会认为这个是垃圾消息
# 我们已经创建了一个队列名为hello,待会我们的消息都会发送到这个队列


# rabbitmq不允许我们直接将消息发送到队列,而是通过一个交换器,现在我们使用一个特殊对交换器,它是一个空对字符串标识对交换器,它能确保我们对消息该放到哪个
# 队列,这个队列需要特殊对rouning_key
channel.basic_publish(exchange="",
                      routing_key="hello",
                      body="hello world",)

print(" [x] Sent 'hello world")

# 在退出之前,我们需要确保网络缓冲区已经清空,且我们对消息的确已经发送到rabbitMQ,我们可以关闭这个连接
connection.close()
