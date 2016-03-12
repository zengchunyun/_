#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""


class Animal(object):
    name = "hello"

    def __init__(self, name):
        self.name = name
        self.__num = 100

    @classmethod  # 类方法,只能访问类属性,不能调用实例属性
    def talk(self):
        print("%s talk wang" % self.name)

    def walk(self):
        print("%s walking now" % self.name)

    @staticmethod  # 静态方法,不能直接访问类属性,以及实例属性
    def habbit(self):
        print(" %s habbit ..." % self.name)

    @property  # 属性,将类方法变成类属性形式对外提供访问
    def total(self):
        print("total pro is %s" % self.__num)

    @property
    def total_num(self):
        print("total  num pro is %s" % self.__num)

    @total_num.setter
    def total_num(self, num):  # 静态属性修改值,如果要修改,则必须传入一个参数
        self.__num = num
        print("total num  set is %s" % self.__num)

    @total_num.deleter
    def total_num(self):
        print("total num del is %s" % self.__num)
        del self.__num

# newdog = Animal("san")
# newdog.talk()
# newdog.walk()
# newdog.habbit(newdog)
# print(newdog._Animal__num)
# newdog.total
# newdog.total_num
# newdog.total_num = 3
# del newdog.total_num
# newdog.total_num  # 已经删除了该实例属性,所以不存在了,报错


#
#
# class A:
#     def f1(self):
#         print("from A")
#
# class B(A):
#     def f1(self):
#         print("from B")
#
# class C(A):
#     def f1(self):
#         print("from C")
#
# class D(B, C):
#     def f3(self):
#         print("from d")
#
#     def f2(self):
#         print("from D")
#
#
# m = D()
# m.f1()
#
# #3.x时经典类和新式类都是默认广度优先
# #2.x 时,新式类使用广度优先,经典类使用深度优先




class Foo:
    """
    hello,
    这里的代码通过类名.__doc__()可以获取到
    """

    def __init__(self):  # 构造方法,通过创建对象时.自动触发执行
        print("__init")
        #  静态字段

    def __del__(self):  #析构方法,当对象在内存中被释放时自动触发执行
        pass

    def __new__(cls, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):  # 创建的对象加括号后,触发执行
        # 构造方法的执行是由创建对象触发的,即:对象 = 类名();call方法的执行是由对象加括号触发的,即对象()或者类()()
        pass

    def __str__(self):  # 当一个类中定义了__str__方法,则在打印对象时,默认输出该返回值
        return "zengchunyun"

    def __getitem__(self, item):
        pass  # 用于索引操作.如字典,这个方法主要用来获取数据

    def __setitem__(self, key, value):
        pass
        # 用于对索引对设置

    def __delitem__(self, key):
        pass
    # 用于删除索引的数据

    def __iter__(self):
        pass  # 用于迭代器,之所以列表,字典,元组可以进行FOR循环,是因为定义了该方法

    def __metaclass__(self):
        pass
    #




a = Foo()
a.__doc__
# print(a.__module__)  # 表示当前操作的对象在哪个模块,仅限在另一个文件调用时才有该属性
print(a.__class__)  # 输出"NoneType  即当前操作的对象的类是什么

#获取类成员
class MM(object):
    def __init__(self):
        self.hello = None
    def say(self):
        pass
print(MM.__dict__)  # 获取类成员
obj = MM()
print(obj.__dict__)  # 获取对象成员

class Foo(object):
    def __init__(self):
        pass

obj = Foo()  # obj 是Foo类实例化的对象
print(type(obj))  # obj对由Foo类创建
print(type(Foo))    #Foo类对象由type类创建

#创建类的两种方式
# 第一种就是上面这种
# 第二种就是type类的构造函数
def func(self):
    print("hello")

Foo = type("Foo",(object,), {"func":func})
#type第一个参数为 类名
# type第二个参数为当前类的基类
# type第三个参数为类的成员


# import socketserver
# socketserver.ThreadingTCPServer


# class WebServer(object):
#     def __init__(self, host):
#         self.host = host
#
#     def start(self):
#         print("starting ...")
#
#     def stop(self):
#         print("stoping ...")
#
#     def restart(self):
#         self.stop()
#         self.start()
#
#
# def run_app():
#     print("running ...")
#
#
# def run_appliation(self):
#     print("running ...", self.host)


# if __name__ == "__main__":
#     server = WebServer("127.0.0.1")
#     import sys
#     if hasattr(server, sys.argv[1]):
#         action = getattr(server, sys.argv[1])
#         action()
#
#         setattr(server, "new_run", run_app)  # 给实例添加新的属性,名为new_run
#
#         server.new_run()
#         setattr(server, "new_run_app", run_appliation)
#         server.new_run_app(server)
#
#         delattr(server, "new_run")  # 删除对象的方法
#         # server.new_run()
#
#         # delattr((WebServer, "stop"))  # 删除类的方法
#         action()
#
#     getattr(server, "dd")

#
# print(type.__subclasses__(type))
#
#
# def make_hook(f):
#     """Decorator to turn 'foo' method into '__foo__'"""
#     f.is_hook = 1
#     return f
#
#
# class MyType(type):
#     def __new__(cls, name, bases, attrs):
#
#         if name.startswith('None'):
#             return None
#
#         # Go over attributes and see if they should be renamed.
#         newattrs = {}
#         for attrname, attrvalue in attrs.iteritems():
#             if getattr(attrvalue, 'is_hook', 0):
#                 newattrs['__%s__' % attrname] = attrvalue
#             else:
#                 newattrs[attrname] = attrvalue
#
#         return super(MyType, cls).__new__(cls, name, bases, newattrs)
#
#     def __init__(self, name, bases, attrs):
#         super(MyType, self).__init__(name, bases, attrs)
#
#         # classregistry.register(self, self.interfaces)
#         print("Would register class %s now." % self)
#
#     def __add__(self, other):
#         class AutoClass(self, other):
#             pass
#         return AutoClass
#         # Alternatively, to autogenerate the classname as well as the class:
#         # return type(self.__name__ + other.__name__, (self, other), {})
#
#     def unregister(self):
#         # classregistry.unregister(self)
#         print("Would unregister class %s now." % self)
#
#
# class MyObject:
#     __metaclass__ = MyType
#
#
# class NoneSample(MyObject):
#     pass
#
# # Will print "NoneType None"
# print(type(NoneSample), repr(NoneSample))
#
#
# class Example(MyObject):
#     def __init__(self, value):
#         self.value = value
#
#     @make_hook
#     def add(self, other):
#         return self.__class__(self.value + other.value)
#
# # Will unregister the class
# Example.unregister()
#
# inst = Example(10)
# # Will fail with an AttributeError
# #inst.unregister()
#
# print(inst + inst)
#
#
# class Sibling(MyObject):
#     pass
#
# ExampleSibling = Example + Sibling
# # ExampleSibling is now a subclass of both Example and Sibling (with no
# # content of its own) although it will believe it's called 'AutoClass'
# print(ExampleSibling)
# print(ExampleSibling.__mro__)
#
