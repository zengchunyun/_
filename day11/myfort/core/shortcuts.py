#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from sqlalchemy.orm import sessionmaker
import sys
import yaml
try:
    from db.models import create_db, Hosts, HostUsers, HostToUser, HostGroup, Groups, Account, AuditEvents, LogType,\
        select_engine, AccountGroup
    from core.views import handle_default_options, CommandError
    from core.shell import Shell
except ImportError:
    pass

DBSession = sessionmaker()
DBSession.configure(bind=select_engine())
session = DBSession()  # 打开数据连接


def parser_file(filename):
    """
    解析参数文件
    :param filename: 必须是一个存了字典数据格式的文件
    :return: 返回一个字典
    """
    try:
        read_file = yaml.load(open(filename))
        if type(read_file) == dict:
            return read_file
        raise IOError
    except IOError:
        raise CommandError("\033[31;1m[ {} ] it's not a real, file read error\033[0m".format(filename))


def check_err(func):
    """
    验证输入装饰器,包括检查提交事务异常
    :param func:
    :return:
    """
    def run_action(argv):
        if len(argv) < 2:
            raise CommandError("\033[31;1mthe following arguments are requires: file \033[0m\n")
        if argv[0] == '-f':
            func(argv)
            try:
                session.commit()
            except Exception:
                session.rollback()
                raise CommandError("\033[31;1mplease insert record before run makemigrations to initialization db"
                                   " \n\tor \nhas repeat insert data\033[0m\n")
        else:
            raise CommandError("\033[31;1musage:\n\t{} -f filename\033[0m\n".format(sys.argv[1]))
        print("\033[33;1mOK\033[0m")
    return run_action


def makemigrations(argv):
    """
    初始化数据库
    :param argv:
    :return:
    """
    create_db()
    print("\033[33;1mOK\033[0m")


def connect_server(argv, hostname, port):
    """
    连接远程服务器
    :param argv: 包含用户认证信息
    :param hostname: 主机地址
    :param port: 主机端口
    :return:
    """
    username = argv.username
    password = argv.password
    shell = Shell(hostname=hostname, port=port, username=username, password=password)
    shell.run()


def login():
    """
    登录堡垒认证模块
    :return:
    """
    lock_count = 3  # 错误次数,只要输入完整的用户名密码后,错误则减1
    retry_count = 6  # 尝试机会,只要一回车,次数减1
    while (retry_count and lock_count) > 0:
        retry_count -= 1
        username = str(input("Login: ")).strip()
        if not username:
            continue
        password = str(input("Password: ")).strip()
        if not password:
            continue  # 如果不输入密码,为了减少数据库IO操作,就不进行密码校验
        get_user = session.query(Account).filter(Account.username == username, Account.password == password).all()
        if get_user:  # 当用户登录成功后,查询用户对应对组
            get_user_group = session.query(Groups).filter(AccountGroup.account == get_user[0]).filter(
                Groups.id == AccountGroup.group_id).all()
            if get_user_group:
                return get_user_group
            else:
                print("\033[31;1muser or password incorrect\033[0m")
        lock_count -= 1
    print("重试次数太多")
    return ''  # 当认证失败,返回空


def runserver(argv):
    """
    启动堡垒主机
    :param argv: 命令行参数
    :return:
    """
    quit_prog = False  # 设置退出程序标记
    get_user_group = login()
    if get_user_group:  # 当查询到用户对组后,再由用户选择,进入对应对主机选择
        while not quit_prog:
            print("\033[33;1mplease choose group number\033[0m")
            for index, group in enumerate(get_user_group, 1):
                print("group{}: {}".format(index, group.groupname))
            groupname_id = None
            while True:
                group_id = str(input(">> : ")).strip()
                if group_id.isdigit():
                    group_id = int(group_id)
                    if group_id in range(1, len(get_user_group) + 1):
                        groupname_id = get_user_group[group_id - 1].id
                        break
                elif group_id.lower() in ['q', 'quit', 'e', 'exit']:
                    quit_prog = True
                    break
                elif group_id.lower() in ['b', 'back']:
                    break
                print("\033[31;1minput error\033[0m")
            if groupname_id:  # 当查询到用户组后,打印用户组,让用户选择
                print("\033[33;1mplease choose host number\033[0m")
                get_group_host = session.query(Hosts).filter(HostGroup.group_id == groupname_id).filter(
                    Hosts.id == HostGroup.host_id).all()
                for index, host in enumerate(get_group_host, 1):
                    print("host{}: [\033[33;1m{:^10}\033[0m] {}".format(index, host.hostname, host.ipaddress))
                hostname_id = None
                hostname = None
                port = None
                while True:
                    host_id = str(input(">> : ")).strip()
                    if host_id.isdigit():
                        host_id = int(host_id)
                        if host_id in range(1, len(get_group_host) + 1):
                            hostname_id = get_group_host[host_id - 1].id
                            hostname = get_group_host[host_id - 1].ipaddress
                            port = get_group_host[host_id - 1].port
                            break
                    elif host_id.lower() in ['q', 'quit', 'e', 'exit']:
                        quit_prog = True
                        break
                    elif host_id.lower() in ['b', 'back']:
                        break
                    print("\033[31;1minput error\033[0m")
                if hostname_id:
                    get_host_user = session.query(HostUsers).filter(HostToUser.host_id == hostname_id).filter(
                        HostUsers.id == HostToUser.user_id).first()
                    if get_host_user:
                        connect_server(get_host_user, hostname, port)  # 获取主机用户名信息
                    else:
                        print("\033[31;1m该主机认证信息不完整,请补全\033[0m")


