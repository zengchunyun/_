#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""


def Foo(n):
    a, b = 0, 1
    while n > 0:
        if a ==0:
            a, b = b, a+b
            yield a

        else:
            yield a+b
            a, b = b, a+b
        n -= 1

for i in Foo(6):
    print(i)