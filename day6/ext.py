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
# def show(arg):
#     global gl_num
#     time.sleep(1)
#     gl_num +=1
#     print (gl_num)
#
# for i in range(10):
#     t = threading.Thread(target=show, args=(i,))
#     t.start()
#
# print('main thread stop')

# import threading
#
#
# def do(event):
#     print ('start')
#     event.wait()
#     print ('execute')
#
#
# event_obj = threading.Event()
# for i in range(10):
#     t = threading.Thread(target=do, args=(event_obj,))
#     t.start()
#
# event_obj.clear()
# inp = input('input:')
# if inp == 'true':
#     event_obj.set()



# from multiprocessing import Process
# from multiprocessing import Manager
#
# import time
#
# li = []
#
# def foo(i):
#     li.append(i)
#     print ('say hi',li)
#
# for i in range(10):
#     p = Process(target=foo,args=(i,))
#     p.start()
#
# print ('ending',li)


#
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


# import threading
# import time
#
# def show(arg):
#     time.sleep(0.3)
#     print ('thread'+str(arg))
#
# for i in range(10):
#     t = threading.Thread(target=show, args=(i,))
#     t.start()
#
# print ('main thread stop')


# from multiprocessing import Process import os
# def info(title): print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())
# def f(name): info('function f') print('hello', name)
# if __name__ == '__main__':
# info('main line')
# p = Process(target=f, args=('bob',)) p.start()
# p.join()
#
#
# from multiprocessing import Pool, process
# import time
#
#
# def Foo(i):
#     time.sleep(2)
#     return i+100
#
#
# def Bar(arg):
#     print (arg)
#
# pool = Pool(5)
# print(pool.apply(Foo,(1,)))
# print(pool.apply_async(func =Foo, args=(1,)).get())
#
# # for i in range(10):
# #     pool.apply_async(func=Foo, args=(i,),callback=Bar)
#
# # print('end')
# pool.close()
# pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
