#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

#
# class MyException(Exception):
#     """
#     自定义异常,继承Exception
#     """
#     def __init__(self, msg):
#         self.msg = msg
#
#     def __str__(self):
#         """
#         当实例化对象后,print对象将打印该值
#         """
#         return self.msg
#
# myexception = MyException
# try:
#
#     num1 = input("num1:")
#     num2 = input("num2")
#     num1 = int(num1)
#     num2 = int(num2)
#     result = num1 + num2
#     print(result)
#     raise myexception("yes. it's ok")
# except ValueError as v:
#     print("value error", v)
# except myexception as e:
#     print(e)
# except KeyboardInterrupt:
#     print("上面无法抓住终止")
# except InterruptedError:
#     print("test")
# except SyntaxError:
#     print("该异常无法捕获")
# except IndentationError:
#     print("该异常依然无法捕获")
# except Exception:
#     print("no")
# else:
#     print("一般测试用例,或者安装,可以使用,比如安装成功,没有错误")
# finally:
#     print("不管前面什么错,最终都会执行这里,除了语法,缩进以外")



import os
import sys
# cur_path = os.path.abspath(os.path.curdir)
# print(cur_path)
# print(os.path.abspath("./u"))
# new_path = os.path.join("../sa")
# print(new_path)
# print(os.path.abspath(new_path))
#
#
# RECV_BUFFER = 1000
#
#
# def readfile(filename, seek):
#         if not os.path.exists(filename):
#             yield False
#             return False
#         total_size = os.path.getsize(filename)
#         total_size -= seek
#         if total_size % RECV_BUFFER == 0:
#             times = int(total_size / RECV_BUFFER)  # 刚好传完的次数
#         else:
#             times = int(total_size / RECV_BUFFER) + 1  # 否则,次数再加一次
#         percent = 0  # 初始百分比
#         count = 100 / times  # 计算每次增加的百分比
#
#         while total_size > 0:
#             percent += float(count)
#             hashes = "#" * int(percent / 100.0 * times)
#             spaces = " " * (times - len(hashes))
#             percent_format = "{:.2f}".format(percent)
#             space = " " * (6 - len(percent_format))
#             sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent_format + space, hashes + spaces))
#             sys.stdout.flush()
#             with open(filename, "rb") as readdata:
#                 readdata.seek(seek)
#                 has_read = readdata.read(RECV_BUFFER)
#                 if has_read:
#                     seek = readdata.tell()
#                     print(seek)
#                     total_size -= RECV_BUFFER
#                     yield has_read, seek
#                 else:
#                     readdata.close()
# temp = open("fff.pdf", "a+b")
# while True:
#             data_obj = readfile("/Users/zengchunyun/Documents/python_project/s12/day8/MyFTP/userdata/zengchunyun/ATM.pdf", 5000)
#             for data in data_obj:
#                 # pass
#                 temp.write(data[0])
#                 print(data[1])
#                 if data[1] == 5000:
#                     break
#
#             break
# temp.close()
#
#
# def writefile(filename, data, total_size=0, seek=0, mode="a+b"):
#     if os.path.exists(filename):
#             yield False
#             return False
#         total_size = os.path.getsize(filename)
#         total_size -= seek
#         if total_size % RECV_BUFFER == 0:
#             times = int(total_size / RECV_BUFFER)  # 刚好传完的次数
#         else:
#             times = int(total_size / RECV_BUFFER) + 1  # 否则,次数再加一次
#         percent = 0  # 初始百分比
#         count = 100 / times  # 计算每次增加的百分比
#
#         while total_size > 0:
#             percent += float(count)
#             hashes = "#" * int(percent / 100.0 * times)
#             spaces = " " * (times - len(hashes))
#             percent_format = "{:.2f}".format(percent)
#             space = " " * (6 - len(percent_format))
#             sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent_format + space, hashes + spaces))
#             sys.stdout.flush()
#             with open(filename, "rb") as readdata:
#                 readdata.seek(seek)
#                 has_read = readdata.read(RECV_BUFFER)
#                 if has_read:
#                     seek = readdata.tell()
#                     print(seek)
#                     total_size -= RECV_BUFFER
#                     yield has_read, seek
#                 else:
#                     readdata.close()
#         percent = 0
#         while percent <= 100:
#             hashes = "#" * int(percent / 100.0 * 50)
#             spaces = " " * (50 - len(hashes))
#             sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent, hashes + spaces))
#             sys.stdout.flush()
#             percent += 1
#         with open(filename, mode) as writedata:
#             writedata.seek(seek)
#             writedata.write(data)
#             writedata.flush()


# os.rename("/Users/zengchunyun/Documents/python_project/s12/day8/temp/fff.pdf", "/Users/zengchunyun/Documents/python_project/s12/day8/temp/ff.pdf")


# import os
# import sys
#
# print(os.stat("test"))

# a = 1
# try:
#     if type(8) is not int:
#         raise TypeError("no")
#     else:
#         print(111)
# except TypeError:
#     print("ok")


# import uuid
# print(type(str(uuid.uuid4())))
# from  multiprocessing import Process,Pool
# import time
#
# def Foo(i):
#     time.sleep(2)
#     return i+100
#
# def Bar(arg):
#     print('-->exec done:',arg)
#
# pool = Pool(5)
#
# for i in range(10):
#     pool.apply_async(func=Foo, args=(i,),callback=Bar)
#     #pool.apply(func=Foo, args=(i,))
#
# print('end')
# pool.close()
# pool.join()#进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。

a = ["1", "2", "3"]
filter_a = filter(lambda i: int(i) < 2, a)
print(list(filter_a))
try:
    assert len(list(filter_a)) == len(a)

except AssertionError:
    print("条件不匹配,")

print("hello")