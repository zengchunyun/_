#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
# import threading
# import time
#
# gl_num = 0
#
#
# def show(arg):
#     global gl_num
#     time.sleep(1)
#     gl_num +=1
#     print(gl_num)
#
# for i in range(10):
#     t = threading.Thread(target=show, args=(i,))
#     t.start()
#
# print('main thread stop')


# import threading
# import time
#
# gl_num = 0
#
# lock = threading.RLock()
#
#
# def Func():
#     lock.acquire()
#     global gl_num
#     gl_num +=1
#     time.sleep(1)
#     print(gl_num)
#     lock.release()
#
# for i in range(10):
#     t = threading.Thread(target=Func)
#     t.start()


# import threading
#
#
# def do(event):
#     print('start')
#     event.wait()
#     print('execute')
#
#
# event_obj = threading.Event()
# for i in range(10):
#     t = threading.Thread(target=do, args=(event_obj,))
#     t.start()
#
# # event_obj.clear()
# inp = input('input:')
# if inp == 'true':
#     event_obj.clear()
#     print("please wait")
#     event_obj.set()


# from multiprocessing import Process
# import threading
# import time
#
# def foo(i):
#     print('say hi',i)
#     time.sleep(20)
#
# for i in range(10):
#     p = Process(target=foo,args=(i,))
#     p.start()

#
# from multiprocessing import Process
# from multiprocessing import Manager
#
# import time
#
# li = []
#
# def foo(i):
#     li.append(i)
#     print('say hi',li)
#     time.sleep(20)  # 多线程时.执行到这.都处于等待状态
#
# for i in range(10):
#     p = Process(target=foo,args=(i,))
#     p.start()
#
# print('ending',li)



# from multiprocessing import Process,Array
# temp = Array('i', [11,22,33,44])
#
# def Foo(i):
#     temp[i] = 100+i
#     for item in temp:
#         print(i,'----->',item)
#
# for i in range(4):
#     p = Process(target=Foo,args=(i,))
#     p.start()

# from multiprocessing import Process,Manager
#
# manage = Manager()
# dic = manage.dict()
#
# def Foo(i):
#     dic[i] = 100+i
#     print(dic.values())
#
# for i in range(2):
#     p = Process(target=Foo,args=(i,))
#     p.start()
#     p.join()


# from multiprocessing import Process, Array, RLock
#
# def Foo(lock,temp,i):
#     """
#     将第0个数加100
#     """
#     lock.acquire()
#     temp[0] = 100+i
#     for item in temp:
#         print(i, '----->', item)
#     lock.release()
#
# lock = RLock()
# temp = Array('i', [11, 22, 33, 44])
#
# for i in range(20):
#     p = Process(target=Foo, args=(lock,temp,i,))
#     p.start()


# from  multiprocessing import Process,Pool
# import time
#
# def Foo(i):
#     time.sleep(2)
#     return i+100
#
# def Bar(arg):
#     print(arg)
#
# pool = Pool(5)
# #print pool.apply(Foo,(1,))
# #print pool.apply_async(func =Foo, args=(1,)).get()
#
# for i in range(10):
#     pool.apply_async(func=Foo, args=(i,),callback=Bar)
#
# print('end')
# pool.close()
# pool.join()#进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。


# import queue
# import threading
# import time
# Queue=queue
# '''
# 这个简单的例子的想法是通过：
# 1、利用Queue特性，在Queue里创建多个线程对象
# 2、那我执行代码的时候，去queue里去拿线程！
# 如果线程池里有可用的，直接拿。
# 如果线程池里没有可用，那就等。
# 3、线程执行完毕，归还给线程池
# '''
#
# class ThreadPool(object): #创建线程池类
#     def __init__(self,max_thread=20):#构造方法，设置最大的线程数为20
#         self.queue = Queue.Queue(max_thread) #创建一个队列
#         for i in range(max_thread):#循环把线程对象加入到队列中
#             self.queue.put(threading.Thread)
#             #把线程的类名放进去，执行完这个Queue
#
#     def get_thread(self):#定义方法从队列里获取线程
#         return self.queue.get()
#
#     def add_thread(self):#定义方法在队列里添加线程
#         self.queue.put(threading.Thread)
#
# pool = ThreadPool(10)
#
# def func(arg,p):
#     print(arg)
#     time.sleep(2)
#     p.add_thread() #当前线程执行完了，我在队列里加一个线程！
#
# for i in range(300):
#     thread = pool.get_thread() #线程池10个线程，每一次循环拿走一个！默认queue.get()，如果队列里没有数据就会等待。
#     t = thread(target=func,args=(i,pool))
#     t.start()


