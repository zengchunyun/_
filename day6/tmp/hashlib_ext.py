#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import hashlib
m = hashlib.md5()
m.update("hello".encode("utf-8"))
m.update(b"hee")
print(m.hexdigest())
