#!/usr/bin/env python
# encoding:utf8
'''
Created on 2016年1月9日
@author: zengchunyun
'''
# l1 = ['1','2','3','4']
# l2 = ['4','5','6']

# s1 = set(l1)  #传入一个集合
# print(s1)   # 第一次输出
# s1.add('33')  # 添加一个元素
# print(s1)  # 第二次输出
# s1.add('33')  # 添加一个相同元素
#
#
# s2 = s1.difference(*l2)
#
# # s1.clear()  # 使用clear属性
# print(s1)
# print(s2)  # 最终返回一个空的集合
#
# s3 = s1.copy()
#
# print(s3)
# print(id(s1))
# print(id(s3))

#
# dic1 ={'k1':'v1','k2':'v2'}
# dic2 ={'k5':'vv','k4':'v2','k3':'v3'}
# s1 = set(dic1)
# print(s1)
# s2 = s1.update(dic2)
# print(s1)
# print(s2)


# l1 = ['1','12','13']
# l2 = ['4','6','1']
# s3=set(['1','13'])
#
# s1 = set(l1)
# s2 = set(l2)
# s4 = s1.union(s2)
# print(s1)
# print(s4)

# print(s1)
# s4 = s1.symmetric_difference_update(s2)
#
# print(s1)
# print(s4)

# s4 = s1.symmetric_difference(s2)
#
# print(s1)
# print(s4)
# s4 = s1.remove('12')
# print(s1)
# print(s4)

# s4 = s1.pop()
# print(s1)
# print(s4)

# print(s1.issuperset(s3))
# print(s3.issuperset(s1))

# print(s1.issubset(s2))
# print(s1.issubset(s3))
# print(s3.issubset(s1))

# s3 = s1.isdisjoint(s2)
# print(s1)
# print(s3)
# s3 = s1.intersection_update(s2)
# print(s1)
# print(s3)
# s3 = s1.intersection(s2)
# print(s1)
# print(s2)
# print(s3)
# s2 = s1.discard('1')
# print(s1)
# print(s2)
# s2 = s1.difference_update(*l2)
#
# print(s1)
# print(s2)

# a= ['1','2','3']
# print(a[:])

# import collections
#
# mydic = collections.defaultdict(list)
# print(mydic)
#
# mydic['k1']
# print(mydic)
# print(mydic.keys())
# print(mydic.values())  #默认值为一个列表类型
#
# newdic={}
# newdic.setdefault('k1',list)
# newdic['k1']
#
# print(newdic)
# print(newdic['k1'])
# print(newdic.values())
#
#
# mydic = collections.OrderedDict(name='zcy',age='25',job='IT')
# print(mydic)
#
# print(mydic.keys())
# print(mydic.values())
# mydic.update(name='hello')
# mydic.update(time='2016')
# print(mydic)

# Point = collections.namedtuple('Point',['x','y','z'])  #创建一个类,类名为Point
#
# myPoint = Point(11,22,33)
# print(myPoint)
# print(myPoint.x)  #直接通过命名元素去访问元组对应的元素,
# print(myPoint[0])  #等同于上面这种方式,但是没有上面这种方式可读性强
# print(myPoint.y)
# print(myPoint.z)




# c1 = collections.Counter("asadgiuokasgiuwgiuqguyfudfssdguysfdus")  #创建一个counter对象
# print(c1)
#
# c1.update('uuusss')
# print(c1)

# c1.subtract('ussuum')
# print(c1)


# c3 = c1.most_common(4)
# print(c3)


# c3 = c1.elements()
#
# print(c3)
#
# for el in c1:
#     print(el)

# c2 = c1.copy()
# print(id(c1))
# print(id(c2))
#
# print(c2)


# c2 = c1.copy()
# print(id(c1))
# print(id(c2))
#
# print(c2)

# c1.update('uuus')
# print(c1)


import collections
# newqueue = collections.deque(['a','b','c'])

# import queue
#
# newqueue = queue.deque(['a','b','c'])
#
# print(newqueue)
# newqueue.append(['d1','d2'])  #追加一个元素到队列
# print(newqueue)
#
# newqueue.appendleft('a1')  #追加一个元素到队列左侧
# newqueue.appendleft('a2') #追加一个元素到队列左侧
# print(newqueue)
#
# newc = newqueue.count('a')  #对队列某个元素进行计数
# print(newc)
#
# newqueue.extend(['e','f','g'])  #扩展队列元素
# print(newqueue)
#
# newqueue.extendleft(['a11','a22','a33'])  #从左侧开始扩展队列
# print(newqueue)
#
# newqueue.insert(2,'aa22')  #插入到下标2的位置
# print(newqueue)
#
# newqueue.reverse()  #顺序反转
# print(newqueue)
#
# newqueue.rotate(4)  #将队列末尾4个元素反转到队列左侧
# print(newqueue)


# import queue
# newqueue = queue.Queue(2)  #设置队列长度为2,也就是队列里只有两个任务
# newqueue.put(['1','2'])  # 放入一个任务
# newqueue.put(2)  # 放入第二个任务
# isempty = newqueue.empty()  #判断队列是否空
# isfull = newqueue.full()  # 判断队列是否满了
# get1 = newqueue.get()  #获取第一个任务
# get2 = newqueue.get() #获取第二个任务
# print(get1)
# print(get2)
# isfull2 = newqueue.full()  #判断队列是否满了,因为已经把任务取出来了,所以这时队列应该是没有满
# isempty2 = newqueue.empty()  #判断队列是否为空
# print(isfull)
# print(isfull2)
# print(isempty)
# print(isempty2)
#
#
# def func():  #没有接收参数
#     print('hello')
#
# func()  # 直接执行函数
# foo = func  #创建一个对象
# foo()  #执行对象
#
# def func(arg):  #传入一个参数
#     print('hello %s' % arg)
#
# func('zengchunyun')
#
# def func(arg1,arg2):  #传入两个参数
#     print('hello %s,%s' % (arg1,arg2))
#
# func('zengchunyun','还你钱')
#
# def func(*args):  #多个参数
#     print('hello %s'%( ''.join(args)))
#
# func('zengchunyun,','钱不是,','还了吗')
#
# def func(*args, **kargs):  #传入任意类型的参数
#     print(kargs)
#
# func(user='zcy',pwd='123')


#
# import json
# inp_str = "[11,22,33,44]"
# inp_list = json.loads(inp_str)
# print(inp_list)
#
# inp_str = '{"k1":123,"k2":456}'
# inp_dict = json.loads(inp_str)
# print(inp_dict)
#
# with open('haproxy.conf','r',encoding='utf-8') as modifyHA:
#    content =  modifyHA.readlines()
#    ccc = '["%s"]' % '" "'.join(content)
#    print(ccc)
#    aa0 = json.loads(ccc)
#    print(aa0)

# a = ['aa','bb'].__contains__('aa')
# print(a)


import collections


mydic = collections.OrderedDict(name='zcy',age='25',job='IT')
print(mydic)

print(mydic.keys())
print(mydic.values())
mydic.update(name='hello')
mydic.update(time='2016')
print(mydic)
