#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import optparse
from twisted.internet.protocol import Protocol, ClientFactory


def parser_args():  # 通过该函数获取用户输入ip及端口信息
    usage = """usage: %prog [options] [hostname]:port ...

This is the Get Poetry Now! client, Twisted version 3.0
Run it like this:

  python twisted_recefile.py port1 port2 port3 ...
"""
    parser = optparse.OptionParser(usage=usage)  # 通过执行该程序时传入参数-h会提示该使用信息
    _, address = parser.parse_args()  # 获取用户执行程序时输入的参数
    print("==addr:", _, address)
    if not address:  # 如果执行程序未输入任何参数,则打印帮助信息,并退出程序
        print(parser.format_help())
        parser.exit()

    def parse_address(addr):  # 定义一个函数将ip及端口分离,通过地址及端口元组形式返回
        if ":" not in addr:
            host = "127.0.0.1"
            port = addr
        else:
            host, port = str(addr).split(":", 1)
        if not str(port).isdigit():
            parser.error("Port must be integers.")
        return host, int(port)
    return map(parse_address, address)  # 通过map方法,将一个可迭代的序列通过分离IP函数得到一个列表包含元组形式的ip端口列表,即[(ip, port),()...]


class PoetryProtocol(Protocol):
    poem = ""  # 初始化空的属性,用于存储接收的数据

    def dataReceived(self, data):  # 当有就绪事件时,这个方法会被触发
        self.poem += data  # 将每次接收的数据追加到上一次接收位置后面
        print('[%s] recv:[%s]' % (self.transport.getPeer(), len(self.poem)))  # 打印对端服务器地址及接收大小

    def connectionLost(self, reason):  # 该方法由服务端触发了 self.transport.loseConnection()这个方法,导致客户端也触发了这个异常
        self.poemReceived(self.poem)  # 然后执行我们自定义的类方法,并将我们接收的数据以参数形式传入

    def poemReceived(self, poem):  # 通过该方法,执行回调函数,并将接收的数据传入执行
        self.factory.poem_finished(poem)  # 该方法执行的是子类定义的方法,


class PoetryClientFactory(ClientFactory):
    protocol = PoetryProtocol  # 将我们自定义的数据处理方法赋值给protocol

    def __init__(self, callback):
        self.callback = callback  # 然后创建实例属性,将下面传入的回调函数赋值给实例属性

    def poem_finished(self, poem):  # 该方法通过上面定义的类PoetryProtocol触发,然后执行我们下面定义的回调函数
        self.callback(poem)  # 该回调函数由父类触发执行


def get_poetry(host, port, callback):  # 该方法开始连接服务端接收数据
    """
    Download a poem from the given host and port and invoke
      callback(poem)
    when the poem is complete.
    """
    from twisted.internet import reactor
    factory = PoetryClientFactory(callback)  # 实例化前面定义的类,并把下面定义的回调函数作为参数传入
    reactor.connectTCP(host, port, factory)  # 调用此方法,并将我们定义的factory事件注册到connectTCP类中


def poetry_main():
    addresses = parser_args()  # 调用函数解析IP及端口,得到一个大列表,
    from twisted.internet import reactor
    poems = []  # 初始化一个列表,用于存储接收的数据

    def got_poem(poem):  # 每次执行,都会将接收的数据参数形式传入该函数
        poems.append(poem)  # 并将该数据追加到列表
        if len(poems) == len(addresses):  # 当列表里存储的元素个数等于我们执行程序时传入的地址数,说明数据接收完成,
            reactor.stop()  # 调用reactor的stop方法关闭客户端与服务器连接

    for address in addresses:
        host, port = address  # 通过遍历循环获取大列表数据,得到ip,port
        get_poetry(host=host, port=port, callback=got_poem)  # 然后调用该方法处理单独的ip,port服务,传入了一个got_poem回调函数
    reactor.run()  # 程序解释到这,才真正开始执行,进入循环轮询select事件中...

    print("main loop done...")  # 当上面这些操作执行完毕,最后才执行这句代码

if __name__ == "__main__":
    poetry_main()  # 程序入口,处理接收服务器数据
