#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
# import pika
#
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()
# channel.queue_declare(queue='hello')
# channel.basic_publish(exchange='', routing_key='hello', body='hello world2')
#
# print(" [x] Sent 'hello world2!'")
# connection.close()


# import pika
#
# connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
# channel = connection.channel()
#
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='hello world',
#                       properties=pika.BasicProperties(
#                           delivery_mode=2,
#                       ))
# print(" [x] sent 'hello world")
# connection.close()


import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'


message = ' '.join(sys.argv[2:]) or "info: Hello world!"
channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=message)

print(" [x] sent %r:%r" % (routing_key, message))
connection.close()