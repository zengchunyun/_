#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine('mysql+pymysql://root:123@127.0.0.1:3306/day11',echo=True)



class Hosts(Base):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(128), unique=True, nullable=False)
    ipaddress = Column(String(128), unique=True, nullable=False)
    username = Column(String(64), unique=True)
    password = Column(String(128))


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(128))


class AuditEvents(Base):
    __tablename__ = 'audit_events'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, ForeignKey('log_type.id'))
    message = Column(String(255), default='')
    date = Column(DateTime)


class Logtype(Base):
    __tablename__ = 'log_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)


# class Child(Base):
#     __tablename__ = 'child'  # 表名
#     id = Column(Integer, primary_key=True)  # 表字段
#     name = Column(String(43))
#     parent_id = Column(Integer, ForeignKey('parent.id'))  # 外键最好不要直接用类名.字段形式,避免类还没有实例化,最好以表名.字段形式
#     # 外键关联到另一张表的id字段,通过查找parent_id字段可以找到父亲是谁
#     # parent = relationship('Parent')  # 通过查到儿子后,通过儿子.parent.name 可以找到父亲是谁,实例相当于儿子.parent等于Parent类.类直接访问自己的name属性
#
#
# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64))
#     children = relationship('Child')  # 当设置外键时,第一张表如果是先创建,可以使用类名形式关系映射,否则会造成未声明先引用,最好以表名.字段进行关系映射
#     # 这个是单向映射关联,即一个父亲对应多个儿子,或者多个儿子对应一个父亲

# class Child(Base):
#     __tablename__ = 'child'  # 表名
#     id = Column(Integer, primary_key=True)  # 表字段
#     name = Column(String(43))
#     parent_id = Column(Integer, ForeignKey('parent.id'))  # 设置child表的字段parent_id为外键关联到parent表的id
#
#
# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64))
#     children = relationship('Child')  # 通过关系映射,将children映射到child表,这样可以查到父亲下有几个儿子了,



# #
# class Parent(Base):
#     __tablename__ = 'parent'  # 表名
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64))
#     # children = relationship('Child', back_populates='parent')  # 第一个参数为类名,当被关联的表先创建时,可以直接写类名,否则只能写字符串形式名字
#     # 第二个参数为双向one-to-many关系,即反向的many-to-one
#
#     def __repr__(self):
#         return "id: {}, name: {}".format(self.id, self.name)
#
#
# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(43))
#     parent_id = Column(Integer, ForeignKey('parent.id'))
#     parent = relationship('Parent', backref='children')

    # def __repr__(self):
    #     return "id: {}, parent_id: {}, ".format(self.id, self.parent_id)
# many to one

# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64))
#     child_id = Column(Integer, ForeignKey("child.id"))
#     childr = relationship("Child")
#
#
# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64))


# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64))
#     child_id = Column(Integer, ForeignKey("child.id"))
#     childr = relationship("Child", back_populates="parents")
#
#
# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64))
#     parents = relationship("Parent", back_populates="childr")


# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64))
#     child_id = Column(Integer, ForeignKey("child.id"))
#     childr = relationship("Child", backref="parents")  # 这段代码,变相的等于在Child类中添加了parents = relationship("Parent", back_populates="childr")
#
#
# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(64))

#one to one

# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(22))
#     child = relationship('Child', uselist=False, back_populates='parents')
#
#
# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(22))
#     parent_id = Column(Integer, ForeignKey('parent.id'))
#     parents = relationship("Parent", back_populates='child')

# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(22))
#     child = relationship("Child", uselist=False, back_populates="parent")
#
#
# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(22))
#     parent_id = Column(Integer, ForeignKey('parent.id'))
#     parent = relationship("Child", back_populates="child")


# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(22))
#     child_id = Column(Integer, ForeignKey("child.id"))
#     child = relationship("Child", back_populates="parent")
#
#
# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(22))
#     parent = relationship("Child", back_populates="child", uselist=False)
#
# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(22))
#     child_id = Column(Integer, ForeignKey("child.id"))
#     child = relationship("Child", backref="parent", uselist=False)
#
#
# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(22))

p_c = Table("p_c", Base.metadata,
           Column("left_id", Integer, ForeignKey("left.id"), primary_key=True),
           Column("right_id",Integer, ForeignKey("right.id"), primary_key=True)
           )

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    name = Column(String(22))
    child = relationship("Child", secondary=p_c,
                         backref="parents")


class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)
    name = Column(String(22))



Base.metadata.create_all(engine)

DBSession = sessionmaker()
DBSession.configure(bind=engine)
session = DBSession()  # 打开数据连接

# # 第一种数据插入方式
# p1 = Parent(name='zeng')
# c1 = Child(name="haha")
# p1.child.append(c1)  # 只有存在relationship关系的对象才能通过append形式添加记录
# # 或者p1.child = [c1]
# session.add(p1)
# 第二种
# p1 = Parent(name='zeng')
# c1 = Child(name='haha')
# c1.parents.append(p1)
# session.add(c1)
# 第三种
# p1 = Parent(name='zeng')
# p1.child = [Child(name="hah")]
# session.add(p1)
# 第四种
p1 = Parent(name="zcy", child=[Child(name='sasa')])
session.add(p1)
session.commit()


# class Association(Base):
#     __tablename__ = 'association'
#     left_id = Column(Integer, ForeignKey("left.id"), primary_key=True)
#     right_id = Column(Integer, ForeignKey("right.id"), primary_key=True)
#     extra_data = Column(String(50))
#     child = relationship("Child")
#
#
# class Parent(Base):
#     __tablename__ = 'left'
#     id = Column(Integer, primary_key=True)
#     children = relationship("Association")
#
# class Child(Base):
#     __tablename__ = 'right'
#     id = Column(Integer, primary_key=True)

