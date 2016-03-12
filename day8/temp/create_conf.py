#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import configparser

def create():
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"ServerAliveInterval": "45",
                         "Compression": "yes",
                         "compressionLevel": "9"}

    config["web"] = {}
    config["web"]["www.baidu.com"] = "127.0.0.1"
    config["web"]["www.qq.com"] = "127.0.0.1"
    config["DNS"] = {}
    config["DNS"]["BJ"] = "127.0.0.1"
    config["DNS"]["SH"] = "127.0.0.1"
    topsecret = config["DNS"]
    topsecret["port"] = "22"
    topsecret["ForwardX11"] = "no"
    config["DEFAULT"]["DNS"] = "yes"
    with open("example.ini", "w") as configfile:
        config.write(configfile)


def read():
    config = configparser.ConfigParser()
    print(config.sections())  # 显示[]列表
    print(config.read("example.ini"))  # 返回列表形式的文件名
    print(config.sections())  # 打印节点
    print("FTP" in config)  # 判断节点是否包含该字段,相当于列表操作
    print("DNS" in config)
    print(config["DNS"]["BJ"])  # 打印DNS节点下BJ的值
    print(config["DEFAULT"]["Compression"])  # 打印默认节点配置
    topsecret = config["DNS"]
    print(topsecret["ForwardX11"])
    print(topsecret["port"])

    for key in config["web"]:
        print(key)

    print(config["DNS"]["ForwardX11"])
    print(topsecret.getboolean('ForwardX11'))
    print(config['DNS'].getboolean('ForwardX11'))
    print(config.getboolean('DNS', 'Compression'))
    print(topsecret.get("Port"))
    print(topsecret.get("CompressionLeveL"))  # 忽略大小写
    print(topsecret.get("Cipher"))
    print(topsecret.get('CompressionLevel', '3'))
    print(config.get('bitbucket.org', 'monster', fallback='No such things as monsters'))
    print(topsecret.getboolean('BatchMode', fallback=True))
    config['DEFAULT']['BatchMode'] = 'no'
    print(topsecret.getboolean('BatchMode', fallback=True))



# # read()
#
#
# parser = configparser.ConfigParser()
# parser.read_dict({'section1': {'key1': 'value1',
#                                'key2': 'value2',
#                                'key3': 'value3', },
#                   'sevtion2': {'keyA': 'valuea',
#                                'keyb': 'valueb',
#                                'keyc': 'valuec', },
#                   'section3': {'foo': 'x',
#                                'bar': 'y',
#                                'baz': 'z', },
#                   })
# print(parser.sections())
# print([option for option in parser['section3']])
#
# from collections import OrderedDict
# parser = configparser.ConfigParser()
# parser.read_dict(
#     OrderedDict((
#         ('s1',
#          OrderedDict((
#              ('1', '2'),
#              ('3', '4'),
#              ('5', '6'),
#          ))
#          ),
#         ('s2',
#          OrderedDict((
#              ('a', 'b'),
#              ('c', 'd'),
#              ('e', 'f'),
#          ))
#          ),
#     ))
# )
# print(parser.sections())
# print([option for option in parser['s1']])
# print([ option for option in parser['s2'].values()])

# create()
def modify():
    config = configparser.RawConfigParser()
    config.read("example.ini")
    if "Section1" not in config.sections():
    # if not config.getboolean("section1"):
        config.add_section("Section1")
    config.set("Section1", "an_int", "13")
    config.set("Section1", "a_bool", "false")
    with open("example.ini", "w") as configfile:
        config.write(configfile)

modify()