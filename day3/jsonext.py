#!/usr/bin/env python
# encoding:utf8
'''
Created on 2016年1月9日
@author: zengchunyun
'''
# import json
# import re

# inn=input("jjj:")
# print(inn)
# ddd=re.findall('\s',inn)
# dff=re.sub('\'', '\"', inn)
# print(dff)
# print(ddd)

# print(json.loads(inn))
#
# content = "123abc456"
# new_content = re.sub('\d+', 'sb', content)
# # new_content = re.sub('\d+', 'sb', content, 1)
# print (new_content)


# a = ['ajj','b','c']
# a.
# b = tuple(a)
# # b = str(a)
# # i = b.find('ajj')
# i = a.index('ajj')
# print(b)
# print(i)
# a = '{"backend": "www.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}'
# import re
#
# import json
#
# # result = re.sub('\W+', ' ', a)
# # print(result)
# result = re.findall('\w+.:', a)
# print(result)
# result3 = re.sub('\W', ' ', str(result))
# #
# print(result3.split())
# # ddd = json.loads(str(result3))
# print(ddd)

# ['        server 100.1.7.9 100.1.7.9 weight 20 maxconn 3000\n', '\n', 'server 100.1.7.999 100.1.7.999 weight 20 maxconn 30\n']




def foo(*args, **kwargs):
    print(args)
    print(kwargs)

a=['11','88']

foo(33,a)