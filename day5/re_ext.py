#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
# import re
# print(re.match('www', "www.baidu.com"))  # 打印匹配结果
# print(re.match('www', "www.baidu.com").group())  # 打印匹配到的结果
# print(re.match('www', "www.baidu.com").end())  # 打印匹配到的结束位置,不包含该索引字符
# print(re.match('www', "www.baidu.comw").endpos)  # 打印最后一个字符串位置
# print(re.match('www', "www.baidu.com").groupdict())
# print(re.match('www', "www.baidu.com").groups())
# print(re.match('www', "www.baidu.com").lastindex)
# print(re.match('www', "www.wwwbaidu.com").pos)  # 打印匹配索引
# print(re.match('www', "www.baidu.com").re)  # 打印编译(解析公式)
# print(re.match('ww', "www.baidu.com").span())  # 打印匹配分片的位置
# print(re.match('www', "www.baidu.com").start())  # 打印匹配开始索引
# print(re.match('www', "www.baidu.com").string)  # 打印被匹配字符串
#
# print(re.search("www", "www.www.com"))
# print(re.search("www", "qq.www.com"))
# print(re.search("www", "www.www.com").string)
# print(re.search("www", "www.www.com").start())
# print(re.search("www", "qq.www.com").start())
# print(re.search("www", "qq.www.com").span())  # 返回匹配到的索引位置
# print(re.search("www", "www.www.com").span())
# print(re.search("www", "qq.www.com").group())
# print(re.search("www", "qq.www.com").groups())
# print(re.search("www", "qq.www.com"))
#
# # search 与match,
# # search 从头匹配,只要找到则停止匹配,如果有多个被匹配,只返回最先匹配到的位置字符
# # match  从头匹配,开头位置匹配不到就不继续匹配


# print(re.sub("\d+", "", "17480hytsakhh54289"))  # 删除数字

# print(re.sub("\d+", "", "17480hytsakhh54289", count=1))  # 删除数字,只删除第一次匹配到的


# a = "123abc456"
# print(re.search("([0-9]*)([a-z]*)([0-9]*)", a).group())  # 模式()分组匹配
# print(re.search("([0-9]*)([a-z]*)([0-9]*)", a).group(0))  # 显示第0组,也就是所有分组
# print(re.search("([0-9]*)([a-z]*)([0-9]*)", a).group(1))  # 显示第一组分组
# print(re.search("([0-9]*)([a-z]*)([0-9]*)", a).group(2))
# print(re.search("([0-9]*)([a-z]*)([0-9]*)", a).groups())  # 返回元组形式的分组匹配

# print(re.findall("\d+", "gghf23812uygc4x36123y9hsoy93y2932"))  # 返回一个列表
#
# print(re.split(",", "445dfds77fg45cxxc3fsdbuu"))  # 以逗号分隔
# print(re.split("\d+", "445dfds77fg45cxxc3fsdbuu", maxsplit=2))  # 分三列

# contactInfo = 'Oldboy School, Beijing Changping Shahe: 010-8343245'
# match = re.search('(?P<last>\w+\s+\w+),(?P<first>\s+\w+\s+\w+\s+\w+): (?P<phone>\S+)', contactInfo)
# print(match.group("last"))  # 打印自定义标签内容
# print(match.group('first'))
# print(match.group("phone"))
# match = re.search('(\w+)|(\s+)(\d+)', contactInfo) #分组
# print(match.group())




