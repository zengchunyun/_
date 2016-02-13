#! /usr/bin/env python3

from publicAPI import auth_account, register_account, change_admin_password
from publicAPI import modify_admin_account_info, add_admin_account, delete_account, change_admin_permission
from config.settings import user_info


def update_info(user_info_dict):  # 接收一个字典字符串,然后写入到文件,把一个字典类型参数写入文件
    import re
    write_data = re.findall('["\'\w,:\s=\d@.\-]+\{*|\}', 'user_info = '+str(user_info_dict).replace("'", '"'))
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
    database.close()
    return True


def atm_self_service(quit_atm_self_service=False):  # ATM自助服务系统
    while not quit_atm_self_service:
        print("""欢迎使用    中国建都银行    自助服务系统
        普通客户大众版平台(1)    银行前台专业版管理中心(2)
        返回(b)    退出(q)
        """)
        wait_choose = str(input("请选择操作:"))
        if wait_choose == "1":
            quit_atm_self_service = public_login(quit_atm_self_service)  # 进入大众版登陆系统
        elif wait_choose == "2":
            quit_atm_self_service = admin_bank_system(quit_atm_self_service)  # 进入管理员操作平台
        elif str(wait_choose).lower() in ['q', 'quit', ]:
            quit_atm_self_service = True
            print("谢谢使用,再见 !")
            break
        elif str(wait_choose).lower() in ['b', 'back', ]:
            break
        else:
            print("操作有误 !!!")
    return quit_atm_self_service


def public_login(quit_public_login=False):
    count = 0  # 用于限制登录次数的计数器
    login_pass = auth_account(user_info['my_bank'])
    if not login_pass and str(login_pass) != str(None):
        count += 1
        print('登陆失败 !!!')
    elif login_pass:
        count = 0  # 重置计数器
        print('欢迎登录')
    if count > 3:
        print("操作过于频繁,请稍后再试")
    return quit_public_login


def admin_bank_system(quit_admin_bank=False):  # 银行管理人员操作平台
    while not quit_admin_bank:
        open_register = "首次注册(2)"
        try:
            admin_database = user_info['admin_bank']
        except KeyError:
            user_info['admin_bank'] = {}
            admin_database = user_info['admin_bank']
        if len(admin_database) > 0:
            open_register = False  # 如果系统存在管理员帐号,则不开放这个功能,后续增加管理员帐号只能登陆后添加
            open_login = "管理员登录(1)"
        else:
            open_login, open_register = open_register, True
        print("""欢迎进入    中国建都银行    管理平台
        %s
        返回(b)    退出(q)
            """ % open_login)
        wait_choose = str(input("请选择操作:"))
        if wait_choose == "1" and not open_register:
            get_admin = auth_account(admin_database, is_admin=True)  # 调用登陆模块
            if get_admin:
                quit_admin_bank = admin_management(get_admin, quit_admin_bank)  # 进入管理员操作中心
            elif not get_admin and str(get_admin) != str(None):
                print("登陆失败 !!!")
        elif wait_choose == "2" and open_register:  # 只有数据库没有任何用户的情况才会开放这个注册功能
            get_database = register_account(admin_database, is_admin=True)  # 调用注册模块
            if get_database:
                user_info['admin_bank'] = get_database  # 更新数据库信息
                update_info(user_info)  # 写入数据库
        elif str(wait_choose).lower() in ['q', 'quit', ]:
            quit_admin_bank = True
            print("谢谢使用,再见 !")
            break
        elif str(wait_choose).lower() in ['b', 'back', ]:
            break
        else:
            print("操作有误 !!!")
    return quit_admin_bank


def admin_management(admin_name, quit_admin_management=False):  # 管理员登陆成功后的账号操作
    while not quit_admin_management:
        print("""中国建都银行    管理中心    [%s]已登陆
        查询帐户(1)  修改帐户(2)  解锁帐户(3)  管理员帐户管理(4)
        注销(b)  退出(q)
        """ % admin_name)
        wait_choose = str(input("请选择操作:"))
        if wait_choose == "1":
            pass
        elif wait_choose == "4":
            quit_admin_management = management_admin_account(admin_name, quit_admin_management)  # 对管理员账号进行操作
        elif str(wait_choose).lower() in ['q', 'quit', ]:
            quit_admin_management = True
            print("谢谢使用,再见 !")
            break
        elif str(wait_choose).lower() in ['b', 'back', ]:
            break
        else:
            print("操作有误 !!!")
    return quit_admin_management


def management_admin_account(admin_name, quit_management_account):
    while not quit_management_account:
        admin_database = user_info['admin_bank']
        print("""中国建都银行    管理中心    [%s]已登陆
        添加管理账号(1)  删除管理账号(2)  更改账号权限(3)  更改账号信息(4)  修改管理员密码(5)
        返回(b)  退出(q)
        """ % admin_name)
        wait_choose = str(input("请选择操作:"))
        if wait_choose == "1":
            get_database = add_admin_account(admin_database, admin_name, is_admin=True)
            if get_database:
                user_info['admin_bank'] = get_database  # 更新数据库信息
                update_info(user_info)
        elif wait_choose == "2":
            get_database = delete_account(admin_database)
            if get_database:
                user_info['admin_bank'] = get_database  # 更新数据库信息
                update_info(user_info)
        elif wait_choose == "3":
            get_database = change_admin_permission(admin_database, admin_name)
            if get_database:
                user_info['admin_bank'] = get_database  # 更新数据库信息
                update_info(user_info)
        elif wait_choose == "4":
            get_database = modify_admin_account_info(admin_database)
            if get_database:
                user_info['admin_bank'] = get_database  # 更新数据库信息
                update_info(user_info)
        elif wait_choose == "5":
            get_database = change_admin_password(admin_database, admin_name)
            if get_database:
                user_info['admin_bank'] = get_database  # 更新数据库信息
                update_info(user_info)
        elif str(wait_choose).lower() in ['q', 'quit', ]:
            quit_management_account = True
            print("谢谢使用,再见 !")
            break
        elif str(wait_choose).lower() in ['b', 'back', ]:
            break
        else:
            print("操作有误 !!!")
    return quit_management_account