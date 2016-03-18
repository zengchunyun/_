#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import os
import yaml
import shelve
from modules.salt_mq import MQServer


base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
conf_dir = os.path.join(base_dir, "config/master.yaml")
conf_dict = yaml.load((open("%s" % conf_dir)))
db_path = conf_dict["auth_db"]
db_path = os.path.join(base_dir, db_path)
connect_database = shelve.open(db_path)  # 打开可持久化数据文件
database = connect_database.get("data")  # 获取键为data的数据
if database is None:
    connect_database["data"] = {}
    database = {}


class AuthServe(object):
    def __init__(self, exchange="auth", exchange_type="topic"):
        self.host = conf_dict['master']
        self.port = conf_dict['publish_port']
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.message = {}
        self.auth = MQServer(self.host, self.port, self.exchange, self.exchange_type)
        self.approval_auth()
        connect_database.close()

    def callback(self, ch, method, properties, body):
        """
        解析队列消息
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        print("get {} message {}".format(method.routing_key, body))
        self.message = yaml.load(str(body, "utf-8"))
        if not self.acl_auth():  # 如果检查该客户端未授权,则进入授权操作
            self.request_auth()
        self.auth.channel.close()  # 关闭通道
        self.auth.close()  # 关闭连接
        self.notice_auth()

    def approval_auth(self):
        """
        接受授权请求
        :return:
        """
        self.auth.consumer(exchange=self.exchange, routing_key="auth", callback=self.callback)

    def request_auth(self):
        """
        标记授权状态
        :return:
        """
        request = None
        while True:
            request = str(input("是否授权? yes/no: ")).strip()
            if request.lower() == "yes":
                request = True
                break
            elif request.lower() == "no":
                request = False
                break
        if type(self.message) == dict:
            self.message["auth"] = request
            minion_id = self.message.get("id")
            if minion_id:
                database[minion_id] = self.message
                connect_database["data"] = database
                self.exchange = minion_id
                print("{}\n[{}]:\n\t[\033[33;1m{}\033[0m]".format("".ljust(20, "-"), minion_id, self.message["auth"]))
        self.message = bytes(str(self.message), "utf8")

    def notice_auth(self):
        """
        通告授权状态
        :return:
        """
        ack_auth = MQServer(self.host, self.port, self.exchange, self.exchange_type)
        ack_auth.publish(self.exchange, routing_key="auth", body=self.message)

    def acl_auth(self):
        """
        检查auth状态
        :return:
        """
        if type(self.message) is not dict:
            return False
        is_auth = self.message.get("auth")
        if is_auth is not None:
            if is_auth is True:
                return True
        return False
