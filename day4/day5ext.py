#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
# import time
# print(time.time())
# print(time.altzone)
# print(time.clock())
# print(time.ctime())
# print(time.daylight)
# print(time.gmtime())
# print(time.localtime())
# print(time.monotonic())
# print(time.timezone)
# print(time.tzset())
# print(time.tzname)
# print(time.process_time())
# print(time.struct_time)
# print(time.perf_counter())
#
#
# def write_to_database(filename, string):
#     with open(filename, 'w') as wr_data:
#         wr_data.write('user_info = %s' % (json.dumps(string)))
#
# write_to_database('./config/settings.py', user_info)
# user_conf = open('./config/settings.py', 'r')
#
# temp_user_db = open('./config/account.db', 'wb')
# read_user_conf = user_conf.read()
# temp_user_db.write(pickle.dumps(read_user_conf))
# temp_user_db.close()
# #
# open_user_db = open('./config/account.db', 'rb')
# read_user_db = pickle.load(open_user_db)
# print(read_user_db)
# open_user_db.close()
#
#
# user_conf = open('./config/settings.py', 'r')
#
# temp_user_db = open('./config/account.db', 'w')
# read_user_conf = user_conf.read()
# temp_user_db.write(json.dumps(read_user_conf))
# temp_user_db.close()
# #
# open_user_db = open('./config/account.db', 'r')
# read_user_db = json.load(open_user_db)
# print(read_user_db)
# open_user_db.close()


# def myljust(str1, width, fillchar=None):
#     if fillchar == None:
#         fillchar = ' '
#     length = len(str(str1).encode('gb2312'))
#     fill_char_size = width - length if width >= length else 0
#     return "%s%s" % (str1, fillchar * fill_char_size)
#
#
# def myrjust(str1, width, fillchar=None):
#     if fillchar == None:
#         fillchar = ' '
#     length = len(str(str1).encode('gb2312'))
#     fill_char_size = width - length if width >= length else 0
#     return "%s%s" % (fillchar * fill_char_size, str1)
#
#
# def mycenter(str1, width, fillchar=None):
#     if fillchar == None:
#         fillchar = ' '
#     length = len(str(str1).encode('gb2312'))
#     fill_char_size = width - length if width >= length else 0
#     if length % 2 == 0:
#         return "%s%s%s" % (fillchar * (fill_char_size // 2), str1, fillchar * (fill_char_size // 2))
#     else:
#         return "%s%s%s" % (fillchar * (fill_char_size // 2 + 1), str1, fillchar * (fill_char_size // 2))
#
# string = "我爱你"
# print(myrjust(string,20))
# print(str(string).encode('gb2312').rjust(20))
#
# import hashlib
# m = hashlib.md5()
# m.update('748'.encode('utf-8'))
# print(m.hexdigest())rdre



# mybank = MyBank(**user_info['my_bank'])
# mybank.register_account(user='zcy', password=520)
# print(mybank.search_account_info("zcy"))
# userinfo = UserInfo(**user_info['account_info'])  # 将一个键为用户名,值为密码的字典数据传入该对象,并实例化一个对象
# userinfo.register(user='zcy', password='777', mail='dasaobing@748.com')
# newname = userinfo.register(user='学霸', password=520, mail='850808158@qq.com', tel=18710155115)
# if newname:  # 如果新增用户不存在,则返回新的用户数据字典
#     user_info['name'] = newname
#
# #
# update_info(user_info)
#
# new_info = userinfo.change_password(333, user='zcy', password=111, new_assword=777)
# if new_info:
#     print('改密成功')
# else:
#     print('改密失败')
# if new_info:  # 如果新增用户不存在,则返回新的用户数据字典
#     user_info['account_info'] = new_info
#
# update_info(user_info)
# if userinfo.login('学霸', '520'):
#     print("学霸登录成功")
# else:
#     print('登陆失败')
# print(userinfo.change_info('学霸'))



