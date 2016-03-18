#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
# from salt_mq import MQServer
# import time


# def run(q, w, e, t):
#     global a
#     print(t)
#     a.channel.close()
#     a.close()
#
#
# while True:
#     m = MQServer("127.0.0.1", exchange="pub", exchange_type="topic")
#     m.publish(exchange="pub", routing_key="pub", body="hhh2")
#     a = MQServer("127.0.0.1", exchange="auth", exchange_type="topic")
#     a.consumer(exchange="auth", callback=run, routing_key="auth")


import pika
import random


def makepassword(rang = "23456789qwertyupasdfghjkzxcvbnm", size = 8):
    return " ".join(random.sample(rang, size)).replace(" ","")
parameters = pika.ConnectionParameters(host = 'localhost' )
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue = 'task_queue' , durable = True )
message = makepassword()
channel.basic_publish(exchange = '',
                      routing_key = 'task_queue' ,
                      body = message,
                      properties = pika.BasicProperties(
                          delivery_mode = 2 , # make message persistent
                      ))
