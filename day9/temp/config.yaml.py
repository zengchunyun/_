#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import yaml


f = yaml.load(open("test.yaml"))
print(f)
print(type(f))
f['cmd'] = 'df'
yaml.dump(f, open('test.yaml', 'w'))

a = yaml.load("""
 - Hesperiidae
 - Papilionidae
 - Apatelodidae
 - Epiplemidae
 - float: True
""")
print(a)