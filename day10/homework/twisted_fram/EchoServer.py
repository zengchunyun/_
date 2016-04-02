#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

from twisted.internet import protocol
from twisted.internet import reactor


class EchoServer(protocol.Protocol):  # 创建Protocol的派生类EchoServer
    def dataReceived(self, data):  # 重写父类dataReceived方法,当有接收到客户端发来数据时,会调用此方法,并将用户数据传入
        self.transport.write(bytes(str(data), "utf8"))  # 通过父类的transport的write方法,将接收到用户的输入,完全的发送给客户端,
        # 由于3.x的需要自己转换发送的数据类型,所以这里使用bytes转换成bytes数据类型


def main():  # 定义程序主函数
    factory = protocol.ServerFactory()  # 实例化ServerFactory类,ServerFactory继承了factory
    factory.protocol = EchoServer  # 重写factory类的protocol属性,将EchoServer类的地址赋给protocol
    reactor.listenTCP(8000, factory, interface="127.0.0.1")
    # print(type(reactor))  # 通过type打印出reactor的父类
    # twisted.internet.selectreactor.SelectReactor
    # 再进一步分析SelectReactor的父类twisted.internet.posixbase.PosixReactorBase下有一个
    # listenTCP方法(port, factory, backlog=50, interface=''),backlog代表最大listen队列为50
    # listenTCP下执行twisted.internet.tcp.Port类
    # PosixReactorBase又继承了父类twisted.internet.base._SignalReactorMixin,然后执行了该父类的run方法
    reactor.run()
    # run方法执行该类本身的startRunning方法,startRunning再调用ReactorBase类的startRunning方法
    # run方法再执行类本身的mainLoop方法
    # mainLoop方法则一直循环执行SelectReactor.doIteration(t)方法,该方法则调用了事件驱动select.select轮询事件
    # 当有可读事件时,执行self._doReadOrWrite方法,该方法通过反射器调用twisted.internet.tcp.Connection的doRead方法,通过该方法
    # 返回self._dataReceived(data),该方法定义了self.protocol.dataReceived(data),这个self.protocol就是我们
    # 这里定义的protocol.ServerFactory().protocol,然后执行dataReceived(data),这个方法已经被我们重写了,也就是我们listenTCP传入的factory
    # 执行factory.protocol.dataReceived(data) 等于执行EchoServer().dataReceived(data)方法


if __name__ == "__main__":
    main()