#

# class Association(Base):
#     __tablename__ = 'association'
#     left_id = Column(Integer, ForeignKey("left.id"), primary_key=True)
#     right_id = Column(Integer, ForeignKey("right.id"), primary_key=True)
#     extra_data = Column(String(50))
#     child = relationship("Child", back_populates="parents")
#     parent = relationship("Parent", back_populates="children")
#
#
# class Parent(Base):
#     __tablename__ = 'left'
#     id = Column(Integer, primary_key=True)
#     children = relationship("Association", back_populates='parent')
#
# class Child(Base):
#     __tablename__ = 'right'
#     id = Column(Integer, primary_key=True)
#     parents = relationship("Association", back_populates="child")

# class Association(Base):
#     __tablename__ = 'association'
#     left_id = Column(Integer, ForeignKey("left.id"), primary_key=True)
#     right_id = Column(Integer, ForeignKey("right.id"), primary_key=True)
#     extra_data = Column(String(50))
#     child = relationship("Child", backref="parents")
#     parent = relationship("Parent", backref="children")
#
#
# class Parent(Base):
#     __tablename__ = 'left'
#     id = Column(Integer, primary_key=True)
#
# class Child(Base):
#     __tablename__ = 'right'
#     id = Column(Integer, primary_key=True)


# Base.metadata.create_all(engine)
#
# DBSession = sessionmaker()
# DBSession.configure(bind=engine)
# session = DBSession()  # 打开数据连接


# p1 = Parent(name="zeng")
# session.add(p1)
# c1 = Child(name="qq")
# # session.add(c1)

# 插入数据方式一
# p = Parent()
# c = Child()
# a = Association(extra_data="ss")
# a.parent = p
# a.child = c
# # 插入数据方式二
# c = Child()
# a = Association(extra_data='dd')
# a.parent = Parent()
# c.parents.append(a)

# 插入数据方式三
# p = Parent()
# a = Association(extra_data="some data")
# a.child = Child()
# p.children.append(a)
#
# for assoc in p.children:
#     print(assoc.extra_data)
#     print(assoc.child)
#
# p = Parent()
# a = Association(extra_data='dasa')
# a.child = Child()
# p.children.append(a)
# session.add(p)
# session.add(a)
# session.add(c)
# session.commit()
# ret = session.query(Child).all()  # SELECT child.id AS child_id, child.parent_id AS child_parent_id FROM child
# print(ret)
# ret = session.query(Child).filter(Parent.id == Child.parent_id).all()  # SELECT child.id AS child_id, child.parent_id AS child_parent_id FROM child, parent WHERE parent.id = child.id
# print(ret)
# print(len(ret))
# ret = session.query(Parent).filter(Child.id == Parent.id).all()
# print(ret)
# ret = session.query(Child).filter(Child.id==1).one()
# print(ret.parent.name)
# ret = session.query(Parent).filter(Parent.id == 1).one()
# print(ret.name)
# print(ret.children.parent_id)
# ret = session.query(Parent).filter(Parent.id ==1).one()
# print(ret)
# print(ret.children)
# print(ret.children[0].name)
# id: 1, parent_id: [<__main__.Child object at 0x10402d320>, <__main__.Child object at 0x10402d5c0>, <__main__.Child object at 0x10402d6a0>, <__main__.Child object at 0x10402d588>],
# [<__main__.Child object at 0x10402d320>, <__main__.Child object at 0x10402d5c0>, <__main__.Child object at 0x10402d6a0>, <__main__.Child object at 0x10402d588>]
# woa
# print(ret[0].children)  # 通过父亲找儿子

# ret = session.query(Child).filter(Child.parent_id == Parent.id).all()
# print(ret)
# print(ret[0].parent.name)  # 通过儿子找父亲
# print(list(map(lambda x: print(x.parent.name), ret)) )


# ret = session.query(Parent).filter(Parent.name == 'zeng').one()
# print(ret)
# print(ret.childr.name)
# ret = session.query(Parent).filter(Parent.name == 'chunyun').one()
# print(ret)
# print(ret.childr.name)
#
# ret = session.query(Parent).filter(Parent.name == 'chun').one()
# print(ret)
# print(ret.childr.name)

# ret = session.query(Parent).filter(Parent.name == 'chunyun').all()
# print(ret[0].child.name)

# 通过儿子的
# ret = session.query(Child).join(Child.parent).group_by(Child.id).all()  # SELECT child.id AS child_id, child.parent_id AS child_parent_id FROM child INNER JOIN parent ON parent.id = child.parent_id GROUP BY child.id
# print(ret)
# print(len(ret))
# ret = session.query(Parent).filter(Child.parent_id == 1).all()
# print(ret)
# ret = session.query(Child).filter(Parent.children).all()  # 通过父亲的
# ret = session.query(Parent).filter(Parent.children).all()
# aaaa = session.query(Parent).all()
# print(aaaa, 999)
# p1 = Parent(name='chunyun',child_id=2)  # 创建一个父亲
# session.add(p1)  # 添加一个父亲
# session.commit()  # 提交事务
# print(session.query(Parent).filter(Parent.id).first())  # 返回一个父亲记录
# c1 = Child(parent_id=session.query(Parent).filter(Parent.id).all()[-1].id)  # 创建一个儿子
# c1 = Child(name='qq')
# session.add(c1)
# print(c1.parent_id)  # 打印儿子的父亲
# session.add(c1)  # 添加儿子
# session.commit()  # 提交事务
# ret = session.query(Child).all()  # 查询所有儿子
# print(ret)
