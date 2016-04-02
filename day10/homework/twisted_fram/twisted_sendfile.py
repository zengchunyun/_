#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import optparse
import os
from twisted.internet.protocol import ServerFactory, Protocol


def pase_args():  # 用于解析用户执行时输入的参数
    usage = """usage: %prog [options] poetry-file

This is the Fast Poetry Server, Twisted edition.
Run it like this:

  python twisted_sendfile.py <path-to-poetry-file>

If you are in the base directory of the twisted-intro package,
you could run it like this:

  python twisted-server-1/fastpoetry.py poetry/ecstasy.txt

to serve up John Donne's Ecstasy, which I know you want to do.
"""
    parser = optparse.OptionParser(usage=usage)  # 执行选项-h将会打印该使用信息
    help = "The port to listen on. Default to a random available port."
    parser.add_option("--port", type="int", help=help)  # 添加选项--port

    help = "The interface to listen on. Default is localhost."
    parser.add_option("--iface", help=help, default="localhost")  # 添加选项 --iface

    options, args = parser.parse_args()  # 将选项及参数进行解析操作

    if len(args) != 1:  # 当参数不是1个时,打印错误提示信息
        parser.error("Provide exactly one poetry file.")
    poetry_file = args[0]  # 将第一个参数作为文件名

    if not os.path.exists(args[0]):  # 当文件不存在时打印错误提示
        parser.error('No such file: %s' % poetry_file)

    return options, poetry_file  # 返回选项及参数,也就是ip,port及文件名


class PoetryProtocol(Protocol):
    def connectionMade(self):  # 当有就绪事件时,
        self.transport.write(self.factory.poem)  # 通过该方法将数据写入到socket发送到客户端,数据通过实例化后的factory的实例属性获得
        self.transport.loseConnection()  # 然后调用loseConnection方法触发断开连接请求


class PoetryFactory(ServerFactory):
    protocol = PoetryProtocol  # 将自定义类赋值给ServerFactory的父类的factory的类属性protocol

    def __init__(self, poem):  # 创建一个实例属性,并把读取的数据赋值给该属性
        self.poem = poem


def main():
    options, poetry_file = pase_args()  # 解析程序执行时传入的参数
    poem = open(poetry_file).read()  # 通过解析参数获取文件路径,并读入数据
    factory = PoetryFactory(poem)  # 将数据参数形式传给我们上面定义的类
    from twisted.internet import reactor
    port = reactor.listenTCP(options.port or 9000, factory, interface=options.iface)  # 通过
    # 调用reactor.listenTCP返回的是twisted.internet.tcp.Port()实例对象
    print("Serving %s on %s." % (poetry_file, port.getHost()))  # 然后调用上面返回实例的对象获取Port类的方法getHost()
    reactor.run()  # 调用reactor的run方法,开始轮询监听注册事件

if __name__ == "__main__":
    main()  # 程序入口
