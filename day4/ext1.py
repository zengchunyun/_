#!/usr/bin/env python
# coding:utf-8
"""
Created on 2016年1月9日
@author: zengchunyun
"""
# import fileinput

# name = iter(['alex', 'hello', 'assa'])  # 创建一个迭代器
# print(name)
# print(name.__next__())  # 通过next方法获取
# print(name.__next__())
# print(name.__next__())
# print(name.__next__())

# print('dddd', end='\t')
# print('sss')
#
# def cash_money(amount):
#     while amount > 0:
#         amount -= 100
#         yield 100
#         print('又来取钱了')
#
#
# atm = cash_money(500)
# print(type(atm))
# print(atm.__next__())
# print(atm.__next__())
# print('烦不烦啊')
# print('不烦')
# print(atm.__next__())

#
# def fei(num):
#     x, y = 0, 0
#     z = 1
#     while x < num:
#         print(z)
#         y, z = z, y + z
#         x = x + 1
#
#
# fei(9)
#
# def fei(num):
#     x, y, z = 0, 0, 1
#     while x < num:
#         if x == 0:
#             yield y
#         else:
#             yield z
#             y, z = z, y + z
#         x += 1
#
# print(fei(9).__next__())
# # fei(9).__next__()
# for i in fei(9):
#     print(i)
#

# import time
#
#
# def consumer(name):  # 定义消费者函数
#     print("%s 准备吃包子啦!" % name)  # 打印消费者名字
#     while True:
#        baozi = yield  # 当代码运行到这时,返回一个迭代器对象,当对象第二次调用时,会接收值并赋值给baozi
#        print("包子[%s]来了,被[%s]吃了!" % (baozi, name))  # 打印当前使用的迭代器对象,及接收的值
#
#
# def producer(*name):  # 定义一个生产者函数,并使用动态参数
#     if len(name) == 3:  # 当传入三个参数时,调用三次消费者函数方法
#         c = consumer(name[0])
#         c2 = consumer(name[1])
#         c3 = consumer(name[2])
#     c.__next__()  # 通过函数内置方法获取迭代器内部元素
#     c2.__next__()
#     c3.__next__()
#     print("老子开始准备做包子啦!")
#     for i in range(1, 11):
#         time.sleep(1)
#         print("做了%s个包子!" % len(name))
#         c.send(i)  # 通过迭代器方法的send属性给生成器传送值
#         c2.send(i)
#         c3.send(i)
#
# producer("alex", 'zengchunyun', 'peiqi')  # 创建一个生产者对象,并传入三个消费者名字



# def login(func):
#     def inner(arg):
#         print("welcome [%s] to home page " % arg)
#         # func(arg)  #将外面的参数传给func
#         return func(arg)  # 把func的返回值返回给外部调用
#
#     return inner  #返回这个方法,只返回一个函数地址,不执行内部代码
#
# def home(name):
#     print("welcome [%s] to home page ")
# @login
# def tv(name):
#     print("welcome [%s] to home page " %(name))
#
# def moive(name):
#     print("welcome [%s] to home page ")
#
#
# # tv = login(tv)
# tv('ff')


# def login(user, pwd):
#     print(user,pwd)
#
#
# def err(user,pwd):
#     print('err')
#
#
# def warr(before, after):
#     def realFunc(func):
#         def beginfunc(user,pwd):
#             before(user,pwd)
#             func(user,pwd)
#             after(user,pwd)
#
#         return beginfunc
#
#     return realFunc
#
#
# @warr(login, err)
# def index(user, pwd):
#     print('index')
#
# index('qq','ff')

#代码先走到warr,会先执行 warr函数,warr函数带两个参数,这两个参数由于是函数,且不是执行函数的方式 .所以只是预先加载该函数参数.
# warr函数返回后,返回一个realFunc函数,这个函数并不会去执行,只是返回一个函数地址,

#这时用户调用index时,会将index这个函数传入realFunc这个函数

#这时才是真正开始执行装饰器额外扩展功能,
#由于index是有参数的,所以beginfunc需要传两个参数进去,

# 最终执行warr的参数函数,以及调用的函数


# def calc(n):
#     print(n)
#     if n/2 > 1:
#         res = calc(n/2)
#         print('res',res)
#
#     print('N',n)
#     return n
#
# calc(10)



# 斐波那契算法

# def fei(arg1, arg2, stop):
#     if arg1 == 0:
#         print(arg1, arg2)
#     arg3 = arg1 + arg2
#     if arg3 < stop:
#         print(arg3)
#         fei(arg2, arg3, stop)
#
#
#
# fei(0, 1, 30)


#二分查找

# def binary_search(data_source, find_n):
#     mid = int(len(data_source) / 2)
#     if int(len(data_source) / 2) >= 1: #  data in left
#         if data_source[mid] > find_n:
#             binary_search(data_source[:mid], find_n)
#             print('data in left [%s]' % data_source[mid])
#
#         elif data_source[mid] < find_n:
#             binary_search(data_source[mid:], find_n)
#             print('data in right [%s]' % data_source[mid])
#         else:
#             print('found data %s ' % data_source[mid])
#     else:
#         print('can not found')
#
# if __name__ == '__main__':
#     data = list(range(600))
#     binary_search(data, 1)

# data = [[col for col in range(4)] for row in range(4)]
#
# for i in range(len(data)):
#     for j in data[i]:
#         print(j)
#         # temp = data[i][j]
#         data[i][j],data[j][i] = data[j][i],data[i][j]
#         # data[j][i] = temp
#
#
# for i in range(len(data)):
#     print(data[i])



# data = [[col for col in range(4)] for row in col]
# print(data)

    # express = "1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )a"
    # first = re.findall('[ \t\n\r\f\v]', express)
    # first = re.findall('[a-zA-Z]', express)
    # second = re.findall('\d|\W', express)
    # third = re.findall('\W', express)
    # print(first)
    # print(second)
    # print(third)
    # print(len(first))
    # print(len(second))
    # print(len(express))