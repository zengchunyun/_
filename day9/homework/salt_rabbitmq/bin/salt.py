#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import os
import sys
import time

base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(base_dir)


def auth_daemon():
    while True:
        from modules.master_daemon import AuthServe
        auth = AuthServe()  # 每次有新授权则进行实例化
        time.sleep(1)

if __name__ == "__main__":
    auth_daemon()