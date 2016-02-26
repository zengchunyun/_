#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

from core.userverify import UserVerify
from core.MyServer import MyServer
from core.game import Soldier, MagicMaster
import shelve
import logging

host, port = "0.0.0.0", 9999  # 定义服务器监听端口
connect_database = shelve.open("../database/database")  # 打开可持久化数据文件
database = connect_database.get("data")  # 获取键为data的数据
show_list = connect_database.get("show_list")  # 获取对话列表
verify = UserVerify(database)  # 将UserVerify类进行实例化

logger = logging.getLogger(__name__)  # 创建一个日志名为Game
logger.setLevel(logging.INFO)  # 日志级别为INFO
con_handler = logging.StreamHandler()  # 创建控制台流处理日志
con_handler.setLevel(logging.DEBUG)  # 设置控制台日志输出级别
file_handler = logging.FileHandler(filename="../database/access.log", encoding="utf8", delay=False)  # 设置记录日志文件属性
file_handler.setLevel(logging.INFO)  # 设置记录日志级别
formatter = logging.Formatter("%(asctime)s  -  %(name)s   -  %(levelname)s  - %(message)s")  # 设置日志格式
con_handler.setFormatter(fmt=formatter)  # 设置控制台输出日志格式
file_handler.setFormatter(fmt=formatter)  # 设置日志文件记录格式
logger.addHandler(con_handler)  # 将控制台日志处理加入到Game日志对象里
logger.addHandler(file_handler)  # 将文件日志处理加入到Game日志对象里


class MyHandlerRequest(MyServer, UserVerify):
    def __init__(self, server_address, database):
        """
        :param server_address: 服务器IP:端口形式参数,用于开启一个新的服务端
        :param database:该数据来源于含有用户名密码信息的字典形式内容
        :return:
        """
        super(MyHandlerRequest, self).__init__(server_address)  # 继承基类的实例属性
        self.database = database  # 覆盖基类的实例属性
        self.retry_count = 3
        self.auth_menu = {"l": self.login,  # 定义登陆菜单按钮快捷键,对应对是基类的注册与登陆方法,还有子类的退出方法
                          "r": self.register,
                          "q": self.quit_game}
        self.begin_menu = {"n": self.new_role,  # 定义开始菜单按钮快捷键,对应的是子类的方法
                           "q": self.quit_game}

    def define_handle(self, request, client_address):
        """
        :param request: 已连接的socket
        :param client_address: 客户端IP端口
        :return: 该方法优先于MyServer定义的方法,通过MyServer的server_start()方法即可调用该类方法
        """
        get_username = self.connect_auth(request, client_address)
        if get_username:  # 如果授权成功,则调用子类方法查询该用户是否有存档
            self.get_history(request, username=get_username)
        else:  # 否则通过子类quit_game方法,调用基类的shutdown_request方法,进行关闭客户端连接
            self.quit_game(request)

    def connect_auth(self, request, client_address):
        """
        :param request: 已连接的socket
        :param client_address: 客户端IP端口
        :return: 只有认证成功的用户才能继续操作
        """
        while self.retry_count > 0:
            self.send_message(request, show_list["login"])
            received = self.recv_message(request)  # 尝试从该socket客户端接收数据
            action = self.auth_menu.get(received)
            if action:
                if str(received) == "q":
                    self.send_message(request, show_list["over"])
                    self.retry_count = 0
                    logger.info("来自客户端[{}:{}]已下线 ...".format(client_address[0], client_address[1]))
                    return False
                self.send_message(request, show_list["name"])
                username = self.recv_message(request)
                self.send_message(request, show_list["password"])
                password = self.recv_message(request)
                get_result = action(username, password)
                if type(get_result) == dict:
                    get_result[username]["store"] = False
                    connect_database["data"] = get_result
                if get_result:
                    self.send_message(request, show_list["welcome"])
                    logger.info("来自客户端[{}:{}]用户名[{}]登陆成功 ...".format(client_address[0], client_address[1], username))
                    return username
                elif str(get_result) == str(None):
                    logger.info("来自客户端[{}:{}]用户名[{}]不存在,登陆失败 ...".format(client_address[0], client_address[1], username))
                else:
                    logger.info("来自客户端[{}:{}]用户名[{}]登陆失败 ...".format(client_address[0], client_address[1], username))
            else:
                logger.info("来自客户端[{}:{}]输入错误,登陆失败 ...".format(client_address[0], client_address[1]))
            self.send_message(request, show_list["failed"])
            self.retry_count -= 1
        else:
            return False

    def get_history(self, request, username):
        """
        :param request: 请求客户端socket
        :param username: 用户名
        :return: 如果有存档,则为真,没有则为假
        """
        get_user_info = connect_database["data"].get(username)
        if get_user_info["store"]:
            self.send_message(request, show_list["continue"])
            self.begin_menu["c"] = self.start_game
        else:
            self.send_message(request, show_list["new"])
        self.retry_count = 10
        while self.retry_count > 0:
            action = self.recv_message(request)
            action = self.begin_menu.get(action)
            if action:
                action(request, username)
                self.retry_count = 0
                break
            else:
                self.send_message(request, show_list["error"])
                self.retry_count -= 1

    def new_role(self, request, username):
        self.send_message(request, show_list["role"])
        role_name = self.recv_message(request)
        connect_database["data"][username]["role_name"] = role_name
        self.send_message(request, show_list["role_job"])
        while True:
            role_job = self.recv_message(request)
            if role_job not in ["1", "2"]:
                self.send_message(request, "%s%s" % (show_list["error"], show_list["role_job"]))
            else:
                break
        connect_database["data"][username]["role_job"] = role_job
        print(connect_database["data"])



    def start_game(self, request, username):
        self.send_message(request, show_list["play"])
        pass

    def quit_game(self, request, flag=None):
        self.shutdown_request(request)

    def recv_message(self, request, buffer=4096):
        """该类方法用于接收用户的请求信息
        :param request:
        :param buffer:
        :return: 以字符串形式返回接收到的用户信息
        """
        message = str(request.recv(buffer), "utf8").strip()
        return message

    def send_message(self, request, message):
        """
        :param request:
        :param message: 将自定义形式,通过字节方式发送到客户端
        :return:
        """
        request.send(bytes(message, "utf8"))


def run():
    """创建一个服务端,监听所有客户端,端口为9999
    实例化一个子类,并设置ip地址复用
    调用父类server_start()方法启动服务端
    :return:
    """
    try:
        server_address = ("0.0.0.0", 9999)
        server = MyHandlerRequest(server_address, database)
        server.allow_reuse_address = True
        logger.info("服务器初始化完成 ...")
        server.server_start(1)
    except KeyboardInterrupt:
        logger.info("服务器已退出 ...")
