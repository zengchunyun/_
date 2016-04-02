#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import redis

# r = redis.Redis(host="127.0.0.1", port=6379)
# r.set("name", "chunyun")
# r.get("name")


# r.set("id", "3")
# print(r.setbit("id", 1, bin(1)))
# print(r.getbit("id", 4))

pool = redis.ConnectionPool(host="127.0.0.1", port=6379)  # 创建连接池
r = redis.Redis(connection_pool=pool)

r.set("foo", "123")  # 添加key  为foo,值为123
print(r.get("foo"))

r.set("foo1", "234", ex=5, px=3, nx=True, xx=False)
print(r.get("foo1"))
"""
:ex 过期时间(秒)
:px 过期时间(毫秒)
:nx 如果设置为True,则只有name不存在时,当前set操作才执行
:xx 如果设置为True,则只有name存在时,当前set操作才执行
"""

r.setnx("foo2", "33")
print(r.get("foo2"))
# r.setex("foo3", )
print(r.get("foo3"))

r.psetex("foo", time_ms="", 3)