#
# import queue
# obj = object() #object也是一个类，我创建了一个对象obj
#
# q = queue.Queue()
# for i in range(10):
#     print(id(obj))#看萝卜号
#     q.put(obj)

#
#
# import contextlib
# import threading
# import time
# import random
#
# doing = []
# def number(l2):
#     while True:
#         print(len(l2),"number")
#         print(threading.active_count(),"---------")
#         time.sleep(1)
#
# t = threading.Thread(target=number,args=(doing,))  #开启一个线程，每一秒打印列表，当前工作中的线程数量
# t.start()
#
#
# #添加管理上下文的装饰器
# @contextlib.contextmanager
# def show(li,iterm):
#     li.append(iterm)
#     yield
#     print("back", iterm)
#     print(threading.active_count(),"---------")
#     '''
#     yield冻结这次操作，就出去了，with就会捕捉到，然后就会执行with下的代码块，当with下的代码块
#     执行完毕后就会回来继续执行yield下面没有执行的代码块！
#     然后就执行完毕了
#     如果with代码块中的非常耗时，那么doing的长度是不是一直是1，说明他没执行完呢？我们就可以获取到正在执行的数量，当他with执行完毕后
#     执行yield的后续的代码块。把他移除后就为0了！
#     '''
#     li.remove(iterm)
#
#
# def task(arg):
#     with show(doing,1):#通过with管理上下文进行切换
#         print(len(doing),"task")
#         print(doing)
#         print(threading.active_count(),"---------")
#         time.sleep(3) #等待10秒这里可以使用random模块来操作~
#
# for i in range(10): #开启20个线程执行
#     print("thread+++++++++++++++++",i)
#     temp = threading.Thread(target=task,args=(i,))
#     temp.start()
#
#
# '''
# 作用：我们要记录正在工作的的列表
# 比如正在工作的线程我把加入到doing这个列表中，如果工作完成的把它从doing列表中移除。
# 通过这个机制，就可以获取现在正在执行的线程都有多少
# '''


# import multiprocessing as mp
# def foo(q):
#     q.put('hello')
# if __name__ == '__main__':
#     mp.set_start_method('spawn')
#     q = mp.Queue()
#     p = mp.Process(target=foo, args=(q,))
#     p.start()
#     print(q.get())
#     p.join()

# import time
# import os
#
# start = time.time()
# for i in range(1000):
#     pid = os.fork()
#     print(pid)
#     if pid == 0:
#         os._exit(0)
#
# print(time.time() - start) # 单位为秒


# import asyncio
#
# def hello_world(loop):
#     print("hello world")
#     # loop.stop()
#
# loop = asyncio.get_event_loop()
#
# loop.call_soon(hello_world, loop)
# loop.run_forever()
# loop.close()


import asyncio
try:
    from socket import socketpair
except ImportError:
    from asyncio.windows_utils import socketpair
# Create a pair of connected file descriptors
rsock, wsock = socketpair()
loop = asyncio.get_event_loop()


def reader():
    data = rsock.recv(100)
    print("Received:", data.decode())
    # We are done: unregister the file descriptor loop.remove_reader(rsock)
    #  Stop the event loop
    loop.stop()
# Register the file descriptor for read event
loop.add_reader(rsock, reader)
# Simulate the reception of data from the network
loop.call_soon(wsock.send, 'abc'.encode()) # Run the event loop
loop.run_forever()
# We are done, close sockets and the event loop
rsock.close()
wsock.close()
loop.close()
