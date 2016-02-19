#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

from account import UserInfo
from record_log import Logger
from calc_credit import get_diff_days


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
        def login_auth(database=None, is_admin=False, log_file=None):  # 将上面函数所需要的参数放在这里
            temp_code = code_func(4)
            wait_code = str(input("请输入验证码:")).strip()
            if str(wait_code).lower() == str(temp_code).lower():
                return public_func(database, is_admin, log_file)
            else:
                print('验证码输入错误 !!!')
                return None
        return login_auth
    return valid_account


@valid_code(valid)  # 对登录模块增加一个验证码功能
def auth_account(database, is_admin=False, log_file=None):
    user = str(input("请输入用户名:")).strip()
    password = str(input("请输入密码:")).strip()
    import time
    today = time.strftime("%Y-%m-%d", time.localtime())
    start_time = None
    last_login_time = None
    if not is_admin:
        get_database = search_account_info(database, user)
        if type(get_database) == dict:
            if get_database.get("user_status"):
                if get_database["user_status"] == "1":
                    print("该用户已被冻结,请联系工作人员解锁 !!")
                    Logger(log_file).write_log(user=user, status=False, event="用户登陆失败")
                    return False
                if get_database.get("status_time"):  # 尝试获取最后一次解锁时间
                    start_time = get_database["status_time"]
                get_match_list = Logger(log_file).get_match_log(user=user, status="login")  # 获取登陆成功的日志
                if get_match_list:
                    last_login = get_match_list[-1]
                    last_login_time = " ".join(last_login.split()[0:2])  # 获取最后一次登陆成功的时间
                if start_time and last_login_time:  # 当既有解锁时间,又有成功登陆时间,则比较大小
                    if start_time < last_login_time:  # 如果登陆时间比解锁时间晚,则登陆时间赋值start_time
                        start_time = last_login_time
                elif last_login_time:  # 否则,如果只有登陆时间,则也赋值给start_time
                    start_time = last_login_time
                if start_time and start_time < today:
                    start_time = today
                if get_database["user_status"] == "0" and Logger(log_file).get_match_count(
                        user=user, status=False, start_time=start_time) > 2:
                    print("该用户已被锁定,请联系工作人员解锁,或第二天再次尝试!")
                    Logger(log_file).write_log(user=user, status=False, event="用户登陆失败")
                    return False
        else:
            return False
    login_check = UserInfo(**database).login(user, password)
    if login_check and is_admin:  # 如果登陆成功,且是管理员身份登陆,则返回当前管理员用户名
        Logger(log_file).write_log(user=user, status=True, event="管理员登陆成功")
        return user
    else:
        if login_check:
            Logger(log_file).write_log(user=user, status="login", event="用户登陆成功")
            return user
        else:
            print("用户名或密码错误")
            Logger(log_file).write_log(user=user, status=False, event="用户登陆失败")
            if not is_admin:
                get_database = search_account_info(database, user)
                if type(get_database) == dict:
                    error_count = Logger(log_file).get_match_count(user=user, status=False, start_time=start_time)
                    if error_count > 2:
                        get_database = lock_account(database, user, log_file=log_file)
                        print("该用户已被锁定,请联系工作人员解锁,或第二天再次尝试!")
                        return get_database
            return False


def lock_account(database, user, log_file=None, user_status="0"):  # 锁定账户
    get_database = UserInfo(**database).change_info(user, user_status=user_status)
    if get_database:
        Logger(log_file).write_log(user=user, status="lock", event="用户已被冻结")
        return get_database
    else:
        return False


def unlock_account(database, user, log_file=None):  # 解锁账户
    import time
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    Logger(log_file).write_log(user=user, status="unlock", event="用户解锁成功")
    return UserInfo(**database).change_info(user=user, user_status="2", status_time=cur_time)


def add_admin_level():  # 添加管理级别定义,默认非字符串0级别的权限都是普通管理员
    level = str(input("请输入管理级别\n有两个级别\n\t1 代表普通管理员\n\t0 代表超级管理员\n\t默认为普通管理级别\n请输入:")).strip()
    if level != "0":
        level = "1"
    return level


def add_credit_limit():
    credit_limit = 0
    while True:
        credit_limit = str(input("请输入该用户信用额度:")).strip()
        if credit_limit.isdigit():
            break
        else:
            print("输入错误,金额只能是数字形式")
    return credit_limit


