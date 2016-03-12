#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
mat = [[1,2,3], [4,5,6], [7,8,9]]
new_mat = [ [row[i] for row in mat] for i in [0,1,2] ] # 嵌套
print(new_mat)



def number(count):
    a, b = 1, 2
    c = b + 1
    while count > 0:
        c = b + 1
        yield c
        count -= 1


for i in number(4):
    print(i)