# class MyBank(object):
#     def __init__(self, **kwargs):
#         self.user = None  # 初始化用户名
#         self.password = None  # 初始化密码
#         self.new_password = None  # 初始化新密码,用于改密码
#         self.user_auth_info = kwargs
#         self.user_info = {}  # 用来存储对应的一个用户名的具体信息
#         self.account_info = ()  # 一般只用来接收用户名和密码
#
#     def search_account_info(self, *args, **kwargs):
#         self.user_info = kwargs
#         self.account_info = args
#         try:
#             self.user = self.user_info['user']
#         except KeyError:
#             try:
#                 self.user = self.account_info[0]
#             except IndexError:
#                 print("必须传入一个参数作为用户名使用,或者字典包含键'user")
#                 return False
#         get_info = UserInfo(**self.user_auth_info).change_info(self.user)
#         if get_info:
#             return get_info[self.user]
#
#     def register_account(self, *args, **kwargs):
#         self.user_info = kwargs
#         self.account_info = args
#         return UserInfo(**self.user_auth_info).register(*self.account_info, **self.user_info)
#
#     def login(self, *args, **kwargs):
#         self.user_info = kwargs
#         self.account_info = args
#         return UserInfo(**self.user_auth_info).login(*self.account_info, **self.user_info)
#
#     def change_password(self, *args, **kwargs):
#         self.user_info = kwargs
#         self.account_info = args
#         return UserInfo(**self.user_auth_info).change_password(*self.account_info, **self.user_info)
#
#


# import time
# print(time.time())  # 以秒的形式返回当前时间,从1970年1月1日开始计算  1455613795.636903
# print(time.altzone)  # 时间差,与标准的格林威治时间相差8小时,以秒返回 -28800.0
# print(time.localtime())  # 以元组形式显示当地时间
# print(time.asctime(time.localtime()))  # 将元组形式的时间格式转换成可读性的时间格式 Tue Feb 16 16:52:51 2016
# print(time.clock())  # 返回CPU执行时间,或第一次调用clock函数的时间 0.047894
# print(time.ctime())  # 返回可读性的时间 Tue Feb 16 16:56:59 2016 等效于asctime(localtime(seconds))
# print(time.gmtime())  # 以元组形式显示格林威治时间
# print(time.localtime(0))
# print(time.mktime(time.gmtime(2)))  # -28798.0
# print(time.mktime(time.gmtime(0)))  # 当秒为0,不会返回0,而是以秒形式返回当前时区的timezone或altzone的值 -28800.0
# print(time.monotonic())
# print(time.perf_counter())
# print(time.process_time())  # 返回内核到用户空闲的CPU这段时间0.045212
# print(time.sleep(0.01))  # 睡眠0.01秒
# print(time.strftime("%p", time.localtime()))  # 格式时间
#     %Y  Year with century as a decimal number.  # 年
#     %m  Month as a decimal number [01,12].  # 月
#     %d  Day of the month as a decimal number [01,31].  # 日
#     %H  Hour (24-hour clock) as a decimal number [00,23].  #小时
#     %M  Minute as a decimal number [00,59].  # 分钟
#     %S  Second as a decimal number [00,61].  # 秒
#     %z  Time zone offset from UTC.  # 当前时区
#     %a  Locale's abbreviated weekday name.  # 星期几,例如Tue
#     %A  Locale's full weekday name.  # 全拼星期几, Tuesday
#     %b  Locale's abbreviated month name. # 几月份,例如 Feb
#     %B  Locale's full month name.  # 全拼月, February
#     %c  Locale's appropriate date and time representation.  # 显示这种格式时间 Tue Feb 16 17:32:19 2016
#     %I  Hour (12-hour clock) as a decimal number [01,12].  # 以12小时进制显示当前时间
#     %p  Locale's equivalent of either AM or PM.  # 显示上午还是下午