def add_statement_date(string="账单日"):
    import time
    while True:
        statement_date = time.strftime("%m-%d", time.localtime())
        try:
            statement_date = str(input("请输入%s\n格式:%s\n请输入:" % (string, statement_date))).strip()
            time.strptime(statement_date, "%m-%d")
            return statement_date
        except ValueError:
            continue


def add_common_info(is_admin=False):  # 额外的扩展信息
    common_info = {}  # 初始化一个空字典,存储用户基本信息
    if is_admin:  # 如果新建的用户是管理员,则增加级别功能定义
        common_info['level'] = add_admin_level()
    print("以下信息可选添加,如果不想输入,直接回车即可")
    mail = str(input("Email地址:")).strip()
    age = str(input("年龄:")).strip()
    cn_name = str(input("中文姓名:")).strip()
    en_name = str(input("English Name:")).strip()
    birthday = str(input("出生年月:")).strip()
    contact = str(input("手机号码:")).strip()
    if not is_admin:
        common_info["credit_limit"] = add_credit_limit()  # 信用额度
        common_info["company"] = str(input("单位全称:")).strip()
        user_status = str(input("是否激活账户\n\t1\t不激活\n\t2\t激活\n默认激活\n请选择: ")).strip()
        if user_status not in ["1", "2"]:
            user_status = "2"
        common_info["user_status"] = user_status  # 用户状态
        common_info["available_credit"] = common_info["credit_limit"]  # 可用额度
        common_info["cash_advance_limit"] = str(round(float(common_info["credit_limit"]) / 2, 2))  # 可借现金
        common_info["statement_date"] = str(add_statement_date("账单日"))  # 账单日
        common_info["payment_due_date"] = str(add_statement_date("到期还款日"))  # 到期还款日
        common_info["new_balance"] = "0.00"  # 本期还款总额
        common_info["balance"] = "0.00"  # 上期账单金额
        common_info["payment"] = "0.00"  # 上期还款金额
        common_info["new_charges"] = "0.00"  # 本期账单金额
        common_info["adjustment"] = "0.00"  # 本期调整金额
        common_info["interest"] = "0.00"  # 循环利息
        common_info["current_balance"] = "0.00"  # 本期应还金额
        common_info["minimum_payment"] = "0.00"  # 最低还款额
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
    def add_info(database, is_admin=False, log_file=None, is_shop_user=False):  # 传入的参数是一个字典
        """
        :param database: 含有用户信息的字典
        :param is_admin: 是否是管理员
        :param log_file: 日志文件名
        :param is_shop_user: 是否商城用户
        :return:
        """
        before = database
        after = register_func(database)  # 得到增加用户后的字典
        if is_shop_user:  # 如果是商城用户注册,直接返回
            return after
        if after:
            database = after
            update_user = set(before).symmetric_difference(set(after))  # 把增加的用户提取出来,更新
            add_user_info = add_common_info(is_admin)  # 针对该用户添加额外的补充用户信息
            if len(database) == 1 and is_admin:  # 当系统为第一次使用时,自动把权限提升为超级管理员级别
                add_user_info['level'] = "0"
            print("用户[%s]注册成功 !" % list(update_user)[0])
            Logger(log_file).write_log(user=list(update_user)[0], status=True, event="用户注册成功")
            return change_account_info(database, list(update_user)[0], add_user_info)
        else:
            Logger(log_file).write_log(status=False, event="用户注册失败")
            return False
    return add_info


@add_extra_info  # 增加额外的扩展信息
def register_account(database, is_admin=False, log_file=None, is_shop_user=False):  # 传入一个字典的键值,也可以是一个空字典
    new_user = str(input("请输入新用户:")).strip()
    new_password = str(input("请输入新密码:")).strip()
    repeat_password = str(input("请再次输入密码:")).strip()
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
    else:
        return False


def change_password(database, user_name, password, new_password):  # 修改密码
    return UserInfo(**database).change_password(user=user_name, password=password, new_password=new_password)


def change_common_info(is_admin=False):  # 修改扩展信息
    common_info = {}
    print("如果对于不想修改的信息,直接回车即可")
    mail = str(input("Email地址:")).strip()
    age = str(input("年龄:")).strip()
    cn_name = str(input("中文姓名:")).strip()
    en_name = str(input("English Name:")).strip()
    birthday = str(input("出生年月:")).strip()
    contact = str(input("手机号码:")).strip()
    if not is_admin:
        company = str(input("单位全称:")).strip()
        if company:
            common_info["company"] = company
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


