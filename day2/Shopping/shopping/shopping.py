#!/usr/bin/env python
# encoding:utf8
'''
Created on 2016年1月9日
@author: zengchunyun
'''
class Shopping(object):

    # 传人两个可选参数，第一个是元组类型，第二个是字典类型，
    def __init__(self, *args, **kwargs):
        if args:
            self.args = args
        else:
            self.args = (0,)
        self.kwargs = kwargs
        self.list = []
        self.start = 1  # 用于显示商品编号的初始值
        self.input = None
        self.index = 0  # 设置获取列表的下标起始位置
        self.totalMoney = 0  # 初始化购物总价
        self.status = False  # 设置登陆状态
        self.flag = False  # 设置登陆显示菜单标记

    def goodsMenu(self, *status):
        self.status = status
        print('欢迎光临中关村倒卖二手货市场'.center(40))
        if type(self.status) == tuple:
            self.status = self.status[0]
        if self.loginStatus():
            if len(self.status) == 2:
                self.status = '%s已登陆' % self.status[1]
            else:
                self.status = '已登陆'
        else:
            self.status = '未登陆'
            self.flag = True
        print('%s%28s\n' % ('请输入对应商品编号选择您需要购买的商品'.ljust(0),
                            self.status.center(24, '*'),
                          ))
        print('%4s%3s%s%s%s' % ('商品编号',
                                '商品名'.rjust(20),
                                '价格(RMB)'.rjust(25),
                                '好评'.rjust(5),
                                '库存'.rjust(5)))
        if self.checkInput() and type(self.kwargs) == dict:
            from collections import OrderedDict
            if self.args:
                self.start = int(self.args[0])

            for index, value in enumerate(OrderedDict(self.kwargs), self.start):
                print('%-10s %s %-5s %s %s' % (str(index).center(6),
                                               self.kwargs[str(value)][0],
                                               str(self.kwargs[str(value)][1]).rjust(8),
                                               str(self.kwargs[str(value)][2]).rjust(8),
                                               str(self.kwargs[str(value)][3]).rjust(6),
                                               ))
            if self.flag:
                print('\n%s%s%s%s%s' % ('帮助(h)'.ljust(10),
                                        '登陆(l)'.ljust(10),
                                        '注册(r)'.ljust(10),
                                        '购物车(s)'.ljust(10),
                                        '退出(q)'.ljust(10),
                                        ))
            else:
                print('\n%s%s%s%s' % ('帮助(h)'.ljust(10),
                                      str(self.status).ljust(10),
                                      '购物车(s)'.ljust(10),
                                      '退出(q)'.ljust(10),
                                      ))

    # 将字典的键生存一个列表
    def getList(self):  # 将第二个参数以列表的形式返回，参数类型必须是字典
        if type(self.kwargs) == dict:
            for keys in enumerate(self.kwargs.keys()):
                self.list.append(keys[1])
            return self.list

    def shopList(self, *args):
        if args:
            self.args = args[0]
            if type(self.args) == list and len(self.args) > 0:
                print('\n%s%s%5s' % ('商品编号'.center(12,'*'),
                                     '商品名称'.center(38,'*'),
                                     '价格'.center(10, '*'),
                                   ))
                for index, keys in enumerate(self.args):
                    print('%s%s%s' % (str(index + 1).center(15),
                                      str(self.kwargs[keys][0]).ljust(22),
                                      str(self.kwargs[keys][1]).rjust(15),
                                      ))
                return True
            else:
                return False

    def total(self, getList, index):  # 注意,这里传入的列表是字典的键生成,元素范围在self.getList方法内
        if type(getList) == list:
            if index and str(index).isdigit():
                self.index = int(index)
            for money in getList:
                self.totalMoney += int(self.kwargs[money][index])
            return self.totalMoney

    # 检查输入是否是数字，如果方法本身传入一个对象，那么会判断输入是否在该对象范围内,否则只判断输入是否为数字
    def checkInput(self, *getObj):
        self.input = self.args
        if str(self.input[0]).isdigit():
            if getObj:
                if not (int(self.input[0]) - 1) in range(len(getObj[0])):
                    return False
            return True  # 如果用户输入有效,则返回True
        else:
            return False

    def loginStatus(self, *status):
        if status:  # 如果传了状态值,类型为tuple
            self.status = status[0]  # 将下标为0的值取出来
            if str(self.status) == str(True):
                return True  # 如果为真,说明用户已登陆
            else:
                return False
        elif self.status:  # 如过self.status本身有值
            if str(self.status[0]) == str(True):  # 将下标为0的值取出来
                return True  # 如果为真,说明用户已登陆
            else:
                return False
        else:
            return False
