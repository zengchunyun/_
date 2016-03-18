#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
# import pika
#
#
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()
# channel.queue_declare(queue='hello')
#
#
# def callback(ch, method, properties, body):
#     print(" [x] Received {}".format(body))
#     import time
#     time.sleep(10)
#     print("ok")
#     ch.basic_ack(delivery_tag=method.delivery_tag)
#
#
# channel.basic_consume(callback, queue='hello', no_ack=False)
#
# print(' [*] Waiting for message. To exit press CTRL+C')
# channel.start_consuming()
# import pika
#
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
# channel = connection.channel()
#
# # make message persistent
# channel.queue_declare(queue='hello', durable=True)
#
#
# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#     import time
#     time.sleep(10)
#     print('ok')
#     ch.basic_ack(delivery_tag = method.delivery_tag)
#
# channel.basic_consume(callback,
#                       queue='hello',
#                       no_ack=False)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()
#
# import pika
#
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
# channel = connection.channel()
#
# # make message persistent
# channel.queue_declare(queue='hello')
#
#
# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#     import time
#     time.sleep(10)
#     print ('ok')
#     ch.basic_ack(delivery_tag = method.delivery_tag)
#
# channel.basic_qos(prefetch_count=1)
#
# channel.basic_consume(callback,
#                       queue='hello',
#                       no_ack=False)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()


import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', type='topic')

result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: {} [binding_keys] ...\n".format(sys.argv[0]))
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange="topic_logs", queue=queue_name, routing_key=binding_key)


print(' [*] Waiting for logs. to exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()