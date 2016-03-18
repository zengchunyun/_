#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import sys
import subprocess
import os
import yaml
import shelve
import threading
import time


base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
conf_dir = os.path.join(base_dir, "config/minion.yaml")
sys.path.append(base_dir)
conf_dict = yaml.load((open("%s" % conf_dir)))
db_path = conf_dict["auth_db"]
db_path = os.path.join(base_dir, db_path)
connect_database = shelve.open(db_path)  # 打开可持久化数据文件
database = connect_database.get("data")  # 获取键为data的数据
if database is None:
    connect_database["data"] = {}
    database = {}


class CmdServe(object):
    def __init__(self, exchange="cmd", exchange_type="topic"):
        self.host = conf_dict['master']
        self.port = conf_dict['publish_port']
        self.minion_id = conf_dict["id"]
        self.exchange = exchange  # 设置交换器名称
        self.exchange_type = exchange_type  # 设置交换器类型
        self.message = {}  # 初始化消息
        self.auth = MQServer(self.host, self.port, self.exchange, self.exchange_type)
        if self.acl_auth():  # 判断自己是否已授权,未授权则不回应
            self.get_request()  # 然后去接收服务端响应
            self.run()
            self.message = {}  # 重置消息

    def acl_auth(self):
        data = database.get(self.minion_id)
        if type(data) is not dict:
            return False
        is_auth = data.get("auth")
        if is_auth is not None:
            if is_auth is True:
                return True
        return False

    def run(self):
        self.message = bytes(str(self.message), "utf8")
        self.auth = MQServer(self.host, self.port, self.exchange, self.exchange_type)
        self.auth.publish(self.exchange, routing_key=self.minion_id, body=self.message)

    def get_request(self):
        self.auth.consumer(exchange=self.exchange, routing_key=self.minion_id, callback=self.callback)

    def callback(self, ch, method, properties, body):
        print("get {} message {}".format(method.routing_key, body))
        self.message = yaml.load(str(body, "utf-8"))
        result = subprocess.Popen(self.message["cmd"], shell=True, stdout=subprocess.PIPE)
        result = result.stdout.read()
        self.message["cmd_result"] = result
        self.auth.channel.close()
        self.auth.close()


def run():
    from modules.minion_daemon import AuthServe
    auth = AuthServe()

if __name__ == "__main__":
    while True:
        from modules.salt_mq import MQServer
        get_auth = threading.Thread(target=run)
        get_auth.start()
        get_auth.join(5)
        cmd = CmdServe()
        time.sleep(5)
