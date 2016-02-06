#! /usr/bin/env python3

from account import UserInfo


class MyBank(object):
    def __init__(self, **kwargs):
        self.user = None  # 初始化用户名
        self.password = None  # 初始化密码
        self.new_password = None  # 初始化新密码,用于改密码
        self.user_auth_info = kwargs
        self.user_info = {}  # 用来存储对应的一个用户名的具体信息
        self.account_info = ()  # 一般只用来接收用户名和密码

    def search_account_info(self, *args, **kwargs):
        self.user_info = kwargs
        self.account_info = args
        try:
            self.user = self.user_info['user']
        except KeyError:
            try:
                self.user = self.account_info[0]
            except IndexError:
                print("必须传入一个参数作为用户名使用,或者字典包含键'user")
                return False
        get_info = UserInfo(**self.user_auth_info).change_info(self.user)
        if get_info:
            return get_info[self.user]

    def register_account(self, *args, **kwargs):
        self.user_info = kwargs
        self.account_info = args
        return UserInfo(**self.user_auth_info).register(*self.account_info, **self.user_info)

    def login(self, *args, **kwargs):
        self.user_info = kwargs
        self.account_info = args
        return UserInfo(**self.user_auth_info).login(*self.account_info, **self.user_info)

    def change_password(self, *args, **kwargs):
        self.user_info = kwargs
        self.account_info = args
        return UserInfo(**self.user_auth_info).change_password(*self.account_info, **self.user_info)
