#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import os
import sys

base_dir = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(base_dir)

if __name__ == "__main__":
    from core.ftpserver import main
    main()

