#!/usr/bin/env python3
# encoding:utf8
'''
Created on 2016年1月9日
@author: zengchunyun
'''

def loginCheck(fb):  # 传入一个密码文件
    from getpass import getpass
    global loginStatus, loginNow, user, pwd, userCart  # 设置全局变量
    retryCount = 0
    os.system('clear')
    while retryCount < 3:
        temp = user
        user = str(input('请输入用户名:')).strip()
        pwd = str(getpass('请输入密码:')).strip()
        if Login(fb).login(user=user, pwd=pwd):  # 调用login方法检查输入的用户
            os.system('clear')
            print('欢迎 %s 回来' % user)
            if str(user) == 'admin':
                user = temp  # 如果是管理员登陆,则把用户名改回普通用户
            elif temp:  # 当用户之前没有登陆时,不执行清空操作
                userCart = []  # 初始化用户的购物车, 如果切换账号登陆,将不保留购物车商品
            if str(user) == str(None):  # 当用户登陆时,修改状态,防止在使用管理员登陆时,也显示已登陆
                loginStatus = (False, user)
            else:
                loginStatus = (True, user)  # 将该对象传给shopping类的menu方法,用于标记当前登陆信息
            loginNow = True  # 用于标记是否登陆
            return True
        else:
            loginStatus = False
            loginNow = False
        retryCount += 1
    else:
        return False

def registerCheck(fb):  # 传入一个密码文件
    from getpass import getpass
    global loginStatus, loginNow, user, pwd
    retryCount = 0
    os.system('clear')
    while retryCount < 3:
        user = str(input('用户名:'))
        pwd = str(getpass('请设置密码:'))
        rePwd = str(getpass('请确认密码:'))
        if pwd == rePwd:
            if Login(fb).register(user=user, pwd=pwd):
                os.system('clear')
                print('注册成功')
                loginStatus = (True, user)
                loginNow = True
                return True
            elif user:
                print('用户已存在,如果忘记密码,请联系管理员找回')
        else:
            print('两次输入密码不一致,请重新输入')
        retryCount += 1
    else:
        return False

def helpDoc():
    os.system('clear')
    print('''购物指南
    购买单件    输入对应商品编号即可
        例如: 商品编号 1,输入 1 即可购买该商品
    购买多件    以英文,或一个空格将商品编号隔开即可
        例如:
            商品编号 1
            商品编号 2
            商品编号 3
        购买时,输入 1 2 3  或者 1,2,3  注意,是英文字符 , 逗号.
        不能重复购买某件商品 可以使用
    修改购物车   目前只做到每次只能删除一件商品,后续会增加多件删除功能
                退出修改使用  b 或者 back
        ...
    '''
    )
    return True

def adminManagement(fb, user, cash):  # 传入密码文件,用户名,对应需要充值的用户金额
    lines = open(fb, 'r').readlines()
    fileLen = len(lines)
    for info in range(fileLen):
        if user in lines[info]:
            tempList = lines[info].split()
            if len(tempList) > 2:
                if str(tempList[2]).isdigit() and str(cash).isdigit():
                    cash = int(tempList[2]) + int(cash)
                lines[info] = lines[info].replace(tempList[2], str(cash))
            else:
                tempList.append(cash)
                result = ' '.join(tempList)
                lines[info] = '%s\n' % result
    open(fb, 'w').writelines(lines)


def payCash(fb, user, money):
    getMoney = open(fb, 'r').readlines()
    fileLen = len(getMoney)
    for cash in range(fileLen):
        if user in getMoney[cash]:
            tempList = getMoney[cash].split()
            if len(tempList) > 2:
                if int(tempList[2]) >= int(money):
                    money = int(tempList[2]) - int(money)
                    print('当前剩余金额: %s' % money)
                    getMoney[cash] = getMoney[cash].replace(tempList[2],str(money))
                    open(fb, 'w').writelines(getMoney)
                    return True
                else:
                    return False
            else:
                os.system('clear')
                print('请联系财务为您充值 !!!')
                return False




