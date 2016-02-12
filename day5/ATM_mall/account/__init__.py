#! /usr/bin/env python3


class UserInfo(object):
    def __init__(self, **kwargs):  # 传入一个字典用户数据
        import hashlib
        self.hash = hashlib  # 新建一个hashlib对象
        self.md5 = None  # 初始化md5变量
        self.user = None  # 初始化用户名
        self.password = None  # 初始化密码
        self.new_password = None  # 初始化新密码,用于改密码
        self.flag = False  # 用于辅助条件判断的变量
        self.user_info = {}  # 用来存储对应的一个用户名的具体信息
        self.account_info = ()  # 一般只用来接收用户名和密码
        self.user_auth_info = kwargs  # 一个用于记录所有用户名密码信息的字典

    def encode_password(self, password, md5_str="zcy850808158"):  # 将密码进行MD5加密
        self.md5 = self.hash.md5(str(md5_str).encode('utf-8'))
        self.md5.update(str(password).encode('utf-8'))
        return self.md5.hexdigest()  # 返回加密后的密码

    def login(self, *args, **kwargs):  # 用来验证用户账户信息
        self.user_info = kwargs  # 接收用户的具体信息,也可能包括账号密码
        self.account_info = args  # 只接收用户的用户名密码
        self.flag = False  # 每次调用前先初始化一次
        try:
            self.user = self.user_info['user']
        except KeyError:
            try:
                self.user = self.account_info[0]
                self.flag = True
            except IndexError:
                print("必须传入一个参数作为用户名使用,或者字典包含键'user")
                return False
        try:
            self.password = self.user_info['password']
        except KeyError:
            try:
                if self.flag:
                    self.password = self.account_info[1]
                else:
                    self.password = self.account_info[0]
            except IndexError:
                print("必须传入一个参数作为密码使用,或者字典包含键'password")
                return False
        if self._user_exist():
            try:
                if self.user_auth_info[self.user]['password'] == self.encode_password(self.password):
                    return True
                else:
                    return False
            except KeyError:
                return False
        else:
            return False

    def register(self, *args, **kwargs):  # 注册用户信息
        self.user_info = kwargs  # 初始化新用户信息
        self.account_info = args
        self.flag = False  # 每次调用该方法都进行初始化一次
        try:  # 尝试把键'user'的值赋值给用户名,并删除对应的键
            self.user = self.user_info['user']
            self.user_info.pop('user')
        except KeyError:  # 如果字典里没有这个user键,就尝试把第一个参数给用户名,并将flag标记为True
            try:
                self.user = self.account_info[0]
                self.flag = True  # 如果字典不存在user键,则标记一下
            except IndexError:
                print("必须传入一个参数作为用户名使用,或者字典包含键'user")
                return False
        try:  # 尝试把键'password'的值赋值给密码,并删除对应的键
            self.password = self.user_info['password']
            self.user_info.pop('password')
        except KeyError:
            try:
                if self.flag:
                    self.password = self.account_info[1]
                else:
                    self.password = self.account_info[0]
            except IndexError:
                print("必须传入一个参数作为密码使用,或者字典包含键'password")
                return False
        if not self._user_exist():  # 如果这个用户之前没有注册,则把这个原来的用户字典信息更新,添加新用户
            if self.password == "":
                print("为了账户的安全性,拒绝使用空密码")
                return False
            self.user_info['password'] = self.encode_password(self.password)
            self.user_auth_info[self.user] = self.user_info
            return self.user_auth_info  # 返回更新后的用户字典信息
        else:
            print("用户已存在,如果忘记密码,请联系工作人员找回 !!!")
            return False

    def change_password(self, *args, **kwargs):  # 修改用户的密码
        self.user_info = kwargs  # 用来接收用户名密码信息
        self.account_info = args  # 用来接收用户名密码信息
        self.flag = False
        try:
            self.user = self.user_info['user']
        except KeyError:
            try:
                self.user = self.account_info[0]
                self.flag = True
            except IndexError:
                print("必须传入一个参数作为用户名使用,或者字典包含键'user")
                return False
        try:
            if self.user_info.get('new_password'):
                self.new_password = self.user_info['new_password']
            self.password = self.user_info['password']
            if not self.new_password:
                if self.flag:
                    self.new_password = self.account_info[1]
                else:
                    self.new_password = self.account_info[0]
        except KeyError:
            try:
                if self.flag:
                    self.password = self.account_info[1]
                    if not self.new_password:
                        self.new_password = self.account_info[2]
                else:
                    self.password = self.account_info[0]
                    if not self.new_password:
                        self.new_password = self.account_info[1]
            except IndexError:
                if self.password:
                    print("必须传入一个参数作为新密码使用,或者字典包含键'new_password'")
                else:
                    print("必须传入一个参数作为旧密码使用,或者字典包含键'password'")
                return False
        except IndexError:
            print("必须传入一个参数作为新密码使用,或者字典包含键'new_password'")
            return False
        if len(self.password) == 32:
            if self.user_auth_info[self.user]['password'] == self.password:
                self.user_auth_info[self.user]['password'] = self.encode_password(self.new_password)
        elif self.login(self.user, self.password):  # 如果老密码验证成功,则进行修改新密码
            self.user_auth_info[self.user]['password'] = self.encode_password(self.new_password)
            return self.user_auth_info  # 返回更新后的用户字典信息

    def change_info(self, *args, **kwargs):  # 只变更用户的普通信息,不包括用户名密码,变更信息只能是字典格式
        self.user_info = kwargs  # 初始化新用户信息
        self.account_info = args  # 只接收用户名密码信息
        self.flag = False  # 每次调用该方法都进行初始化一次
        try:
            self.user = self.user_info['user']
            self.user_info.pop('user')
        except KeyError:
            try:
                self.user = self.account_info[0]
            except IndexError:
                print("必须传入一个参数作为用户名使用,或者字典包含键'user")
                return False
        if not self._user_exist():
            print('该用户不存在 !!!')
            return False
        if self.user_info.get('password'):
            self.user_info.pop('password')
        self.user_auth_info[self.user].update(self.user_info)
        return self.user_auth_info

    def delete_account(self, *args, **kwargs):  # 删除用户,如果没有字典形式的用户名,则取第一个参数作为用户名
        self.user_info = kwargs
        self.account_info = args
        if self.user_info.get('user'):
            self.user = self.user_info['user']
        else:
            try:
                self.user = self.account_info[0]
            except IndexError:
                print("必须传入一个参数作为用户名使用,或者字典包含键'user")
                return False
        if self._user_exist():  # 检查用户是否存在,存在则删除
            self.user_auth_info.pop(self.user)
            return self.user_auth_info
        else:
            print('该用户不存在 !!!')
            return False

    def _user_exist(self):  # 内部调用方法,用来检查该用户是否存在
        if self.user_auth_info.get(self.user):
            return True
        else:
            return False
