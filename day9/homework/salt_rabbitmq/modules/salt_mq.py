#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import pika


class MQServer(object):
    def __init__(self, host, port=5672, exchange=None, exchange_type="topic"):
        """
        初始化MQ设置
        :param host: MQ服务器地址
        :param port: MQ端口
        :param exchange: 交换器名称
        :param exchange_type: 交换器类型,默认关键字类型
        :return:
        """
        self.host = host
        self.port = port
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.queue = None
        self.connection = self.connect()
        self.channel = self.connect_channel()
        self.create_exchange()

    def connect(self):
        """
        连接MQ服务器
        :return:
        """
        return pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))

    def connect_channel(self):
        """
        创建频道
        :return:
        """
        return self.connection.channel()

    def create_exchange(self):
        """
        定义交换器名称,防止发布时,如果交换器不存在,异常
        :return:
        """
        self.channel.exchange_declare(exchange=self.exchange, type=self.exchange_type)

    def publish(self, exchange=None, routing_key=None, body=None):
        """
        创建发布者
        :param exchange: 交换器名称
        :param routing_key: 路由KEY
        :param body:消息主体
        :return:
        """
        if exchange:
            self.exchange = exchange
        self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=body)
        self.close()

    def consumer(self, exchange=None, routing_key=None, callback=None):
        """
        创建消费者
        :param exchange:
        :param routing_key:
        :param callback:
        :return:
        """
        if exchange:
            self.exchange = exchange
        self.create_queue()
        self.channel.queue_bind(queue=self.queue, exchange=self.exchange, routing_key=routing_key)
        self.channel.basic_consume(consumer_callback=callback, queue=self.queue, no_ack=True)
        self.start()

    def create_queue(self):
        """
        生成队列,当关闭consumer时,加上exclusive=True,queue也会被删除
        :return:
        """
        self.queue = self.channel.queue_declare(exclusive=True).method.queue  # 为每个消费者生成不同的队列

    def close(self):
        """
        关闭消息连接
        :return:
        """
        self.connection.close()

    def start(self):
        self.channel.start_consuming()
