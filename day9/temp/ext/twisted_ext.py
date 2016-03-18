#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from twisted.internet import protocol
from twisted.internet import reactor


class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)


def main():
    factory = protocol.ServerFactory()
    factory.protocol = Echo

    reactor.listenTCP(1234, factory)
    reactor.run()

if __name__ == "__main__":
    main()