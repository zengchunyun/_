#!/usr/bin/env python3

import re
import os
import time
from publicAPI import auth_account, register_account, change_admin_password
from publicAPI import modify_admin_account_info, add_admin_account, delete_account, change_admin_permission
from config.goods import goods
from config.settings import user_info
from publicAPI import register_account, for_super_admin_change_password, for_admin_unlock_account, for_admin_lock_account
from record_log import Logger
from publicAPI import change_user_credit_line, show_account_info, for_owner_change_password
from publicAPI import transfer_cash, search_history_log
from publicAPI import for_admin_withdraw_money
from ATM import update_info
from publicAPI import myljust
bank_log_file = "china_bank.log"  # 银行基本日志
sold_log_file = "sold_bank.log"  # 用户交易日志


class Shopping(object):
    def __init__(self, **kwargs):
        self.user = None  # 初始化一个用户名,用于标记登陆状态
        self.args = None
        self.kwargs = kwargs
        self.cart = {}  # 设置一个商品编号映射价格的字典
        self.list = []
        self.index = 0  # 设置获取列表的下标起始位置
        self.totalMoney = 0  # 初始化购物总价
        self.status = False  # 设置登陆状态
        self.flag = False  # 设置登陆显示菜单标记

    def goods_menu(self, status):
        self.status = status
        print('欢迎光临中关村倒卖二手货市场'.center(40))
        self.user = self.login_status(self.status)
        if self.user:
            self.status = '%s已登陆' % self.user
        else:
            self.status = '未登陆'
            self.flag = True
        goods_num = "商品编号"
        goods_name = "商品名"
        goods_price = "价格(RMB)"
        is_good = "好评"
        store = "库存"
        print('%s%s\n' % ('请输入对应商品编号选择您需要购买的商品'.ljust(28), self.status.center(26, '*')))
        print('%s%s%s%s%s' % (goods_num.ljust(12), goods_name.ljust(35), goods_price.ljust(14),
                              is_good.ljust(10), store.ljust(12)))
        if type(self.kwargs) == dict:
            self.list = list(self.kwargs.keys())
            self.list.sort()
            for value in self.list:
                index = str(value)
                first = str(self.kwargs[str(value)][0])
                second = str(self.kwargs[str(value)][1])
                third = str(self.kwargs[str(value)][2])
                fourth = str(self.kwargs[str(value)][3])
                print("%s%s%s%s%s" % (index.ljust(12), first.ljust(40), second.ljust(14),
                                      third.ljust(12), fourth.ljust(12)))
            if self.flag:
                print("""帮助(h)    登陆(l)    注册(r)    购物车(s)    退出(q)  返回(b)""")
            else:
                print("""帮助(h)    %s    购物车(s)    退出(q)  注销(b)""" % str(self.status))

    def shop_list(self, *args, print_now=True):  # 显示购物车,并返回一个包含商品编号对应价格的字典
        self.args = args
        self.cart = {}
        if self.args and type(self.args[0]) == list:
            self.list = self.args[0]
            self.list.sort()
            if print_now:
                print('\n%s%s%s' % ('商品编号'.ljust(12), '商品名称'.ljust(35), '价格'.ljust(14)))
            for index in range(len(self.list)):
                keys = self.list[index]
                if print_now:
                    print('%s%s%s' % (str(keys).ljust(12),
                                      str(self.kwargs[keys][0]).ljust(40), str(self.kwargs[keys][1]).ljust(14)))
                if int(self.kwargs[keys][3]) > 0:
                    if not print_now:
                        self.kwargs[keys][3] = str(int(self.kwargs[keys][3]) - 1)
        return self.kwargs

    def total(self, get_list, index):
        """
        :param get_list: 购物车列表
        :param index: 商品价格在字典列表的索引位置
        :return: 总金额
        """
        self.totalMoney = 0
        if type(get_list) == list:
            if index and str(index).isdigit():
                self.index = int(index)
            for money in get_list:
                self.totalMoney += int(self.kwargs[money][index])
            return self.totalMoney

    def login_status(self, user_name):
        self.user = user_name
        if str(self.user) != str(None) and self.user:
            return self.user
        else:
            return False


def help_doc():
    os.system('clear')
    print('''购物指南
    购买单件    输入对应商品编号即可
        例如: 商品编号 1,输入 1 即可购买该商品
    购买多件    以英文,或空格将商品编号隔开即可
        例如:
            商品编号 1
            商品编号 2
            商品编号 3
        购买时,输入 1 2 3  或者 001,002,003  注意,是英文字符 , 逗号.
        也可以使用 1*3 注意,中间没有空格,这样就一次性购买了三件1号商品
    修改购物车   目前只做到每次只能删除一件商品,后续会增加多件删除功能
                退出修改使用  b 或者 back
        ...
    ''')
    return True


