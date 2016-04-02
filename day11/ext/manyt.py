#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from sqlalchemy import create_engine,and_,or_,func,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship

Base = declarative_base()  # 生成一个SqlORM 基类


Host2Group = Table('host_2_group', Base.metadata,
                   Column('host_id', ForeignKey('host.id'), primary_key=True),
                   Column('group_id', ForeignKey('group.id'), primary_key=True),)
engine = create_engine("mysql+pymysql://root:123@localhost:3306/day11",echo=True)


class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True,autoincrement=True)
    hostname = Column(String(64), unique=True,nullable=False)
    ip_addr = Column(String(128), unique=True,nullable=False)
    port = Column(Integer, default=22)
    groups = relationship('Group',
                          secondary=Host2Group,
                          back_populates='host_list')

    def __repr__(self):
        return "<id=%s,hostname=%s, ip_addr=%s>" % (self.id, self.hostname, self.ip_addr)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    host_list = relationship('Host',
                             secondary=Host2Group,
                             back_populates='groups')

    def __repr__(self):
        return  "<id=%s,name=%s>" % (self.id, self.name)

Base.metadata.create_all(engine)  # 创建所有表结构

if __name__ == '__main__':
    SessionCls = sessionmaker(bind=engine) #创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
    session = SessionCls() # 连接的实例

    # g1 = Group(name='g1')
    #
    # h1 = Host(hostname='localhost', ip_addr='127.0.0.1')
    # h2 = Host(hostname='ubuntu', ip_addr='192.168.1.55', port=10000)
    # h2.groups = [g1]
    h1 = Host(hostname="aa1s", ip_addr="1.1.11.1", groups=[Group(name='root1')])
    # h2.groups.append(g1)
    session.add(h1)

    session.commit()