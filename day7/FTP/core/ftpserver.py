#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import socketserver
import subprocess
import sys
import os
import logging
import shelve
from core.userverify import UserVerify

connect_database = shelve.open("../database/database")  # 打开可持久化数据文件
database = connect_database.get("data")  # 获取键为data的数据
verify = UserVerify(database)  # 将UserVerify类进行实例化

output_console = True  # 将日志输出到屏幕
logfile = None  # 定义日志文件
encoding = "utf8"  # 定义日志编码
loglevel = logging.DEBUG  # 日志输出级别
formatter = logging.Formatter("%(asctime)s  -  %(name)s   -  %(levelname)s  - %(message)s")  # 日志记录格式
logger = logging.getLogger(__name__)  # 创建日志对象
logger.setLevel(loglevel)  # 设置日志记录级别
if output_console:
    console_handler = logging.StreamHandler()  # 创建控制台日志输出对象
    console_handler.setLevel(loglevel)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
if logfile:  # 当设置了文件名,则日志记录到文件
    file_handler = logging.FileHandler(filename=logfile, encoding=encoding)  # 创建日志文件对象
    file_handler.setLevel(loglevel)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


class FTPServer(socketserver.BaseRequestHandler):
    buffer = 1024  # 设置接收缓存大小
    enable_anonymous = False  # 启用匿名方式认证
    anon_public = "./pub"  # 设置服务器公共服务目录
    home_dir = None  # 该字段在此处修改无效,将用于用户家目录
    login_status = None  # 该字段在此处修改无效

    @property
    def __login(self):
        """
        将用户名密码验证通过静态方法提供,防止外部修改
        :return:验证通过,返回用户名
        """
        self.sendall(bytes("ftp不提供匿名服务\n请输入用户名:", "utf8"))
        username = str(self.recvall(), "utf-8)")
        self.sendall(bytes("请输入密码:", "utf8"))
        password = str(self.recvall(), "utf-8")
        self.home_dir = None
        if verify.login(username, password):
            self.sendall(bytes("欢迎使用贵宾VIP 文件服务器", "utf8"))
            return username
        else:
            self.sendall(bytes("用户名或密码错误", "utf8"))
            return False

    @property
    def __user_home(self):
        return self.home_dir

    @__user_home.setter
    def __user_home(self, username):
        if self.enable_anonymous:
            self.home_dir = os.path.abspath(self.anon_public)
        else:
            new_path = os.path.join(self.anon_public, username)
            self.home_dir = os.path.abspath(new_path)
        if not os.path.isdir(self.home_dir):
            os.makedirs(self.home_dir, exist_ok=False)
        os.chdir(self.home_dir)

    def handle(self):
        self.parent_dir = os.path.abspath(os.path.dirname(self.anon_public))
        self.local_file = None
        self.remote_file = None

        if self.enable_anonymous:
            self.login_status = "anonymous"
            self.__user_home = self.login_status
            self.home_dir = self.__user_home
        else:
            self.login_status = False  # 设置用户登陆状态,登陆成功则该字段被赋予登陆名
        while True:
            command = self.recvall()
            if command:
                if self.login_status:
                    logger.info("处理客户端：[{}]端口: [{}]请求".format(*self.request.getpeername()))
                    command = str(command, "utf-8")
                    if len(command.split()) > 1:
                        attr = command.split()[0]
                    else:
                        attr = command
                    if hasattr(self, attr):  # 如果用户请求合理,则返回用户请求
                        attr = getattr(self, attr)
                        command = command.split("|")[0]  # 去除用户管道操作
                        command = command.split("&")[0]  # 去除用户多命令操作
                        attr(command)  # 调用类方法执行
                    else:
                        self.sendall(bytes("command not found", "utf8"))
                else:
                    self.login_status = self.__login
                    if self.login_status:
                        self.__user_home = self.login_status
                        self.home_dir = self.__user_home
            else:
                logger.info("关闭客户端:[{}] 端口:[{}]".format(*self.client_address))
                os.chdir(self.parent_dir)
                self.request.close()
                break

    def recv_data(self):
        return self.request.recv(self.buffer)

    def send_data(self, data):
        return self.request.send(data)

    def recvall(self):
        while True:
            client_respone_message = self.recv_data()
            logger.debug("收到客户端[{}]请求消息[{}]".format(self.request, client_respone_message))
            request_message = str(client_respone_message.decode()).split("|")
            if len(request_message) > 3:
                self.remote_file = request_message[3]
                self.local_file = request_message[4]
            if request_message[0] == "DATA_SIZE":
                cmd_res_size = int(request_message[1])
                logger.debug("向客户端[{}]发送确认消息".format(self.request))
                self.request.send(b"CLIENT_READY_TO_RECV")
                data = b''
                received_size = 0
                while received_size < cmd_res_size:
                    data += self.recv_data()
                    received_size = len(data)
                    logger.debug("收到客户[{}]端消息[{}]".format(self.request, data))
                return data
            break

    def parse_command(self, data):
        if len(str(data).split()) > 1:
            remote_file = str(data).split(maxsplit=1)[1].strip("'")
            local_file = remote_file
            if len(str(remote_file).split()) > 1:
                remote_file, local_file = str(remote_file).split()
            if str(data).split()[0] == "get":
                remote_file, local_file = local_file, remote_file
                return local_file, remote_file
            elif str(data).split()[0] == "put":
                return local_file, remote_file

    def sendall(self, data, command=None):
        local_remote = self.parse_command(command)
        while True:
            if local_remote:
                message = "DATA_SIZE|{}|LOCAL_REMOTE|{}|{}".format(len(data), *local_remote)
            else:
                message = "DATA_SIZE|{}".format(len(data))
            respone_message = bytes(message, "utf8")
            self.request.send(respone_message)
            logger.debug("服务端socket[%s]发送请求消息[%s]" % (self.request, respone_message))
            client_ack = self.recv_data()
            if client_ack.decode() == 'CLIENT_READY_TO_RECV':
                logger.debug("服务端socket[%s]得到确认消息[%s]" % (self.request, client_ack))
                total_size = len(data)
                logger.debug("服务端socket[%s]开始发送消息,大小[%s]" % (self.request, total_size))
                while total_size > 0:
                    total_size -= self.request.send(data)
                logger.debug("服务端发送消息完成socket[%s]" % self.request)
                break

    def readfile(self, filename, seek):
        total_size = os.path.getsize(filename)
        if total_size % 100 == 0:
            buffer = int(total_size / 100)
        else:
            buffer = int(total_size / 99)
        percent = 0
        while total_size > 0:
            percent += 1
            hashes = "#" * int(percent / 100.0 * 50)
            spaces = " " * (50 - len(hashes))
            sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent, hashes + spaces))
            sys.stdout.flush()
            with open(filename, "rb") as readdata:
                readdata.seek(seek)
                has_read = readdata.read(buffer)
                if has_read:
                    seek = readdata.tell()
                    total_size -= buffer
                    yield has_read, seek
                else:
                    readdata.close()

    def writefile(self, filename, data, seek=0, mode="a+b"):
        percent = 0
        while percent <= 100:
            hashes = "#" * int(percent / 100.0 * 50)
            spaces = " " * (50 - len(hashes))
            sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent, hashes + spaces))
            sys.stdout.flush()
            percent += 1
        with open(filename, mode) as writedata:
            writedata.seek(seek)
            writedata.write(data)
            writedata.flush()

    def get(self, cmd):
        self.local_file = str(cmd).split()[1]
        if os.path.isfile(self.local_file):
            get_file = os.path.abspath(self.local_file)
            for data in self.readfile(get_file, 0):
                self.sendall(data[0])
        else:
            self.sendall(bytes("文件不存在", "utf8"), cmd)

    def put(self, cmd):
        self.sendall(bytes(cmd, "utf8"), cmd)
        seek = 0
        while True:
            data = self.recvall()
            if not data:
                break
            self.writefile(self.local_file, data, seek)
            seek += len(data)

    def exec(self, command):
        stdout = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = stdout.stderr.read()
        if not result:
            result = stdout.stdout.read()
        return result

    def ls(self, cmd):
        if sys.platform.startswith("win32"):
            cmd = str(cmd).replace("ls", "dir")
            self.dir(cmd)
        else:
            result = self.exec(cmd)
            self.sendall(result, cmd)

    def dir(self, cmd):
        if sys.platform.startswith("win32"):
            result = self.exec(cmd)
            self.sendall(result, cmd)
        else:
            cmd = str(cmd).replace("dir", "ls")
            self.ls(cmd)

    def bye(self, cmd):
        """
        注销用户登陆状态
        :return:
        """
        self.login_status = None
        os.chdir(self.parent_dir)
        self.sendall(bytes("谢谢使用", "utf8"))

    def quit(self, cmd):
        self.bye(cmd)

    def cd(self, cmd):
        if len(str(cmd).split()) > 1:
            new_path = str(cmd).split()[1]
        else:
            new_path = self.home_dir
        old_path = os.path.join(self.parent_dir, os.path.basename(self.anon_public))
        new_path = os.path.abspath(new_path)
        if new_path > old_path:
            cur_path = os.path.abspath(new_path)
            if os.path.isdir(cur_path):
                os.chdir(cur_path)
            else:
                self.sendall(bytes("访问目录不存在,或您无权限访问", "utf8"))
        else:
            self.sendall(bytes("权限不足,访问拒绝", "utf-8"))

    def pwd(self, cmd):
        abspath = os.path.abspath(os.path.curdir)
        old_path = os.path.join(self.parent_dir, os.path.basename(self.anon_public))
        cur_path = abspath.split(old_path)[1]
        return self.sendall(bytes("当前路径:\n%s" % cur_path, "utf8"))

    def mkdir(self, cmd):
        if len(str(cmd).split()) > 2:
            new_folder = str(cmd).split()[1]
            mode = str(cmd).split()[2]
            if not mode.isdigit():
                self.sendall(bytes("mode格式只能是数字,例如0777", "utf8"))
        elif len(str(cmd).split()) > 1:
            new_folder = str(cmd).split()[1]
            mode = "0750"
        else:
            self.sendall(bytes("语法不正确,格式 mkdir folder_name [mode],默认mode为0750", "utf8"))
            return False
        if not os.path.exists(str(cmd).split()[1]):
            result = self.exec(cmd)
            self.sendall(result, cmd)
        else:
            self.sendall(bytes("目标目录已存在", "utf8"))

    def rmdir(self, cmd):
        if len(str(cmd).split()) == 2:
            folder = str(cmd).split()[1]
            result = self.exec(cmd)
            self.sendall(result, cmd)
        else:
            self.sendall(bytes("语法不正确,rmdir folder_name", "utf8"))

    def help(self, cmd):
        doc = """
        ls 查看当前目录       cd remote-dir 进入远程主机目录
        dir 查看当前目录      chmod mode file-name  设置远程主机的文件权限
        bye 注销当前用户      delete remote-file  删除远程主机的文件
        get remote-file [local-file]    将远程主机文件保存到本地硬盘local-file位置
        mdelete [remote-files]  删除远程主机多个文件
        get remote-files [local-file]    将远程文件下载到本地
        put local-file [remote-file]    将本地文件上传到服务器
        pwd 查看当前目录
        quit 退出FTP会话,同bye
        size filename 显示远程主机文件大小
        mkdir folder_name [mode] 创建目录
        """
        self.sendall(bytes(doc, "utf8"))


def main():
    server_address = ("0.0.0.0", 9999)
    # FTPServer.enable_anonymous = True  # 启用匿名登陆
    ftpserver = socketserver.ThreadingTCPServer(server_address, FTPServer)
    ftpserver.allow_reuse_address = True
    ftpserver.serve_forever(1)

if __name__ == '__main__':
    main()
