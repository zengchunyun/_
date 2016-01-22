#!/usr/bin/env python
# encoding:utf8
"""
Created on 2016年1月9日
@author: zengchunyun
"""


class HAproxy(object):

    def __init__(self, fb, ):
        import re
        self.re_match = re.compile('\w+.*$')
        self.re_match_line = re.compile('^\w+.*$')  # 针对行查找非空白特殊字符
        self.file = fb  # 传入一个文件
        self.args = None
        self.file_list = []  # 将文件读出后存入的列表
        self.main_list = []  # 将文件第一列的非空行开头内容写入这个列表
        self.add_list = []
        self.ref_list = []  # 用于参照排序的列表
        self.new_dict = {}  # 存储更新后的文件字典数据
        self.flag = False  # 设置标志位,用于辅助判断条件用

    def format_write(self, *ref_list, **new_dict):
        self.ref_list = list(ref_list)
        self.new_dict = new_dict
        temp_keys = list(self.new_dict.keys())
        deff_keys = set(self.ref_list).symmetric_difference(temp_keys)
        with open(self.file, 'w') as wr:
            wr.seek(0)
            if deff_keys:  # 对比是否新增键,如果新增,则对键进行排序插入
                for value in self.ref_list:
                    first_half_key = str(list(deff_keys)[0]).split()[0]
                    if first_half_key in value:
                        self.ref_list.insert(self.ref_list.index(value), list(deff_keys)[0])
                        break
            for key in self.ref_list:  # 参照列表的元素顺序进行读取字典内容
                if self.new_dict.get(key):  # 如果字典存在这个键才进行操作
                    wr.write('%s\n' % key)  # 先写入文件的第一列内容,在对第一列下面的内容进行判断格式化
                    if type(self.new_dict[key]) == list:  # 首先获取的值必须是列表形式才行
                        if self.new_dict[key].count(''):  # 这里是针对有空行的文件进行排序处理
                            for index in range(self.new_dict[key].count('')):  # 把有空行的移到后面
                                self.new_dict[key].remove('')
                                self.new_dict[key].append('')
                        for value in self.new_dict[key]:  # 开始写入字典值到文件
                            wr.write(str('\t%s\n' % ''.join(value)).expandtabs(8))  # 以8个空格为一个TAB键宽度写入

    def main_conf(self):  # 以列表形式返回配置的第一列内容
        self.main_list = []  # 新建一个空列表
        with open(self.file, 'r') as get_main_conf:
            get_list = get_main_conf.readlines()
            get_length = len(get_list)
            for index in range(get_length):
                result = self.re_match.match(get_list[index])  # 只匹配非空格,空行开头的内容
                if result:
                    self.main_list.append(result.group())  # 将取到的内容追加到列表
        return self.main_list  # 返回一个列表

    def format_dict(self, *args):  # 可以选择性的将所要获取的字段传入,如果不传入参数,将打印整个文本成字典返回
        if args:
            if type(args[0]) == list:  # 如果第一个参数为列表,则self.args 等于args[0],即第一个参数
                self.args = args[0]
            elif len(args) > 0:
                self.args = list(args)  # 如果该属性有参数,self.args就会被转换成列表
            self.main_list = self.args
        elif self.args:
                if type(self.args) != list:
                    self.args = list(self.args)  # 如果self.args有值,最终也会变成列表
                self.main_list = self.args
        else:
            self.main_list = self.main_conf()  # 如果既没有传参数,也没有给self.args赋值,那么就会使用默认列表
        from collections import defaultdict
        get_dict = defaultdict(list)  # 新建字典,默认字典键值为list
        with open(self.file, 'r+') as format_content:
            get_list = format_content.readlines()  # 将文本转换为列表
            get_length = len(get_list)  # 获取文本行数
            for key in self.main_list:
                for index in range(get_length):
                    result = self.re_match_line.match(get_list[index])  # 只匹配非空行,空格开头内容
                    if result:
                        if result.group() == key:
                            self.flag = True
                            get_list[index] = ''
                    if self.flag and get_list[index]:
                        if result and result.group() != key:  # 只匹配行与得到的列表元素相同的内容
                            self.flag = False
                            break
                        else:
                            get_dict[key].append(get_list[index].strip())  # 将以空行,空格内容追加到键对应值的列表
        return get_dict  # 返回一个字典
