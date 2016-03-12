#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""


class UserVerify(object):
    def __init__(self, database):
        """
        :param database: 含有用户名密码的数据
        :return:
        """
        if type(database) == dict:
            self.database = database
        else:
            raise TypeError("must give a database type of  dict")
        self.user = None
        self.password = None

    def login(self, user, password):
        """
        :param user: 用户名
        :param password: 密码
        :return: 认证成功为真,否则不存在为None,存在为False
        """
        self.user = user
        self.password = password
        if self.user_check(self.user):
            if self.password_check(self.password):
                return True
            else:
                return False
        else:
            return None  # "user not exist"

    def register(self, user, password):
        """
        :param user: 用户名
        :param password: 密码
        :return: 如果注册成功,返回更新后的数据,否则假
        """
        self.user = user
        self.password = password
        if self.user_check(self.user):
            return False
        else:
            self.password = self.encode_password(self.user, password)
            self.database[self.user] = {"password": self.password}
            return self.database

    def user_check(self, user):
        """
        :param user: 用户名
        :return: 用户名存在则返回用户名对应的密码
        """
        if self.database.get(user):
            try:
                return self.database[user]["password"]
            except KeyError:
                return False

    def password_check(self, password):
        """
        :param password: 密码
        :return: 返回密码匹配结果
        """
        self.password = self.user_check(self.user)
        if self.password and self.password == self.encode_password(self.user, password):
            return True

    def encode_password(self, user, password):
        """
        :param user: 使用用户名作为hash参数,实现
        :param password:普通明文密码
        :return:加密密码
        """
        import hashlib
        self.user = user
        self.password = password
        md5 = hashlib.md5(str(self.user).encode("utf-8"))
        md5.update(str(self.password).encode("utf-8"))
        self.password = md5.hexdigest()
        return self.password
