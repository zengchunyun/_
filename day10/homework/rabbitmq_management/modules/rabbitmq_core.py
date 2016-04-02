#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import pika
import uuid
import time
import logging
import argparse


class RabbitMQServer(object):
    def __init__(self, host="localhost", port=5672, logger=None, timeout=16):
        """
        :param host: rabbitmq服务器IP
        :param port: rabbitmq服务器端口
        :param logger: 日志对象
        :return:
        """
        self.host = host
        self.port = port
        self.response = []  # 存放接收客户端返回的消息列表
        self.queue_name = None  # 队列名称
        self.log = logger
        self.correlation_id = None
        self.exchange = "topic_os"  # 设置交换器名称
        self.exchange_type = "topic"  # 设置交换器类型
        self.connection = self.connect_server()
        self.channel = self.connection.channel()
        self.log.debug("Create channel {}".format(self.channel.channel_number))
        self.create_exchange()
        self.create_queue()
        self.channel.basic_consume(consumer_callback=self.callback,
                                   queue=self.queue_name,
                                   no_ack=True)
        self.timeout = timeout + 1  # 设置一个任务最长执行的时间,超过这个设置时间则不继续等待任务返回结果

    def connect_server(self):
        """
        连接到rabbitmq服务器
        :return:
        """
        self.log.info("Connecting to {}:{}".format(self.host, self.port))
        return pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host,
            port=self.port,
        ))

    def create_queue(self):
        """
        创建队列
        :return:
        """
        self.queue_name = self.channel.queue_declare(exclusive=True).method.queue
        self.log.debug("Create queue {}".format(self.queue_name))

    def create_exchange(self):
        """
        创建交换器
        :return:
        """
        self.channel.exchange_declare(exchange=self.exchange,
                                      type=self.exchange_type)

    def callback(self, ch, method, properties, body):
        """
        回调方法,用于接收客户端返回的结果
        :param ch: channel
        :param method: 队列方法
        :param properties: 队列属性
        :param body: 主体消息
        :return:
        """
        self.response.append(body)  # 将接收的消息追加到队列

    def start(self, cmd, routing_key="remote.call"):
        self.response = []  # 存储客户端返回的数据
        self.correlation_id = str(uuid.uuid4())
        self.log.info("exec command {}".format(cmd))
        self.log.debug("routing key {}".format(routing_key))
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=routing_key,  # 该routing key用于让交换器分派消息到绑定了该routing key的队列
                                   properties=pika.BasicProperties(
                                       reply_to=self.queue_name,
                                       correlation_id=self.correlation_id
                                   ),
                                   body=cmd)
        before = time.monotonic()  # 纪录执行操作前的时间
        after_len = 0  # 用于计算接收回来的数据长度
        while True:
            if len(self.response) != after_len:  # 当接收的数据不为空,则计算当前接收的数据长度
                before_len = len(self.response)
            else:
                before_len = after_len  # 为了避免网络延时造成接发出去的任务与收到的任务回复不完整,则休眠一小会,如果网络环境很差,这个值可能需要增大
                time.sleep(0.4)
            self.connection.process_data_events()  # 处理数据事件,检查是否有消息发回到此队列
            if len(self.response) == before_len and before_len:
                break
            after = time.monotonic()  # 纪录执行完一个任务后的时间
            if (after - before) > self.timeout:  # 当执行时间大于16s,则判定任务超时返回
                break
        return self.response  # 返回接收到的数据列表


def set_log():
    """
    设置日志对象,可以通过配置文件配置基本日志属性,如果没有使用配置文件,则使用默认设置,默认只会将日志输出到控制台
    :return: 返回日志对象
    """
    try:
        from config.settings import output_console, log_file, encoding, log_level, \
            console_log_level, file_log_level, formatter
    except ImportError:
        output_console = True
        log_file = None
        log_level = logging.DEBUG
        console_log_level = logging.INFO
        encoding = "utf8"
        file_log_level = logging.INFO
        formatter = logging.Formatter("%(asctime)s  -  %(name)s   -  %(levelname)s  - %(message)s")
    logger = logging.getLogger(__name__)  # 创建日志对象
    logger.setLevel(log_level)  # 设置日志记录级别
    if output_console:  # 当设置了输出屏幕日志,则启用该日志打印屏幕功能,默认开启
        console_handler = logging.StreamHandler()  # 创建控制台日志输出对象
        console_handler.setLevel(console_log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    if log_file:  # 当设置了文件名,则启用记录日志文件功能,默认关闭
        file_handler = logging.FileHandler(filename=log_file, encoding=encoding)  # 创建日志文件对象
        file_handler.setLevel(file_log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


def main():
    """
    程序入口,通过接收命令行参数执行任务
    :return:
    """
    try:
        from config.settings import server, port, timeout
    except ImportError:
        server = "localhost"
        port = 5672
        timeout = 16
    description = """
    该工具可用于控制绑定了不同路由KEY的主机处理不同的事件
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--exec", metavar="任务指令,如果指令包含参数,需要引号''引起")
    parser.add_argument("--bind", metavar="key", help="绑定不同的key,可以发送不同的任务", nargs="?")
    args = parser.parse_args()  # 解析参数
    cmd = args.exec
    bind_key = args.bind
    if not cmd:
        parser.error("\033[31;1mthe following arguments are requires: command\033[0m")
    if not bind_key:
        bind_key = "remote.call"
    logger = set_log()
    server = RabbitMQServer(host=server, port=port, logger=logger, timeout=timeout)
    response = server.start(cmd=cmd, routing_key=bind_key)
    for message in response:
        message = eval(str(message, "utf-8"))
        host_id = message["host"]
        data = message["data"]
        print("\n{}\n[\033[33;1m{}\033[0m]\n{}\n{}".format(
            "".ljust(60, "-"), host_id, str(data, "utf-8"), "".ljust(60, "-")))


if __name__ == "__main__":
    main()
