#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
# from greenlet import greenlet
#
#
# def test1():
#     print 12
#     gr2.switch()
#     print 34
#     gr2.switch()
#
#
# def test2():
#     print 56
#     gr1.switch()
#     print 78
#
# gr1 = greenlet(test1)
# gr2 = greenlet(test2)
# gr1.switch()
#
#
# import gevent
#
# def foo():
#     print('Running in foo')
#     gevent.sleep(0)
#     print('Explicit context switch to foo again')
#
# def bar():
#     print('Explicit context to bar')
#     gevent.sleep(0)
#     print('Implicit context switch back to bar')
#
# gevent.joinall([
#     gevent.spawn(foo),
#     gevent.spawn(bar),
# ])


import time
import threading

