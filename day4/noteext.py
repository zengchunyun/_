#!/usr/bin/env python
# coding:utf-8
"""
Created on 2016年1月9日
@author: zengchunyun
"""



# print(type(len('kkk')).mro())

# number = iter(1,2,3)
# print(number)

#
# class C(object):
#             @property
#             def x(self):
#                 "I am the 'x' property."
#                 return self._x
#
#             @x.setter
#             def x(self, value):
#                 self._x = value
#
#             @x.deleter
#             def x(self):
#                 del self._x
#
# C().x()

# names = iter(['zeng', 'chun', 'yun'])
# print(names)
# print(names.__next__())
# print(names.__next__())
# print(names.__next__())
# print(names.__next__())
#



# a = float(1)
# b = float(2)
# c = a + b
#
# print(c)


# def func():
#     print('hello')
#
# print(func)
# print(type(func))
# func()
# print(func())
# print(type(func()))
#
# def wrapper(func):
#     def inner():
#         print(func)  # 输出是一个函数对象
#         func()  # 这里实际是执行我们这个例子中原先定义的index函数对象的函数体
#     return inner
#     # print(func)  # 打印参数
#     # return func  # 返回参数 ,现在注释掉这个返回值
#
#
# @wrapper  # 使用装饰器
# def index():
#     print('welcome')
#
# print(type(index))  # 加上一句输出类型代码的语句
# index()

# 首先看看这种情况
# 代码执行到index()时,啥也没有,我们明明打印了一句welcome,为什么买药输出信息,这也就再次证明了,
# 实质是这个index已经等价于装饰器的inner这个函数了,因为装饰器返回的是inner这个函数对象
# 我们既想用装饰器,又想执行调用装饰器的内部代码时怎么办呢?
# 我们已经知道,装饰器会携带一个参数,这个参数是引用装饰器对象的一个函数对象
# 既然是一个函数对象,那我们是不是可以直接执行这个函数对象呢?
# 答案是肯定的,所以我们直接在这个执行这个函数对象,等于就是执行我们原先拿个函数的函数体
# 这个例子就满足了我们的需求,当我们不调用index函数时,得到的仅仅是一个函数对象,并不会执行函数体代码

# 执行顺序是,解释器从上往下读取代码
# 遇到函数时,只加载定义的函数对象,并不执行函数体代码
# 然后遇到装饰器@wrapper时
# 解释器会跳到这个wrapper函数
# 然后执行这个wrapper函数内部代码
# 我们通过观察得知,这个wrapper函数一定会传入一个参数,因为测试发现,不传入一个参数,程序执行会抛出需要一个参数的异常错误.
# 通过分析这个参数,发现这个参数打印结果是一个函数对象
# 然后wrapper函数体代码执行完毕后,继续往下执行,遇到函数index,
# 也是只是加载这个函数对象,并不执行内部函数体代码
# 当遇到代码index()时,结合到我们之前积累的函数基础知识,
# 这个写法实际是开始执行一个函数,所以解释器会跳到指定的index函数对象
# 然后开始执行这个函数体代码块,
# 整个执行过程就结束了

# 首先解释器还是从上往下读取代码
# 遇到函数时,只加载定义的函数对象,并不执行函数体代码
# 然后遇到装饰器@wrapper时
# 解释器会跳到这个wrapper函数
# 然后执行这个wrapper函数内部代码
# 通过分析这个参数,发现这个参数打印结果是一个函数对象
# 然后wrapper函数体代码执行完毕后,继续往下执行,遇到函数index,
# 也是只是加载这个函数对象,并不执行内部函数体代码
# 关键点来了
# 代码执行到打印对象类型的语句时,结果却是一个NoneType的类型,根据我们之前对函数的基本介绍,这里的类型应该是一个函数类型才对啊
# 怎么回事呢?我们明明定义了index函数,怎么打印的类型却是NoneType类型?
# 我们之前也看到只有函数没有返回值时,函数默认会返回一个None对象,故而这个对象的类型也就是NoneType类型了,
# 我们仅仅只是加了一个装饰器代码@wrapper,其他都没有变,为什么会出现这个情况呢
# 我们上一个例子已经说明,这个装饰器会携带一个参数,这个参数为一个函数对象,
# 实际上,这个时候这个装饰器会对引用装饰器的函数,也就是我们这里的index函数进行重构,
# 所以如果我们如果不返回一个函数对象时,那么这个时候的index实质是一个普通的对象,不是函数类型了
# 它已经被赋予None这个值了,而None不是一个函数对象,所以就没有调用方法,就不能以括号方式执行
# 这时解释器读到index()这句代码,大家依据之前的理念,都能看出这个是去执行index这个函数内部代码块的语句
# 但是这个时候,解释器却在这个时候抛出异常了
# 返回类型错误,TypeError: 'NoneType' object is not callable
# 这个错误说我们的index执行后,是不能被调用的,只有对象类型为函数才有内置调用方法
# 因为这个index已经被重构,返回值已经变成了None,也就是说,index 对象目前仅仅是一个普通标识符,不是函数


