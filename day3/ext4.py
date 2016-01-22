#!/usr/bin/env python
# encoding:utf8
'''
Created on 2016年1月9日
@author: zengchunyun
'''

import re

obj = re.match('\d+', '123uuasf')
if obj:
    print (obj.group())

obj = re.search('\d+', 'u123uu888asf')
if obj:
    print (obj.group())


a = "123abc456"
print (re.search("([0-9]*)([a-z]*)([0-9]*)", a).group())

print (re.search("([0-9]*)([a-z]*)([0-9]*)", a).group(0))
print (re.search("([0-9]*)([a-z]*)([0-9]*)", a).group(1))
print (re.search("([0-9]*)([a-z]*)([0-9]*)", a).group(2))

print (re.search("([0-9]*)([a-z]*)([0-9]*)", a).groups())


obj = re.findall('\d+', 'fa123uu888asf')
print (obj)



content = "123abc456"
new_content = re.sub('\d+', 'sb', content)
# new_content = re.sub('\d+', 'sb', content, 1)
print (new_content)


content = "'1 - 2 * ((60-30+1*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2) )'"
new_content = re.split('\*', content)
# new_content = re.split('\*', content, 1)
print (new_content)


content = "'1 - 2 * ((60-30+1*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2) )'"
new_content = re.split('[\+\-\*\/]+', content)
# new_content = re.split('\*', content, 1)
print (new_content)


inpp = '1-2*((60-30 +(-40-5)*(9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2))'
inpp = re.sub('\s*','',inpp)
new_content = re.split('\(([\+\-\*\/]?\d+[\+\-\*\/]?\d+){1}\)', inpp, 1)
print (new_content)

a={1:'323'}
print(a[1])






def check_conf():


if __name__ == '__main__':
    import os
    haproxy = HAproxy
    quit_HA = False
    file_name = 'haproxy.conf'
    os.system('clear')

    while not quit_HA:  # 当不是退出操作时,一直循环
        action()
        get_action = str(input('请选择操作:')).strip()  # 获取用户输入,并去除输入字段两边的空格
        if get_action == '1':
            first_menu = haproxy(file_name).main_conf()  # 获取配置文件第一列数据
            os.system('clear')
            while not quit_HA:
                for index, value in enumerate(first_menu, 1):
                    print(index, value)  # 打印第一列数据
                get_action = str(input('请选择:')).strip()

                if get_action.isdigit() and (int(get_action) - 1) in range(len(first_menu)):
                    os.system('clear')
                    print('%s 具体配置如下:\n' % (first_menu[int(get_action) - 1]))
                    second_menu = haproxy(file_name).format_dict(
                            first_menu[int(get_action) - 1])[first_menu[int(get_action) - 1]]

                    for line in range(len(second_menu)):
                        print(second_menu[line].strip('\n'))  # 打印对应的具体配置内容
                elif get_action.lower() in ['b', 'back', ]:
                    break
                elif get_action.lower() in ['q', 'quit', ]:
                    quit_HA = True
                    break
                else:
                    os.system('clear')
                    print('输入错误 !!!')
        elif get_action.lower() in ['q', 'quit', ]:
            quit_HA = True
            break
        else:
            os.system('clear')
            print('输入错误 !!!')




#!/usr/bin/env python
# encoding:utf8
'''
Created on 2016年1月9日
@author: zengchunyun
'''

# #!/usr/bin/env python
# #coding:utf-8
#
# def Before(request,kargs):
#     print ('before')
#
# def After(request,kargs):
#     print ('after')
#
#
# def Filter(before_func,after_func):
#     def outer(main_func):
#         def wrapper(request,kargs):
#
#             before_result = before_func(request,kargs)
#             if(before_result != None):
#                 return before_result;
#
#             main_result = main_func(request,kargs)
#             if(main_result != None):
#                 return main_result;
#
#             after_result = after_func(request,kargs)
#             if(after_result != None):
#                 return after_result;
#
#         return wrapper
#     return outer
#
# @Filter(Before, After)
# def Index(request,kargs):
#     print ('index')
#
#
# if __name__ == '__main__':
#     Index(1,2)

def wrapper(func):
    def result():
        print ('before')
        func()
        print ('after')
    return result

@wrapper
def foo():
    print ('foo')

foo()