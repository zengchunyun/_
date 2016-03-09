#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

import socketserver
import logging
import json
import shelve
import os
import sys
import subprocess
import time
from settings.settings import LISTEN, PORT, RECV_BUFFER, BASE_DIR, LOG_DIR, USER_DATA, database,\
    LOG_FILE, LOG_LEVEL, CONSOLE_LOG_LEVEL, FILE_LOG_LEVEL, OUTPUT_CONSOLE, FORMATTER, ENCODING,\
    ENABLE_ANONYMOUS, PUBLIC_DATA, QUTOTA_SIZE
from core.userverify import UserVerify


connect_database = shelve.open(database)  # 打开可持久化数据文件
database = connect_database.get("data")  # 获取键为data的数据
verify = UserVerify(database)  # 将UserVerify类进行实例化


class FTPServer(object):
    ERROR_CODE = {
        100: "Entering Passive Mode .",
        101: "Service ready for new user.",
        102: "Not logged in.",
        103: "User Logged out ",
        104: "User logged in, proceed.",
        105: "User name okay, need password.",
        106: "Need account for storing files.",
        107: "Need account for login.",
        200: "Command okay.",
        201: "Syntax error in parameters or arguments.",
        202: "Command not implemented.",
        203: "File status.",
        204: 'Directory created.',
        205: "Requested file action okay, completed.",
        206: "Requested file action not taken.",
        207: "Data connection open; no transfer in progress.",
        208: "Data connection already open; transfer starting.",
        209: "Requested file action pending further information",
        450: "Requested action not taken. File unavailable (e.g., file not found, no access).",
        451: "Requested action aborted. Data type unknown.",
        452: "Requested action not taken. File name not allowed",
        453: "Closing data connection. Requested file action successful (for example, file transfer or file abort).",
        454: "Requested file action aborted. Exceeded storage allocation (for current directory or dataset).",
        455: "Requested action not taken. Insufficient storage space in system.File unavailable (e.g., file busy).",
        500: "Requested action aborted. Local error in processing.",
        501: "Can't open data connection.",
        502: "Connection closed; transfer aborted.",
        503: "Service not available, closing control connection",
        504: "Service closing control connection.",
    }

    def __init__(self, request, client_address, server):
        """
        初始化服务端日志设置,然后开始处理已收到的请求
        :param request: 请建立连接的socket请求
        :param client_address: 客户端的IP及端口信息
        :param server: 服务器自身的IP端口信息
        :return:
        """
        self.home_dir = None  # 用于设置用户家目录
        self.request = request
        self.login = False
        self.request_message = None  # 将每次的请求存入该属性
        self.request_command = None  # 将每次请求的指令存入该属性
        self.client_address = client_address
        self.server = server
        self.retry_count = 3  # 设置最大尝试登陆次数
        self.logger = logging.getLogger(__name__)  # 创建日志对象
        self.get_code = None
        # 定义命令列表,可以起到限制命令功能
        self.command_list = ["ls", "info", "pwd", "cd", "put", "get", "dir", "help", "bye", "quit", "mkdir", "rmdir", "rm", "chmod"]
        if OUTPUT_CONSOLE:
            self.console_handler = logging.StreamHandler()  # 创建控制台日志输出对象
        if LOG_FILE:  # 当设置了文件名,则日志记录到文件
            self.file_handler = logging.FileHandler(filename=LOG_FILE, encoding=ENCODING)  # 创建日志文件对象
        self.set_log()  # 设置日志
        try:
            self.handle()
        except ConnectionResetError:
            self.shutdown_request()
        except BrokenPipeError:
            self.shutdown_request()

    def handle(self):
        """
        只要有请求进来,然后开始处理请求
        :return:
        """
        while True:
            try:
                self.logger.debug("——————————————————等待用户新请求信息————————————————————")
                data = self.recv_all()
                self.logger.debug("handle 收到data [{}]".format(data))
                if len(str(data)) > 0:
                    self.exec_instruction(data)
                    if self.retry_count < 1:
                        self.logger.warning("该用户尝试登陆次数过于频繁,已将该客户端强制登出系统")
                        break
                else:
                    self.shutdown_request()
                    break
            except OSError:
                self.logger.warning("该客户端[{}]端口[{}]可疑".format(*self.client_address))
                self.shutdown_request()
                break

    def exec_instruction(self, instruction):
        """
        :param instruction: 根据请求内容开始分配对应的请求
        :return:
        """
        if type(instruction) == bytes:
            instruction = str(instruction, ENCODING)
        if type(instruction) != str:
            instruction = str(instruction)
        self.request_command = instruction
        self.logger.info("收到客户端[{}]端口[{}]请求数据[{}]".format(*self.client_address, self.request_command))
        if instruction.count("|") > 0:
            self.logger.debug("——————————————客户端指令错误,准备通知客户端此消息——————————————")
            self.send_all("201", {"data": self.ERROR_CODE.get(201)})
            self.logger.debug("————————————告知客户端错误信息完毕——————————")
        else:
            instruction = instruction.split()  # 将指令解析,分隔 command|{"json_data"}
            if len(instruction) > 1:
                attr = instruction[0]
                if len(attr.split()) > 1:
                    attr, command = attr.split()[0], attr
            else:
                attr = instruction[0]
            if not self.login:
                self.logger.info("检测到该客户端未登陆")
                self.login = self._auth_login
                self.retry_count -= 1
                self.logger.info("客户端[{}]端口[{}]用户未登陆,开始进行身份认证".format(*self.client_address))
                if self.retry_count < 1:
                    self.logger.debug("客户端重试次数过多,准备进入关闭该客户端连接任务")
                    self.shutdown_request()
                    self.logger.debug("已将一个客户端连接强制关闭")
            elif self.login:
                self.retry_count = 3  # 当验证通过,则重置登陆次数
                self.logger.debug("客户端[{}]端口[{}],进入指令控制中心".format(*self.client_address))
                if hasattr(self, attr) and attr in self.command_list:
                        attr = getattr(self, attr)
                        self.logger.debug("——————————————————正在执行客户端请求中 ...——————————————————")
                        attr()
                        self.logger.debug("————————————————————请求执行完毕————————————————————")
                else:
                    if attr != "101":  # 101为客户端程序第一次主动发起连接服务器的请求代码,故忽略该错误指令
                        self.logger.debug("用户输入了错误的请求信息,准备向客户端通告此错误")
                        self.send_all("202", {"data": self.ERROR_CODE.get(202)})
                        self.logger.debug("通告客户端信息完毕")

    @property
    def _auth_login(self):
        """
        针对用户进行认证及设置用户家目录
        :return: 返回登陆成功的用户名
        """
        try:
            if ENABLE_ANONYMOUS:
                self.logger.debug("向客户端发送登陆欢迎语")
                self.send_all("104", {"data": "欢迎登陆FTP", "username": "anonymous"})
                self.logger.debug("检查客户端家目录状态")
                if not os.path.exists(PUBLIC_DATA):
                    os.makedirs(PUBLIC_DATA)
                self.home_dir = PUBLIC_DATA
                os.chdir(self.home_dir)
                self.logger.info("客户端[{}]端口[{}],用户名[{}]身份认证成功".format(*self.client_address, "anonymous"))
                return "anonymous"
            self.send_all("102", {"data": self.ERROR_CODE.get(102)})
            self.send_all("107", {"data": "用户名: "})
            name = self.recv_all()
            if type(name) is not bytes:
                raise TypeError("没有得到正确的值")
            username = str(name, ENCODING)
            self.send_all("105", {"data": "密码: "})
            pwd = self.recv_all()
            if type(pwd) is not bytes:
                raise TypeError("没有得到正确的值")
            password = str(pwd, ENCODING)
            if verify.login(username, password):
                self.send_all("104", {"data": "欢迎登陆FTP", "username": username})
                if not os.path.exists(os.path.join(USER_DATA, username)):
                    os.makedirs(os.path.join(USER_DATA, username))
                    sys.stdout.flush()
                self.home_dir = os.path.join(USER_DATA, username)
                os.chdir(self.home_dir)
                self.logger.info("客户端[{}]端口[{}],用户名[{}]身份认证成功".format(*self.client_address, username))
                return username
            else:
                self.logger.warning("客户端登陆失败,准备通告客户端此错误信息")
                self.send_all("102", {"data": self.ERROR_CODE.get(102)})
                self.logger.debug("错误信息通过完毕,正在返回下一个任务流")
                return False
        except TypeError:
            self.logger.debug("身份验证时,出现了一点小问题,被忽略 ...")
            self.retry_count = -1
            return False

    def shutdown_request(self):
        """
        关闭断开的请求连接
        :return:
        """
        try:
            self.logger.info("客户端[{}]端口[{}]已离开,正在断开客户端连接请求 ...".format(*self.client_address))
            self.logger.debug("尝试最后一次发送给客户端断开请求")
            self.send_all("504", {"data": self.ERROR_CODE.get(504)})
            self.request.close()
            self.logger.debug("与客户端连接断开")
        except OSError:
            self.logger.warning("客户端[{}]端口[{}]已强制断开连接".format(*self.client_address))
            pass

    def recv_data(self):
        """
        接收请求数据
        :return: 返回已收到的数据
        """
        data = self.request.recv(RECV_BUFFER)
        if len(data) > 0:
            self.logger.debug("接收到一条消息")
            return data
        else:
            self.logger.debug("未接收到消息")
            return False

    def send_data(self, data):
        """
        发送请求数据
        :param data: bytes数据类型
        :return: 返回已发送的大小
        """
        self.logger.debug("发送了一条消息")
        return self.request.send(data)

    def recv_all(self):
        """
        接收所有数据
        :return: 返回已接受到的所有数据
        """
        self.logger.debug("————————————————进入接收所有数据模式——————————————")
        self.logger.debug("第一次接收")
        respond_message = self.recv_data()
        if not type(respond_message) is bytes:
            self.logger.debug("分离信息时遇到错误,返回空 ...")
            return
        self.logger.debug("收到消息[{}]".format(respond_message))
        self.request_message = respond_message
        respond_message = str(respond_message, ENCODING).split("|")
        self.logger.debug("正在分离用户信息 ...")
        respond_json_data = self.str_to_json(respond_message[1])
        total_size = respond_json_data.get("total_size")
        if total_size is None:
            self.logger.debug("接收总大小数据为空,将该值设为-1")
            total_size = -1
        self.logger.debug("得到分离新[total_size][{}]".format(total_size))
        self.logger.debug("第一次回应")
        self.send_data(b"READY_TO_RECIVE")
        self.logger.debug("回应发送完毕")
        data = b""
        temp = "-1"
        received_size = -1
        self.logger.debug("开始进入循环接收数据中 ...")
        while received_size != total_size and temp:
            temp = self.recv_data()
            if temp:
                data += temp
                received_size = len(data)
                self.logger.debug("收到数据大小[{}]".format(received_size))
        if respond_json_data.get("md5") and self.encode_data(data) != respond_json_data.get("md5"):
            self.logger.warning("向客户端发送警告,md5值不一致")
            self.send_all("451", {"data": self.ERROR_CODE.get(451)})
            self.logger.debug("md5值警告发送完毕")
        else:
            if respond_message[0] == "504":
                self.logger.debug("收到指令[{}],准备断开连接".format(self.ERROR_CODE.get(504)))
                return 504
            elif respond_message[0] == "452":
                self.logger.warning("权限不足[{}]".format(self.ERROR_CODE.get(452)))
                return 452
            elif respond_message[0] == "201":
                self.logger.warning("命令不正常[{}]".format(self.ERROR_CODE.get(201)))
                return 201
            elif respond_message[0] == "451":
                self.logger.warning("md5值异常[{}]".format(self.ERROR_CODE.get(451)))
                return 451
            else:
                self.logger.debug("————————————————将接收对数据返回给下一个任务————————————————")
                return data

    def send_all(self, code, json_data):
        """
        发送所有数据
        :param code: FTP代码
        :param json_data: 字典数据类型,发送前自动转换为json
        :return:
        """
        self.logger.debug("————————————————————进入发送所有数据模式————————————————————————————")
        self.logger.debug("发送数据内容[{}]".format(json_data))
        data = json_data["data"]  # data只能是二进制数据
        self.logger.debug("将请求的指令[{}]提取出来".format(data))
        if not type(data) is bytes:  # 如果数据不是bytes类型,将转换成bytes
            data = bytes(data, ENCODING)
        if not json_data.get("total_size"):
            json_data["total_size"] = len(data)  # 计算数据长度
        self.logger.debug("计算本次发送指令数据大小[{}]".format(json_data["total_size"]))
        json_data["md5"] = self.encode_data(data)
        self.logger.debug("计算数据的md5值[{}]".format(json_data["md5"]))
        self.logger.debug("将请求指令与额外信息分离")
        json_data.pop("data")
        message = '{}|{}'.format(code, self.json_to_str(json_data))
        if not type(message) is bytes:  # 如果数据不是bytes类型,将转换成bytes
            message = bytes(message, ENCODING)
        self.logger.debug("第一次发送请求[{}]".format(message))
        self.send_data(message)
        self.logger.debug("第一次接收客户端回应")
        request_reply = self.recv_data()
        if not request_reply:
            self.logger.debug("没有收到服务器回应,返回False")
            return False
        self.logger.debug("客户端回应[{}]".format(request_reply))
        if request_reply == b"READY_TO_RECIVE":
            self.logger.debug("开始循环发送数据中 ...")
            total_size = json_data["total_size"]
            self.logger.debug("本次发送数据大小[{}]".format(total_size))
            while total_size > 0:
                total_size -= self.send_data(data)
            return True
        else:
            self.logger.debug("客户端回应[{}]错误".format(request_reply))
            return False

    def set_log(self):
        """
        设置日志输出方式
        :return:
        """
        self.logger.setLevel(LOG_LEVEL)  # 设置日志记录级别
        if OUTPUT_CONSOLE:  # 当设置了输出屏幕日志,则启用该日志打印屏幕功能,默认开启
            self.console_handler.setLevel(CONSOLE_LOG_LEVEL)
            self.console_handler.setFormatter(FORMATTER)
            self.logger.addHandler(self.console_handler)
        if LOG_FILE:  # 当设置了文件名,则启用记录日志文件功能,默认关闭
            self.file_handler.setLevel(FILE_LOG_LEVEL)
            self.file_handler.setFormatter(FORMATTER)
            self.logger.addHandler(self.file_handler)

    @staticmethod
    def json_to_str(obj):
        """
        :param obj: 字典或列表等其他数据类型
        :return: 返回一个字符串类型
        """
        json_obj = json.dumps(obj)
        return json_obj

    @staticmethod
    def str_to_json(obj):
        """
        :param obj: 字符串类型
        :return: 还原成真实的数据类型
        """
        json_obj = json.loads(obj)
        return json_obj

    @staticmethod
    def bytes_to_str(bytesobj):
        return str(bytesobj, ENCODING)

    def get_abspath(self, fileobj):
        cur_path = os.path.abspath(fileobj)
        self.logger.debug("绝对路径[{}]".format(cur_path))
        return cur_path

    def is_owner(self, file_location):
        """
        通过与用户家目录进行对比,判断用户指定的位置是否属于家目录范围
        :param file_location: 文件目标位置
        :return: 属于返回文件对绝对路径
        """
        self.logger.debug("检查用户的权限是否可以访问该文件名")
        if file_location.split("/")[0] == "":  # 当用户输入的起始位置为绝对路径/开始,则对该路径进行拼接,加上用户家目录处理
            file_location = os.path.join(self.home_dir, "./{}".format(file_location.split("/", maxsplit=1)[1]))
        new_path = os.path.abspath(file_location)
        commonpath = os.path.commonpath([new_path, self.home_dir])
        if commonpath == self.home_dir:
            self.logger.debug("给用户返回一个绝对路径")
            return self.get_abspath(file_location)
        else:
            self.logger.debug("该用户无此权限访问该文件名")
            return False

    @staticmethod
    def encode_data(obj):
        """
        :param obj: 将对象转换成字符串加密
        :return: 返回字符串加密结果
        """
        import hashlib
        md5 = hashlib.md5(str(obj).encode("utf-8"))
        md5.update(str(obj).encode("utf-8"))
        data_md5 = md5.hexdigest()
        return data_md5

    def check_type(self, filename):
        filename = self.get_abspath(filename)
        if os.path.isdir(filename):
            return "dir"
        if os.path.isfile(filename):
            return "file"
        else:
            return False

    def pwd(self):
        self.logger.debug("查看当前路径")
        abspath = os.path.abspath(os.path.curdir)
        cur_path = abspath.split(self.home_dir)[1]
        if len(cur_path) < 1:
            cur_path = "/{}".format(cur_path)
        return self.send_all("200", {"data": "当前路径\n{}".format(cur_path)})

    def get(self):
        self.logger.debug("——————————客户端请求get数据——————————————————")
        get_args = self.parse_cmd()
        if get_args:
            self.logger.debug("解析命令成功[{}]".format(get_args))
            in_server_file, to_client_location = get_args
        else:
            self.logger.debug("解析失败,准备向客户端通告错误消息")
            self.send_all("201", {"data": self.ERROR_CODE.get(201)})
            self.logger.debug("客户端使用get请求失败")
            return False
        seek = 0  # 默认seek值为0
        file_type = self.check_type(in_server_file)
        self.logger.debug("文件属性[{}]".format(file_type))
        last_seek = self.str_to_json(self.bytes_to_str(self.request_message).split("|")[1]).get("seek")
        if last_seek:
            self.logger.debug("获取到上一次seek值[{}]".format(last_seek))
            seek = last_seek
        self.logger.debug("获取到seek值[{}]".format(seek))
        in_server_file = self.is_owner(in_server_file)
        if not in_server_file or not os.path.exists(in_server_file):
            self.logger.debug("权限不足,准备向客户端通过此消息")
            self.send_all("452", {"data": self.ERROR_CODE.get(452)})
            self.logger.debug("get请求失败,返回False")
            return False
        total_size = os.path.getsize(in_server_file)
        self.logger.debug("get文件的总大小为[{}]".format(total_size))
        if str(file_type) == "dir":
            self.send_all("453", {"data": self.ERROR_CODE.get(453), "type": file_type})
            return True
        while True:
            self.logger.debug("开始循环读取文件中 ...")
            data_obj = self.readfile(in_server_file, seek)
            for data in data_obj:
                if type(data) == bool and not data:
                    self.logger.warning("文件[{}]不存在".format(in_server_file))
                    break
                else:
                    self.logger.debug("获取到数据大小[{}]".format(data[1]))
                    self.send_all("208", {"data": data[0],
                                          "seek": data[1],
                                          "file_size": total_size,
                                          "save_to_file": to_client_location})
            print()
            break
        self.logger.info("客户端[{}][{}]接收文件[{}]完成".format(*self.client_address, in_server_file))

    def parse_cmd(self):
        """
        解析命令参数,主要针对get命令,
        :return: 解析成功,将返回本地服务器文件,及客户端的文件名
        """
        if len(str(self.request_command).split()) == 3:
            in_server_file = str(self.request_command).split()[1]
            to_client_location = str(self.request_command).split()[2]
        elif len(str(self.request_command).split()) == 2:
            in_server_file = str(self.request_command).split()[1]
            to_client_location = str(self.request_command).split()[1]
        else:
            return False
        return in_server_file, to_client_location

    def handle_exist_file(self, filepath, action=None):
        if action == "1":
            reduce_size = os.stat(filepath).st_size
            os.remove(filepath)
            if reduce_size:
                self.modify_size(-reduce_size)
        elif action == "2":
            os.rename(filepath, "{}_2".format(filepath))
        elif action == "3":
            return os.path.getsize(filepath)

    def check_file_path(self, filename):
        """
        检查文件状态,是否存在,或者是否为目录
        :param filename:
        :return:
        """
        action = str(None)  # 初始化一个属性,用来存储用户针对文件操作
        if os.path.exists(filename):
            if os.path.isdir(filename):
                self.logger.debug("当前存在相同文件名的目录,请更换其他名字")
            elif os.path.isfile(filename):
                while True:
                    self.logger.debug("服务端存在相同文件名文件,准备发送交互信息")
                    self.send_all("209", {"data": "当前目录已存在该文件\n\t1.覆盖\n\t2.重命名原文件\n\t3.继续上传\n 请选择: "})
                    self.logger.debug("交互消息发送完毕,准备接收交互消息")
                    action = self.bytes_to_str(self.recv_all())
                    self.logger.debug("交互消息接收完毕,准备判断结果")
                    if action in ["1", "2", "3"]:
                        self.logger.debug("交互结果符合要求,准备通告客户端处理结果")
                        self.send_all("208", {"data": self.ERROR_CODE.get(208)})
                        self.logger.debug("交互通告结束")
                        break
        else:
            self.logger.debug("检查目录是否创建,未创建则尝试新建目录")
            basedir = os.path.dirname(filename)
            if not os.path.exists(basedir):
                os.makedirs(basedir)  # 如果多级目录,不存在则创建
        self.logger.debug("返回文件状态结果")
        return self.handle_exist_file(filename, action)

    def put(self):
        self.logger.debug("——————————————————进入put操作模式————————————————————")
        get_args = self.parse_cmd()
        if get_args:
            self.logger.debug("指令解析成功[{}]".format(get_args))
            to_client_location, in_server_file = get_args
        else:
            self.logger.debug("指令解析失败,返回False")
            return False
        in_server_file = self.is_owner(in_server_file)
        if not in_server_file:
            self.logger.info("权限不足,准备向客户端通告[{}]".format(in_server_file))
            self.send_all("452", {"data": self.ERROR_CODE.get(452)})
            self.logger.debug("权限不足,通告完毕,返回False")
            return False
        if os.path.isdir(in_server_file):
            in_server_file = os.path.join(in_server_file, to_client_location)
        seek = 0
        file_info = self.str_to_json(self.bytes_to_str(self.request_message).split("|")[1])
        last_seek = self.check_file_path(in_server_file)
        if last_seek:
            self.logger.debug("检查到上一次seek大小[{}]".format(last_seek))
            seek = last_seek
        file_type = file_info.get("type")
        if str(file_type) == "dir":
            if not os.path.exists(in_server_file):
                os.makedirs(in_server_file)
                if self.get_size(os.stat(in_server_file).st_size):
                    self.logger.info("目录[{}]创建成功".format(in_server_file))
                    self.modify_size(os.stat(in_server_file).st_size)
                    self.send_all("453", {"data": self.ERROR_CODE.get(453)})
                    return True
                else:
                    os.removedirs(in_server_file)
                    self.send_all("455", {"data": self.ERROR_CODE.get(455)})
            return True
        self.logger.debug("准备告知客户端已准备接收文件,并告知客户端接收seek位置")
        avail_size = database.get(self.login)
        if avail_size:
            avail_size = database[self.login]["avail"]
        else:
            avail_size = QUTOTA_SIZE
        self.send_all("208", {"data": self.ERROR_CODE.get(208), "seek": seek, "avail": avail_size})
        self.logger.debug(" 通告消息发送完毕")
        received_size = 0
        total_size = file_info.get("file_size")
        if not self.get_size(total_size):
            self.logger.warning("该用户[{}]空间不够".format(self.login))
            self.send_all("455", {"data": self.ERROR_CODE.get(455)})
            return False
        if not total_size or total_size <= seek:
            self.logger.info("上传数据小于本地已存在的文件大小")
            return False
        percent = 0  # 初始百分比
        total_size -= seek
        while received_size != total_size:
            self.logger.debug("==========接收文件中 ...============")
            data = self.recv_all()
            try:
                self.request_message = str(self.request_message, ENCODING).split("|")
            except TypeError:
                break
            self.logger.debug("收到[{}]".format(self.request_message))
            respond_json_data = self.str_to_json(self.request_message[1])
            if respond_json_data.get("md5") and self.encode_data(data) != respond_json_data.get("md5"):
                self.logger.debug("数据接收不完整 !!!继续接收完,但不写入")
                received_size += len(data)
                continue

            seek = respond_json_data.get("seek")
            self.writefile(in_server_file, data, total_size, seek, "a+b")
            if total_size % RECV_BUFFER == 0:
                times = int(total_size / RECV_BUFFER)  # 刚好传完的次数
            else:
                times = int(total_size / RECV_BUFFER) + 1  # 否则,次数再加一次
            count = 100 / times  # 计算每次增加的百分比
            percent += float(count)
            hashes = "#" * int(percent / 100.0 * 65)
            spaces = " " * (65 - len(hashes))
            percent_format = "{:.2f}".format(percent)
            space = " " * (6 - len(percent_format))
            sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent_format + space, hashes + spaces))
            sys.stdout.flush()
            received_size += len(data)
        print()
        self.logger.debug("——————————————put请求完毕————————————————————————")

    def readfile(self, filename, seek):
        if not os.path.exists(filename):
            self.send_all("452", {"data": self.ERROR_CODE.get(452)})
            yield False
            return False
        total_size = os.path.getsize(filename)
        total_size -= seek  # 减去已发送的数据大小
        if total_size % RECV_BUFFER == 0:
            times = int(total_size / RECV_BUFFER)  # 刚好传完的次数
        else:
            times = int(total_size / RECV_BUFFER) + 1  # 否则,次数再加一次
        if times == 0:
            self.send_all("453", {"data": self.ERROR_CODE.get(453)})
            self.logger.info("文件[{}]读取完毕".format(filename))
            return False
        percent = 0  # 初始百分比
        count = 100 / times  # 计算每次增加的百分比

        while total_size > 0:
            percent += float(count)
            hashes = "#" * int(percent / 100.0 * 65)
            spaces = " " * (65 - len(hashes))
            percent_format = "{:.2f}".format(percent)
            space = " " * (6 - len(percent_format))
            sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent_format + space, hashes + spaces))
            sys.stdout.flush()
            with open(filename, "rb") as readdata:
                readdata.seek(seek)
                has_read = readdata.read(RECV_BUFFER)
                if has_read:
                    seek = readdata.tell()
                    total_size -= RECV_BUFFER
                    yield has_read, seek
                else:
                    readdata.close()

    def writefile(self, filename, data, total_size, seek=0, mode="a+b"):
        self.modify_size(len(data))  # 实时更新磁盘空间大小
        if not total_size:
            return True
        with open(filename, mode) as writedata:
            writedata.seek(seek)
            writedata.write(data)
            writedata.flush()

    def help(self):
        doc = """
        ls 查看当前目录
        info 显示当前用户使用空间状态
        cd dir 进入远程主机目录
        dir 查看当前目录
        chmod file-name [mode] 设置远程主机的文件权限 ,默认755,mode只能是三位数字权限,最大777,读4,写2,执行1
        bye 注销当前用户
        rm remote-file  删除远程主机的文件,不能删除目录
        rmdir remote-dir  删除远程主机目录
        get remote-files [local-file]    将远程文件下载到本地
        put local-file [remote-file]    将本地文件上传到服务器
        pwd 查看当前目录
        quit 退出FTP会话,同bye
        mkdir folder_name [mode] 创建目录 默认权限755,mode只能是三位数字权限,最大777,读4,写2,执行1
        """
        self.send_all("200", {"data": doc})

    def cd(self):
        if len(str(self.request_command).split()) > 1:
            new_path = str(self.request_command).split()[1]
        else:
            new_path = "."
        new_abspath = self.is_owner(new_path)
        if new_abspath:
            if os.path.isdir(new_abspath):
                os.chdir(new_abspath)
            else:
                self.send_all("452", {"data": "访问目录不存在,或您无权限访问"})
        else:
            self.send_all("452", {"data": "权限不足,访问拒绝"})

    @staticmethod
    def exec(command):
        stdout = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = stdout.stderr.read()
        if not result:
            result = stdout.stdout.read()
        return result

    def ls(self):
        if sys.platform.startswith("win32"):
            self.request_command = str(self.request_command).replace("ls", "dir")
            self.dir()
        else:
            result = self.exec(self.request_command)
            self.send_all("200", {"data": result})

    def dir(self):
        if sys.platform.startswith("win32"):
            result = self.exec(self.request_command)
            self.send_all("200", {"data": result})
        else:
            self.request_command = str(self.request_command).replace("dir", "ls")
            self.ls()

    def mkdir(self):
        if len(str(self.request_command).split()) > 2:
            new_folder = str(self.request_command).split()[1]
            mode = str(self.request_command).split()[2]
            if mode.isdigit() and len(mode) == 3:
                test = list(filter(lambda i: int(i) <= 7, str(mode)))
                if len(test) == 3:
                    mode = "0o{}".format(mode)
                else:
                    self.send_all("201", {"data": self.ERROR_CODE.get(201)})
                    return False
            else:
                self.send_all("201", {"data": self.ERROR_CODE.get(201)})
                return False
        elif len(str(self.request_command).split()) > 1:
            new_folder = str(self.request_command).split()[1]
            mode = "0o755"
        else:
            self.send_all("201", {"data": self.ERROR_CODE.get(201)})
            return False
        if not os.path.exists(str(self.request_command).split()[1]):
            os.makedirs(new_folder, mode=eval(mode))
            self.send_all("204", {"data": self.ERROR_CODE.get(204)})
        else:
            self.send_all("200", {"data": "目标目录已存在"})

    def rmdir(self):
        if len(str(self.request_command).split()) == 2:
            folder = str(self.request_command).split()[1]
            if os.path.isdir(folder):
                try:
                    os.removedirs(folder)
                    self.send_all("200", {"data": self.ERROR_CODE.get(200)})
                except OSError:
                    self.send_all("452", {"data": self.ERROR_CODE.get(452)})
            else:
                self.send_all("202", {"data": self.ERROR_CODE.get(202)})
        else:
            self.send_all("201", {"data": self.ERROR_CODE.get(201)})

    def rm(self):
        if len(str(self.request_command).split()) == 2:
            filename = str(self.request_command).split()[1]
            if os.path.isfile(filename):
                reduce_size = os.stat(filename).st_size
                os.remove(filename)
                self.modify_size(-reduce_size)
                self.send_all("200", {"data": self.ERROR_CODE.get(200)})
            else:
                self.send_all("202", {"data": self.ERROR_CODE.get(202)})
        else:
            self.send_all("201", {"data": self.ERROR_CODE.get(201)})

    def chmod(self):
        if len(str(self.request_command).split()) > 2:
            folder = str(self.request_command).split()[1]
            mode = str(self.request_command).split()[2]
            if mode.isdigit() and len(mode) == 3:
                test = list(filter(lambda i: int(i) <= 7, str(mode)))
                if len(test) == 3:
                    mode = "0o{}".format(mode)
                else:
                    self.send_all("201", {"data": self.ERROR_CODE.get(201)})
                    return False
            else:
                self.send_all("201", {"data": self.ERROR_CODE.get(201)})
                return False
        elif len(str(self.request_command).split()) > 1:
            folder = str(self.request_command).split()[1]
            mode = "0o755"
        else:
            self.send_all("201", {"data": self.ERROR_CODE.get(201)})
            return False
        if os.path.exists(folder):
            os.chmod(folder, mode=eval(mode))
            self.send_all("200", {"data": self.ERROR_CODE.get(200)})
        else:
            self.send_all("452", {"data": self.ERROR_CODE.get(452)})

    def bye(self):
        """
        注销用户登陆状态
        :return:
        """
        self.login = None
        self.send_all("200", {"data": "谢谢使用"})

    def quit(self):
        self.bye()

    def modify_size(self, size):
        """
        修改写入数据的大小
        :param size:
        :return:
        """
        user_database = database.get(self.login)
        if user_database:
            total_size = user_database.get("qutota")
            used_size = user_database.get("used")
            avail_size = user_database.get("avail")
            if not total_size:
                total_size = QUTOTA_SIZE
            if not used_size:
                used_size = 0
            if not avail_size:
                avail_size = 0
            if (size + int(used_size)) < int(total_size):
                used_size = int(used_size) + size
                avail_size = int(total_size) - int(used_size)
                user_database["qutota"] = total_size
                user_database["used"] = used_size
                user_database["avail"] = avail_size
                database[self.login] = user_database
                connect_database["data"] = database
                return database

    def get_size(self, size):
        """
        匿名用户不计算大小,返回为真,普通用户进配额检测
        :param size: 准备写入的数据大小
        :return: 如果空间可用,返回真,匿名用户不参与计算配额,
        """
        if not size:
            return True
        user_database = database.get(self.login)
        if user_database:
            total_size = user_database.get("qutota")
            used_size = user_database.get("used")
            if not total_size:
                total_size = QUTOTA_SIZE
            if not used_size:
                used_size = 0
            if (size + int(used_size)) < int(total_size):
                return True
            return False
        return True

    def info(self):
        user_database = database.get(self.login)
        if user_database:
            total_size = user_database.get("qutota")
            used_size = user_database.get("used")
            avail_size = user_database.get("avail")
            msg = """用户名     [{}]
            总大小     [{}]
            已使用     [{}]
            可用空间    [{}]
            """.format(self.login, total_size, used_size, avail_size)
            self.send_all("200", {"data": msg})
            return True


def main():

    try:
        server_address = (LISTEN, int(PORT))
        server = socketserver.ThreadingTCPServer(server_address, FTPServer)
        server.serve_forever(2)
    except KeyboardInterrupt:
        server.server_close()
        print("服务器强制被关闭")
    except OSError:
        print("Address already in use")
