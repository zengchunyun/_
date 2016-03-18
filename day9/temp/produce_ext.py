#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import threading
import time
import queue


def consumer(n):
    while True:
        print("\033[32;1mconsumer [%s] \033[0m get task: %s " % (n, q.get()))
        time.sleep(1)
        q.task_done()


def producer(n):
    count = 1
    while True:
        while True:
            # if q.qsize() < 3:
            print("producer [%s] produced a new task : %s" % (n, count))
            q.put(count)
            count += 1

            print("all task has been consumed by consumers ...")
            q.join()
            # if q.qsize() < 3:
            #     print("producer [%s] produced a new task : %s" % (n, count))
            #     q.put(count)
            #     count += 1
            #
            #     print("all task has been consumed by consumers ...")

q = queue.Queue()
c1 = threading.Thread(target=consumer, args=[1,])
c2 = threading.Thread(target=consumer, args=[2,])
c3 = threading.Thread(target=consumer, args=[3,])
c4 = threading.Thread(target=consumer, args=[4,])
c5 = threading.Thread(target=consumer, args=[5,])
c6 = threading.Thread(target=consumer, args=[6,])

p1 = threading.Thread(target=producer, args=["zeng",])
p2 = threading.Thread(target=producer, args=["chun",])
p3 = threading.Thread(target=producer, args=["yun",])


c1.start()
c2.start()
c3.start()
c4.start()
c5.start()
c6.start()
p1.start()
p2.start()
p3.start()


