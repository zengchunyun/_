#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
该客户端允许独立使用,而不依赖本程序其它组件
"""
import socket
import select
import sys
import logging
import time

logger = logging.getLogger( __name__)  # 创建一个日志名为Game
logger.setLevel(logging.INFO)  # 日志级别为INFO
con_handler = logging.StreamHandler()  # 创建控制台流处理日志
con_handler.setLevel(logging.DEBUG)  # 设置控制台日志输出级别
file_handler = logging.FileHandler(filename="access.log", encoding="utf8", delay=False)  # 设置记录日志文件属性
file_handler.setLevel(logging.INFO)  # 设置记录日志级别
formatter = logging.Formatter("%(asctime)s  -  %(name)s   -  %(levelname)s  - %(message)s")  # 设置日志格式
con_handler.setFormatter(fmt=formatter)  # 设置控制台输出日志格式
file_handler.setFormatter(fmt=formatter)  # 设置日志文件记录格式
logger.addHandler(con_handler)  # 将控制台日志处理加入到Game日志对象里
logger.addHandler(file_handler)  # 将文件日志处理加入到Game日志对象里


def client():
    sys.stdout.write('<魔兽终端>: ')
    sys.stdout.flush()


def connect_server(sock=None):
    """
    :param sock: 已建立的socket
    :return: 返回建立连接的socket
    """
    if sock:
        shutdown_sock(sock)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    sock.connect((host, port))
    return sock


def shutdown_sock(sock):
    try:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except OSError:
        sock.close()

if __name__ == "__main__":
    host, port = "127.0.0.1", 9999
    recv_buffer = 4096
    quit_game = False
    count = 0
    try:
        while count < 60:
            try:
                sock = connect_server()
                # client()
                while not quit_game:
                    rlist = [sys.stdin, sock]  # 设置读取列表
                    read_list, write_list, error_list = select.select(rlist, [], [], 1)
                    for socks in read_list:
                        if socks == sock:
                            try:
                                received = str(sock.recv(recv_buffer), "utf-8")
                            except ConnectionResetError:
                                count += 1
                                logger.info("正在尝试重新连接 ...")
                                sock = connect_server(sock)
                                logger.info("连接服务器引擎成功 ...")
                            if received:
                                count = 0  # 连接成功,重置尝试次数
                                sys.stdout.write(received)
                                client()
                        else:
                            data = sys.stdin.readline()
                            sock.sendall(bytes(data, "utf-8"))
            except ConnectionRefusedError:
                logger.info("服务器不可达 ...")
                time.sleep(count)
                count += 1
            except ConnectionResetError:
                pass
            except OSError:
                logger.info("您已和服务器断开连接 ...")
    except KeyboardInterrupt:
                logger.info("您已强制退出 ...")
