#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor


class QOTDFactory(Factory):
    def buildProtocol(self, addr):
        return QOTD()


class QOTD(Protocol):
    def connectionMade(self):
        self.transport.write("An apple a day keeps the doctor away\r\n")
        self.transport.loseConnection()  # 这个loseConnection在write方法执行完后,会被立即调用\
        # 当所有的数据被Twisted write到系统外,也就是说全部发出去后,然后它会安全的使用transport写入开始lost,也就是
        # 开始执行关闭连接操作,如果一个生产者有在使用这个transport,loseConnection将只会关闭这个连接一次,

endpoint = TCP4ClientEndpoint(reactor, host="127.0.0.1", port=8007)
endpoint.listen(QOTDFactory())
reactor.run()