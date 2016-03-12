#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

import subprocess

# stdout = subprocess.run("ifconfig", stdout=subprocess.PIPE)
# print(stdout.stdout)

# ret = subprocess.call("ifconfig")  #   打印返回结果
# print(ret)

ret = subprocess.Popen("python", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print(ret.stdin.write(b"print('hello')\n"))
print(ret.communicate())
