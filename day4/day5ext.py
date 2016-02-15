#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import time
print(time.time())
print(time.altzone)
print(time.clock())
print(time.ctime())
print(time.daylight)
print(time.gmtime())
print(time.localtime())
print(time.monotonic())
print(time.timezone)
print(time.tzset())
print(time.tzname)
print(time.process_time())
print(time.struct_time)
print(time.perf_counter())
#
#
# def write_to_database(filename, string):
#     with open(filename, 'w') as wr_data:
#         wr_data.write('user_info = %s' % (json.dumps(string)))
#
# write_to_database('./config/settings.py', user_info)
# user_conf = open('./config/settings.py', 'r')
#
# temp_user_db = open('./config/account.db', 'wb')
# read_user_conf = user_conf.read()
# temp_user_db.write(pickle.dumps(read_user_conf))
# temp_user_db.close()
# #
# open_user_db = open('./config/account.db', 'rb')
# read_user_db = pickle.load(open_user_db)
# print(read_user_db)
# open_user_db.close()
#
#
# user_conf = open('./config/settings.py', 'r')
#
# temp_user_db = open('./config/account.db', 'w')
# read_user_conf = user_conf.read()
# temp_user_db.write(json.dumps(read_user_conf))
# temp_user_db.close()
# #
# open_user_db = open('./config/account.db', 'r')
# read_user_db = json.load(open_user_db)
# print(read_user_db)
# open_user_db.close()


# def myljust(str1, width, fillchar=None):
#     if fillchar == None:
#         fillchar = ' '
#     length = len(str(str1).encode('gb2312'))
#     fill_char_size = width - length if width >= length else 0
#     return "%s%s" % (str1, fillchar * fill_char_size)
#
#
# def myrjust(str1, width, fillchar=None):
#     if fillchar == None:
#         fillchar = ' '
#     length = len(str(str1).encode('gb2312'))
#     fill_char_size = width - length if width >= length else 0
#     return "%s%s" % (fillchar * fill_char_size, str1)
#
#
# def mycenter(str1, width, fillchar=None):
#     if fillchar == None:
#         fillchar = ' '
#     length = len(str(str1).encode('gb2312'))
#     fill_char_size = width - length if width >= length else 0
#     if length % 2 == 0:
#         return "%s%s%s" % (fillchar * (fill_char_size // 2), str1, fillchar * (fill_char_size // 2))
#     else:
#         return "%s%s%s" % (fillchar * (fill_char_size // 2 + 1), str1, fillchar * (fill_char_size // 2))
#
# string = "我爱你"
# print(myrjust(string,20))
# print(str(string).encode('gb2312').rjust(20))
#
# import hashlib
# m = hashlib.md5()
# m.update('748'.encode('utf-8'))
# print(m.hexdigest())rdre



# mybank = MyBank(**user_info['my_bank'])
# mybank.register_account(user='zcy', password=520)
# print(mybank.search_account_info("zcy"))
# userinfo = UserInfo(**user_info['account_info'])  # 将一个键为用户名,值为密码的字典数据传入该对象,并实例化一个对象
# userinfo.register(user='zcy', password='777', mail='dasaobing@748.com')
# newname = userinfo.register(user='学霸', password=520, mail='850808158@qq.com', tel=18710155115)
# if newname:  # 如果新增用户不存在,则返回新的用户数据字典
#     user_info['name'] = newname
#
# #
# update_info(user_info)
#
# new_info = userinfo.change_password(333, user='zcy', password=111, new_assword=777)
# if new_info:
#     print('改密成功')
# else:
#     print('改密失败')
# if new_info:  # 如果新增用户不存在,则返回新的用户数据字典
#     user_info['account_info'] = new_info
#
# update_info(user_info)
# if userinfo.login('学霸', '520'):
#     print("学霸登录成功")
# else:
#     print('登陆失败')
# print(userinfo.change_info('学霸'))



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