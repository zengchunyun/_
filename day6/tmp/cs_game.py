#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""


class Role(object):  # 定义一个类,名为Role,继承基类object
    user_count = 0  # 类属性

    def __init__(self, name, role, weapon, life_value):  # 析构方法
        self.name = name  # 实例属性
        self.role = role
        self.weapon = weapon
        self.life_val = life_value

    def buy_weapon(self, weapon):  # 类方法
        print("%s is buying [%s]" % (self.name, weapon))
        self.weapon = weapon


# 创建两个实例
p1 = Role("Sanjiang", "Police", "b10", 90)  # 将一个类变成一个具体的对象的过程,叫做实例化
t1 = Role("Zengchunyun", "police", "AK47", 100)

import sys
exit()
sys.exit()


import subprocess
p = subprocess.Popen('fdisk -l',shell=True,stdout=subprocess.PIPE)
c = subprocess.Popen("sed -n '/Disk \/dev/p",shell=True,stdout=subprocess.PIPE,stdin=p.stdout)
c1 = subprocess.Popen("awk '/sd/{print $2}'",shell=True,stdout=subprocess.PIPE,stdin=c.stdout)
c2 = subprocess.Popen("awk -F':' '{print $1}']''",shell=True,stdout=subprocess.PIPE,stdin=c1.stdout)
print (c2.stdout.read())