@check_err
def create_users(argv):
    """
    插入数据到用户表
    :param argv:
    :return:
    """
    filename = argv[1]
    get_info = parser_file(filename)
    for user, info in get_info.items():
        username = user
        if type(info) != dict:
            raise CommandError("\033[31;1mdata format error\033[0m")
        password = info.get('password')
        auth_type = info.get('auth_type')
        if not (user and auth_type):  # 插入的数据必须有这两个字段
            raise CommandError("\033[31;1mdata format error\033[0m")
        insert_user = HostUsers(username=username, password=password, auth_type=auth_type)
        session.add(insert_user)


@check_err
def create_fort_user(argv):
    """
    创建堡垒主机用户表
    :param argv:
    :return:
    """
    filename = argv[1]
    get_info = parser_file(filename)
    for user, info in get_info.items():
        username = user
        if type(info) != dict:
            raise CommandError("\033[31;1mdata format error\033[0m")
        password = info.get('password')
        if not (user and password):  # 插入的数据必须有这两个字段
            raise CommandError("\033[31;1mdata format error\033[0m")
        insert_user = Account(username=username, password=password)
        session.add(insert_user)


@check_err
def create_groups(argv):
    """
    创建主机组表
    :param argv:
    :return:
    """
    filename = argv[1]
    get_info = parser_file(filename)
    for group, info in get_info.items():
        if type(info) != dict:
            raise CommandError("\033[31;1mdata format error\033[0m")
        groupname = info.get("groupname")
        if not groupname:  # 插入的数据必须有这个字段
            raise CommandError("\033[31;1mdata format error\033[0m")
        insert_group = Groups(groupname=groupname)
        session.add(insert_group)


@check_err
def create_hosts(argv):
    """
    插入数据到主机表
    :param argv:
    :return:
    """
    filename = argv[1]
    get_info = parser_file(filename)
    for host, info in get_info.items():
        hostname = host
        if type(info) != dict:
            raise CommandError("\033[31;1mdata format error\033[0m")
        ipaddress = info.get('ipaddress')
        port = info.get('port')
        if not (hostname and ipaddress):  # 插入数据必须提供这两个数据格式
            raise CommandError("\033[31;1mdata format error\033[0m")
        insert_host = Hosts(hostname=hostname, ipaddress=ipaddress, port=port)
        session.add(insert_host)


@check_err
def bind_host_user(argv):
    """
    将主机绑定到对应的连接用户,即为服务器指定登录用户名密码关系
    :param argv:
    :return:
    """
    filename = argv[1]
    get_info = parser_file(filename)
    for bind, info in get_info.items():
        if type(info) != dict:
            raise CommandError("\033[31;1mdata format error\033[0m")
        hostname = info.get("hostname")
        username = info.get("username")
        if not (hostname and username):
            raise CommandError("\033[31;1mdata format error\033[0m")
        try:
            get_user_id = session.query(HostUsers).filter(HostUsers.username == username).one()
            get_host_id = session.query(Hosts).filter(Hosts.hostname == hostname).one()
        except Exception:
            raise CommandError("\033[31;1mplease addition the host and user record before setup relationship\033[0m")
        insert = HostToUser()
        insert.user = get_user_id
        get_host_id.auth_user.append(insert)
        session.add(insert)


@check_err
def bind_host_group(argv):
    """
    将主机添加到不同的组
    :param argv:
    :return:
    """
    filename = argv[1]
    get_info = parser_file(filename)
    for bind, info in get_info.items():
        if type(info) != dict:
            raise CommandError("\033[31;1mdata format error\033[0m")
        hostname = info.get("hostname")
        groupname = info.get("groupname")
        if not (hostname and groupname):
            raise CommandError("\033[31;1mdata format error\033[0m")
        try:
            get_group_id = session.query(Groups).filter(Groups.groupname == groupname).one()
            get_host_id = session.query(Hosts).filter(Hosts.hostname == hostname).one()
        except Exception:
            raise CommandError("\033[31;1mplease addition the host and user record before setup relationship\033[0m")
        insert = HostGroup()
        insert.group = get_group_id
        insert.host = get_host_id
        session.add(insert)


@check_err
def bind_user_group(argv):
    """
    将堡垒用户添加到主机组
    :param argv:
    :return:
    """
    filename = argv[1]
    get_info = parser_file(filename)
    for bind, info in get_info.items():
        if type(info) != dict:
            raise CommandError("\033[31;1mdata format error\033[0m")
        username = info.get("username")
        groupname = info.get("groupname")
        if not (username and groupname):
            raise CommandError("\033[31;1mdata format error\033[0m")
        try:
            get_group_id = session.query(Groups).filter(Groups.groupname == groupname).one()
            get_user_id = session.query(Account).filter(Account.username == username).one()
        except Exception:
            raise CommandError("\033[31;1mplease addition the host and user record before setup relationship\033[0m")
        insert = AccountGroup()
        insert.groups = get_group_id
        insert.account = get_user_id
        session.add(insert)
