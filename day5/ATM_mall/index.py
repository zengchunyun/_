#! /usr/bin/env python3


import re
from config.settings import user_info
from account import UserInfo


def update_info(user_info):  # 接收一个字典字符串,然后写入到文件
    write_data = re.findall('["\'\w,:\s=\d@.\-]+\{*|\}', 'user_info = '+str(user_info).replace("'", '"'))
    count = 0
    with open('./config/settings.py', 'w') as database:
        for content in write_data:
            if content.find('{') != -1:
                database.write('%s%s\n' % (str(count * '\t').expandtabs(4), content))
                count += 1
            elif content.find('}') != -1:
                database.write('%s%s\n' % (str(count * '\t').expandtabs(4), content))
                count -= 1
            else:
                database.write('%s%s\n' % (str(count * '\t').expandtabs(4), content))


def show_user_info():
    get_info = user_info['admin_bank']['root']
    if type(get_info) == dict:
        for k, v in get_info.items():
            if type(v) == dict:
                print('\naccount:[%s]' % k)
                for k2, v2 in v.items():
                    print(k2, v2, end=" | ")
                print()
            else:
                print(k, v, end=" | ")


def level_define(level):
    if str(level) == "0":
        level = "超级管理员"
    else:
        level = "普通管理员"
    return level


def valid(code_length):
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
            return code


def add_admin_level():
    level = str(input("请输入管理级别\n有两个级别\n\t1 代表普通管理员\n\t0 代表超级管理员\n\t默认为普通管理级别\n请输入:"))
    if level != "0":
        level = "1"
    return level


def add_common_info():  # 额外的扩展信息
    common_info = {}  # 初始化一个空字典,存储用户基本信息
    if isadmin:
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
    return common_info


def search_account_info(database, user):
    get_info = UserInfo(**database).change_info(user)
    if get_info:
        return get_info[user]


def add_extra_info(register_func):
    def add_info(database):
        before = database
        after = register_func(database)
        if after:
            database = after
            update_user = set(before).symmetric_difference(set(after))
            add_user_info = add_common_info()
            if len(database) == 1 and isadmin:  # 当系统为第一次使用时,自动把权限提升为超级管理员级别
                add_user_info['level'] = "0"
            return change_account_info(database, list(update_user)[0], add_user_info)
        else:
            return False
    return add_info


def valid_code(code_func):  # 传入一个验证码功能和登陆授权功能的函数
    def valid_account(public_func):  # 传入添加了装饰器的函数名
        def login_auth(database=None):  # 将上面函数所需要的参数放在这里
            temp_code = code_func(4)
            wait_code = str(input("请输入验证码:"))
            if str(wait_code).lower() == str(temp_code).lower():
                return public_func(database)
            else:
                print('验证码输入错误 !!!')
                return None
        return login_auth
    return valid_account


@valid_code(valid)  # 对登录模块增加一个验证码功能
def auth_account(database):
    global admin_name
    user = str(input("请输入用户名:"))
    password = str(input("请输入密码:"))
    if isadmin:
        admin_name = user
    else:
        admin_name = None
    return UserInfo(**database).login(user, password)


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


def change_account_info(database, user, common_info):  # 变更用户的除用户名密码以外的信息
    return UserInfo(**database).change_info(user, **common_info)


def change_admin_permission():
    if user_info['admin_bank'][admin_name]['level'] == ("0" or 0):
        pass
    else:
        print("普通管理员[%s]没有权限修改管理员帐号信息" % admin_name)
        return False
    select_user = str(input("请输入要更改的用户名:"))
    if search_account_info(user_info['admin_bank'], select_user):
        level = add_admin_level()
        wait_choose = str(input("确认修改[%s]权限修改为[%s]吗: y/n " % (select_user, level_define(level))))
        if wait_choose.lower() in ["y", "yes", ]:
            change_level_result = change_account_info(user_info['admin_bank'], select_user, {'level': level})
            if change_level_result:
                user_info['admin_bank'] = change_level_result
                update_info(user_info)
                print("管理员[%s]级别已修改为[%s]" % (select_user, level_define(level)))
        else:
            print("操作未改变 !!!")


