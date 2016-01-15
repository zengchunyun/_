#!/usr/bin/env python
# encoding:utf8
'''
Created on 2016年1月9日
@author: zengchunyun
'''

class Login(object):

    def __init__(self, filename):
        self.user = None  # 初始化用户名
        self.pwd = None  # 初始化密码
        self.db = filename  # 初始化数据读取文件

    def login(self, user, pwd):  # 用户登陆检查
        self.user = user
        self.pwd = pwd
        if not self.checkUser(self.user):  # 检查用户是否存在
            try:
                with open(self.db, 'r') as getInfo:
                    for info in getInfo.readlines():
                        if str(info).split()[0] == self.user and str(info).split()[1] == self.pwd:
                            return True  # 用户验证通过返回True
                    else:
                        print('用户名或密码错误 !!!')
                        return False
            except IndexError as i:
                print("数据存储格式错误 !!!", i)
                return False
        else:
            print('%s 该用户没有注册' % self.user)
            return False

    def register(self, user, pwd, ):  # 注册用户
        self.user = user
        self.pwd = pwd
        if self.checkUser(self.user):
            try:
                with open(self.db, 'a+') as writeInfo:
                    writeInfo.writelines("%s\t%s\n" % (self.user, self.pwd))
                    return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    def checkUser(self, user):  # 检查用户不存在则返回True
        self.user = user
        if self.user:
            try:
                with open(self.db, 'a+') as check:  # 以追加写读方式打开文件,防止文件不存在出现不想要的结果
                    check.seek(0)
                    for info in check.readlines():
                        if info != '\n':
                            if info.split()[0] == self.user:
                                return False
                    else:
                        return True
            except IndexError as i:
                print("数据存储格式错误 !!!", i)
                return False
        else:
            import os
            os.system('clear')
            print('用户名不能为空 !!!')
            return False
