#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from twisted.internet import reactor
from twisted.internet import protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(bytes("hello zengchunyun", "utf8"))

    def dataReceived(self, data):
        print("server said: {}".format(data))
        self.transport.loseConnection()

    def connectionLost(self, reason):
        print("Connection lost")


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye")
        reactor.stop()


def main():
    f = EchoFactory()
    reactor.connectTCP("localhost", 1234, f)
    reactor.run()


if __name__ == "__main__":
    main()