# 无参装饰器,有参函数
# def wrapper(func):
#     def inner(name):  # 这个参数最终会传给这个函数体内部需要调用参数的对象
#         func(name)  # 这个参数个数是由原来的函数,也就是我们这里的index函数决定参数个数的
#     return inner
#
#
# @wrapper  # 使用装饰器
# def index(name):  # 传入一个参数
#     print('welcome %s' % name)
#
# index('zengchunyun')
#
#
# # 无参装饰器,多参函数
# def wrapper(func):
#     def inner(*args):  # 使用动态参数
#         func(*args)
#     return inner
#
#
# @wrapper  # 使用装饰器
# def index(*args):  # 传入一个参数
#     print('welcome %s' % ' '.join(args))
#
# index('zengchunyun', 'goodbye')
#
#
# # 无参装饰器,多参函数2
# def wrapper(func):
#     def inner(*args, **kwargs):  # 使用动态参数
#         func(*args, **kwargs)
#     return inner
#
#
# @wrapper  # 使用装饰器
# def index(*args, **kwargs):  # 传入一个参数
#     print('welcome %s' % ' '.join(args))
#
# index('zengchunyun', 'goodbye')


# # 有参装饰器,多参函数2
# def one():
#     print('one')
#
#
# def two():
#     print('two')
#
#
# def func(arg1, arg2):
#     def wrapper(oldfunc):
#         def inner(*args, **kwargs):  # 使用动态参数
#             arg1()
#             arg2()
#             oldfunc(*args, **kwargs)
#         return inner
#     return wrapper
#
#
# @func(one, two)  # 使用装饰器
# def index(*args, **kwargs):  # 传入一个参数
#     print('welcome %s' % ' '.join(args))
#
# index('zengchunyun', 'goodbye')
#
# # 解释器遇到装饰器,由于这个装饰器是一个可执行函数
# # 故而先执行函数,再次就成了我们所认知的普通装饰器了

# a = 100
# while a > 0:
#         if a % 2 != 0:
#             if a % 3 != 0:
#                 if a % 5 != 0:
#                     if a % 7 != 0:
#                         print(a)
#                         11
#         else:
#             pass
#             # print(a,1111)
#         a -= 1
#
# 2**0            1  0   1
# 2**0            1  2   3
# 2**1            2  3   5
# 2**1            2  5   7
#
# 2**2            4  7   11
# 2**1            2  11  13
# 2**2            4  13  17
# 2**1            2  17  19
# 2**2            4  19  23
# 2**1 + 2**2     6  23  29
# 2**1            2  29  31
# 2**1 + 2**2     6  31  37
# 2**2            4  37  41
#
# # 1,3,5,7,9,
# # 11,13,17,19,
# # 23,29,
# # 31,37,39,
# # 41,43,47,
# # 53,59
#
#
# 1 3 5 7 9
# 1 3   7 9
#   3     9
# 1     7 9
# 1 3   7
#   3     9


# def func(num):
#     if num / 2 > 0:
#         num -= 1
#         print(num)
#         num = func(num)
#         print('quit')
#     return num
#
# func(10)


# def binary_search(data_list,find_num):
#     mid_pos = int(len(data_list) / 2)  # 计算需要查找数据的长度的一半
#     mid_val = data_list[mid_pos]  # 获取中间位置的那个值
#     print(data_list)  # 查看每次剩余筛选的数据列表
#     if len(data_list) > 0:  # 当列表长度大于0时,则一直查找
#         if mid_val > find_num:  # 如果中间的数比实际要查找的数大,那么这个数肯定在左边
#             print("%s should be in left of [%s]" % (find_num, mid_val))
#             binary_search(data_list[:mid_pos], find_num)
#         elif mid_val < find_num:  # 如果中间的数比实际查找的数小,那么这个数肯定在右边
#             print("%s should be in right of [%s]" % (find_num, mid_val))
#             binary_search(data_list[mid_pos:], find_num)
#         else:  # 如果中间数与实际查找的数恰巧相等,那么这个数肯定是要找的拿个数
#             print("Find %s" % find_num)
#
#     else:  # 否则就是买药这个数
#         print("cannot find [%s] in data_list" % find_num)
#
# if __name__ == '__main__':
#     primes = [1, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
#     binary_search(primes, 1)   # 在列表里面查找1


# array = [[col for col in range(4)] for row in range(4)]  # 初始化一个4*4数组
# # array=[[col for col in 'abcd'] for row in range(4)]
#
# for row in array:  # 旋转前先看看数组长啥样
#     print(row)
#
# for i, row in enumerate(array):
#
#     for index in range(i, len(row)):
#         tmp = array[index][i]  # 将每一列数据在每一次遍历前,临时存储
#         array[index][i] = array[i][index]  # 将每一次遍历行的值,赋值给交叉的列
#         print(tmp, array[i][index])  # = tmp
#         array[i][index] = tmp  # 将之前保存的交叉列的值,赋值给交叉行的对应值
#     for r in array:  # 打印每次交换后的值
#         print(r)