def modify_admin_account_info(database, admin_name, is_admin=False, log_file=None):  # 任何管理员都能修改普通信息
    select_user = str(input("请输入要更改的用户名:")).strip()
    if search_account_info(database, select_user):
        common_info = change_common_info(is_admin)
        change_check = change_account_info(database, select_user, common_info)
        if change_check:
            Logger(log_file).write_log(user=admin_name, status=True, event="用户%s信息修改成功" % select_user)
            return change_check


def is_super_admin(database, admin_name=None):  # 判断用户是不是超级管理员
    if admin_name and database[admin_name]['level'] == "0":
        return True
    else:
        return False


def add_admin_account(database, admin_name, is_admin=False, log_file=None):  # 添加管理员帐号
    if is_super_admin(database, admin_name):
        register_check = register_account(database, is_admin, log_file=log_file)
        if register_check:
            return register_check
    else:
        print("普通管理员[%s]没有权限修改管理员账号信息" % admin_name)
        return False


def is_last_super_admin(database):  # 传入一个字典,含有level的键值,
    super_count = 0
    if not database:
        return True
    for level in database.values():
        if type(level) == dict:
            if level.get('level') and level["level"] == "0":
                super_count += 1
    if super_count < 1:
        return True
    else:
        return False


def delete_account(database, admin_name, is_admin=False, log_file=None):
    select_user = str(input("请输入要删除的用户名:")).strip()
    delete_check = UserInfo(**database).delete_account(select_user)  # 如果返回的不是字典,则说明不存在该用户
    if not is_last_super_admin(delete_check) or (not is_admin and type(delete_check) == dict):
        wait_choose = str(input("确认删除[%s]吗 y/n:" % select_user)).strip()
        if wait_choose.lower() in ["y", "yes", ]:
            print("用户[%s]已被删除" % select_user)
            Logger(log_file).write_log(user=admin_name, status=True, event="用户%s删除成功" % select_user)
            return delete_check
        else:
            print("操作未改变 !!!")
            return False
    elif type(delete_check) == dict:
        print("管理员[%s]是最后一个具有超级管理权限的账号,操作不允许" % select_user)
        Logger(log_file).write_log(user=admin_name, status=False, event="用户%s删除失败" % select_user)
        return False


def level_define(level):  # 将定义的数字级别功能转换成文字显示
    if str(level) == "0":
        level = "超级管理员"
    else:
        level = "普通管理员"
    return level


def user_status_define(status):
    if str(status) == "1":
        status = "未激活"
    elif str(status) == "2":
        status = "激活"
    else:
        status = "锁定"
    return status


def change_admin_permission(database, admin_name, log_file=None):  # 更改管理员帐号权限
    if is_super_admin(database, admin_name):
        select_user = str(input("请输入要更改的用户名:")).strip()
        if search_account_info(database, select_user):
            level = add_admin_level()
            wait_choose = str(input("确认修改[%s]权限修改为[%s]吗: y/n " % (select_user, level_define(level)))).strip()
            if wait_choose.lower() in ["y", "yes", ]:
                change_level_check = change_account_info(database, select_user, {'level': level})
                if change_level_check:
                    if is_last_super_admin(change_level_check):
                        print("管理员[%s]是最后一个具有超级管理权限的帐号,操作不允许" % select_user)
                        Logger(log_file).write_log(user=admin_name, status=False, event="用户%s权限修改失败" % select_user)
                        change_account_info(database, select_user, {'level': "0"})  # 回退权限
                        return False
                    else:
                        print("管理员[%s]级别已修改为[%s]" % (select_user, level_define(level)))
                        Logger(log_file).write_log(user=admin_name, status=True, event="用户%s权限修改成功,级别已修改为[%s]" % (select_user,level_define(level)))
                        return change_level_check
            else:
                print("操作未改变 !!!")
                return False
    else:
        print("普通管理员[%s]没有权限修改管理员账号信息" % admin_name)
        Logger(log_file).write_log(user=admin_name, status=False, event="操作不允许")
        return False


