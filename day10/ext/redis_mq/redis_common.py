#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import redis


class RedisHelper(object):
    def __init__(self):
        self.__conn = redis.Redis(host="127.0.0.1")
        self.chan_pub = 'fm104.5'
        self.chan_sub = 'fm104.5'

    def public(self, msg):
        self.__conn.publish(self.chan_pub, message=msg)
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub
