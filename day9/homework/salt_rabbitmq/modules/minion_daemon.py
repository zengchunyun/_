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
conf_dir = os.path.join(base_dir, "config/minion.yaml")  # minion配置文件路径
conf_dict = yaml.load((open("%s" % conf_dir)))  # 使用yaml读取配置
db_path = conf_dict["auth_db"]  # 获取授权数据库文件位置
db_path = os.path.join(base_dir, db_path)
connect_database = shelve.open(db_path)  # 打开可持久化数据文件
database = connect_database.get("data")  # 获取键为data的数据
if database is None:
    connect_database["data"] = {}
    database = {}


class AuthServe(object):
    def __init__(self, exchange="auth", exchange_type="topic"):
        self.host = conf_dict['master']  # 消息队列IP
        self.port = conf_dict['publish_port']  # 消息队列端口
        self.minion_id = conf_dict['id']  # minion端的唯一ID
        self.exchange = exchange  # 设置交换器名称
        self.exchange_type = exchange_type  # 设置交换器类型为关键字类型
        self.message = {}  # 初始化空消息字典
        self.auth = MQServer(self.host, self.port, self.exchange, self.exchange_type)  # 实例化消息对象
        if not self.acl_auth():  # 检查客户端是否已授权
            self.request_auth()  # 开始请求授权
            self.get_notice_auth()  # 获取授权状态
            self.message = {}  # 重置消息

    def acl_auth(self):
        if self.message and type(self.message) is dict:  # 如果有消息,且类型是字典型
            data = self.message  # data值则为self.message
        else:
            data = database.get(self.minion_id)  # 否则通过可持久化数据里找
            if type(data) is not dict:  # 如果找不到相关的则返回
                return False
        is_auth = data.get("auth")  # 获取授权状态
        if is_auth is not None:
            if is_auth is True:
                return True  # 只有授权了才返回True
        return False

    def request_auth(self):
        """
        请求授权
        :return:
        """
        auth = {"auth": "syn", "id": self.minion_id}
        self.message = bytes(str(auth), "utf8")  # 转换消息编码
        self.auth.publish(self.exchange, routing_key="auth", body=self.message)  # 发布一条消息

    def get_notice_auth(self):
        """
        获取授权状态
        :return:
        """
        self.exchange = self.minion_id  # 设置交换器名以minion_id为命名,只能是为该ID的minion才能收到此消息
        self.auth = MQServer(self.host, self.port, self.exchange, self.exchange_type)
        self.auth.consumer(exchange=self.exchange, routing_key="auth", callback=self.callback)  # 获取一条消息

    def callback(self, ch, method, properties, body):
        print("get {} message {}".format(method.routing_key, body))
        self.message = yaml.load(str(body, "utf-8"))
        if self.acl_auth():  # 如果检查该客户端未授权,则进入授权操作
            database[self.minion_id] = self.message
            connect_database["data"] = database
        self.auth.channel.close()  # 关闭通道
        self.auth.close()  # 关闭连接
