#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import pika
import subprocess
import threading
import time
import sys


class RabbitMQClient(object):
    def __init__(self, host="localhost", port=5672, timeout=15, host_id=None, binding_keys=None):
        """
        :param host: rabbitmq服务器IP
        :param port: 服务器端口
        :param timeout: 任务最大超时时间
        :param host_id: 唯一主机ID,用于标识处理任务的主机
        :param binding_keys: 绑定不同的路由key,用于接收不同的事件任务
        :return:
        """
        self.host = host
        self.port = port
        self.response = None
        self.queue_name = None
        self.exchange = "topic_os"  # 设置交换器名称
        self.exchange_type = "topic"  # 设置交换器类型
        self.binding_keys = binding_keys
        self.id = self.get_id()  # 设置客户端的唯一ID,一般以客户端IP为唯一ID
        if host_id:
            self.id = host_id  # 如果配置文件设置了ID属性,则以配置文件为优先
        self.connection = self.connect_server()
        self.channel = self.connection.channel()
        self.create_exchange()  # 创建交换器
        self.create_queue()  # 创建队列
        self.bind()
        self.timeout = timeout  # 设置一个任务最长执行的时间,超过这个设置时间则返回超时提示

    def connect_server(self):
        """
        连接到rabbitmq服务器
        :return:
        """
        return pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host,
            port=self.port,
        ))

    def get_id(self):
        """
        通过获取系统的IP来定义一个客户端的ID
        :return: 返回最终确定的IP
        """
        import re
        self.exec_call("ip addr 2> /dev/null ||ifconfig")
        get_ip = self.response
        result = re.findall("(\d+\.\d+\.\d+\.\d+)", str(get_ip, "utf-8"))
        for ip in result:
            if ip != "127.0.0.1" and not (ip.endswith("255") or ip.startswith("255")):
                return ip

    def create_queue(self):
        """
        创建队列
        :return:
        """
        self.queue_name = self.channel.queue_declare(exclusive=True).method.queue

    def create_exchange(self):
        """
        创建交换器,避免客户端先启动,而连接的交换器不存在异常
        :return:
        """
        self.channel.exchange_declare(exchange=self.exchange, type=self.exchange_type)

    def bind(self):
        """
        绑定路由key,方便接收不同类型的任务
        :return:
        """
        print("Routing key {}".format(self.binding_keys))
        for binding_key in self.binding_keys:
            self.channel.queue_bind(queue=self.queue_name,
                                    exchange=self.exchange,
                                    routing_key=binding_key)

    def exec_call(self, command):
        """
        执行命令,并把错误或正确结果赋值给self.response
        :param command: 从rabbitmq服务器获取任务命令
        :return:
        """
        if type(command) == bytes:
            command = str(command, "utf-8")
        result = subprocess.Popen(args=command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self.response = (result.stdout.read() or result.stderr.read())

    def callback(self, ch, method, properties, body):
        """
        回调方法,用于执行任务并返回结果到rabbitmq服务器
        :param ch:  相当于self.channel
        :param method:
        :param properties:接收到任务带的额外属性
        :param body:任务消息
        :return:
        """
        before = time.monotonic()  # 纪录代码执行到这所花费时间
        exec_cmd = threading.Thread(target=self.exec_call, args=(body,))
        exec_cmd.start()
        exec_cmd.join(self.timeout)
        after = time.monotonic()  # 代码执行完到这所花费时间,用于计算执行过程是否超时
        if (after - before) > self.timeout:  # 当执行任务大于设定的默认超时时间,则说明任务已经超时了,将返回超时信息给服务器
            self.response = bytes("command exec timeout", "utf8")
        print(" [*] Got a task {}".format(str(body, "utf8)")))
        message = {"host": self.id, "data": self.response}
        ch.basic_publish(exchange="",
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=properties.correlation_id,),
                         body=bytes(str(message), "utf-8"))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        """
        启动客户端,进入等待接收任务状态,且每次只接收一个任务
        :return:
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback,
                                   queue=self.queue_name)
        print(" [x] Awaiting RPC request")
        self.channel.start_consuming()


def main():
    """
    新建客户端实例,用于处理任务请求,并返回处理结果给rabbitMQ服务器
    :return:
    """
    try:
        from config.settings import server, port, timeout, host_id, binding_keys
    except ImportError:
        server = "localhost"
        port = 5672
        timeout = 15
        host_id = None
        binding_keys = ["remote.call"]
    binding_list = sys.argv[1:]  # 路由KEY支持接收控制台输入,优先级最高
    if binding_list:
        binding_keys = binding_list
    client = RabbitMQClient(host=server, port=port, timeout=timeout, host_id=host_id, binding_keys=binding_keys)
    client.start()


if __name__ == "__main__":
    main()
