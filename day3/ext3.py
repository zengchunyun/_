#!/usr/bin/env python
# encoding:utf8
'''
Created on 2016年1月9日
@author: zengchunyun
'''

# import smtplib
# from email.mime.text import MIMEText
# from email.utils import formataddr
#
# def mail(user):
#     ret =True
#     try:
#         msg = MIMEText('垃圾邮件', 'plain', 'utf-8')
#         msg['From'] = formataddr(["武沛齐",'wptawy@126.com'])
#         msg['To'] = formataddr(["走人",'424662508@qq.com'])
#         msg['Subject'] = "主题"
#
#         server = smtplib.SMTP("smtp.126.com", 25)
#         server.login("wptawy@126.com", "WW.3945.59")
#         server.sendmail('wptawy@126.com', [user,], msg.as_string())
#         server.quit()
#     except Exception:
#         ret = False
#     return ret
#
# ret = mail('424662508@qq.com')
#
# if ret:
#     print('发送成功')
# else:
#     print('发送失败')


# def show():
#     print('a')
#     if 1== 1:
#         print('c')
#         return [11,22]
#     print('b')
#
# show()
#
# def show(a1):
#     print(a1)
#
# show(2)
#
# def show(a1,a2):
#     print(a1,a2)
# show(11,22)
#
# def show(a1,a2=111):
#     print(a1,a2)
#
# show(11121)
#
# show(a2=21212,a1=2121212)


# def show(*args):
#     print(args,type(args))
#
# show(11,22)
# show(11)
# show([11,22,33,44])
#


def show(*args, **kwargs):
	print(args, type(args))
	print(kwargs, type(kwargs))
	print(''.join(str(args)))


show(11,22,33,44)
#
# show(a=11,b=33)
#
# show(11,22,33,a=111,b=444)
#
# li = [11,22,33]
# d1 = {'2':212,'q':33232}
#
# show(li,d1)
#
# show(*li,**d1)

# s1 = "{0} is {1}"
#
# ret = s1.format('alex','sb')
#
#
#
# print(ret)
#
# ll = ['alex','sb']
# ret = s1.format(*ll)
#
# print(ret)
#
# s2 = "{name} is {actor}"
# res = s2.format(name='alex',actor='sb')
#
# print(res)
#
# d1 ={'name':'alex','actor':'sb'}
#
# res = s2.format(**d1)
# print(res)

# func = lambda a: a+1
#
# ret = func(1)
# print(ret)

# print(abs(-1))
# ret = all(['',[],{},None])
# ret2 = all([1,2,3])  #所有元素为真才为真
# print(ret2)
# print(ret)
#
# ret3 = any(['',[],{},None,1])  # 只要任意一个是真则为真
# print(ret3)
#
# print(bool([]))    # None '' [] {} 0
#
# print(bin(111))
# print(ord('1'))
# print(chr(49))
#
# print(bytearray('hell',encoding='utf-8'))
# print(bytearray('我',encoding='utf-8'))
# print(bytes('fff',encoding='utf-8'))
#
# a =list()
# print(callable(a))  #是否可调用,   即__call__ 方法


# compile()  #将代码编译



# map1 = map(lambda x:x+11,[11,22,33])
# print(list(map1))

# round(9.5)  #四舍五入
# dir()  # 成员的的值
#
# vars()  # 返回字典

# f = open('testlog','r',encoding='utf-8')
# f.write('我hhsas')
# f.close()
# f = open('testlog','rb')
# a = f.read(3)  # 读取字符
# a1 =f.tell()
#
# print(a)
# print(a1)
#
# f.close()
#
# print(bytes(a).decode(encoding='utf-8'))
#
# 1、用户输入字符串
# 	‘{"backend": "test.oldboy.org","record":{"server": "100.1.7.999","weight": 20,"maxconn": 30}}’
# 2、字典
# 	dic
#
# 3、添加
# 2、删除（可选、）