def check_map_list(first, second):
    """
    :param first: 第一个作为参考列表
    :param second: 第二个用户输入内容
    :return: 如果全部匹配则返回匹配的列表
    """
    match_list = []
    new_list = []
    if (type(first) or type(second)) != list:
        return False
    try:
        for index in range(len(second)):
            item = second[index]
            temp_list = str(item).split("*")
            if len(temp_list) == 2 and not temp_list.count(""):
                new_list.extend(str("%s " % temp_list[0] * int(temp_list[1])).split())
            else:
                new_list.append(item)
    except ValueError:
        return False
    second = new_list
    for item in second:
        for value in first:
            if item == value or str(int(value)) == item:
                match_list.append(value)
                break
    if len(second) != len(match_list):
        return False
    return match_list


def check_list_intersection(first, second):
    """
    :param first: 第一个父列表
    :param second: 第二个子列表
    :return: 返回差集列表
    """
    new_list = []
    if (type(first) or type(second)) != list:
        return False
    if not len(first) >= len(second):
        first, second = second, first
    for item in first:
        if item in second:
            second.remove(item)
            new_list.append(item)
    if len(second) == 0:
        for index in new_list:
            for item in first:
                if index == item:
                    first.remove(item)
                    break
        return first
    else:
        return False


def shop_cart(quit_cart, cart_list, shop_db, user_name=None):
    while not quit_cart:
        global shop_cart_list
        print("""结算(1)  继续购买(2)  清空购物车(3)  修改购物车(4)
        返回(b)  退出(q)
        """)
        wait_choose = str(input("请选择操作:"))
        if wait_choose == "1":
            if not user_name:
                print("您当前未登陆,请您先登陆,再进入购物车结算 ...")
                break
            get_total_money = Shopping(**shop_db).total(cart_list, 1)
            print(get_total_money)
        elif wait_choose == "3":
            shop_cart_list = []
            print("购物车已清空,请您重新选择")
            break
        elif wait_choose == "4":
            choose = str(input('请选择要移除的商品编号:')).strip()
            choose_list = re.split(',+|\s+', choose)  # 设置分割符,方便用户多选择操作,将用户输入以分隔符提取出来放在一个列表内
            get_match_list = check_map_list(cart_list, choose_list)
            if get_match_list:
                goods_num = len(get_match_list)
                shop_cart_list = check_list_intersection(cart_list, get_match_list)
                if shop_cart_list:
                    print("您已移除[%s]件商品" % goods_num)
            else:
                print("操作有误 !!!")
        elif wait_choose.lower() in ["2", "b", "back"]:
            break
        elif wait_choose.lower() in ["q", "quit"]:
            quit_cart = True
            print("谢谢使用,再见 !")
            break
        else:
            print("操作有误 !!!")
    return quit_cart

shop_cart_list = []  # 定义全局变量,购物车


def shop_mall(quit_atm):  # 商城购物中心
    new_goods = goods  # 新建一个字典变量
    new_shopping = Shopping  # 新建一个对象
    os.system('clear')
    get_user = None
    global shop_cart_list
    while not quit_atm:
        try:
            user_database = user_info["shop_account"]
        except KeyError:
            user_info["shop_account"] = {}
            user_database = user_info["shop_account"]
        new_shopping(**new_goods).goods_menu(get_user)  # 获取商品的编号列表,第一个参数为显示的编号顺序,不填则默认为1,第二个是一个字典类型数据
        menu_list = list(new_goods.keys())  # 获取商品编号
        choose = str(input('请选择:')).strip()
        choose_list = re.split(',+|\s+', choose)  # 设置分割符,方便用户多选择操作,将用户输入以分隔符提取出来放在一个列表内
        get_match_list = check_map_list(menu_list, choose_list)
        if get_match_list:
            print("添加[%s]件商品到购物车成功" % len(get_match_list))
            shop_cart_list.extend(get_match_list)
            get_new_goods = new_shopping(**new_goods).shop_list(shop_cart_list, print_now=False)
            if get_new_goods:
                update_info(get_new_goods, file_path='./config/goods.py', name="goods = ")
        elif choose.lower() == "s":
            if shop_cart_list:
                new_shopping(**new_goods).shop_list(shop_cart_list)
                quit_atm = shop_cart(quit_atm, shop_cart_list, new_goods, user_name=get_user)
            else:
                print("您的购物车什么也没有哦 ...")
        elif choose.lower() in ['l', 'login', ]:  # 登陆检查
            get_user = auth_account(user_database, log_file=bank_log_file)
            if get_user:
                new_shopping(**new_goods).login_status(get_user)
        elif choose.lower() in ['r', 'register', ]:  # 注册检查
            get_database = register_account(user_database, log_file=bank_log_file, is_shop_user=True)
            if type(get_database) == dict:
                user_info["shop_account"] = get_database
                update_info(user_info)
                print("用户注册成功")
        elif choose.lower() in ['h', 'help', ]:  # 帮助
            help_doc()
        elif str(choose).lower() in ['q', 'quit', ]:
            quit_atm = True
            print("谢谢使用,再见 !")
            break
        elif str(choose).lower() in ['b', 'back', ]:
            break
        else:
            print("操作有误 !!!")
    return quit_atm
