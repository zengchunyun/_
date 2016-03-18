#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import queue
import threading
import time


message = queue.Queue()


def producer(i):
    while True:
        print("put in ", i)
        message.put(i)
        time.sleep(1)
        if i > 10:
            break


def consumer(i):
    while True:
        time.sleep(1)
        msg = message.get()
        print("get out", msg)


for i in range(2):
    t = threading.Thread(target=producer, args=(i,))
    t.start()

for i in range(10):
    t = threading.Thread(target=consumer, args=(i,))
    t.start()