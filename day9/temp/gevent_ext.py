#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import gevent


def foo():
    print("\033[32;1m running in foo\033[0m")
    gevent.sleep(1)
    print("\033[32;1mExplicit context switch\033[0m")


def bar():
    print("Explicit context to bar")
    gevent.sleep(1)
    print("Implicit context switch back to bar")


def ex():
    print("runing ex now ")
    gevent.sleep(2)
    print("implicit ex now")


gevent.joinall([gevent.spawn(foo),
               gevent.spawn(bar),
               gevent.spawn(ex)]
               )