#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import ChoiceType
try:
    from conf.settings import DATABASES
except ImportError:
    pass
Base = declarative_base()


class Hosts(Base):
    """
    主机表
    """
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(128), unique=True, nullable=False)
    ipaddress = Column(String(128), unique=True, nullable=False)
    port = Column(Integer, default=22)
    # auth_user = Column(Integer, ForeignKey("host_users.id"))
    # get_username = relationship("HostUsers")
    group = relationship('HostGroup',
                         backref="host")
    auth_user = relationship('HostToUser',
                             backref='auth_users')


class HostUsers(Base):
    """
    主机用户表
    """
    __tablename__ = 'host_user'
    TYPES = [
        (u'key', u'KEY'),
        (u'password', u'PWD'),
    ]
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(128))
    auth_type = Column(ChoiceType(TYPES))


class HostToUser(Base):
    """
    主机与用户关系表
    """
    __tablename__ = 'host_to_user'
    user_id = Column(Integer, ForeignKey("host_user.id"), primary_key=True)
    host_id = Column(Integer, ForeignKey("hosts.id"), primary_key=True)
    user = relationship('HostUsers')


class Groups(Base):
    """
    主机组表
    """
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    groupname = Column(String(64), unique=True, nullable=False)


class HostGroup(Base):
    """
    主机与主机组关系表
    """
    __tablename__ = 'host_group'
    host_id = Column(Integer, ForeignKey("hosts.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    group = relationship("Groups")


class Account(Base):
    """
    堡垒主机用户表
    """
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(128))


class AccountGroup(Base):
    """
    堡垒用户关联主机组表
    """
    __tablename__ = 'account_group'
    account_id = Column(Integer, ForeignKey("account.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)
    groups = relationship("Groups", backref="account")
    account = relationship("Account", backref="groups")


class AuditEvents(Base):
    """
    日志记录表
    """
    __tablename__ = 'audit_events'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, ForeignKey('log_type.id'))
    message = Column(String(255), default='')
    date = Column(DateTime)
    log_type = relationship('LogType', backref='events')


class LogType(Base):
    """
    日志记录类型表
    """
    __tablename__ = 'log_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)


def select_engine():
    """
    选择数据引擎
    :return: 返回引擎对象
    """
    try:
        database_string = DATABASES['default']
    except NameError:
        print("\033[31;1m[DATABASE] is not defined,please check the settings\033[0m")
        exit(1)
    if database_string.get('ENGINE') == 'mysql':
        db = database_string.get('NAME')
        host = database_string.get('HOST')
        port = database_string.get('PORT')
        user = database_string.get('USER')
        password = database_string.get('PASSWORD')
        engine = create_engine('mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}'.format(
            user=user, pwd=password, host=host, port=port, db=db), echo=False)
        return engine


def create_db():
    """
    创建数据库
    :return:
    """
    engine = select_engine()
    if engine:
        Base.metadata.create_all(engine)

if __name__ == "__main__":
    DATABASES = {
        'default': {
            'ENGINE': 'mysql',
            'NAME': 'day11',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'USER': 'root',
            'PASSWORD': '123',
        }
    }
    create_db()
    DBSession = sessionmaker()
    DBSession.configure(bind=select_engine())
    session = DBSession()  # 打开数据连接
    ret = session.query(Hosts).all()
    print(ret)
    session.commit()
