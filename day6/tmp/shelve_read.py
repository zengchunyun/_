#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

import shelve

d = shelve.open("shelve_test")
a = d.get("t1")  # 如果键值不存在返回None
print(a.n)


print(d.get("t2"))
t2 = d.get("t2")
print(t2.n)


import pickle


# f = open("pickle_test", "wb")
# pickle.dump(t2, f)
# pickle.dump(a, f)
# f.close()

f = open("pickle_test", "rb")
t2 = pickle.load(f)
print(t2)