def management_admin_account():
    global quit_atm
    while not quit_atm:
        print("""中国建都银行    管理中心
        添加管理账号(1)  删除管理账号(2)  更改账号权限(3)  更改账号信息(4)
        返回(b)  退出(q)
        """)
        wait_choose = str(input("请选择操作:"))
        if wait_choose == "1":
            register_result = register_account(user_info['admin_bank'])
            if register_result:
                user_info['admin_bank'] = register_result
                update_info(user_info)
        elif wait_choose == "3":
            change_admin_permission()
        elif wait_choose == "4":
            select_user = str(input("请输入要更改的用户名:"))
            if search_account_info(user_info['admin_bank'], select_user):
                common_info = change_common_info()
                change_result = change_account_info(user_info['admin_bank'], select_user, common_info)
                if change_result:
                    user_info['admin_bank'] = change_result
                    update_info(user_info)
        elif str(wait_choose).lower() in ['q', 'quit', ]:
            quit_atm = True
            break
        elif str(wait_choose).lower() in ['b', 'back', ]:
            break
        else:
            print("操作有误 !!!")


def admin_management():  # 管理员登陆成功后的账号操作
    global quit_atm
    global isadmin
    while not quit_atm:
        print("""中国建都银行    管理中心
        查询帐户(1)  修改帐户(2)  解锁帐户(3)  管理员帐户管理(4)
        返回(b)  退出(q)
        """)
        wait_choose = str(input("请选择操作:"))
        if wait_choose == "1":
            isadmin = False
            pass
        elif wait_choose == "4":
            management_admin_account()  # 对管理员账号进行操作
        elif str(wait_choose).lower() in ['q', 'quit', ]:
            quit_atm = True
            break
        elif str(wait_choose).lower() in ['b', 'back', ]:
            break
        else:
            print("操作有误 !!!")


def admin_bank_system():  # 银行管理人员操作平台
    global quit_atm
    global isadmin
    open_register = "临时开放注册功能(2)"
    while not quit_atm:
        if len(user_info['admin_bank']) > 0:
            open_register = ""  # 如果系统存在管理员帐号,则不开放这个功能,后续增加管理员帐号只能登陆后添加
        print("""欢迎进入  中国建都银行  管理平台
            管理员登录(1)    %s
            返回(b)    退出(q)
            """ % open_register)
        wait_choose = str(input("请选择操作:"))
        if wait_choose == "1":
            isadmin = True
            login_result = auth_account(user_info['admin_bank'])  # 调用登陆模块
            if login_result:
                admin_management()  # 进入管理员操作中心
            elif not login_result and str(login_result) != str(None):
                print("登陆失败 !!!")
        elif wait_choose == "2" and open_register:  # 只有数据库没有任何用户的情况才会开放这个注册功能
            register_result = register_account(user_info['admin_bank'])  # 调用注册模块
            if register_result:
                user_info['admin_bank'] = register_result  # 更新数据库信息
                update_info(user_info)  # 写入数据库
        elif str(wait_choose).lower() in ['q', 'quit', ]:
            quit_atm = True
            break
        elif str(wait_choose).lower() in ['b', 'back', ]:
            break
        else:
            print("操作有误 !!!")


def atm_self_service():  # ATM自助服务系统
    global quit_atm
    global isadmin
    count = 0  # 用于限制登录次数的计数器
    while not quit_atm:
        print("""欢迎使用 中国建都银行  自助服务系统
        普通客户大众版平台(1)    银行前台专业版管理中心(2)
        返回(b)    退出(q)
        """)
        wait_choose = str(input("请选择操作:"))
        if wait_choose == "1":
            isadmin = False
            login_pass = auth_account(user_info['my_bank'])
            if not login_pass and str(login_pass) != str(None):
                count += 1
                print('登陆失败 !!!')
            elif login_pass:
                count = 0  # 重置计数器
                print('欢迎登录')
            if count > 3:
                quit_atm = True
                print("操作过于频繁,请稍后再试")
                break
        elif wait_choose == "2":
            isadmin = True
            admin_bank_system()  # 进入管理员操作平台
        elif str(wait_choose).lower() in ['q', 'quit', ]:
            quit_atm = True
            break
        elif str(wait_choose).lower() in ['b', 'back', ]:
            break
        else:
            print("操作有误 !!!")


def shop_service():
    print('shopping')


def main():
    global quit_atm
    while not quit_atm:
        print("""欢迎使用一站式购物平台
        ATM自助服务(1)  商场购物(2)""")
        wait_choose = str(input("\n请选择操作:"))
        if wait_choose == "1":
            atm_self_service()  # 进入ATM自助服务系统
        elif wait_choose == "2":
            shop_service()  # 进入商城购物平台
        elif str(wait_choose).lower() in ['q', 'quit', ]:
            quit_atm = True
            break
        else:
            print("操作有误 !!!")


if __name__ == '__main__':
    quit_atm = False  # 设置退出条件
    isadmin = False  # 设置标志权限,如果是管理员,则设置为真
    admin_name = None
    main()
