#!/usr/bin/env python3
# encoding:utf8
'''
Created on 2015年12月27日
@author: zengchunyun
'''
from getpass import getpass

RetryCount = 0  # 初始化最大重复输入密码次数，每次输入用户名密码信息机会只有三次，超过则退出
LockCount = 2  # 初始化锁定次数，由于第一次比较前，该值次数会减去1，所以这里值改成2，同一个账号输错密码，超过3次，则锁定该账号
CompName = None  # 初始化一个临时用来存储用户上一次输入的用户名
UserName = None  # 初始化用户登陆名，与CompName作比较用
Passwd = None  # 初始化密码
flag = False  # 设置一个标记，用于判断用户输入的登陆信息是否为真，只有通过验证时或被锁定，该标记才为True

while RetryCount < 3:  # 当用户重复输入验证信息大于三次时，则停止循环
    UserName = str(input('请输入用户名：')).strip()  # 去除用户输入的两侧空白字符
    OpenLockFile = open('lockAccount.db', 'a+')  # 以追加方式打开该文件，如果不存在，则创建该文件
    OpenLockFile.seek(0)  # 由于是追加模式，所以文件指针在末尾，这里将指针指向文件开头位置
    for info in OpenLockFile.readlines():
        if str(info.strip()) == UserName:  # 通过迭代方式查询该账号是否被锁定，如果已经锁定，则退出程序
            print('该用户已经被锁定，请联系后台管理员解锁！！！')
            flag = True
            break
    OpenLockFile.close()
    if not flag:
        Passwd = str(getpass('请输入密码：')).strip()  # 使用密文方式处理用户输入
        if CompName == UserName:  # 当上一次用户名与这一次用户名相同时，则会这个用户名计数次数加1，超过三次则锁定
            LockCount += 1
        else:
            CompName = UserName  # 如果上一次用户名与本次不一样，则本次输入的用户名值赋给CompName，并且计数减1
            LockCount -= 1
        OpenAccountFile = open('account.db', 'r')  # 以只读方式打开账号信息文件
        for info in OpenAccountFile.readlines():  # 迭代方式去匹配用户输入信息是否匹配，匹配则中断迭代查询，并将flag标记为True
            if UserName == info.split()[0] and Passwd == info.split()[1]:
                print('登陆成功！')
                flag = True
                break
        else:
            if LockCount == 2 and UserName:  # 当同一个账号输错2次时，且账号不为空，将提示用户此信息
                print('您还有一次机会，输入错误三次，账号将被锁定')
            else:
                print('用户名或密码错误！')  # 当用户名密码验证未通过，则提示用户错误信息
        OpenAccountFile.close()
    if flag:
        break  # 当用户登陆成功或账户被锁定，则终止整个循环
    RetryCount += 1
else:  # 当用户重试三次则结束本次循环
    if LockCount == 3 and UserName:  # 同一个账号错误输入三次，且用户名不能为空，则将此账号写入锁定文件
        OpenLockFile = open('lockAccount.db', 'a')
        OpenLockFile.write('%s\n' % (UserName))
        OpenLockFile.close()
        print('用户密码输入错误三次，已被锁定！！！')
    else:
        print('您错误输入超过三次，请稍后再试！！！')
