#!/usr/bin/env python3
# encoding:utf8

import city     # 导入查询的数据
from collections import OrderedDict     # 导入有序词典模块
import os   # 导入系统模块。待会会用到该模块的清除当前屏幕的一个函数功能

china = city.china      # 将字典赋值给一个新的变量，简化后面的调用
exitSearch = False   # 定义退出查询的条件
os.system('clear')  # 清除屏幕内容

while not exitSearch:  # 当条件不为真时，也就是说，只要exitSearch一直为假，则程序始终循环，为真时，则停止循环
    print('++++++++++++++++++++请选择要查询的区域++++++++++++++++++++\n++++++++++++++++++++++退出请按++quit++++++++++++++++++++++\n|')
    firstIndex = []  # 新建一个列表，用来存储一级菜单的键值
    for index, keys in enumerate(OrderedDict(china), 1):    # 使用排序字典并打印键值下标
        print('|%20s    %-28s|' % (int(index), keys))       # 打印一级菜单,将下标加1方便用户查看习惯
        firstIndex.append(keys)     # 将一级字典键值追加到firstIndex列表，为使用索引方式查询数据提供方便
    nextMenu = input('|\n+++++请选择区域：').strip()    # 获取用户需要查询的列表下标
    if nextMenu.lower() in ('q', 'quit', 'e', 'exit'):  # 判断用户是否要退出查询
        print('\n谢谢使用！再见 ...')
        exitSearch = True       # 当该变量为True时，程序将终止循环
        break
    elif nextMenu.isdigit():    # 判断用户输入的是否是数字
        if int(nextMenu) - 1 in range(len(china)):  # 判断用户输入是否正确,只有输入的下标在显示的索引范围内则为有效输入
            os.system('clear')  # 清除屏幕内容
            secondMenu = china[firstIndex[int(nextMenu) - 1]]    # 通过用户提供的列表下标先将列表的下标对应的值找到，并当成字典的键值，赋值给secondMenu
            searchCity = firstIndex[int(nextMenu) - 1]  # 通过用户输入的下标，找到对应的区域，然后在二级菜单中提示用户该城市的属于哪块区域的
            while not exitSearch:   # 当不是退出，则一直循环
                print('+++++++++++++++++%s++++包含以下城市+++++++++++++++++\n++++++++++++++++++++++退出请按++quit++++++++++++++++++++++\n|' % searchCity)
                secondIndex = []  # 新建一个列表，用来存储二级菜单的键值
                for index, keys in enumerate(secondMenu, 1):    # 迭代方式打印用户的二级菜单
                    print('|%20s    %-28s' % (int(index), keys))   # 打印序列号和字典键值
                    secondIndex.append(keys)    # 将二级菜单的键值追加到secondIndex列表，为使用索引查询数据提供方便
                nextMenu = input('|\n+++++++++++++++++返回上一级菜单请按++back+++++++++++++++++\n+++++请选择城市:').strip()    # 获取用户需要查询的列表下标
                if nextMenu.lower() in ('b', 'back'):    # 判断用户是否要返回上一级菜单
                    os.system('clear')  # 清除屏幕内容
                    break
                else:
                    if nextMenu.lower() in ('q', 'quit', 'e', 'exit'):     # 判断用户是否要退出查询
                        exitSearch = True
                        break
                    elif nextMenu.isdigit():
                        if int(nextMenu) - 1 in range(len(secondMenu)):
                            os.system('clear')  # 清除屏幕内容
                            print('+++++++++++++++++++%-2s++++包含以下地区+++++++++++++++++++\n++++++++++++++++++++++退出请按++quit++++++++++++++++++++++\n|' % (secondIndex[int(nextMenu) - 1]))
                            print(' '.join(secondMenu[secondIndex[int(nextMenu) - 1]]))     # 打印三级菜单
                            while not exitSearch:
                                nextMenu = input('|\n返回上级菜单请按back: ').strip()
                                if nextMenu.lower() in ('b', 'back'):    # 判断用户是否要返回上一级菜单
                                    os.system('clear')  # 清除屏幕内容
                                    break
                                elif nextMenu.lower() in ('q', 'quit', 'e', 'exit'):     # 判断用户是否要退出查询
                                    exitSearch = True
                                    break
                                else:
                                    print('输入错误！！！')
                        else:
                            os.system('clear')  # 清除屏幕内容
                            print('输入错误！！！')
                    else:
                        os.system('clear')  # 清除屏幕内容
                        print('输入错误！！！')
        else:
            os.system('clear')  # 清除屏幕内容
            print('输入错误！！！')
    else:
        os.system('clear')  # 清除屏幕内容
        print('输入错误！！！')
    if exitSearch:
        print('\n谢谢使用！再见 ...')
        break
