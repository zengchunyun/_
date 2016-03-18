#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import os
import sys
import threading

base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(base_dir)


def auth_daemon():
    from modules.master_command import main
    main()


if __name__ == "__main__":
    auth = threading.Thread(target=auth_daemon)
    auth.start()
