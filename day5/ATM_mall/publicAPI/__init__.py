#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

from account import UserInfo


def valid(code_length):  # 生存一个验证码,验证码长度由传入参数决定
            import random
            code = ""  # 初始化一个验证码
            for number in range(code_length):
                if number != random.randrange(1, 4):
                    temp_number = chr(random.randint(65, 90))
                else:
                    temp_number = random.randint(0, 9)
                code += str(temp_number)
            print("验证码:\033[35m{0}\033[0m\033[34m{1}\033[0m\033[33m{2}\033[0m\033[31m{3}\033[0m".format(
                    code[0], code[1], code[2], code[3]))
            return code  # 返回随机生成的验证码


def valid_code(code_func):  # 传入一个验证码功能和登陆授权功能的函数
    def valid_account(public_func):  # 传入添加了装饰器的函数名
        def login_auth(database=None, is_admin=False):  # 将上面函数所需要的参数放在这里
            temp_code = code_func(4)
            wait_code = str(input("请输入验证码:"))
            if str(wait_code).lower() == str(temp_code).lower():
                return public_func(database, is_admin)
            else:
                print('验证码输入错误 !!!')
                return None
        return login_auth
    return valid_account


@valid_code(valid)  # 对登录模块增加一个验证码功能
def auth_account(database, is_admin=False):
    user = str(input("请输入用户名:"))
    password = str(input("请输入密码:"))
    if is_admin:
        admin_name = user
    else:
        admin_name = None
    login_check = UserInfo(**database).login(user, password)
    if login_check:
        return admin_name
    else:
        return login_check


def add_admin_level():  # 添加管理级别定义,默认非字符串0级别的权限都是普通管理员
    level = str(input("请输入管理级别\n有两个级别\n\t1 代表普通管理员\n\t0 代表超级管理员\n\t默认为普通管理级别\n请输入:"))
    if level != "0":
        level = "1"
    return level


def add_common_info(is_admin):  # 额外的扩展信息
    common_info = {}  # 初始化一个空字典,存储用户基本信息
    if is_admin:  # 如果新建的用户是管理员,则增加级别功能定义
        common_info['level'] = add_admin_level()
    print("以下信息可选添加,如果不想输入,直接回车即可")
    mail = str(input("E-mail:"))
    age = str(input("Age:"))
    cn_name = str(input("中文姓名:"))
    en_name = str(input("English Name:"))
    birthday = str(input("出生年月:"))
    contact = str(input("手机号码:"))
    common_info['mail'] = mail
    common_info['age'] = age
    common_info['cn_name'] = cn_name
    common_info['en_name'] = en_name
    common_info['birthday'] = birthday
    common_info['contact'] = contact
    return common_info


def change_account_info(database, user, common_info):  # 变更用户的除用户名密码以外的信息
    return UserInfo(**database).change_info(user, **common_info)


def add_extra_info(register_func):  # 添加扩展信息的装饰器
    def add_info(database, is_admin=False):  # 传入的参数是一个字典
        before = database
        after = register_func(database)  # 得到增加用户后的字典
        if after:
            database = after
            update_user = set(before).symmetric_difference(set(after))  # 把增加的用户提取出来,更新
            add_user_info = add_common_info(is_admin)  # 针对该用户添加额外的补充用户信息
            if len(database) == 1 and is_admin:  # 当系统为第一次使用时,自动把权限提升为超级管理员级别
                add_user_info['level'] = "0"
            print("用户[%s]注册成功 !" % list(update_user)[0])
            return change_account_info(database, list(update_user)[0], add_user_info)
        else:
            return False
    return add_info


@add_extra_info  # 增加额外的扩展信息
def register_account(database):  # 传入一个字典的键值,也可以是一个空字典
    new_user = str(input("请输入新用户:"))
    new_password = str(input("请输入新密码:"))
    repeat_password = str(input("请再次输入密码:"))
    if new_password == repeat_password and new_password != "":  # 当两次输入密码一致,且密码不为空,才会进入数据库读取注册操作
        return UserInfo(**database).register(new_user, new_password)  # 调用公共的用户信息管理方法处理
    else:
        if new_password == "":
            print("密码不能为空 !!!")
        else:
            print("两次输入密码不一致 !!!")
        return False


def search_account_info(database, user):  # 返回指定用户的具体信息,如果不存在则不返回
    get_info = UserInfo(**database).change_info(user)
    if get_info:
        return get_info[user]


def change_password(database, user_name, password, new_password):  # 修改密码
    return UserInfo(**database).change_password(user=user_name, password=password, new_password=new_password)


