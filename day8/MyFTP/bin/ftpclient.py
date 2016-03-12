#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socket
import json
import os
import sys
import logging
import selectors


class MyFTPClient(object):
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
    recv_buffer = 8000  # 设置接收缓冲大小
    output_console = True  # 输出到屏幕
    logLevel = logging.DEBUG  # 日志输出级别
    logfile = None  # 日志文件名称
    encoding = "utf8"  # 编码格式
    timeout = 500  # 超时时间,单位毫秒
    formatter = logging.Formatter("%(asctime)s  -  %(name)s   -  %(levelname)s  - %(message)s")  # 日志记录格式

    def __init__(self, server_address):
        """初始化socket,及设置日志输出
        :param server_address: 定义服务器IP端口信息
        :return:
        """
        self.server_address = server_address  # 定义服务器IP和端口
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP连接socket
        self.selector = selectors.DefaultSelector()
        self.request_message = None  # 将每次的请求存入该属性
        self.request_command = None  # 将每次请求的指令存入该属性
        # 定义命令列表
        self.command_list = ["put", "get"]
        self.logger = logging.getLogger(__name__)  # 创建日志对象
        if self.output_console:
            self.console_handler = logging.StreamHandler()  # 创建控制台日志输出对象
        if self.logfile:  # 当设置了文件名,则日志记录到文件
            self.file_handler = logging.FileHandler(filename=self.logfile, encoding=self.encoding)  # 创建日志文件对象
        self.set_log()  # 设置日志
        self.login = False

    def connect_server(self):
        """
        连接服务器
        :return:
        """
        self.socket.connect(self.server_address)
        self.logger.debug("客户端[{}][{}]已连接服务器[{}]".format(*self.socket.getsockname(), self.socket.getpeername()))
        self.logger.debug("客户端注册文件描述符[%s]" % self.socket.fileno())
        self.logger.debug("主动请求连接服务器 ...")
        self.sendall("101", {"data": "101"})

    def client_start(self):
        """
        启动客户端
        :return:
        """
        self.selector.register(self.socket, selectors.EVENT_READ, self.connect_server())

        while True:
            self.logger.debug("————————————————正在轮询事件——————————————————")
            events = self.selector.select(0.1)
            if not events:
                try:
                    self.logger.debug("准备向服务器[{}][{}]发送请求".format(*self.socket.getpeername()))
                except OSError:
                    break
                self.send_request()
            else:
                self.logger.info("有{}个新事件，开始处理......".format(len(events)))
                self.handle_request(events)

    def handle_request(self, events):
        """
        :param events: 处理事件信息
        :return:
        """
        self.logger.debug("————————————————————————————数据处理中 ...——————————————————————————")
        for key, mask in events:
            self.recvall()
        self.logger.debug("————————————————————————————数据处理完毕 !——————————————————————————")

    def prompt(self):
        prompt = "ftp {}{}{}"

        if self.login:
            prompt = prompt.format("[ ", self.login, " ]$ ")
        else:
            prompt = prompt.format("", "> ", "")
        data = bytes(str(input(prompt)).strip(), self.encoding)
        return data

    def send_request(self):
        """
        对服务器发送指令操作
        :return:
        """
        self.logger.debug("开始输入请求 ...")
        data = self.prompt()
        if len(data) < 1:  # 如果没有输入任何数据,则返回
            return
        self.logger.debug("——————————————————准备执行请求——————————————————————")
        self.exec_instruction(data)
        self.logger.debug("_________________请求执行完毕————————————————————————")

    def exec_instruction(self, instruction):
        """
        :param instruction: 根据请求内容开始分配对应的请求
        :return:
        """
        self.logger.debug("进入请求解析中心")
        instruction = str(instruction, self.encoding)
        self.request_command = instruction
        self.logger.debug("请求内容[{}]".format(self.request_command))
        if instruction.count("|") > 0:
            self.logger.debug("请求内容含有非法字符")
            print(self.ERROR_CODE.get(201))
        else:
            instruction = instruction.split()  # 将指令解析,分隔 command|{"json_data"}
            if len(instruction) > 1:
                attr = instruction[0]
                if len(attr.split()) > 1:
                    attr, command = attr.split()[0], attr
            else:
                attr = instruction[0]
            if hasattr(self, attr) and attr in self.command_list:
                    attr = getattr(self, attr)
                    self.logger.debug("——————————————————正在执行客户端请求中 ...——————————————————")
                    attr()
                    self.logger.debug("————————————————————请求执行完毕————————————————————")
            else:
                self.logger.debug("——————————————————准备向服务器发送指令——————————————————")
                self.sendall("100", {"data": self.request_command})
                self.logger.debug("————————————————————————指令发送完毕————————————————————")

    def recv_data(self):
        """
        接收请求数据
        :return: 返回已收到的数据
        """
        data = self.socket.recv(self.recv_buffer)
        if len(data) > 0:
            self.logger.debug("接收到一条消息")
            return data
        else:
            self.logger.debug("未接收到消息")
            return False

    def send_data(self, data):
        """
        发送数据
        :param data: bytes类型数据
        :return: 返回已发送的大小
        """
        self.logger.debug("发送了一条消息")
        return self.socket.send(data)

    def recvall(self):
        """
        接收所有数据
        :return:
        """
        self.logger.debug("————————————————进入接收所有数据模式——————————————")
        self.logger.debug("第一次接收")
        respond_message = self.recv_data()
        if not type(respond_message) is bytes:
            self.logger.debug("分离信息时遇到错误,返回空 ...")
            return
        self.logger.debug("收到消息[{}]".format(respond_message))
        self.request_message = respond_message
        respond_message = str(respond_message, self.encoding).split("|")
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
            self.sendall("451", {"data": self.ERROR_CODE.get(451)})
            self.logger.debug("md5值警告发送完毕")
        else:
            if respond_message[0] == "208":
                return data
            elif respond_message[0] == "504":
                self.logger.debug("收到指令[{}],准备断开连接".format(self.ERROR_CODE.get(504)))
                self.shutdown_request(self.socket, self.ERROR_CODE.get(504))
            elif respond_message[0] == "104":
                self.login = respond_json_data.get("username")
                self.logger.debug("用户[{}]认证成功 ...".format(self.login))
            elif respond_message[0] == "452":
                print(self.ERROR_CODE.get(452))
                self.logger.debug("权限不足")
                return 452
            elif respond_message[0] == "451":
                print(self.ERROR_CODE.get(451))
                self.logger.debug("md5值异常")
                return 451
            else:
                print(str(data, self.encoding))

    def sendall(self, code, json_data):
        """
        :param code: ftp代码
        :param json_data: 字典类型数据,将被转换为json格式
        :return:
        """
        self.logger.debug("——————————————————————————进入发送所有数据模式————————————————————————")
        self.logger.debug("发送数据内容[{}]".format(json_data))
        data = json_data["data"]  # data只能是二进制数据
        self.logger.debug("将发送数据提取[{}]出来".format(data))
        if not type(data) is bytes:  # 如果数据不是bytes类型,将转换成bytes
            data = bytes(data, self.encoding)
        if not json_data.get("total_size"):
            json_data["total_size"] = len(data)  # 计算数据长度
        self.logger.debug("计算本次发送指令数据大小[{}]".format(json_data["total_size"]))
        json_data["md5"] = self.encode_data(data)
        self.logger.debug("计算数据的md5值[{}]".format(json_data["md5"]))
        self.logger.debug("将请求指令与额外信息分离")
        json_data.pop("data")
        message = '{}|{}'.format(code, self.json_to_str(json_data))
        if not type(message) is bytes:  # 如果数据不是bytes类型,将转换成bytes
            message = bytes(message, self.encoding)
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
            self.logger.debug("————————————————————————所有数据发送完毕 !——————————————————————————")
            return True
        else:
            self.logger.debug("客户端回应错误 ...")
            return False

    def shutdown_request(self, request, message):
        """
        :param request: 已建立连接的socket
        :param message: 消息提醒
        :return:
        """
        self.logger.info(message.format(*request.getpeername()))
        self.selector.unregister(request)
        request.close()
        self.logger.debug("与服务器连接断开")

    def set_log(self):
        """
        设置日志
        :return:
        """
        self.logger.setLevel(self.logLevel)  # 设置日志记录级别
        if self.output_console:  # 当设置了输出屏幕日志,则启用该日志打印屏幕功能,默认开启
            self.console_handler.setLevel(self.logLevel)
            self.console_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.console_handler)
        if self.logfile:  # 当设置了文件名,则启用记录日志文件功能,默认关闭
            self.file_handler.setLevel(self.logLevel)
            self.file_handler.setFormatter(self.formatter)
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

    @staticmethod
    def get_abspath(file_location):
        """
        :param file_location: 文件目标位置
        :return: 属于返回文件对绝对路径
        """
        return os.path.abspath(file_location)

    def bytes_to_str(self, bytesobj):
        return str(bytesobj, self.encoding)

    @staticmethod
    def handle_exist_file(filepath, action=None):
        if action == "1":
            os.remove(filepath)
        elif action == "2":
            os.rename(filepath, "{}_2".format(filepath))
        elif action == "3":
            return os.path.getsize(filepath)

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
            print(self.ERROR_CODE.get(201))
            return False
        return in_server_file, to_client_location

    def check_file_path(self, filename):
        """
        检查文件状态,是否存在,或者是否为目录
        :param filename:
        :return:
        """
        action = str(None)  # 初始化一个属性,用来存储用户针对文件操作
        if os.path.exists(filename):
            if os.path.isdir(filename):
                print("当前存在相同文件名的目录,请更换其他名字")
            elif os.path.isfile(filename):
                while True:
                    action = input("当前目录已存在该文件\n\t1.覆盖\n\t2.重命名原文件\n\t3.继续下载\n 请选择: ")
                    if action in ["1", "2", "3"]:
                        break
        else:
            basedir = os.path.dirname(filename)
            if not os.path.exists(basedir):
                os.makedirs(basedir)  # 如果多级目录,不存在则创建
        return self.handle_exist_file(filename, action)

    def get(self):
        """
        通过get从服务器上下载单个文件
        :return:
        """
        self.logger.debug("——————————客户端请求get数据——————————————————")
        get_args = self.parse_cmd()
        if get_args:
            self.logger.debug("指令解析成功[{}]".format(get_args))
            in_server_file, to_client_location = get_args
        else:
            self.logger.debug("指令解析失败,返回False")
            return False
        to_client_location = self.get_abspath(to_client_location)
        if os.path.isdir(to_client_location):
            to_client_location = os.path.join(to_client_location, in_server_file)
        seek = 0
        last_seek = self.check_file_path(to_client_location)
        if last_seek:
            self.logger.debug("检查到上一次seek大小[{}]".format(last_seek))
            seek = last_seek
        self.logger.debug("准备告知客户端已准备接收文件,并告知客户端接收seek位置")
        self.sendall("208", {"data": self.request_command, "seek": seek})
        self.logger.debug(" 通告消息发送完毕")
        received_size = 0
        total_size = None
        percent = 0  # 初始百分比
        while received_size != total_size:
            self.logger.debug("==========接收文件中 ...============")
            data = self.recvall()
            file_type = self.str_to_json(self.bytes_to_str(self.request_message).split("|")[1]).get("type")
            if str(file_type) == "dir":
                os.makedirs(to_client_location)
                self.logger.info("目录[{}]创建成功".format(to_client_location))
                return True
            self.request_message = str(self.request_message, self.encoding).split("|")
            self.logger.debug("收到[{}]".format(self.request_message))
            respond_json_data = self.str_to_json(self.request_message[1])
            if str(total_size) == str(None):
                total_size = respond_json_data.get("file_size")
                if not total_size or total_size <= seek:
                    self.logger.info("下载数据小于本地已存在的文件大小")
                    return False
                total_size -= seek
            if respond_json_data.get("md5") and self.encode_data(data) != respond_json_data.get("md5"):
                self.logger.debug("数据接收不完整 !!!")
                break
            seek = respond_json_data.get("seek")
            self.writefile(to_client_location, data, total_size, seek, "a+b")
            if total_size % self.recv_buffer == 0:
                times = int(total_size / self.recv_buffer)  # 刚好传完的次数
            else:
                times = int(total_size / self.recv_buffer) + 1  # 否则,次数再加一次
            count = 100 / times  # 计算每次增加的百分比
            percent += float(count)
            hashes = "#" * int(percent / 100.0 * 65)  # 指定进度条宽度
            spaces = " " * (65 - len(hashes))
            percent_format = "{:.2f}".format(percent)
            space = " " * (6 - len(percent_format))
            sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent_format + space, hashes + spaces))
            sys.stdout.flush()
            received_size += len(data)
        print()
        self.logger.debug("——————————————————————————get请求完毕————————————————————————")

    def check_type(self, filename):
        filename = self.get_abspath(filename)
        if os.path.isdir(filename):
            return "dir"
        if os.path.isfile(filename):
            return "file"
        else:
            return False

    def put(self):
        self.logger.debug("——————————客户端请求get数据——————————————————")
        get_args = self.parse_cmd()
        if get_args:
            self.logger.debug("解析命令成功[{}]".format(get_args))
            in_client_location, to_server_file = get_args
        else:
            print(self.ERROR_CODE.get(201))
            self.logger.debug("客户端使用put请求失败")
            return False
        in_client_location = os.path.abspath(in_client_location)
        if not os.path.exists(in_client_location):
            print(self.ERROR_CODE.get(452))
            self.logger.debug("put请求失败,返回False")
            return False
        seek = 0
        file_type = self.check_type(in_client_location)
        self.logger.debug("文件属性[{}]".format(file_type))
        self.logger.debug("客户端发送通告信息,告知服务器上传的基本信息")

        total_size = os.path.getsize(in_client_location)
        self.sendall("208", {"data": self.request_command, "seek": seek, "type": file_type, "file_size": total_size})  # 先发送请求,告知服务端
        if str(file_type) == "dir":
            return True
        self.logger.debug("客户端接收服务端对上传文件对响应")
        get_respond = self.recvall()
        get_code = self.bytes_to_str(self.request_message).split("|")[0]
        while get_code == "209":  # 如果对端存在重名文件,将接收到该代码
            self.logger.debug("客户端文件与服务器端文件存在冲突,交互中 ...")
            data = self.prompt()
            if len(data) < 1:
                data = "0"
            self.sendall("209", {"data": data})
            self.recvall()
            get_code = self.bytes_to_str(self.request_message).split("|")[0]
            if get_code == "208":
                self.logger.info("客户端选择了[{}]方式处理文件".format(data))
                self.recvall()
                break
        if type(get_respond) is not bytes and str(get_code) in ["453", "455", "452"]:
            self.logger.debug("服务端遇到其他状态,故放弃本次上传操作")
            return False
        avail_size = self.str_to_json(self.bytes_to_str(self.request_message).split("|")[1]).get("avail")
        self.logger.debug("当前剩余可用空间[{}]".format(avail_size))
        last_seek = self.str_to_json(self.bytes_to_str(self.request_message).split("|")[1]).get("seek")
        self.logger.debug("上一次服务端已接收数据大小[{}]".format(last_seek))
        if last_seek:
            self.logger.debug("获取到上一次seek值[{}]".format(last_seek))
            seek = last_seek
        elif str(last_seek) == str(None):
            self.logger.debug("权限不足,或无法访问目标文件")
            return False
        self.logger.debug("获取到seek值[{}]".format(seek))
        if str(avail_size) != str(None) and avail_size < total_size:
            print(self.ERROR_CODE.get(455))
            return False
        if seek >= total_size:
            print(self.ERROR_CODE.get(453))
            return True
        self.logger.debug("put文件的总大小为[{}]".format(total_size))
        while True:
            self.logger.debug("开始循环读取文件中 ...")
            data_obj = self.readfile(in_client_location, seek)
            for data in data_obj:
                if type(data) == bool and not data:
                    self.logger.warning("文件[{}]不存在".format(in_client_location))
                    break
                else:
                    self.logger.debug("获取到数据大小[{}]".format(data[1]))
                    send_check = self.sendall("208", {"data": data[0],
                                                      "seek": data[1],
                                                      "file_size": total_size,
                                                      "save_to_file": to_server_file})
                    if not send_check:
                        return False
            print()
            break
        self.logger.info("客户端[{}][{}]上传文件[{}]完成".format(*self.server_address, to_server_file))

    @staticmethod
    def writefile(filename, data, total_size, seek=0, mode="a+b"):
        if not total_size:
            return True
        with open(filename, mode) as writedata:
            writedata.seek(seek)
            writedata.write(data)
            writedata.flush()

    def readfile(self, filename, seek):
        if not os.path.exists(filename):
            self.sendall("452", {"data": self.ERROR_CODE.get(452)})
            yield False
            return False
        total_size = os.path.getsize(filename)
        total_size -= seek  # 减去已发送的数据大小
        if total_size % self.recv_buffer == 0:
            times = int(total_size / self.recv_buffer)  # 刚好传完的次数
        else:
            times = int(total_size / self.recv_buffer) + 1  # 否则,次数再加一次
        if times == 0:
            self.sendall("453", {"data": self.ERROR_CODE.get(453)})
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
                has_read = readdata.read(self.recv_buffer)
                if has_read:
                    seek = readdata.tell()
                    total_size -= self.recv_buffer
                    yield has_read, seek
                else:
                    readdata.close()


if __name__ == "__main__":
    try:
        server_listen_address = ("127.0.0.1", 8500)
        MyFTPClient.output_console = False
        connect_ftp = MyFTPClient(server_listen_address)
        connect_ftp.client_start()
    except ConnectionRefusedError:
        pass
    # except BrokenPipeError:
    #     pass
    except KeyboardInterrupt:
        connect_ftp.logger.critical("客户端退出 ...")
