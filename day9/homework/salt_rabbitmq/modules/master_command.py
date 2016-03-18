#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import os
import yaml
import shelve
from modules.salt_mq import MQServer
import argparse
parser = argparse.ArgumentParser(prog='salt', usage='%(prog)s -h [options] command',
                                 description='通过salt可以对服务器进行批量管理')
parser.add_argument("cmd", help="对服务器所执行对操作,如果命令包含参数,请用双引号引起", metavar="cmd.run command", nargs="+")
parser.add_argument("--server", help="管理单个服务器", metavar="minion id")
args = parser.parse_args()
server = args.server
try:
    assert len(args.cmd) == 2
    command = args.cmd[1]
except AssertionError:
    print("执行命令方式为:cmd.run [具体命令], 如:cmd.run 'ls'")
    exit(1)


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


class CmdServe(object):
    def __init__(self, minion_id=server, exchange="cmd", exchange_type="topic"):
        self.host = conf_dict['master']
        self.port = conf_dict['publish_port']
        self.minion_id = minion_id
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.message = {}
        self.auth = MQServer(self.host, self.port, self.exchange, self.exchange_type)
        if self.acl_auth():
            self.run()
            self.get_request()
            self.message = {}  # 重置消息
        else:
            print("\n\033[31;1mminion does not exists or has not authorized\033[0m\n")

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
        cmd = {"cmd": command}
        self.message = bytes(str(cmd), "utf8")
        self.auth.publish(self.exchange, routing_key=self.minion_id, body=self.message)

    def get_request(self):
        self.auth = MQServer(self.host, self.port, self.exchange, self.exchange_type)
        self.auth.consumer(exchange=self.exchange, routing_key=self.minion_id, callback=self.callback)

    def callback(self, ch, method, properties, body):
        print("{}\n[{}]:\n".format("".ljust(20, "-"), method.routing_key))
        self.message = eval(str(body, "utf-8"))
        print(str(self.message["cmd_result"], "utf-8"))
        self.auth.channel.close()
        self.auth.close()


def main():
    if str(server).count("*"):
        for key, value in database.items():
            if value.get("auth") is True:
                cmd = CmdServe(key)
    else:
        cmd = CmdServe()