import os
# print(os.abort())  # 终止进程
# print(os.access())
# print(os.chdir())
# print(os.chflags())
# print(os.chmod())
# print(os.chown())
# print(os.chdir())
# print(os.chroot())
# print(os.close())
# print(os.closerange())
# print(os.cpu_count())  # cpu数量
# print(os.confstr())
# print(os.WTERMSIG())
# print(os.WSTOPSIG())
# print(os.writev())
# print(os.write())
# print(os.WIFSTOPPED())
# print(os.WIFSIGNALED())
# print(os.WIFEXITED())
# print(os.WIFCONTINUED())
# print(os.WEXITSTATUS())
# print(os.WCOREDUMP())
# print(os.walk())
# print(os.wait())
# print(os.utime())
# print(os.urandom(1))
# print(os.unlink())
# print(os.uname())
# print(os.umask())
# print(os.ttyname())
# print(os.truncate())
# print(os.tmpnam())
# print(os.tmpfile())
# print(os.times())
# print(os.system())
# print(os.sysconf())
# print(os.sync())
# print(os.symlink())
# print(os.strerror())
# print(os.statvfs())
# print(os.stat_float_times())
# print(os.spawnvpe())
# print(os)
# print(os.getcwd())  # 获取当前目录
# print(os.chdir('/'))  # 切换到/目录
# print(os.getcwd())
# print(os.curdir)  # 当前目录
# print(os.pardir)  # 上一级目录
# print(os.makedirs("test/test2", mode=777, exist_ok=True))  # 创建多层目录
# print(os.removedirs("test"))  # 移除目录
# print(os.mkdir("test", mode=777))  # 创建单层目录
# print(os.rmdir('test'))  # 删除空目录
# print(os.listdir(os.curdir))  # 显示当前目录文件
# print(os.remove("test"))  # 删除test文件
# print(os.rename("old", "newname"))  # 重命名文件,如果当前存在重名文件,则报错
# print(os.stat("re_ext.py"))
# print(os.sep)  # 打印系统路径分隔符
# print(list(os.linesep))  # 打印系统换行符
# print(os.pathsep)  # 打印path变量分隔符
# print(os.name)  # 输出字符串指示当前使用平台。win->'nt'; Linux->'posix'
# print(os.system("command"))  # 执行系统命令
# print(os.environ)  # 打印环境变量
# print(os.path.abspath(os.curdir))  # 打印当前绝对路径
# print(os.path.split(os.curdir))  # 讲目录分隔为二元组返回
# print(os.path.dirname(os.pardir))  # 打印目录
# print(os.path.basename(os.curdir))  # 打印当前文件
# print(os.path.exists("test"))  # 打印当前是否存在test文件
# print(os.path.isabs(os.path.abspath(os.curdir)))  # 判断是否绝对路径
#
# print(os.path.isfile("test"))  # 判断test是不是一个文件
# print(os.path.isdir("test"))  # 判断test是不是一个目录
# print(os.path.join("/test", "test2"))  # 将多个路径组合成一个新路径,忽略绝对路径之前的参数
# print(os.path.getatime("re_ext.py"))  # 打印文件的最后存取时间,时间撮形式返回
# print(os.path.getmtime("re_ext.py"))  # 打印文件最后修改时间
# print(os.path.getsize("re_ext.py"))  # 打印文件大小



import sys
print(sys.argv)  # 列表形式返回命令行参数,第一个元素是文件本身
print(sys.modules)  # 打印系统所有模块,字典形式返回
# print(sys.exit(2))  # 打印程序返回代码
print(sys.version)  # 打印python版本
print(sys.maxsize)  # 打印最大值
print(sys.path)  # 返回当前PYTHONPATH环境变量
print(sys.platform)  # 返回操作系统平台名称
print(sys.stdout.write("inpu9t"))  # 返回标准输出长度
# print(sys.stdin.readlin()[:-1])  # 标准输入,并分片取开头到倒数第一个(不包含)的内容
print(sys.modules.keys())  # 打印所有模块名
print(sys.modules.values())  # 打印所有模块位置
print(sys.exc_info())  # 获取当前正在处理的异常类,exc_type、exc_value、exc_traceback当前处理的异常详细信息
print(sys.hexversion)  # 获取十六进制的版本值
print(sys.api_version)  # 获取Cpython API版本
print(sys.version_info)  # 打印版本详细信息
print(sys.displayhook(2))  # 如果value非空，这个函数会把他输出到sys.stdout，并且将他保存进__builtin__._.指在python的交互式解释器里，’_’ 代表上次你输入得到的结果，hook是钩子的意思，将上次的结果钩过来
print(sys.getdefaultencoding())  # 获取当前默认编码格式
print(sys.getfilesystemencoding())  # 获取文件系统编码
print(sys.builtin_module_names)  # 打印内置模块名
print(sys.executable)  # 打印python解释权程序路径
print(sys.getprofile())
print(sys.getallocatedblocks())
# print(sys.copyright)  # 打印python版权信息
print(sys.byteorder)  # 本地字节规则的指示器，big-endian平台的值是’big’,little-endian平台的值是’little’
# print(sys.exc_value)
print(sys.stdin)  # 标准输入
print(sys.stdout)  # 标准输出
print(sys.stderr)  # 标准错误输出
print(sys.maxunicode)  #   打印最大unicode值

# import time
# def consumer(name):
#     print("%s 准备吃包子啦！"%name)
#     while True:
#         baozi = yield
# 
#         print("包子[%s]来了，被[%s]吃了" % (baozi, name))
# 
# def producer(name):
#     c = consumer("A")
#     c2 = consumer("B")
#     c.__next__()
#     c2.__next__()
#     print("老子开始准备做包子啦！")
#     for i in range(10):
#         time.sleep(1)
#         print("做了2个包子！")
#         c.send(i)
#         c2.send(i)
# 
# producer("alex")


    
