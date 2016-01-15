#!/usr/bin/env python3

import search
import os

class GetInfo(object):
    # 传人两个可选参数，第一个是元组类型，第二个是字典类型，
    def __init__(self,*args,**kwargs):  
        if args:
            self.args = args
        else:
            self.args = (0,)
        self.kwargs = kwargs
        self.list = []      
    # 打印字典的索引和值
    def getMenu(self,*args):    # 根据用户的传人的第一个参数按指定起始位置排序，并将第二个参数打印出来
        print('请输入对应的序号获取需要查找的内容\n退出请按q\n')
        if self.checkInput() and type(self.kwargs) == dict:
            from collections import OrderedDict  
            if self.args:
                self.start = int(self.args[0])
            else:
                self.start = 1
            for index,value in enumerate(OrderedDict(self.kwargs),self.start):
                print(index,value)
        if not self.kwargs:
            self.kwargs = args
            if  self.checkInput():
                if self.args:
                    self.start = int(self.args[0])
                else:
                    self.start = 1
                for index,value in enumerate(self.kwargs[0],self.start):
                    print(index,value)
    # 将字典的键生存一个列表        
    def getList(self):  #将第二个参数以列表的形式返回，参数类型必须是字典
        if type(self.kwargs) == dict:
            for index,keys in enumerate(self.kwargs):
                self.list.append(keys)
            return self.list
        
    def showList(self,obj): # 传入混合型的非字典类型与字典类型的列表，返回内嵌字典的键与非字典元素组合的新列表
        self.kwargs = obj
        if type(self.kwargs) == list:
            if len(self.kwargs) > 0:
                for index in range(len(self.kwargs)):
                    if type(self.kwargs[index]) == dict:
                        for key,value in self.kwargs[index].items():
                            self.list.append(key)
                    if type(self.kwargs[index]) == str:
                        self.list.append(self.kwargs[index])
                return self.list
        
    # 检查输入是否是数字，如果方法本身传入一个对象，那么会判断输入是否在该对象范围内
    def checkInput(self,*getObj):
        self.input = self.args
        if str(self.input[0]).isdigit():
            if getObj:
                if not (int(self.input[0]) - 1) in range(len(getObj[0])):
                    return False                
            return True
        else:
            return False

china = search.arrCity # 将字典数据赋值给新变量china
getInfo = GetInfo # 新建一个对象，并将对象赋值给getInfo
quitSearch = True   # 设置退出条件

os.system('clear')  # 清空屏幕内容
while quitSearch:   #当不是退出操作时，则一直循环
    getInfo(1,**china).getMenu()   # 显示一级菜单
    getInput = input('\n请选择：')
    if getInfo(getInput).checkInput(getInfo(**china).getList()): # 传入用户输入，并将一个列表传入，判断输入是否在对象范围内
        os.system('clear')
        secondIndex = getInfo(**china).getList()[int(getInput) - 1]  # 获取用户输入所对应的键      
        while quitSearch:
            getInfo(1,**china[secondIndex]).getMenu() #显示二级菜单
            print('\n返回（b）')
            getInput = input('请选择：')
            if getInfo(getInput).checkInput(getInfo(**china[secondIndex]).getList()): # 传入用户输入，并将一个列表传入，判断输入是否在对象范围内
                os.system('clear')
                threeIndex = getInfo(**china[secondIndex]).getList()[int(getInput) - 1] # 获取用户输入所对应的键 
                threeDict = china[secondIndex][threeIndex]  
                newList = getInfo().showList(threeDict)  #传入一个对象，可能是字典，也可能是列表，最终返回一个列表
                while quitSearch:                    
                    getInfo(1).getMenu(newList)  # 显示三级菜单
                    print('\n返回（b）')
                    getInput = input('请选择：')
                    if str(getInput) == 'b':  # 输入b返回
                        os.system('clear')
                        break
                    elif str(getInput) == 'q':  # 输入q退出
                        quitSearch = False
                        print('谢谢使用，再见')
                        break
                    else:
                        os.system('clear')
                        print('输入错误！！！')
            elif str(getInput) == 'b':
                os.system('clear')
                break
            elif str(getInput) == 'q':
                quitSearch = False
                print('谢谢使用，再见')
                break
            else:
                os.system('clear')
                print('输入错误！！！')
    elif str(getInput) == 'b':
        os.system('clear')
        break
    elif str(getInput) == 'q':
        quitSearch = False
        print('谢谢使用，再见')
        break
    else:
        os.system('clear')
        print('输入错误！！！')