#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):  # 该方法调用是在执行run后立即执行的方法
        self.transport.write(bytes("hello zengchunyun", "utf8"))

    def dataReceived(self, data):  # 此方法最终调用与connectionMade类似,该方法是在服务器响应后执行的
        print("server said: {}".format(str(eval(data), "utf-8")))
        self.transport.loseConnection()  # 调用loseConnection(),程序会接收到一个异常处理,然后就执行connectionLost这个方法

    def connectionLost(self, reason):  # 该方法是因为执行了loseConnection()才会触发的
        print("connection lost")


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient  # ClientFactory方法继承父类factory,将父类protocol属性修改为EchoClient,也就是把一个类赋值给protocol

    def clientConnectionFailed(self, connector, reason):  # 重写了父类ClientFactory的方法
        print("Connection failed goodbye!")
        reactor.stop()  # 终止连接

    def clientConnectionLost(self, connector, reason):  # 重写了父类ClientFactory的方法
        print("Connection lost goodbye")
        reactor.stop()  # 终止连接


def main():
    f = EchoFactory()  # 实例化EchoFactory
    reactor.connectTCP("localhost", 8000, f)
    # twisted.internet.selectreactor.SelectReactor
    # 再进一步分析SelectReactor的父类twisted.internet.posixbase.PosixReactorBase调用了
    # connectTCP(self, host, port, factory, timeout=30, bindAddress=None):方法
    #
    #
    # 然后该方法执行twisted.internet.tcp.Connector(),由于这次传入的是client的ClientFactory,
    #
    reactor.run()  # 一直等待连接到指定的端口来
    # run方法执行该类本身的startRunning方法,startRunning再调用ReactorBase类的startRunning方法
    # run方法再执行类本身的mainLoop方法
    # mainLoop方法则一直循环执行SelectReactor.doIteration(t)方法,该方法则调用了事件驱动select.select轮询事件
    # 当有就绪事件时,执行self._doReadOrWrite方法,该方法根据角色类型,及这个程序角色为client,将此角色一块通过反射方式,
    # 执行twisted.internet.tcp.BaseClient().doConnect,再调用self._connectDone(),该方法调用self.protocol.makeConnection(self)
    # 然后这个方法又调用self.connectionMade(),由于这个方法已经被我们重写了,所以执行的是EchoClient().connectionMade()


if __name__ == "__main__":
    main()
