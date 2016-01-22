#!/usr/bin/env python
# encoding:utf8
'''
Created on 2016年1月9日
@author: zengchunyun
'''
set
# old_dict = {
#     "#1":{ 'hostname':1, 'cpu_count': 2, 'mem_capicity': 80 },
#     "#2":{ 'hostname':1, 'cpu_count': 2, 'mem_capicity': 80 },
#     "#3":{ 'hostname':1, 'cpu_count': 2, 'mem_capicity': 80 },
# }
#
# new_dict = {
#     "#1":{ 'hostname':1, 'cpu_count': 2, 'mem_capicity': 800 },
#     "#3":{ 'hostname':1, 'cpu_count': 2, 'mem_capicity': 80 },
#     "#4":{ 'hostname':2, 'cpu_count': 2, 'mem_capicity': 80 },
# }
#
# old = set(old_dict.keys())
# new = set(new_dict.keys())
#
# aa = old.difference(new)
# print(aa)
# update_set = old.intersection(new)
# print(update_set)
#
# delete_set = old.difference(update_set)
# print(delete_set)
#
# add_set = new.difference(update_set)
# print(add_set)
# #
# update_set = old.intersection(new)
# print(update_set)
# delete_set = old.symmetric_difference(update_set)   # 对称差
# print(delete_set)
# add_set = new.symmetric_difference(update_set)
# print(add_set)

# old = set(old_dict)
# new = set(new_dict)
# print(old)
# o1 = old.difference(new_dict)  # 新加入
# print(old)
# o2 = old.intersection(new_dict)  # 交集
# print(old)
# o3 = old.intersection_update(new_dict)
# print(old)
# print(o1)
# print(o2)
# print(o3)

import collections
# obj = collections.Counter('dshihogidodisgdihaahdoihdogfsf')
#
# ret = obj.most_common(2)
# print(ret)
# print(obj)
# # for e in obj.elements():
# #     print(e)
# for i in obj.items():
#     print(i)


MytupleClass = collections.namedtuple('MytupleClass',['x', 'y', 'z'])
# print(help(MytupleClass))
obj = MytupleClass(11,22,33)
print(obj.x)
print(obj.y)
print(obj.z)

myqueue = collections.deque([11,22,33,44])
myqueue.append(11)  #末尾追加
myqueue.appendleft(12)  # 向左添加
aa =  myqueue.count(11)  # 计数
print(aa)
myqueue.extend([13,14,55])  # 向右扩展
myqueue.extendleft([31,32,34])  #向左扩展
print(myqueue)
myqueue.rotate(1)  # 将队列末尾1个队列放到队列前,以此类推
print(myqueue)
print(myqueue.index(11))