#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import threading
import time


class CountdownThread(threading.Thread):
    def __init__(self, count):
        threading.Thread.__init__(self)
        self.count = count

    def run(self):
        while self.count > 0:
            print("Counting down", self.count)
            self.count -= 1
            time.sleep(5)
        return


# def countdown(n):
#     while n > 0:
#         print(n)
#         n -= 1
# print(time.ctime())
# COUNT = 100000000
#
# t1 = threading.Thread(target=countdown, args=(COUNT//2,))
# t2 = threading.Thread(target=countdown, args=(COUNT//2,))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# t1 = CountdownThread(COUNT)
# t2 = CountdownThread(COUNT)
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# countdown(COUNT)
# print(time.ctime())


# Ticks loosely map to interpreter instructions
# import dis
# print(dis.dis(CountdownThread))
#
# def sayhi(num):
#     print("running on number", num)
#     time.sleep(2)
#
# t1 = threading.Thread(target=sayhi, args=(1,))
# t2 = threading.Thread(target=sayhi, args=(2,))
# t1.start()
# t2.start()
# print(t1.getName())
# print(t2.getName())
#
#
# t1 = CountdownThread(1)
# t2 = CountdownThread(2)
# t1.start()
# t2.start()
#
# import time
# import threading
#
# def run(n):
#
#     print('[%s]------running----\n' % n)
#     time.sleep(2)
#     print('--done--')
#
# def main():
#     for i in range(5):
#         t = threading.Thread(target=run,args=[i,])
#         #time.sleep(1)
#         t.start()
#         t.join(1)
#         print('starting thread', t.getName())
#
#
# m = threading.Thread(target=main,args=[])
# m.setDaemon(True) #将主线程设置为Daemon线程,它退出时,其它子线程会同时退出,不管是否执行完任务
# m.start()
#m.join(timeout=2)
# print("---main thread done----")
#
#
# t = threading.Timer(20.0, sayhi, args=(1,))
# t.start()


# from multiprocessing import Pool
#
# def f(x):
#     return  x * x
#
# if __name__ == "__main__":
#     with Pool(5) as p:
#         print(p.map(f, [1, 2, 3]))

# from multiprocessing import Process
#
# def f(name):
#     print('hello', name)
# if __name__ == "__main__":
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()

#
# from multiprocessing import Process
# import os
#
# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print("process id:", os.getpid())
#
#
# def f(name):
#     info('function f')
#     print("hello", name)
#
# if __name__ == "__main__":
#     info("main line")
#     p = Process(target=f, args=("bob",))
#     p.start()
#     p.join()


# import multiprocessing as mp
#
# def foo(q):
#     q.put("hello")
#
# if __name__ == "__main__":
#     # mp.set_start_method("forkserver")
#     # q = mp.Queue()
#     # p = mp.Process(target=foo, args=(q,))
#     # p.start()
#     # print(q.get())
#     # p.join()
#     ctx = mp.get_context("spawn")
#     q = ctx.Queue()
#     p = ctx.Process(target=foo, args=(q,))
#     p.start()
#     print(q.get())
#     p.join()


from multiprocessing import Process, Queue

print("\uC854".encode("gbk"))
s = "哈哈"
ss = u'哈哈'

print(repr(s))
print(repr(ss))

print(s.decode('utf-8').encode('gbk'))
print(ss.encode('gbk'))

print(s.decode('utf-8'))
print(ss)