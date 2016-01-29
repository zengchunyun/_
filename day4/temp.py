#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年1月9日
@author: zengchunyun
"""
    # operational = ['+', '-', '*', '/', '%', ]
    # express = "1 - 2 * ( (60-30 +(-40/5*1) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )"
    # # filter_value = re.findall('\d+|\W', express)
    # # print(filter_value)
    # # filter_value = re.findall('\(.*[\d|\+|\-|\*|\/]*\)', express)
    # filter_value = re.search('\(.*[\d|\+|\-|/]*\)', express)
    # first_filter = filter_value.group()
    # print(first_filter)
    # filter_value = re.search('\([\s\d|\+|\-|\*|/]*\)', first_filter)  # 匹配第一次内括号
    # first_calc = filter_value.group()
    # print(first_calc)
    # one = re.split('[\+|\-|\(|\)]', first_calc)
    # print(one)
    # one = re.findall('\d+|\W', first_calc)
    # print(one)
    # if '/' in one:
    #     index = one.index('/')
    #     left = one[:index]
    #     right = one[index+1:]
    #     print(left)
    #     print(right)
    #     if '*' in right:
    #         pass
    # elif '/' in one:
    #     print(one.index('/'))
    # aa = re.search('.*[/|\*]', first_calc)
    # print(aa.group())
    # filter_value = re.split('[\+|\-|\*|\/]', first_filter,maxsplit=3)
    # filter_left_brackets = filter_value.count('(')
    # filter_right_brackets = filter_value.count(')')
    # print(filter_left_brackets)
    # print(filter_right_brackets)
    # print(filter_value.group())

    # print(Calculator().addition(1, 2))
    # print(Calculator().subtraction(1, 2))
    # print(Calculator().multiplication(1, 2))
    # print(Calculator().division('1', 2))
    # main()

# 输入分析处理
# 统计有多少对括号
# 定位括号位置
# 统计各个运算符个数
# 定位运算符位置
#
# #
# import json
# a = "9.933574043664715e+44"
# m = json.loads(a)
# print(int(m))
# print(type(m))


# a = '1adsd1fdfd,3,asa1'
# # print(a.split('1',2))
# a = [1,2]
# x,y = a
# print(x)
# print(y)
import re
express='1-2*((60-30+(-40/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
oo = re.sub("\([^()]+\)", '-8.0', express)
print(oo)