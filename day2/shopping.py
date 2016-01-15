#!/usr/bin/env python
# encoding:utf8
'''
Created on 2016年1月9日
@author: zengchunyun
'''
# name = 'hello'
# print("%s world" % name)
# print("{name} world".format(name = name))
#
# print(name + " world")
# print("{0} world".format(name))
#
# print("{0} world,{1}".format(name,"I like python"))
#


# 0 1 0
# 1 0 1
# 0 1 0
# num = 11
# print(bin(num))
# # rrr = num.__abs__()
# # rrr = num.__add__(999)
# # rrr = num.__and__(2)
# # rrr = num.__bool__()
# # rrr = num.__divmod__(2)
# # rrr=num.__eq__(1)
# # rrr = num.__float__()
# # rrr = num.__floor__()
# # rrr = num.__floordiv__(9)
# rrr = num.__getattribute__("bit_length")
# rrr = num.__ge__(181)
# rrr = num.__hash__()
# rrr = num.__index__()
# rrr = num.__invert_()
# print(int.__invert__(num))

# rrr= num.__le__(111)
# rrr = num.__lshift__(1)
# rrr = num.__lt__(11)
# rrr = num.__mod__(3)
# rrr = num.__mul__(2)
# rrr = int.__neg__()
# rrr = int.__new__(num)
# rrr = num.__ne__(181)
# rrr = num.__or__(7)
# rrr = num.__pos__()
# rrr = num.__pow__(2)
# rrr = num.__radd__(-2)
# rrr = num.__rand__(2)
# rrr = num.__rdivmod__(3)
# rrr = num.__repr__()
# rrr = num.__sizeof__()
# rrr = num.__str__()
# rrr = num.__sub__(2)
# rrr = num.__truediv__(3)
# rrr = num.__trunc__()
# rrr = num.__xor__(7)
# rrr = num.bit_length()
# c = 2.3-2.5j
# rrr = c.real
# rrr = c.imag
# rrr = c.conjugate()

# rrr = num.conjugate()
# rrr = int.from_bytes(6,"big")
# rrr=num.__format__("20")
# rrr = int.from_bytes(bytes=b'1', byteorder='little')

# num = 2
# rrr = num.to_bytes(5,byteorder='little')

# print(rrr)
# for i in rrr:
    # print(i)
# print(type(rrr))
# print(len({'k1':'v1'}))
# print(str.maketrans('k'))
# str.translate(str.maketrans({'k':'v'}))
# A = 'Hello gg'
# print(A.istitle())
# print(A.isspace())

# sC = "hhEllo"
# print(sC.__add__(' a'))
# print(sC.__contains__('hu'))
# print(sC.__eq__('hello'))
# print( sC.__format__('    ') )
# print(sC.__getattribute__('__add__'))
# print(sC.__getitem__(4))
# print(sC.__getnewargs__())
# print(sC.__ge__('HeLLo'))
# print(sC.__gt__('HElloO'))
# print(sC.__hash__())
# aaa=sC.__iter__()
# print(type(aaa))
# for i in aaa:
#     print(i)
# print(sC.__iter__())
# print(sC.__len__())
# print(sC.__le__('HellO'))
# print(sC.__mod__('9'))
# print(sC.__mul__(3))
# print(sC.__new__())
# print(sC.__ne__('hhello'))
# print(sC.__repr__())
# print(sC.__rmod__(0))
# print(sC.__str__())
# print(sC.zfill(7))

# print(sC.upper())
# print(sC.translate(table="{'k':}"))
# import string
# instr = ''
# outstr = ''
# table = string.make
# instr = 'abc'
# outstr = '123'
# table = sC.maketrans(instr,outstr)
# print(table)
# print(sC.translate(table=table,'123'))

# print("hellQ oo".title())
# print("helOo".swapcase())
# print(" hel,lo ".strip())
# print("hello".startswith('h',2))
# print("hello\nooo".splitlines())
# print("hello world".split())
# print(" hello world ".lstrip())
# print(" hello world".rsplit())
# print("hello world ".rpartition('he'))
# print("hello world".rjust(20,'+'))
# print("hello world".rindex('wo'))

