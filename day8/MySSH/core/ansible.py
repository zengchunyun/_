#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import argparse
import paramiko
import os
import subprocess
import uuid
from multiprocessing import Process, Pool
from settings.conf_template import MakeConf


parser = argparse.ArgumentParser(prog='ansible', usage='%(prog)s -h [options] command',
                                 description='通过ansible可以对服务器进行批量管理')
parser.add_argument("--server", help="管理单个服务器[ip]", metavar="ip", nargs="?")
parser.add_argument("--servers", help="管理一组或多组服务器(通过配置文件定义好分组)", metavar="group1 group2 ...", nargs="+")
parser.add_argument("-e", help="对服务器所执行对操作,如果命令包含参数,请用双引号引起", metavar=" command|[get|put]", nargs="?")
parser.add_argument("-f", help="上传或下载对文件名", metavar="local remote | remote local", nargs="+")
parser.add_argument("-u", help="user name for remote server", metavar="username")
parser.add_argument("-p", help=" required password for remote user", metavar="password")
args = parser.parse_args()

server = args.server  # 获取单台服务器名
servers = args.servers  # 获取一组服务器名
cmd = args.e  # 需要执行的操作
if not cmd:
    print("-e 至少需要指定一个指令操作")
    exit(1)
if str(cmd) != ("put", "get"):  # 当解析的命令行参数不为put,get时,统一交给远程服务器执行返回结果
    option = cmd
    cmd = "ssh"

filename = args.f  # 获取文件名

if filename:
    try:
        assert len(filename) < 3
        local_path = filename[0]  # 获取用户输入的路径位置
        remote_path = filename[1]
    except AssertionError:
        print("only need two args")
        exit(1)

username = args.u  # 获取远程主机用户名
password = args.p  # 获取远程主机密码
if not username:  # 此处密码优先级低于控制台输入
    username = "zengchunyun"
if not password:
    password = " "


