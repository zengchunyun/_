#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import sys
import os


base_dir = os.path.dirname(os.path.abspath(os.path.curdir))
sys.path.append(base_dir)


if __name__ == "__main__":
    from core.main import run
    run()