if __name__ == '__main__':
    import goods
    from login.login import Login
    from shopping.shopping import Shopping
    import re
    import os
    import time
    newGoods = goods.goods  # 新建一个字典变量
    newShopping = Shopping  # 新建一个对象
    quitShopping = False  # 设置退出条件
    userCart = []  # 初始化用户的购物车
    chooseList = []  # 初始化一个用户选择购物的列表
    dbFile = 'account.db'
    user = None  # 初始化一个用户名变量,作为全局变量使用
    loginStatus = False  # 设置用户登陆状态,
    goCart = False
    flag = False
    loginNow = False  # 登陆标记
    os.system('clear')

    while not quitShopping:
        newShopping(1, **newGoods).goodsMenu(loginStatus)  # 获取商品的编号列表,第一个参数为显示的编号顺序,不填则默认为1,第二个是一个字典类型数据
        menuList = newShopping(**newGoods).getList()  # 获取键列表
        choose = str(input('请选择:')).strip()
        chooseList = re.split(',|\ |\n', choose)  # 设置分割符,方便截取用户多选择操作,将用户输入以分隔符提取出来放在一个列表内
        for check in range(len(chooseList)):
            if Shopping(chooseList[check]).checkInput(menuList):  # 检查用户输入
                userCart.append(menuList[int(chooseList[check]) - 1])  # 存储用户输入的商品编号,并映射到对应商品的KEY值
                goCart = True
            elif choose.lower() in ['l', 'login', ]:  # 登陆检查
                loginCheck(dbFile)
                if len(userCart) == 0:
                    goCart = False  # 当切换用户时,如果购物车是空的,则不进入结算环节
                break
            elif choose.lower() in ['r', 'register', ]:  # 注册检查
                registerCheck(dbFile)
            elif choose.lower() in ['q', 'quit', 'exit', ]:  # 退出
                quitShopping = True
                goCart = False
                print('\n谢谢使用,再见 !!!')
                break
            elif choose.lower() in ['h', 'help', ]:  # 帮助
                helpDoc()
            elif choose.lower() in ['s', 'shop', ]:
                if Shopping(**newGoods).shopList(userCart):  #  打印购物车列表内容
                    quitCart = False
                    while not quitCart:
                        getOrder = input('是否修改购物车清单(y/n): ')
                        if str(getOrder).lower() in ['y', 'yes', ]:
                            while not quitCart:
                                os.system('clear')
                                Shopping(**newGoods).shopList(userCart)
                                if len(userCart) == 0:  # 当购物车清空,返回主菜单
                                    quitCart = True
                                    goCart = False
                                    break
                                getOrderNum = str(input('请输入需要取消订单的对应商品编号:')).strip()
                                chooseList = re.split(',|\ |\n', getOrderNum)
                                for check in range(len(chooseList)):
                                    if Shopping(chooseList[check]).checkInput(userCart):
                                        userCart.remove(userCart[int(chooseList[check]) - 1])  # 将用户的选择输入移除
                                    elif getOrderNum.lower() in ['b', 'back', ]:  # 返回主菜单
                                        quitCart = True
                                        break
                                    else:
                                        print('输入错误 !!!')
                        elif str(getOrder).lower() in ['n', 'no', ]:
                            quitCart = True
                            break
                        else:
                            print('输入错误 !!!')
                else:
                    os.system('clear')
                    print('您的购物车是空的哟,快去买点东西吧 !!!\n')
            elif choose.lower() == 'console':
                if loginCheck('ca.db'):
                    while True:
                        getUser = input('请输入需要操作的用户名: ')
                        if not Login(dbFile).checkUser(getUser) and getUser:  # 判断用户输入是否正确
                            chargeCash = input('请输入充值金额: ')
                            if str(chargeCash).isdigit():  # 判断用户输入是否为数字
                                adminManagement(dbFile, getUser, chargeCash)
                            else:
                                print('输入错误,请谨慎操作用户数据 !!!')
                        elif str(getUser).lower() == 'back':
                            os.system('clear')
                            break
                        elif str(getUser).lower() == 'exit':
                            print('\n谢谢使用,再见 !!!')
                            quitShopping = True
                            goCart = False
                            break
                        else:
                            print('输入错误,请谨慎操作用户数据 !!!')
            else:
                os.system('clear')
                print('输入错误!!!')
                goCart = False
                break
        while goCart:
            choose = str(input('是否继续购买y/n:')).strip()
            if choose.isalpha():
                if str(choose).lower() in ['y', 'yes', ]:
                    os.system('clear')
                    break
                if str(choose).lower() in ['n', 'no', ]:
                    if not loginNow:
                        print('您必须先登陆账号才能进行结算操作')
                        time.sleep(2)
                        if loginCheck(dbFile):
                            os.system('clear')
                    money = newShopping(**newGoods).total(userCart, 1)
                    if payCash(dbFile, user, money):
                        os.system('clear')
                        print('总共需要支付:%s元' % money)
                        print('您的订单已提交,我们将尽快安排为您派送订单 ...')
                        goCart = False
                        break
                    else:
                        os.system('clear')
                        print('钱不够')
                        break
