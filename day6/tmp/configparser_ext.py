#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import configparser
#
# config = configparser.ConfigParser()
# config["DEFAULT"] = {'ServerAliveInterval': '45',
#                       'Compression': 'yes',
#                      'CompressionLevel': '9'}
#
# config['bitbucket.org'] = {}
# config['bitbucket.org']['User'] = 'hg'
# config['topsecret.server.com'] = {}
# topsecret = config['topsecret.server.com']
# topsecret['Host Port'] = '50022'     # mutates the parser
# topsecret['ForwardX11'] = 'no'  # same here
# config['DEFAULT']['ForwardX11'] = 'yes'
# with open('example2.ini', 'w') as configfile:
#    config.write(configfile)
#

# config = configparser.ConfigParser()
# sec = config.sections()
# print(sec)
# re_con = config.read("example.ini")
# print(re_con)
# sec =config.sections()
# print(sec)
# print("bitbucket.org" in sec)
# print(config["bitbucket.org"]["user"])  # 读取子节点部分信息
# print(config['DEFAULT']['Compression'])
# topsecret = config["topsecret.server.com"]
# print(topsecret["ForwardX11"])  # 读取默认配置
#
# print(topsecret['port'])
#
#
# for key in config["bitbucket.org"]:
#     print((key))


config = configparser.ConfigParser()
config.read("example.ini")

config.read('example2.ini')

# ########## 读 ##########
secs = config.sections()
#print secs
print(secs)
# config.options('group2')
#print options

item_list = config.items('group2')
print(item_list)

#val = config.get('group1','key')
#val = config.getint('group1','key')

# ########## 改写 ##########
#sec = config.remove_section('group1')
config.write(open('i.cfg', "w"))

#sec = config.has_section('wupeiqi')
#sec = config.add_section('wupeiqi')
#config.write(open('i.cfg', "w"))


#config.set('group2','k1',11111)
#config.write(open('i.cfg', "w"))

#config.remove_option('group2','age')
#config.write(open('i.cfg', "w"))
