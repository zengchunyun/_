#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import threading
import time


def say(msg):
    print("say :{}".format(msg))
    time.sleep(2)

t = threading.Thread(target=say, args=(1,))  # 函数不能加括号,参数必须用逗号分隔
t.start()

print("over ???")  # 程序并未在运行到这段代码时结束


def say(msg):
    print("say :{}".format(msg))
    time.sleep(2)

t = threading.Thread(target=say, args=(1,))
t.start()
t.join()

print("game over")  # 通过join实现wait方式,最终执行完这段代码就结束了


class MyThread(threading.Thread):
    def __init__(self, msg):
        threading.Thread.__init__(self)  # 经典类继承
        # super(MyThread, self).__init__(self)
        self.msg = msg

    def run(self):  # 必须在类中实现一个这个RUN方法,为线程start调用
        time.sleep(2)
        print(self.msg)

t = MyThread('hello')
t.start()


for i in range(10):
    t = threading.Thread(target=say, args=(i,))
    t.start()

print("程序执行到这,未结束")


t_list = []  # 创建一个空列表,将线程实例加入进去
for i in range(10):
    t = threading.Thread(target=say, args=(i,))
    t_list.append(t)
    t.start()
    print(t.getName())  # 获取线程名


for i in t_list:
    i.join()

print("程序执行到这,结束了")



#线程锁
num = 100
lock = threading.Lock()


def addNum():
    global num
    print("get num {}".format(num))
    time.sleep(2)  # 如果锁加在这,程序将等待200秒
    lock.acquire()  # 加上锁,实际上变成串行运行
    num -= 1
    lock.release()  # 释放锁

t_list = []

for i in range(100):
    t = threading.Thread(target=addNum)
    t.start()
    t_list.append(t)


for i in t_list:
    i.join()  # 阻塞,等待

print("程序运行结束,num = [{}]".format(num))



#红绿灯
event = threading.Event()
def car(n):
    while True:
        time.sleep(1)
        if event.isSet():  # 绿灯
            print("car [%s] is running.." % n)
        else:
            print("car [%s] is waiting for the red light..." % n)
            event.wait()

def light():
    if not event.isSet():
        event.set()  # wait 就不阻塞, # 绿灯状态
    count = 0
    while True:
        if count < 10:
            print("\033[42;1m---green light on ---\033[0m")
        elif count < 13:
            print("\033[43;1m---yellow light on ---\033[0m")
        elif count < 20:
            if event.isSet():
                event.clear()
            print("\033[41;1m---red light on ---\033[0m")
        else:
            count = 0
            event.set()  # 打开绿灯
        time.sleep(1)
        count += 1

if __name__ == "__main__":
    event = threading.Event()
    Light = threading.Thread(target=light)
    Light.start()

    for i in range(3):
        t = threading.Thread(target=car, args=(i,))
        t.start()