def change_common_info():  # 修改扩展信息
    common_info = {}
    print("如果对于不想修改的信息,直接回车即可")
    mail = str(input("E-mail:"))
    age = str(input("Age:"))
    cn_name = str(input("中文姓名:"))
    en_name = str(input("English Name:"))
    birthday = str(input("出生年月:"))
    contact = str(input("手机号码:"))
    if mail:
        common_info['mail'] = mail
    if age:
        common_info['age'] = age
    if cn_name:
        common_info['cn_name'] = cn_name
    if en_name:
        common_info['en_name'] = en_name
    if birthday:
        common_info['birthday'] = birthday
    if contact:
        common_info['contact'] = contact
    return common_info  # 只返回需要更改的信息,以字典形式返回


def modify_admin_account_info(database):  # 任何管理员都能修改普通信息
    select_user = str(input("请输入要更改的用户名:"))
    if search_account_info(database, select_user):
        common_info = change_common_info()
        change_check = change_account_info(database, select_user, common_info)
        if change_check:
            return change_check


def is_super_admin(database, admin_name=None):  # 判断用户是不是超级管理员
    if admin_name and database[admin_name]['level'] == "0":
        return True
    else:
        return False


def add_admin_account(database, admin_name, is_admin=False):  # 添加管理员帐号
    if is_super_admin(database, admin_name):
        register_check = register_account(database, is_admin)
        if register_check:
            return register_check
    else:
        print("普通管理员[%s]没有权限修改管理员账号信息" % admin_name)
        return False


def is_last_super_admin(database):  # 传入一个字典,含有level的键值,
    super_count = 0
    for level in database.values():
        if level['level'] == "0":
            super_count += 1
    if super_count < 1:
        return True
    else:
        return False


def delete_account(database):
    select_user = str(input("请输入要删除的用户名:"))
    delete_check = UserInfo(**database).delete_account(select_user)
    if delete_check:
        if not is_last_super_admin(delete_check):
            wait_choose = str(input("确认删除[%s]吗 y/n:" % select_user))
            if wait_choose.lower() in ["y", "yes", ]:
                print("用户[%s]已被删除" % select_user)
                return delete_check
            else:
                print("操作未改变 !!!")
                return False
        else:
            print("管理员[%s]是最后一个具有超级管理权限的账号,操作不允许" % select_user)
            return False


def level_define(level):  # 将定义的数字级别功能转换成文字显示
    if str(level) == "0":
        level = "超级管理员"
    else:
        level = "普通管理员"
    return level


def change_admin_permission(database, admin_name):  # 更改管理员帐号权限
    if is_super_admin(database, admin_name):
        select_user = str(input("请输入要更改的用户名:"))
        if search_account_info(database, select_user):
            level = add_admin_level()
            wait_choose = str(input("确认修改[%s]权限修改为[%s]吗: y/n " % (select_user, level_define(level))))
            if wait_choose.lower() in ["y", "yes", ]:
                change_level_check = change_account_info(database, select_user, {'level': level})
                if change_level_check:
                    if is_last_super_admin(change_level_check):
                        print("管理员[%s]是最后一个具有超级管理权限的帐号,操作不允许" % select_user)
                        change_account_info(database, select_user, {'level': "0"})  # 回退权限
                        return False
                    else:
                        print("管理员[%s]级别已修改为[%s]" % (select_user, level_define(level)))
                        return change_level_check
            else:
                print("操作未改变 !!!")
                return False
    else:
        print("普通管理员[%s]没有权限修改管理员账号信息" % admin_name)
        return False


def change_admin_password(database, admin_name):
    if is_super_admin(database, admin_name):
        select_user = str(input("请输入要更改的用户名:"))
        account_info = search_account_info(database, select_user)
        if account_info:
            new_password = str(input("请输入新密码:"))
            repeat_password = str(input("请再次输入新密码:"))
            if new_password == repeat_password:
                old_password = account_info['password']
                change_admin_password_check = change_password(database, select_user, old_password, new_password)
                print("用户[%s]密码修改成功 !" % select_user)
                return change_admin_password_check
            else:
                print("两次输入不一致")
                return False
    else:
        old_password = str(input("请输入当前密码:"))
        new_password = str(input("请输入新密码:"))
        repeat_password = str(input("请再次确认新密码:"))
        if new_password == repeat_password and new_password != "":
            change_admin_password_check = change_password(database, admin_name, old_password, new_password)
            print("用户[%s]密码修改成功 !" % admin_name)
            return change_admin_password_check
        else:
            print("密码修改不成功 !")
            return False

