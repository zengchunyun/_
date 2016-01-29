#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年1月29日
@author: zengchunyun
"""


def get_all_brackets(*string):  # 获取传入字符串外层括号内的所有字符
    if string:
        find_brackets = re.search('\(.*[\d|\+|\-|*|/|%].*\)', string[0])
        if find_brackets:  # 如果输入的内容里找到带括号的
            return find_brackets.group()  # 获取所有带括号的元素


def get_brackets(*string):  # 获取传入字符串第一个内层括号内的所有字符
    if string:
        next_bracket = re.search('\([\s\d|\.|\+|\-|\*|/|%]*\)', string[0])  # 匹配第一组空格
        if next_bracket:
            return next_bracket.group()  # 返回第一组内容


def strip_add_sub(express):  # 专治各种刁钻运算符号
    while '++' in express or '--' in express or '+-' in express or '-+' in express:
            express = express.replace('--', '+')  # 同减为加
            express = express.replace('++', '+')  # 同加为加
            express = express.replace('+-', '-')  # 加减为减
            express = express.replace('-+', '-')  # 减加为减
    return express


def get_result(express):  # 每次只处理一个同级别的运算操作,级同一个括号内的,或者是一个没有括号的运算操作
    total = 0  # 初始化一个结果
    e_str = re.findall('[\d|\.]+\e\+[\d|\.]+', express)  # 匹配计算数值长度是否过大,
    if e_str:
        import json
        new_e_str = json.loads(e_str[0])
        if len(e_str[0]) == len(express):  # 匹配是否仅剩最后一个大数据
            return int(new_e_str)
        express = express.replace(str(e_str[0]), str(int(new_e_str)))  # 把长度很大的数转换为整形的字符串
    new_str = str(express).strip('(,)')  # 去除括号
    if not re.findall('[\*|/|%]+', new_str):  # 如果是纯加减运算
        new_str = strip_add_sub(new_str)  # 先去除特殊连续运算符号
        new_list = re.findall('[\+|\-]+[\d|\.]+|[\d|\.]+', new_str)  # 对字符串进行加减运算
        for value in new_list:
            total += float(value)
        return float(total).__round__(16)
    else:  # 对字符串进行乘除运算
        new_str = re.search('[\d|.]+\*\*[\d|\.]+', express)  # 优先匹配**
        if not new_str:
            new_str = re.search('[\d|\.]*[\*|/|%|\*\*|//]+[\-]*[\d|\.]+', express)  # 优先匹配的决定优先级高低
        if new_str:
            new_str = new_str.group()
            try:
                if len(new_str.split('**')) > 1:  # 处理幂运算
                    total = float(new_str.split('**')[0]) ** float(new_str.split('**')[1])
                elif len(new_str.split('//')) > 1:  # 处理地板除运算
                    total = float(new_str.split('//')[0]) // float(new_str.split('//')[1])
                elif len(new_str.split('/')) > 1:  # 处理整除运算
                    total = float(new_str.split('/')[0]) / float(new_str.split('/')[1])
                elif len(new_str.split('%')) > 1:  # 取模运算
                    total = float(new_str.split('%')[0]) % float(new_str.split('%')[1])
                elif len(new_str.split('*')) > 1:  # 乘法运算
                    total = float(new_str.split('*')[0]) * float(new_str.split('*')[1])
            except ZeroDivisionError:
                return '被除数不能为0'
            except OverflowError:
                return '计算数值超过程序计算范围'
            new_str = express.replace(new_str, str(total))
            return get_result(new_str)
        else:
            return express


def check_input(string):
    result = re.findall('\d|\s|\+|\-|\*|/|%|\(|\)|\.', string)
    if len(string) != len(result):  # 首先匹配合法字符长度是否与原字符相等
        return False
    result = re.findall('[a-zA-Z]|[\*|/]{3,}', string)  # 判断输入内容是否正确
    # 去除非法格式输入,例如 **1,(*6,2*,1+2(1+2),1+1+(),1+2*-4,具体注释参考README文档
    format_err = re.findall('[\(]+[\*|/|%]+\d+|'
                            '^[\*|/|%]+\d+|'
                            '\d[\.]*[\+|\-|\*|/|%]+$|'
                            '\d[\.]*[\+|\-|\*|/|%]+\)|'
                            '\d+\(|'
                            '\(\)|'
                            '[\*|/]{3,}|'
                            '[%]{2,}|'
                            '\)+\(+', string)
    left_count = str(string).count('(')  # 计算左边括号的个数
    right_count = str(string).count(')')  # 计算右边括号的个数
    if left_count != right_count or result or format_err:  # 当括号不成对,或有字母或非法格式出现,则返回False
        return False
    else:
        return True


def main(express):
    all_brackets = get_all_brackets(express)  # 获取所有的带括号里面的内容
    if all_brackets:  # 如果获取到的内容带括号
        next_bracket = get_brackets(all_brackets)  # 获取第一组括号的内容
    else:
        next_bracket = re.findall('.*', express)  # 如果没有输入括号的内容
        next_bracket = next_bracket[0]  # 取列表的第一个元素,即所有的内容
    result = get_result(next_bracket)  # 开始执行算术
    express = str(express).replace(str(next_bracket), str(result))  # 把每次的计算结果替换掉表达式内容
    if re.findall('[\+|\*|/|%]+', str(express)):  # 如果表达式里没有运算符了,则返回,负数除外
        return main(express)  # 返回最终结算结果
    return express  # 返回每一次递归后替换的结果

if __name__ == '__main__':
    import re
    quitCalc = False
    while not quitCalc:
        # string = "1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) )+(2- (-4*3)/ (16-3*2) )"
        string = str(input('请输入需要计算的内容:'))
        first_format = ''.join(string.split(' '))  # 先将用户输入的所有空格去除
        if check_input(first_format):  # 如果输入格式通过匹配规则,则进行数据处理
            result = main(first_format)  # 将格式化后的数据传入主函数模块处理
            if result:
                result = re.sub('[\.]+0+', '', result)  # 把结果小数点后是0的去掉
                print(result)  # 当结果不为假时,打印输出结果
        elif string.lower() in ['q', 'quit', ]:
            quitCalc = True
            print('谢谢使用, 再见 !!!')
            break
        else:
            print('输入错误 !!!')
