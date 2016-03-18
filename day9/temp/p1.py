#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
# from salt_mq import MQServer
# import time
#
#
# def run(q, w, e, t):
#     global a
#     print(t)
#     a.channel.close()
#     a.close()
#
#
# while True:
#     m = MQServer("127.0.0.1", exchange="auth", exchange_type="topic")
#     m.publish(exchange="auth", routing_key="auth", body="hhh2")
#     a = MQServer("127.0.0.1", exchange="pub", exchange_type="topic")
#     a.consumer(exchange="pub", callback=run, routing_key="pub")


import pika
import time
connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost' ))
channel = connection.channel()
channel.queue_declare(queue = 'task_queue' , durable = True )
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count = 1 )
channel.basic_consume(callback,
                      queue = 'task_queue' )
channel.start_consuming()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,) )
    print ("正在搞呀")
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)
channel.basic_consume(callback,
                      queue='hello')