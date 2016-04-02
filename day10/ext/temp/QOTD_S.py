#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from twisted.protocols.basic import LineReceiver


class Answer(LineReceiver):
    answer = {'How are you?': 'Fine', None: "I don't know what you mean"}

    def lineReceived(self, line):
        if self.answer.has_key(line):
            self.sendLine(self.answer[line])
        else:
            self.sendLine(self.answer[None])