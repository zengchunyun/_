#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

#
# import shelve
#
# d = shelve.open('shelve_test') #打开一个文件
#
# class Test(object):
#     def __init__(self,n):
#         self.n = n
#
#
# t = Test(123)
# t2 = Test(123334)
#
# name = ["alex","rain","test"]
# d["test"] = name # 持久化列表
# d["t1"] = t      # 持久化类
# d["t2"] = t2
#
# d.close()


import shelve

new_shelve = shelve.open("shelve_file")  # 打开一个可持久化文件

d1 = {"k1": "v1", "k2":"v2"}  # 定义要存储的数据
l2 = ["1", '2', 3]

new_shelve["d1"] = d1  # 存取一个数据到shelve文件,定义格式为key,value形式
new_shelve["l2"] = l2
# new_shelve.close()  #


print(new_shelve.keys())
print(type(new_shelve.keys()))
print(new_shelve.values())
new_shelve['l3'] = ["110", 112]
test_l1 = new_shelve.get('l2')
print('l2' in new_shelve.keys())  # 判断对象是否存在'l2'键
print(list(new_shelve.keys()))  # 打印当前可持久化数据的键值
for k, v in new_shelve.items():  # 遍历数据
    print(k, v)
print(test_l1)
test_l1.append(33)  # 修改数据
print(test_l1)
new_shelve['l2'] = test_l1  # 改变可持续化里的数据

print(new_shelve['l2'])