# print(time.strptime("2016", "%Y"))  # 以元组形式返回一个结构化时间,
# print(time.tzset())  # 初始化本地时区或重新初始化
import datetime
print(datetime.datetime.now())  # 显示当前时间
print(datetime.timedelta(days=5))
print(datetime.datetime.now() - datetime.timedelta(days=5))  # 显示5天前的时间
print(datetime.date.today())  # 显示当前日期
print(datetime.date.ctime(datetime.date.today()))  # 显示可读性时间
print(datetime.date.strftime(datetime.date.today(), "%Y"))  # 格式化时间

import time
import datetime
print(datetime.date.fromtimestamp(time.time()))
print(datetime.date.fromtimestamp(time.time() - 86400))  # 减去一天的秒数
print(datetime.datetime.now().date())
print(datetime.datetime.now().time())
print(datetime.datetime.now().today())
print(datetime.datetime.now().year)
print(datetime.datetime.now().weekday())  # 打印星期几,从开始,0-6,0为周日
print(datetime.datetime.now().utctimetuple())  # 打印UTC struct时间
print(datetime.datetime.now().utcoffset())
print(datetime.datetime.now().tzname())
print(datetime.datetime.now().toordinal())
print(datetime.datetime.now().timetz())
print(datetime.datetime.now().timetuple())  # 打印struct时间
print(datetime.datetime.now().timestamp())  # 显示时间戳
print(datetime.datetime.now().month)  # 显示月
print(datetime.datetime.now().replace(2016, 9, 12))  # 替换指定时间打印
print(datetime.datetime.now() - datetime.datetime.now().replace(2016, 2, 11))  # 计算时间差
print(datetime.datetime.now() + datetime.timedelta(seconds=10))  # 加10秒,显示10秒后的时间


time_before = datetime.datetime.now().replace(2016, 9, 12)
print(type(time_before))
print(str(time_before))


def month_to_days(year, month, day):  # 计算从1月1日开始,到指定日期的天数
    """
    :param year: 年
    :param month: 月
    :param day: 日
    :return: 返回一个元组 整月的天数,和具体指定日期的天数,一年天数
    """
    total_days = 0  # 到本月底的天数
    today_days = 0  # 到今天为止的天数
    this_year = 0
    while True:
        days = 31  # 一月
        today_days = total_days + day
        total_days += days
        if month in ["Jan", 1] and day in range(1, days):
            break
        year = int(year)
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            days = 29
            this_year = 366
        else:
            days = 28  # 二月
            this_year = 355
        today_days = total_days + day
        total_days += days
        if month in ["Feb", 2] and day in range(1, days):
            break
        days = 31  # 三月
        today_days = total_days + day
        total_days += days
        if month in ["Mar", 3] and day in range(1, days):
            break
        days = 30  # 四月
        today_days = total_days + day
        total_days += days
        if month in ["Apr", 4] and day in range(1, days):
            break
        days = 31  # 五月
        today_days = total_days + day
        total_days += days
        if month in ["May", 5] and day in range(1, days):
            break
        days = 30  # 六月
        today_days = total_days + day
        total_days += days
        if month in ["Jun", 6] and day in range(1, days):
            break
        days = 31  # 七月
        today_days = total_days + day
        total_days += days
        if month in ["Jul", 7] and day in range(1, days):
            break
        days = 31  # 八月
        today_days = total_days + day
        total_days += days
        if month in ["Aug", 8] and day in range(1, days):
            break
        days = 30  # 九月
        today_days = total_days + day
        total_days += days
        if month in ["Sep", 9] and day in range(1, days):
            break
        days = 31  # 十月
        today_days = total_days + day
        total_days += days
        if month in ["Oct", 10] and day in range(1, days):
            break
        days = 30  # 十一月
        today_days = total_days + day
        total_days += days
        if month in ["Nov", 11] and day in range(1, days):
            break
        days = 31  # 十二月
        today_days = total_days + day
        total_days += days
        if month in ["Dec", 12] and day in range(1, days):
            break
        else:
            return False
    return total_days, today_days, this_year


# datetime.datetime.strptime("2016/02-18", "%Y/%m/%d")

print(str("77.9"))