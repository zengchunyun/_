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
from settings.settings import LISTEN, PORT, RECV_BUFFER, BASE_DIR, LOG_DIR, USER_DATA, database,\
    LOG_FILE, LOG_LEVEL, CONSOLE_LOG_LEVEL, FILE_LOG_LEVEL, OUTPUT_CONSOLE, FORMATTER, ENCODING,\
    ENABLE_ANONYMOUS, PUBLIC_DATA
from core.userverify import UserVerify


connect_database = shelve.open(database)  # 打开可持久化数据文件
database = connect_database.get("data")  # 获取键为data的数据
verify = UserVerify(database)  # 将UserVerify类进行实例化


class FTPServer(object):
    ERROR_CODE = {
        125: "Data connection already open; transfer starting.",
        150: "File status okay; about to open data connection.",
        200: "Command okay.",
        202: "Command not implemented, superfluous at this site.",
        211: "System status, or system help reply.",
        212: "Directory status.",
        213: "File status.",
        220: "Service ready for new user.",
        221: "Service closing control connection.",
        225: "Data connection open; no transfer in progress.",
        226: "Closing data connection. Requested file action successful (for example, file transfer or file abort).",
        227: "Entering Passive Mode (h1,h2,h3,h4,p1,p2).",
        230: "User logged in, proceed. Logged out if appropriate.",
        250: "Requested file action okay, completed.",
        257: '"PATHNAME" created.',
        331: "User name okay, need password.",
        332: "Need account for login.",
        350: "Requested file action pending further information",
        421: "Service not available, closing control connection.This may be a reply to any command if the service knows it must shut down.",
        425: "Can't open data connection.",
        426: "Connection closed; transfer aborted.",
        450: "Requested file action not taken.",
        451: "Requested action aborted. Local error in processing.",
        452: "Requested action not taken. Insufficient storage space in system.File unavailable (e.g., file busy).",
        500: "Syntax error, command unrecognized. This may include errors such as command line too long.",
        501: "Syntax error in parameters or arguments.",
        502: "Command not implemented.",
        503: "Bad sequence of commands.",
        504: "Command not implemented for that parameter.",
        530: "Not logged in.",
        532: "Need account for storing files.",
        550: "Requested action not taken. File unavailable (e.g., file not found, no access).",
        551: "Requested action aborted. Page type unknown.",
        552: "Requested file action aborted. Exceeded storage allocation (for current directory or dataset).",
        553: "Requested action not taken. File name not allowed",
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
        # 定义命令列表,可以起到限制命令功能
        self.command_list = ["ls", "pwd", "cd", "put", "get", "dir", "help", "bye", "quit", "mkdir", "rmdir", "rm", "chmod"]
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
                data = self.recvall()
            except OSError:
                self.logger.warning("该客户端[{}]端口[{}]可疑".format(*self.client_address))
                self.shutdown_request()
                break
            if data:
                self.logger.info("收到客户端[{}]端口[{}]请求数据[{}]".format(*self.client_address, data.decode()))
                self.exec_instruction(data)
                if self.retry_count < 1:
                    self.logger.warning("该用户尝试登陆次数过于频繁,已将该客户端强制登出系统")
                    break
            else:
                self.shutdown_request()
                break

    def exec_instruction(self, instruction):
        """
        :param instruction: 根据请求内容开始分配对应的请求
        :return:
        """
        instruction = str(instruction, ENCODING)
        self.request_command = instruction
        if instruction.count("|") > 0:
            self.logger.debug("——————————————客户端指令错误,准备通知客户端此消息——————————————")
            self.sendall("501", {"data": self.ERROR_CODE.get(501)})
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
            if self.login:
                self.retry_count = 3  # 当验证通过,则重置登陆次数
                self.logger.debug("客户端[{}]端口[{}],进入指令控制中心".format(*self.client_address))
                if hasattr(self, attr) and attr in self.command_list:
                        attr = getattr(self, attr)
                        self.logger.debug("——————————————————正在执行客户端请求中 ...——————————————————")
                        attr()
                        self.logger.debug("————————————————————请求执行完毕————————————————————")
                else:
                    if attr != "220":  # 220为客户端程序第一次主动发起连接服务器的请求代码,故忽略该错误指令
                        self.logger.debug("用户输入了错误的请求信息,准备向客户端通告此错误")
                        self.sendall("502", {"data": self.ERROR_CODE.get(502)})
                        self.logger.debug("通告客户端信息完毕")
            else:
                self.logger.info("客户端[{}]端口[{}]用户未登陆,开始进行身份认证".format(*self.client_address))
                if self.retry_count < 1:
                    self.logger.debug("客户端重试次数过多,准备进入关闭该客户端连接任务")
                    self.shutdown_request()
                    self.logger.debug("已将一个客户端连接强制关闭")

    @property
    def _auth_login(self):
        """
        针对用户进行认证及设置用户家目录
        :return: 返回登陆成功的用户名
        """
        try:
            if ENABLE_ANONYMOUS:
                self.logger.debug("向客户端发送登陆欢迎语")
                self.sendall("230", {"data": "欢迎登陆FTP", "username": "anonymous"})
                self.logger.debug("检查客户端家目录状态")
                if not os.path.exists(PUBLIC_DATA):
                    os.mkdir(PUBLIC_DATA)
                self.home_dir = PUBLIC_DATA
                os.chdir(self.home_dir)
                self.logger.info("客户端[{}]端口[{}],用户名[{}]身份认证成功".format(*self.client_address, "anonymous"))
                return "anonymous"
            self.sendall("530", {"data": self.ERROR_CODE.get(530)})
            self.sendall("332", {"data": "用户名: "})
            username = str(self.recvall(), ENCODING)
            self.sendall("331", {"data": "密码: "})
            password = str(self.recvall(), ENCODING)
            if verify.login(username, password):
                self.sendall("230", {"data": "欢迎登陆FTP", "username": username})
                if not os.path.exists(os.path.join(USER_DATA, username)):
                    os.makedirs(os.path.join(USER_DATA, username))
                self.home_dir = os.path.join(USER_DATA, username)
                os.chdir(self.home_dir)
                self.logger.info("客户端[{}]端口[{}],用户名[{}]身份认证成功".format(*self.client_address, username))
                return username
            else:
                self.logger.warning("客户端登陆失败,准备通告客户端此错误信息")
                self.sendall("530", {"data": self.ERROR_CODE.get(530)})
                self.logger.debug("错误信息通过完毕,正在返回下一个任务流")
                return False
        except TypeError:
            self.logger.debug("身份验证时,出现了一点小问题,被忽略 ...")
            return False

    def shutdown_request(self):
        """
        关闭断开的请求连接
        :return:
        """
        try:
            self.logger.info("客户端[{}]端口[{}]已离开,正在断开客户端连接请求 ...".format(*self.client_address))
            self.logger.debug("尝试最后一次发送给客户端断开请求")
            self.sendall("221", {"data": self.ERROR_CODE.get(221)})
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
        self.logger.debug("接收到一条消息")
        return self.request.recv(RECV_BUFFER)

    def send_data(self, data):
        """
        发送请求数据
        :param data: bytes数据类型
        :return: 返回已发送的大小
        """
        self.logger.debug("发送了一条消息")
        return self.request.send(data)

    def recvall(self):
        """
        接收所有数据
        :return: 返回已接受到的所有数据
        """
        self.logger.debug("————————————————进入接收所有数据模式——————————————")
        self.logger.debug("第一次接收")
        respond_message = self.recv_data()
        if len(respond_message) < 1:
            self.logger.debug("分离信息时遇到错误 ...")
            return False
        self.logger.debug("收到消息[{}]".format(respond_message))
        self.request_message = respond_message
        respond_message = str(respond_message, ENCODING).split("|")
        self.logger.debug("正在分离用户信息 ...")
        respond_json_data = self.str_to_json(respond_message[1])
        total_size = respond_json_data.get("total_size")
        self.logger.debug("得到分离新[total_size][{}]".format(total_size))
        if total_size:
            self.logger.debug("第一次回应")
            self.send_data(b"READY_TO_RECIVE")
            self.logger.debug("回应发送完毕")
            data = b""
            temp = "-1"
            received_size = -1
            self.logger.debug("开始进入循环接收数据中 ...")
            while received_size != total_size and len(temp) != 0:
                temp = self.recv_data()
                data += temp
                received_size = len(data)
                self.logger.debug("收到数据大小[{}]".format(received_size))
            if respond_json_data.get("md5") and self.encode_data(data) != respond_json_data.get("md5"):
                self.logger.warning("向客户端发送警告,md5值不一致")
                self.sendall("451", {"data": self.ERROR_CODE.get(451)})
                self.logger.debug("md5值警告发送完毕")
            else:
                self.logger.debug("————————————————将接收对数据返回给下一个任务————————————————")
                return data
        else:
            self.logger.debug("发送消息的大小为[{}],未发送".format(total_size))
        self.logger.debug("________________接收所有数据完毕————————————————————————————")

    def sendall(self, code, json_data):
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
        self.logger.debug("客户端回应[{}]".format(request_reply))
        if request_reply == b"READY_TO_RECIVE":
            self.logger.debug("开始循环发送数据中 ...")
            total_size = json_data["total_size"]
            self.logger.debug("本次发送数据大小[{}]".format(total_size))
            while total_size > 0:
                total_size -= self.send_data(data)
        else:
            self.logger.debug("客户端回应错误")
        self.logger.debug("————————————————————————所有数据发送完毕 !——————————————————————————")

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

    @staticmethod
    def get_abspath(fileobj):
        cur_path = os.path.abspath(fileobj)
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

    def pwd(self):
        self.logger.debug("查看当前路径")
        abspath = os.path.abspath(os.path.curdir)
        cur_path = abspath.split(self.home_dir)[1]
        return self.sendall("200", {"data": "当前路径\n/{}".format(cur_path)})

    def get(self):
        self.logger.debug("——————————客户端请求get数据——————————————————")
        get_args = self.parse_cmd()
        if get_args:
            self.logger.debug("解析命令成功[{}]".format(get_args))
            in_server_file, to_client_location = get_args
        else:
            self.logger.debug("解析失败,准备向客户端通告错误消息")
            self.sendall("504", {"data": self.ERROR_CODE.get(504)})
            self.logger.debug("客户端使用get请求失败")
            return False
        seek = 0  # 默认seek值为0
        last_seek = self.str_to_json(self.bytes_to_str(self.request_message).split("|")[1]).get("seek")
        if last_seek:
            self.logger.debug("获取到上一次seek值[{}]".format(last_seek))
            seek = last_seek
        self.logger.debug("获取到seek值[{}]".format(seek))
        in_server_file = self.is_owner(in_server_file)
        if not in_server_file or not os.path.exists(in_server_file):
            self.logger.debug("权限不足,准备向客户端通过此消息")
            self.sendall("553", {"data": self.ERROR_CODE.get(553)})
            self.logger.debug("get请求失败,返回False")
            return False
        total_size = os.path.getsize(in_server_file)
        self.logger.debug("get文件的总大小为[{}]".format(total_size))
        while True:
            self.logger.debug("开始循环读取文件中 ...")
            data_obj = self.readfile(in_server_file, seek)
            for data in data_obj:
                if type(data) == bool and not data:
                    self.logger.warning("文件[{}]不存在".format(in_server_file))
                    break
                else:
                    self.logger.debug("获取到数据大小[{}]".format(data[1]))
                    self.sendall("125", {"data": data[0],
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

    @staticmethod
    def handle_exist_file(filepath, action=None):
        if action == "1":
            os.remove(filepath)
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
                    self.sendall("350", {"data": "当前目录已存在该文件\n\t1.覆盖\n\t2.重命名原文件\n\t3.继续下载\n 请选择: "})
                    self.logger.debug("交互消息发送完毕,准备接收交互消息")
                    action = self.bytes_to_str(self.recvall())
                    self.logger.debug("交互消息接收完毕,准备判断结果")
                    if action in ["1", "2", "3"]:
                        self.logger.debug("交互结果符合要求,准备通告客户端处理结果")
                        self.sendall("125", {"data": self.ERROR_CODE.get(125)})
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
            self.logger.info("权限不足,准备向客户端通过[{}]".format(in_server_file))
            self.sendall("553", {"data": self.ERROR_CODE.get(553)})
            self.logger.debug("权限不足,通告完毕,返回False")
            return False
        seek = 0
        last_seek = self.check_file_path(in_server_file)
        if last_seek:
            self.logger.debug("检查到上一次seek大小[{}]".format(last_seek))
            seek = last_seek
        self.logger.debug("准备告知客户端已准备接收文件,并告知客户端接收seek位置")
        self.sendall("125", {"data": self.ERROR_CODE.get(125), "seek": seek})
        self.logger.debug(" 通告消息发送完毕")
        received_size = 0
        total_size = None
        percent = 0  # 初始百分比
        while received_size != total_size:
            self.logger.debug("==========接收文件中 ...============")
            data = self.recvall()
            self.request_message = str(self.request_message, ENCODING).split("|")
            self.logger.debug("收到[{}]".format(self.request_message))
            respond_json_data = self.str_to_json(self.request_message[1])
            if str(total_size) == str(None):
                total_size = respond_json_data.get("file_size")
                if not total_size or total_size <= seek:
                    self.logger.info("上传数据小于本地已存在的文件大小")
                    return False
            if respond_json_data.get("md5") and self.encode_data(data) != respond_json_data.get("md5"):
                self.logger.debug("数据接收不完整 !!!")
                break
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
            self.sendall("553", {"data": self.ERROR_CODE.get(553)})
            yield False
            return False
        total_size = os.path.getsize(filename)
        total_size -= seek  # 减去已发送的数据大小
        if total_size % RECV_BUFFER == 0:
            times = int(total_size / RECV_BUFFER)  # 刚好传完的次数
        else:
            times = int(total_size / RECV_BUFFER) + 1  # 否则,次数再加一次
        if times == 0:
            self.sendall("226", {"data": self.ERROR_CODE.get(226)})
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

    @staticmethod
    def writefile(filename, data, total_size, seek=0, mode="a+b"):
        if not total_size:
            return True
        with open(filename, mode) as writedata:
            writedata.seek(seek)
            writedata.write(data)
            writedata.flush()

    def help(self):
        doc = """
        ls 查看当前目录
        cd dir 进入远程主机目录
        dir 查看当前目录
        chmod mode file-name  设置远程主机的文件权限
        bye 注销当前用户
        rm remote-file  删除远程主机的文件,不能删除目录
        rmdir remote-dir  删除远程主机目录
        get remote-files [local-file]    将远程文件下载到本地
        put local-file [remote-file]    将本地文件上传到服务器
        pwd 查看当前目录
        quit 退出FTP会话,同bye
        mkdir folder_name [mode] 创建目录
        """
        self.sendall("200", {"data": doc})

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
                self.sendall("212", {"data": "访问目录不存在,或您无权限访问"})
        else:
            self.sendall("212", {"data": "权限不足,访问拒绝"})

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
            self.sendall("200", {"data": result})

    def dir(self):
        if sys.platform.startswith("win32"):
            result = self.exec(self.request_command)
            self.sendall("200", {"data": result})
        else:
            self.request_command = str(self.request_command).replace("dir", "ls")
            self.ls()

    def mkdir(self):
        if len(str(self.request_command).split()) > 2:
            new_folder = str(self.request_command).split()[1]
            mode = str(self.request_command).split()[2]
            if not mode.isdigit():
                self.sendall("501", {"data": self.ERROR_CODE.get(501)})
        elif len(str(self.request_command).split()) > 1:
            new_folder = str(self.request_command).split()[1]
            mode = "0750"
        else:
            self.sendall("501", {"data": self.ERROR_CODE.get(501)})
            return False
        if not os.path.exists(str(self.request_command).split()[1]):
            os.makedirs(new_folder, mode=int(mode))
            self.sendall("257", {"data": self.ERROR_CODE.get(257)})
        else:
            self.sendall("200", {"data": "目标目录已存在"})

    def rmdir(self):
        if len(str(self.request_command).split()) == 2:
            folder = str(self.request_command).split()[1]
            if os.path.isdir(folder):
                os.removedirs(folder)
                self.sendall("200", {"data": self.ERROR_CODE.get(200)})
            else:
                self.sendall("502", {"data": self.ERROR_CODE.get(502)})
        else:
            self.sendall("501", {"data": self.ERROR_CODE.get(501)})

    def rm(self):
        if len(str(self.request_command).split()) == 2:
            filename = str(self.request_command).split()[1]
            if os.path.isfile(filename):
                os.remove(filename)
                self.sendall("200", {"data": self.ERROR_CODE.get(200)})
            else:
                self.sendall("502", {"data": self.ERROR_CODE.get(502)})
        else:
            self.sendall("501", {"data": self.ERROR_CODE.get(501)})

    def chmod(self):
        if len(str(self.request_command).split()) > 2:
            folder = str(self.request_command).split()[1]
            mode = str(self.request_command).split()[2]
            if not mode.isdigit():
                self.sendall("501", {"data": self.ERROR_CODE.get(501)})
        elif len(str(self.request_command).split()) > 1:
            folder = str(self.request_command).split()[1]
            mode = "0750"
        else:
            self.sendall("501", {"data": self.ERROR_CODE.get(501)})
            return False
        if os.path.exists(folder):
            os.chmod(folder, mode=int(mode))
            self.sendall("200", {"data": self.ERROR_CODE.get(200)})
        else:
            self.sendall("450", {"data": self.ERROR_CODE.get(450)})

    def bye(self):
        """
        注销用户登陆状态
        :return:
        """
        self.login = None
        self.sendall("200", {"data": "谢谢使用"})

    def quit(self):
        self.bye()


def main():
    try:
        server_address = (LISTEN, int(PORT))
        server = socketserver.ThreadingTCPServer(server_address, FTPServer)
        server.serve_forever(2)
    except KeyboardInterrupt:
        server.server_close()
        print("服务器强制被关闭")
