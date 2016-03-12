#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""


def initdb():
    """以下密码都是123,是根据用户名进行加密得到的,避免即使密码一样,但是用户名不同,得到的密码也不同
    :return:
    """
    import shelve
    create_database = shelve.open("database")
    user_info = {"oldboy": {"password": "484d81f3893c04df63dc6bd2aedc917c"},
                 "zengchunyun": {"password": "86a5897e933c466bb2b6c945845ab76b"}}
    create_database["data"] = user_info
    create_database.close()


if __name__ == "__main__":
    initdb()
