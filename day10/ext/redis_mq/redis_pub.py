#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from redis_common import RedisHelper

obj = RedisHelper()
obj.public('hello')  # 发布一条消息到频道fm104.5
