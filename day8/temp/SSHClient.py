#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import paramiko

# # 创建SSH对象
# ssh = paramiko.SSHClient()
# # 允许连接不在know_hosts文件中的主机
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # 连接服务器
# ssh.connect(hostname='127.0.0.1', port=22, username='root', password='123')
#
# # 执行命令
# stdin, stdout, stderr = ssh.exec_command('df')
# # 获取命令结果
# result = stdout.read()
# print(result)
#
# # 关闭连接
# ssh.close()


# import paramiko
#
# transport = paramiko.Transport(('127.0.0.1', 22))
# transport.connect(username='zengchunyun', password=' ')
#
# ssh = paramiko.SSHClient()
# ssh._transport = transport
#
# stdin, stdout, stderr = ssh.exec_command('df')
# print (stdout.read())
#
# transport.close()

import os
import sys

import argparse

parser = argparse.ArgumentParser(description="Provess some integer.")

parser.add_argument("integers", metavar='N', type=int, nargs='+',
                    help="an integer for the accumulator")
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
args = parser.parse_args()
# print(args.integers)
# print(args.accumulate)
# print(args.accumulate(args.integers))

# parser = argparse.ArgumentParser(prog='myprogram', usage='%(prog)s [options]',
#                                  epilog='And that ok',
#     description='sum the integers at the command line')
# # parser.add_argument(
# #     'integers', metavar='int', nargs='+', type=int,
# #     help='an integer to be summed')
# parser.add_argument(
#     '--log', default=sys.stdout, type=argparse.FileType('w'),
#     help='the file where the sum should be written')
# o = parser.add_argument('--foo', help='foo help the %(prog)s program', nargs='+')
# parser.add_argument('bar', nargs='?', help='bar help')
# parser.add_argument('--pare', type=int)
# args = parser.parse_args()
# print(args.bar)
# print(args.foo)
# # print(o)
# # parser.print_help()
# # args.log.write('%s' % sum(args.integers))
# # args.log.close()
#
# import getopt
#
# args = '-a -b -cfoo -d bar a1 a2'.split()
# print(args)
# optlist, args = getopt.getopt(args,'abc:d:')
# print(optlist)
# print(args)

# b = (10*i for i in [1,2,3,4])
# print(type(b))