def change_user_credit_line(database, admin_name, log_file=None):
    select_user = str(input("请输入要修改信用额度的用户名: ")).strip()
    credit_limit = add_credit_limit()
    current_info = search_account_info(database, select_user)
    if type(current_info) == dict:
        current_credit_limit = database[select_user]["credit_limit"]
        current_available_credit = database[select_user]["available_credit"]
        current_cash_advance_limit = database[select_user]["cash_advance_limit"]
        if current_credit_limit == current_available_credit:
            current_available_credit = credit_limit
            current_cash_advance_limit = str(float(credit_limit) / 2)
        get_database = change_account_info(database, select_user, {"credit_limit": credit_limit,
                                                                   "cash_advance_limit": current_cash_advance_limit,
                                                                   "available_credit": current_available_credit})
        if get_database:
            print("用户额度修改成功,目前该用户额度为[%s]" % credit_limit)
            Logger(log_file).write_log(user=admin_name, status=True, event="用户%s额度修改成功,额度已修改为[%s]" % (select_user, credit_limit))
            return get_database
    else:
        Logger(log_file).write_log(user=admin_name, status=False, event="用户%s不存在,修改额度失败" % select_user)
        return False


def for_super_admin_change_password(database, admin_name, log_file=None):
    select_user = str(input("请输入要更改的用户名:")).strip()
    account_info = search_account_info(database, select_user)
    if account_info:
        new_password = str(input("请输入新密码:")).strip()
        repeat_password = str(input("请再次输入新密码:")).strip()
        if new_password == repeat_password and new_password != "":
            old_password = account_info['password']
            change_admin_password_check = change_password(database, select_user, old_password, new_password)
            if change_admin_password_check:
                print("用户[%s]密码修改成功 !" % select_user)
                Logger(log_file).write_log(user=admin_name, status=True, event="用户%s密码修改成功" % select_user)
                return change_admin_password_check
        else:
            if new_password == "":
                print("密码不能为空 !!!")
            else:
                print("两次输入不一致")
            Logger(log_file).write_log(user=admin_name, status=False, event="用户%s密码修改失败" % select_user)
            return False


def for_owner_change_password(database, user_name, log_file=None):
    old_password = str(input("请输入当前密码:")).strip()
    new_password = str(input("请输入新密码:")).strip()
    repeat_password = str(input("请再次确认新密码:")).strip()
    if new_password == repeat_password and new_password != "":
        change_admin_password_check = change_password(database, user_name, old_password, new_password)
        if change_admin_password_check:
            print("用户[%s]密码修改成功 !" % user_name)
            Logger(log_file).write_log(user=user_name, status=False, event="用户%s密码修改失败" % user_name)
            return change_admin_password_check
    else:
        if new_password == "":
            print("密码不能为空 !!!")
        else:
            print("两次输入不一致 !!!")
        Logger(log_file).write_log(user=user_name, status=False, event="用户%s密码修改失败" % user_name)
        return False


def change_admin_password(database, admin_name, log_file=None):
    if is_super_admin(database, admin_name):
        return for_super_admin_change_password(database, admin_name, log_file=log_file)
    else:
        return for_owner_change_password(database, admin_name, log_file=log_file)


def for_admin_unlock_account(database, admin_name, log_file=None):
    select_user = str(input("请选择需要解锁的用户:")).strip()
    get_database = unlock_account(database, select_user, log_file=log_file)
    if get_database:
        print("用户[%s]解锁成功" % select_user)
        Logger(log_file).write_log(user=admin_name, status=True, event="用户%s解锁成功" % select_user)
        return get_database
    else:
        Logger(log_file).write_log(user=admin_name, status=False, event="用户%s不存在,解锁失败" % select_user)
        return False


def for_admin_lock_account(database, admin_name, log_file=None):
    select_user = str(input("请选择需要挂失的用户:")).strip()
    get_database = lock_account(database=database, user=select_user, log_file=log_file, user_status="1")
    if get_database:
        print("用户[%s]挂失成功" % select_user)
        Logger(log_file).write_log(user=admin_name, status=True, event="用户%s挂失成功" % select_user)
        return get_database
    else:
        Logger(log_file).write_log(user=admin_name, status=False, event="用户%s不存在,挂失失败" % select_user)
        return False


