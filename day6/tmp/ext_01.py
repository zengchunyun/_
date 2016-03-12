#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import shutil
import os

#
# fsrc = open("test", 'r')  # 读取test
# fdst = open("test2", "w")
# shutil.copyfileobj(fsrc, fdst, length=1)  # 拷贝文件对象到另一个文件
# shutil.copyfile("./test", "tmp/aa")  # 拷贝文件到指定目录
# print(os.stat("test"))
# shutil.copymode("test", "test2")  # 拷贝文件权限
# print(os.stat("test2"))
#
# shutil.copystat("test", "test2")  # 拷贝文件状态信息,包括atime,mtime
# print(os.stat("test2"))
# shutil.copy("test", "test3")  # 仅拷贝文件和权限,状态信息不拷贝
# print(os.stat("test3"))
# shutil.copy2("test", "test4")  # 拷贝文件和修改时间mtime
# print(os.stat("test4"))
# shutil.ignore_patterns("*est*")  # 忽略文件模式
# shutil.copytree(".", "tmp", symlinks=False, ignore=shutil.ignore_patterns("*est*", "tmp*"))  # 忽略包含est和tmp开头的文件


# shutil.rmtree(path="tmp", ignore_errors=False, onerror=None)  # 递归删除tmp目录,不忽略错误
#
# shutil.move("test2", "test5")  # 把test2 移动到test5.相当于重命名
# shutil.make_archive("new_test", format="gztar", root_dir="./tmp/")
# import zipfile
# # 压缩
# new_zip = zipfile.ZipFile('new_test.zip', 'w')  # 创建一个归档文件,创建时,模式为'w'
# new_zip.write('test3')  # 把test3文件压缩进去
# new_zip.write('test4')  # 把test4压缩进去
# new_zip.setpassword(b'123')  # 设置压缩密码,测试无效果
# new_zip.close()  # 写入关闭
# # 解压
# new_zip_decompress = zipfile.ZipFile("new_test.zip", 'r')  # 打开压缩包,模式 'r'
# print(new_zip_decompress.filelist)  # 查看压缩包内文件
# new_zip_decompress.extractall()  # 解压压缩包
# new_zip_decompress.close()
# print(new_zip_decompress.setpassword(b"123"))



# zz = zipfile.ZipInfo(filename="new_zip.zip")
# print(zz.create_version)
# print(zz.filename)
# print(zz.flag_bits)
#
# import tarfile
# new_tar = tarfile.open('test.tar', 'w')  # 在当前目录新建一个tar压缩文件
# new_tar.add('test3', arcname='test3')  # 指定压缩文件路径,指定压缩后的名字
# new_tar.add("test4", arcname="test4")
# new_tar.close()  # 压缩完毕
#
# extra_tar = tarfile.open("test.tar", 'r')
# extra_tar.extractall()  # 解压所有
# extra_tar.close()

import shelve





class MyRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(time.strftime('%Y-%m-%d %H:%M:%S') + ' %s' % str(self.request))
        print(time.strftime('%Y-%m-%d %H:%M:%S') + ' %s' % str(self.client_address))
        print(time.strftime('%Y-%m-%d %H:%M:%S') + ' %s' % str(self.server))
        conn = self.request
        try:
            if self.auth():
                conn.send('Login success!')
                flag = True
            else:
                conn.send('Login failed!')
                flag = False
                conn.close()

            while flag:
                data = conn.recv(1024)
                if data == 'ACK':
                    print(time.strftime('%Y-%m-%d %H:%M:%S') + ' 客户端断开连接 ... ')
                    break
                print(time.strftime('%Y-%m-%d %H:%M:%S') + ' 传过来的命令 %s' % data)
                result = MyFTP().ls(str(data))
                retries = 1
                while True:
                    readFile = result[0].read()
                    if not readFile and retries == 1:
                        conn.sendall(result[1].read())
                        print(time.strftime('%Y-%m-%d %H:%M:%S') + ' 读取完毕')
                        break
                    time.sleep(0.01)
                    conn.sendall(readFile)
                    retries += 1
                    if not readFile:
                        print(time.strftime('%Y-%m-%d %H:%M:%S') + ' 读取完毕')
                        break
                time.sleep(0.4)
                conn.send('FIN')
            conn.close()

        except KeyError:
            print(88)

    def auth(self):
        connect_database = shelve.open("../database/database")
        database = connect_database.get("data")
        verify = UserVerify(database)
        conn = self.request
        str()
        print(bytes(u"请输入用户名"))
        conn.send(bytes("请输入用户名:"))
        username = conn.recv(1024)
        conn.send(bytes("请输入密码:"))
        password = conn.recv(1024)
        login = None
        if username and password:
            try:
                login = verify.login(user=username, password=password)
            except SystemExit as e:
                print(e)
                conn.close()
        if not login:
            return False
        else:
            return True