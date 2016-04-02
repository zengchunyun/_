#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import event_fram


class MyHandler(event_fram.BaseHandler):
    def execute(self):
        print("event driver execute MyHandler")


event_fram.event_list.append(MyHandler)
event_fram.run()