def show_account_info(database, user_name, is_admin=False, log_file=None):
    if type(database) != dict:
        Logger(log_file).write_log(user=user_name, status=False, event="查询失败")
        return False
    if is_admin:
        select_user = str(input("请输入要查询的用户信息: ")).strip()
    else:
        select_user = user_name
    get_database = search_account_info(database, select_user)
    if type(get_database) == dict:
        try:
            cn_name = get_database['cn_name']
            en_name = get_database['en_name']
            age = get_database['age']
            mail = get_database['mail']
            birthday = get_database['birthday']
            mobile = get_database['contact']
            company = get_database['company']
            user_status = user_status_define(get_database['user_status'])
            cash_advance_limit = get_database['cash_advance_limit']
            credit_limit = get_database['credit_limit']
            available_credit_limit = get_database['available_credit']
            statement_date = get_database['statement_date']
            payment_due_date = get_database["payment_due_date"]
            new_charges = get_database["new_charges"]
            current_balance = get_database["current_balance"]
            minimum_payment = get_database["minimum_payment"]
        except KeyError:
            pass
        print("""
    用户[%s]信息如下
    账户信息
    ====================================================
    用户名                %s
    中文名                %s
    英文名                %s
    年龄                  %s
    邮箱                  %s
    生日                  %s
    手机号码               %s
    单位全称               %s
    用户状态               %s
    信用额度               ￥%s
    可用额度               ￥%s
    未出账分期本金          ￥%s
    预借现金可用额度         ￥%s
    每月账单日              %s日

    还款信息
    ====================================================
    自动还款              未开通
    本期到期还款日          %s日
    本期账单金额          ￥%s
    本期剩余应还金额       ￥%s
    本期剩余最低还款金额    ￥%s
    ====================================================
    """ % (select_user, select_user, cn_name, en_name, age, mail, birthday, mobile, company,
           user_status, credit_limit, available_credit_limit, 0, cash_advance_limit,
           statement_date, payment_due_date, new_charges, current_balance, minimum_payment))


def transfer_cash(database, user_name, log_file, sold_log=None):
    count = 0
    user_database = search_account_info(database, user_name)
    user_money = user_database["credit_limit"]
    import time
    while count < 3:
        select_user = str(input("请输入需要转账的卡号:"))
        if select_user == user_name:
            print("不能给自己转账")
            continue
        get_select_user_database = search_account_info(database, select_user)
        if type(get_select_user_database) == dict:
            current_money = get_select_user_database["credit_limit"]
            money = str(input("请输入需要转账金额:"))
            if not str(money).isdigit():
                print("输入错误, 请重新输入!")
                continue
            if float(money) > float(user_money):
                print("余额不足,请重新输入")
                continue
            while True:
                wait_choose = str(input("是否需要验证对方信息\n\t默认验证\nyes/no: "))
                if wait_choose.lower() in ["n", "no"]:
                    break
                wait_choose = str(input("请输入对方姓名:"))
                if wait_choose == get_select_user_database["cn_name"]:
                    break
                else:
                    print("验证未通过")
            wait_choose = str(input("确认转账?\n您将给用户[%s]转账金额为%s元\n请确认 yes/no: " % (select_user, money)))
            if wait_choose.lower() in ["y", "yes"]:
                user_database["credit_limit"] = str(float(user_money) - float(money))
                get_select_user_database["credit_limit"] = str(float(current_money) + float(money))
                current_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
                Logger(sold_log).write_log(user=user_name, status="%s" % money,
                                           event="给用户[%s]转账成功,转账金额为[%s]" % (select_user, money), cur_time=current_time)
                Logger(log_file).write_log(user=user_name, status="transfer",
                                           event="给用户[%s]转账成功,转账金额为[%s]" % (select_user, money),)
                return database
            else:
                print("操作取消 !!")
                break
        count += 1
    return False


def select_date(string="开始时间", is_sold=False):
    """
    :param string: 自定义提示内容
    :param is_sold: 是否是查询交易日志格式
    :return: 输入正确的日期格式
    """
    import time
    date_format = "%Y-%m-%d"
    if is_sold:
        date_format = "%Y/%m/%d"
    count = 0
    while count < 3:
        statement_date = time.strftime(date_format, time.localtime())
        try:
            count += 1
            statement_date = str(input("请输入%s\n格式:%s\n请输入:" % (string, statement_date))).strip()
            time.strptime(statement_date, date_format)
            return statement_date
        except ValueError:
            print("格式输入错误")
            continue


