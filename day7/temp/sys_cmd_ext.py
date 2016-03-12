#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import sys
import os
#
# print(os.path.abspath("./pub"))
# new_path = os.path.join("./pub", "root")
# home = os.path.abspath(new_path)
# if os.path.isdir(home):
#     print(999)
# else:
#     print(os.makedirs(home, exist_ok=False))
#
# import re
# a = "/root/sasa/ppp"
# b = "/root"
#
# c = a.split(b)[1]
# print(c)
#
# c = "/sasa/ppp"
#
#
#
# c = a.replace(b, "")
# c = re.sub(b, '', a)
# print(a)
# new_path = "."
# print(os.path.abspath(new_path))
# new_path = ".."
# print(os.path.abspath(new_path))
# new_path = "../../day7"
# print(os.path.abspath(new_path))
# new_path = "./s12"
# print(os.path.abspath(new_path))
import sys
import os
import time

percent = 0
while percent <= 100:
    hashes = "#" * int(percent / 100.0 * 50)
    spaces = " " * (50 - len(hashes))
    sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent, hashes + spaces))
    sys.stdout.flush()
    percent += 1

# def readfile(filename, seek):
#     total_size = os.path.getsize(filename)
#     if total_size % 100 == 0:
#         buffer = int(total_size / 100)
#     else:
#         buffer = int(total_size / 99)
#     percent = 0
#     while total_size > 0:
#         percent += 1
#         hashes = "#" * int(percent / 100.0 * 50)
#         spaces = " " * (50 - len(hashes))
#         sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent, hashes + spaces))
#         sys.stdout.flush()
#         time.sleep(0.1)
#         with open(filename, "rb") as readdata:
#             readdata.seek(seek)
#             has_read = readdata.read(buffer)
#             if has_read:
#                 seek = readdata.tell()
#                 total_size -= buffer
#                 yield has_read, seek
#             else:
#                 readdata.close()
#
# filename = "class.png"
# newpng = open("newpng0.png", "wb")
# a = readfile(filename, 0)
# for i in a:
#     newpng.write(i[0])


#
# def progress_test():
#     bar_length = 100
#     for percent in range(1, 101):
#         hashes = '#' * int(percent/100.0 * bar_length)
#         spaces = ' ' * (bar_length - len(hashes))
#         sys.stdout.write("\r已完成:[{}%] [{}] ".format(percent, hashes + spaces))
#         sys.stdout.flush()
#         time.sleep(0.1)
#
# progress_test()

#
# def fillchar():
#     readfile(filename, 0).__next__()
#     print("\r[{}%]".format(i), end="")
#     os.write(1, b"#")
#
# if __name__ == '__main__':
#     for i in range(1, 103):
#         time.sleep(0.1)
#         fillchar()


# import time
# import sys

# def progress_test():
#     bar_length=20
#     for percent in range(0, 100):
#         hashes = '#' * int(percent/100.0 * bar_length)
#         spaces = ' ' * (bar_length - len(hashes))
#         sys.stdout.write("\rPercent: [%s] %d%%"%(hashes + spaces, percent))
#         sys.stdout.flush()
#         time.sleep(1)
#
# progress_test()


# import sys
# import time

#
#
# def progress(width, percent):
#     print "%s %d%%\r" % (('%%-%ds' % width) % (width * percent / 100 * '='), percent),
#     if percent >= 100:
#         print
#         sys.stdout.flush()
#
# # Simulate doing something ...
# for i in range(100):
#     progress(50, (i + 1))
#     time.sleep(0.1) # Slow it down for demo
#
#
# import sys,time
# j = '#'
# if __name__ == '__main__':
#   for i in range(1, 61):
#     j += '#'
#     sys.stdout.write(str(int((i/60)*100))+'% ||'+j+'->'+"\r")
#     sys.stdout.flush()
#     time.sleep(0.5)
#     print

#
# import sys,time
# if __name__ == '__main__':
#   for i in range(1, 61):
#     sys.stdout.write("\r[%s]#\b\b"% i)
#     sys.stdout.flush()
#     time.sleep(0.5)
# print



