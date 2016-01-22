#!/usr/bin/env python
# encoding:utf8
'''
Created on 2016年1月9日
@author: zengchunyun
'''


import copy

l1 = [10,'a1',[110,111],'ds',]
l2 = copy.copy(l1)

print(l1)
print(l2)
l1[1] = 11  #改变L1的值
l1[2][0] = 1111
print(l1)
print(l2)
print(id(l1))
print(id(l2))
print(id(l1[2][0]))
print(id(l2[2][0]))

import copy

l1 = [10,'a1',[110,111],'ds',]
l2 = copy.deepcopy(l1)

print(l1)
print(l2)
l1[1] = 11  #改变L1的值
l1[2][0] = 1111
print(l1)
print(l2)
print(id(l1))
print(id(l2))
print(id(l1[2][0]))
print(id(l2[2][0]))
# num = 110
# copynum = num
#
# print(id(num))
# print(id(copynum))
#
# a1 = 'hello'
# copya1 = a1
#
# print(id(a1))
# print(id(copya1))



# copy.copy()  # 浅拷贝


# copy.deepcopy()  # 深拷贝

# 赋值


# a1 = 111
# a2 = 111
# a1 = 'asas'
# a2 = 'asas'
# print(id(a1))
# print(id(a2))
# a3 = a2
# print(id(a3))
#
# a2 = copy.copy(a1)
# print(id(a2))
# a3 = copy.deepcopy(a2)
# print(id(a3))
#
# a1 = {1:'a', 2:'c',3: [1, 2, 3]}
# # print(id(a1))
#
# a2 = copy.copy(a1)
# # print(id(a2))
#
# a3 = copy.deepcopy(a2)
# # print(id(a3))
#
# print(id(a1[1]))
# print(id(a2[1]))
# print(id(a3[1]))
#
# print(id(a1[3]))
# print(id(a3[3]))
#
# print(id(a1[3][1]))
# print(id(a2[3][1]))
#
# print(id(a3[3][1]))


# cpuinfo = {
#     'cpu':[90,],
#     'mem':[80,],
# }
# print(cpuinfo)
# newa = copy.copy(cpuinfo)
# print(newa)
# newa['cpu'][0] = 22
# print(newa)
# print(cpuinfo)
#
# newa2 = copy.deepcopy(cpuinfo)
# newa2['cpu'][0] = 33
# print(newa2)
# print(cpuinfo)
#
# def mail():
#     a = 1
#     a += 1
#     print(a)
#
# mail()
#
# a = mail
# a()
#
# dict