def show_format_log(log_list, is_sold=False):
    if type(log_list) == list:
        first = "操作日期"
        second = "时间"
        third = "操作事件"
        fourth = "操作状态"
        fifth = "用户"
        if is_sold:
            first = "交易日"
            second = "记账日"
            third = "交易摘要"
            fourth = "人民币金额"
            fifth = "卡号"
        title = "%s%s%s%s%s" % (first.ljust(12), second.ljust(12), third.ljust(50), fourth.ljust(14), fifth.ljust(12))
        print(title)
        for log in log_list:
            record_list = str(log).split(maxsplit=4)
            if len(record_list) == 5:
                sold = record_list[0]
                posted = record_list[1]
                description = record_list[4]
                rmb_amount = record_list[3]
                card_num = record_list[2]
                if is_sold:
                    posted = sold
                length_sold = myljust(first.ljust(12), sold)
                length_posted = myljust(second.ljust(12), posted)
                length_description = myljust(third.ljust(50), description)
                length_rmb_amount = myljust(fourth.ljust(14), rmb_amount)
                length_card_num = myljust(fifth.ljust(12), card_num)
                print("%s%s%s%s%s" % (str(sold).ljust(length_sold),
                                      str(posted).ljust(length_posted),
                                      str(description).ljust(length_description),
                                      str(rmb_amount).ljust(length_rmb_amount),
                                      str(card_num).ljust(length_card_num)))


def myljust(column, string):
    length_column = len(str(column))
    length_string = len(str(string).encode("gbk"))
    if length_string > length_column:
        length_string -= length_string - length_column
    elif length_string < length_column:
        length_string += length_column - length_string
    else:
        length_string -= 2
    return length_string


def search_history_log(user_name, log_file, sold_log=None, is_sold=False):
    """
    :param user_name: 操作的用户名
    :param log_file: 银行基本日志文件
    :param sold_log: 银行交易日志文件
    :param is_sold: 是否查询交易日志
    :return:
    """
    start_date = select_date("开始日期", is_sold=is_sold)
    end_date = select_date("结束日期", is_sold=is_sold)
    check_date = get_diff_days(start_date, end_date)
    if is_sold and sold_log:
        Logger(log_file).write_log(user=user_name, status="True", event="查询交易记录日志")
        log_file = sold_log
    if check_date and int(check_date) >= 0:
        get_match_list = Logger(log_file).get_match_log(user=user_name, start_time=start_date, end_time=end_date)
        show_format_log(get_match_list, is_sold=is_sold)
        return True
    else:
        print("日期范围输入有误!!!")
        return False


def for_admin_withdraw_money(database, user_name, log_file, sold_log, is_admin=False):
    count = 0
    if is_admin:
        select_user = str(input("请输入需要取现的用户名: "))
    else:
        select_user = user_name
    get_select_user_db = search_account_info(database, select_user)
    if type(get_select_user_db) == dict:
        while count < 3:
            count += 1
            current_money = get_select_user_db["cash_advance_limit"]
            wait_choose = str(input("请输入取现金额:"))
            try:
                get_money = float(wait_choose)
                total = get_money * 1.05
                print("手续费为金额的%5,实际扣除金额为[{0}]".format(total))
                current_money = float(current_money)
                if current_money < total:
                    print("取现金额不足,请重新输入")
                    continue
                elif get_money % 100 != 0:
                    print("取现金额只能为100整数")
                    continue
                while True:
                    choose = str(input("确认取钱吗? yes/no: "))
                    if choose.lower() in ["y", "yes"]:
                        get_money = total
                        reduce_money = current_money - get_money
                        get_select_user_db["cash_advance_limit"] = reduce_money
                        print("您已取现[%s],剩余可用现金额度[%s]元" % (get_money, reduce_money))
                        Logger(log_file).write_log(user=user_name, status="True", event="取现成功,取现金额[%s]元,剩余[%s]元" % (get_money, reduce_money))
                        Logger(sold_log).write_log(user=user_name, status=get_money, event="取现成功,取现金额[%s]元,剩余[%s]元" % (get_money, reduce_money), date_format="/")
                        return database
                    else:
                        count += 3
                        print("操作取消")
                        break
                else:
                    break
            except KeyError:
                print("输入错误,金额不能是非数字类型")