class Ansible(object):
    def __init__(self, host, port=22, action=""):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.__transport = None
        self._ftp = None
        self._ssh = None
        if hasattr(self, action):  # 通过反射执行对应的属性方法
            self.action = getattr(self, action)
        else:
            self.action = None

    def connect_server(self):
        """
        连接到服务器
        :return:
        """
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        self.__transport = transport

    def sftp(self):
        self._ftp = paramiko.SFTPClient.from_transport(self.__transport)

    def ssh(self, command):
        """
        通过远程连接服务器执行系统命令
        :param command: 系统命令行及参数选项,
        :return: 如果错误,则返回错误信息,否则返回正常信息
        """
        self._ssh = paramiko.SSHClient()
        self._ssh._transport = self.__transport
        stdin, stdout, stderr = self._ssh.exec_command(command)
        ret = stderr.read()
        if not ret:
            ret = stdout.read()
        return ret

    @staticmethod
    def exec_command(command):
        ret = subprocess.call(command, shell=True, stdout=subprocess.PIPE)
        return ret

    @staticmethod
    def get_id():
        return str(uuid.uuid4())

    def close(self):
        self.__transport.close()

    def put(self, *args):
        """
        通过获取控制台输入,对文件进行上传操作
        :return:
        """
        localabspath = os.path.abspath(local_path)
        remote_dir = os.path.dirname(remote_path)
        remote_file = os.path.basename(remote_path)
        local_dir = os.path.dirname(localabspath)
        if not os.path.exists(localabspath):
            return False
        get_uuid = self.get_id()
        local_file = "{}/{}.tar.gz".format(local_dir, get_uuid)
        self.exec_command(
            "cd {};tar -czf {} `basename {}`".format(local_dir, local_file, localabspath))
        self.sftp()
        ret = self.ssh("if ! test -e {};then mkdir -p {};fi;echo $?".format(remote_dir, remote_dir))
        if type(ret) == bytes:
            if str(ret, "utf-8").strip() != "0":
                return False
        self._ftp.put(localpath=local_file, remotepath=remote_path)
        self.exec_command("cd {};rm -rf {}".format(local_dir, local_file))
        ret = self.ssh(
            'cd {};if [ "{}" == "`basename {}`" ];then mv -f {} `basename {}`;tar zxf `basename {}`;'
            'else tar zxf {};mv -f `basename {}` {};fi;echo $?'.format(
                remote_dir, remote_file, localabspath, remote_file, local_file, local_file, remote_file, localabspath,
                remote_file))
        if type(ret) == bytes:
            if str(ret, "utf-8").strip() != "0":
                return False
            else:
                return True

    def get(self, *args):
        """
        通过获取控制台输入参数,对文件进行下载操作
        :return:
        """
        remote = local_path
        localabspath = os.path.abspath(remote_path)
        remote_dir = os.path.dirname(remote)
        local_dir = os.path.dirname(localabspath)
        local_file = os.path.basename(localabspath)
        get_uuid = self.get_id()
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        if os.path.isfile(local_dir):
            return False
        if os.path.isdir(localabspath):  # 当下载指定的位置为目录,程序是不允许的,所以需要使用额外的中转文件处理
            temp_file = "{}/{}.tar.gz".format(local_dir, get_uuid)
        else:
            temp_file = localabspath
        remote_file = "{}/{}.tar.gz".format(remote_dir, get_uuid)
        self.sftp()
        ret = self.ssh(
            "if test -e {};then cd `dirname {}`;tar -czf `basename {}` `basename {}`;echo $?;else echo 1;fi"
            .format(remote, remote, remote_file, remote))
        if type(ret) == bytes:
            if str(ret, "utf-8").strip() != "0":
                return False
        self._ftp.get(remotepath=remote_file, localpath=temp_file)
        local_cmd = 'cd {};if [ "`basename {}`" == "`basename {}`" ];' \
                    'then mv -f `basename {}` `basename {}`;tar xzf `basename {}`;' \
                    'else tar zxf `basename {}`;mv -f `basename {}` {};fi'
        ret = self.exec_command(local_cmd.format(
            local_dir, temp_file, remote, temp_file, remote_file, remote_file, temp_file, remote, local_file))
        if str(ret).strip() != "0":
                return False
        ret = self.ssh("cd `dirname {}`;rm -rf {};echo $?".format(remote, remote_file))
        if type(ret) == bytes:
            if str(ret, "utf-8").strip() != "0":
                return False
            else:
                return True

    def start(self, arg):
        ret = self.exec_command("ping -c2 {}".format(self.host))
        if str(ret) != "0":
            return False
        self.connect_server()
        if self.action:
            return self.action(arg)
        self.close()


def exec_management(server_address):
    """
    对单台服务器执行指定任务
    :param server_address: 合法IP地址
    :return:
    """
    ansible = Ansible(server_address, action=cmd)
    result = ansible.start(option)
    if type(result) == bytes:
        print(str(result, "utf-8"))
    else:
        print(result)


def check_ip(ip_address):
    """
    检查IP地址合法性,0.0.0.0 - 255.255.255.255 之间都为有效地址
    :param ip_address:
    :return:
    """
    import re
    pattern = "(2(5[0-5]|[0-4][0-9])|1\d{2}|[1-9]\d|[0-9])(\.(2(5[0-5]|[0-4][0-9])|1\d{2}|[1-9]\d|[0-9])){3}$"
    result = re.match(pattern, ip_address)
    return True if result else False


def parser_host(cluster):
    """
    获取节点主机地址
    :param cluster:
    :return:
    """
    if type(cluster) != list:
        cluster = str(cluster).split()
    conf = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "settings/settings.ini")
    new_conf = MakeConf(conf)
    host_list = []
    for node in cluster:
        for key in new_conf.read(node):
            print(key)
            host = new_conf.read(node, key)
            if check_ip(host):
                host_list.append(host)
    return host_list


def main(maxpool=10):
    get_host_list = []
    if server:
        if not check_ip(server):
            print("ip address is invaild")
            return False
        get_host_list.append(server)
    if servers:
        get_host_list.extend(parser_host(servers))
    pool = Pool(maxpool)
    for host in get_host_list:
        pool.apply_async(func=exec_management, args=(host,))
    pool.close()
    pool.join()


if __name__ == "__main__":
    main(10)