# strA = 'hello 1233飒飒'
# table1 = str.maketrans('123','我很好','飒飒')
# print(strA.translate(table1))
# print(table1)

# print("hello".rfind('e'))
# print('hello world'.replace('e','o'))
# print('hello world'.rpartition('el'))
# print("   hello world   ".lstrip())

# print("HELLo22".lower())
# print("hello world".ljust(20,'+'))
# print('+'.join(('hello','world')))
# print('Hello'.isupper())
# print('HELLO1'.isupper())
# print('Hello'.istitle())
# print('Hello world'.istitle())
# print(' hello'.isspace())
# print(' '.isspace())
# print('hello world'.isprintable())
# print('\n'.isprintable())

# print('111'.isnumeric())
# print('壹'.isnumeric())
# print('1q'.isnumeric())
# print('b01'.isnumeric())
# print('Hello'.islower())
# print('hello1'.islower())
# print('def'.isidentifier())
# print('hello'.isidentifier())
# print('2a2'.isidentifier())

# print('hello'.isdigit())
# print('111e'.isdigit())
# print('壹'.isdigit())
# print('121'.isdigit())
# print('11'.isdecimal())
# print('壹'.isdecimal())
# print('11d'.isdecimal())

# print('hee'.isalpha())
# print('Hello'.isalpha())
# print('1212'.isalpha())
# print('hhee1'.isalpha())

# print('hew11'.isalnum())
# print('HHH'.isalnum())
# print('112'.isalnum())
# print('  q '.isalnum())
# print('!!@~d'.isalnum())

# print('hello'.index('e'))
# print('hello'.index('el'))
# print('hello'.index('e',1,1))
# print('hello'.format_map('aa'))
# print('hello{0}'.format(' world'))
# print('hello{0}{1}'.format(' world',' python'))
# print('hello{name}'.format(name=' world'))
# print('hello'.find('he',0))
# print('hello'.find('h',1))
# print('hello\tworld'.expandtabs(tabsize=8))

# print('hello'.endswith('lo',3))

# print('我好'.encode())
# print('hello'.encode())
# # print('hela!~@@~!\xe2lo'.encode('gbk',errors='strict'))
# print(b'\xe6\x88\x91\xe5\xa5\xbd'.decode('utf-8'))

##  print('heelloe'.count('e',1,2))

# print('aaa'.center(22,'+'))
# print('hDasdd23ellAo'.casefold())
# print('1hEello Wo2rld'.capitalize())


# goods = {
#     1:['apple','5000'],
#     2:['car','50000'],
# }

food = {'1':'apple','2':'banana'}
print(food.values())
# goods = {'1':'TV','22':'Computer'}
# print(food.update(goods))
# print(food)

# print(food.setdefault('3','orange'))
# print(food)
# print(food.popitem())

# result = food.pop('1')
# print(result)
# print(food.keys())
# print(food.items())
# print(food.get('22'))
# print(food.get('1'))
# print(food.get('22','neworange'))
# print(food.get('1','neworange'))
# print(food)
# print(food.fromkeys(('w'),('2','5')))
# print(food)

# newfood = food.copy()
# print(newfood)
# print(food)
# food.clear()
# print(food)


#
# payCash.seek(0)
#         if cash:
#             if len(cash[0]) == 2:
#                 flag = True
#         else:
#             print('%s %s' % ('用户名'.ljust(5), '余额'.ljust(5)))
#         for info in payCash.readlines():
#             infoList = info.split()
#             if flag:
#                 if infoList[0] == cash[0][0]:
#                     print('将要为用户%s冲入金额%s元' % (cash[0][0], cash[0][1]))
#                     cash = cash[0][1]
#                     if len(infoList) > 2:
#                         print(payCash.tell())
#                         data.replace(infoList[2], cash, count=1)
#             elif len(infoList) > 2:
#                 name, cash = info.split()[0], info.split()[2]
#                 print("%s %-6s" % (str(name).rjust(5),
#                                    str(cash).rjust(7),
#                                    ))