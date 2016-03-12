#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import io

f = open("myfile.txt", "w", encoding="utf-8")
print(f)
f = io.StringIO("some initial text data")
print(f)
# f = io.open("myfile2.txt", "w")
f = io.FileIO("myfile2.txt")
print(f)

f = open("myfile.jpg", "wb")
print(f)
f = io.BytesIO(b"some initial binary data: \x00\x01")
print(f)
# f = io.BufferedReader(b"some")
# print(f)
import socket

# server = socket.socket()
# f = server.makefile("w").readable()
# f.readable()

import getpass
print(getpass.getuser())  # 获取环境变量里的LOGNAME,USER,LNAME,USERNAME

import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
print(code)
from abc import ABCMeta
from abc import abstractmethod


class Foo:
    def __getitem__(self, index):
        pass

    def __len__(self):
        pass

    def get_iterator(self):
        return iter(self)


class MyIterable(metaclass=ABCMeta):

    @abstractmethod
    def __iter__(self):
        while False:
            yield None

    def get_iterator(self):
        return self.__iter__()

    @classmethod
    def __subclasshook__(cls, C):
        if cls is MyIterable:
            if any("__iter__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

# MyIterable.register(Foo)

# print(Foo().get_iterator())
# import gc
#
# print(gc.isenabled())
#
import pwd
#
# print(pwd.getpwuid(0))
print(pwd.getpwnam("zengchunyun"))
# # print(pwd.getpwall())

import pwd
import crypt
import getpass
from hmac import compare_digest as compare_hash

def login():
    username = input('Python login: ')
    cryptedpasswd = pwd.getpwnam(username)[1]
    if cryptedpasswd:
        if cryptedpasswd == 'x' or cryptedpasswd == '*':
            raise ValueError('no support for shadow passwords')
        cleartext = getpass.getpass()
        return compare_hash(crypt.crypt(cleartext, cryptedpasswd), cryptedpasswd)


print(login())
# import crypt
# from hmac import compare_digest as compare_hash
# plaintext = input("python login:")
# hashed = crypt.crypt(plaintext)
# if not compare_hash(hashed, crypt.crypt(plaintext, hashed)):
#     raise ValueError("hashed version doesn't validate against original")
# print(hashed)
