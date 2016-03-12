#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import threading
import time


# def sayhi(num):
#     print("running on number: %s" % num)
#     time.sleep(3)
#
#
# if __name__ == "__main__":
#     t1 = threading.Thread(target=sayhi, args=(1,))
#     t2 = threading.Thread(target=sayhi, args=(2,))
#     t1.start()
#     t2.start()


#
# def sayhi(num):
#     print("running on number: %s" % num)
#     time.sleep(3)
#
#
# if __name__ == "__main__":
#     t1 = threading.Thread(target=sayhi, args=(1,))
#     t2 = threading.Thread(target=sayhi, args=(2,))
#     t1.start()
#     t2.setDaemon(True)
#     t2.start()
#
#     print(t1.getName())  # 调用self.name属性
#     print(t2.getName())  # 获取进程名
#     print(t1.is_alive())  # 打印进程是否运行  两个名称一样
#     print(t2.isAlive())  # 打印进程是否还运行着, 通过赋值,,将is_alive值给isAlive 变量
#     print(t1.name)  # 打印进程名  # 类封装成属性了
#     print(t1.daemon)
#     print(t2.daemon)  # 检查是否为守护进程


# def sayhi(num):
#     print("running on number: %s" % num)
#     time.sleep(3)
#
#
# class Mythread(threading.Thread):
#     def __init__(self, num):
#         threading.Thread.__init__(self)
#         self.num = num
#
#     def run(self):
#         print("running on number: %s" % self.num)
#         time.sleep(3)
#
#
# if __name__ == "__main__":
#     t1 = Mythread(1)
#     t2 = Mythread(2)
#     t1.start()
#     t2.start()



#
#
# def sayhi(num):
#     print("running on number: %s" % num)
#     time.sleep(3)
#
#
# class Mythread(threading.Thread):
#     def __init__(self, num):
#         threading.Thread.__init__(self)
#         self.num = num
#
#     def run(self):
#         print("running on number: %s" % self.num)
#         time.sleep(3)
#         return 2
#
#
# if __name__ == "__main__":
#     t1 = Mythread(1)
#     t2 = Mythread(2)
#     t1.setDaemon(True)  # 将主线程设置为Daemon线程,它退出时,其它子线程会同时退出,不管任务是否执行完成任务
#     t1.start()
#     t2.start()
#     print(t1.run())

j_list = []  # 将线程实例添加到里面
def foo(n):
    print("____running________" % n)
    time.sleep(2)
    print("done")

def main():
    for i in range(5):
        t = threading.Thread(target=foo, args=[i,])
        t.start()
        j_list.append(t)
    for t in j_list:
        t.join()  # 设置等待,可以设置超时时间,

