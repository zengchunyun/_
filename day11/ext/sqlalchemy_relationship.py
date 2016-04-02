#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine("mysql+pymysql://root:123@localhost:3306/day11", echo=True)
Base = declarative_base()  # 定义一个映射


class User(Base):
    __tablename__ = 'users'  # 设置表名
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    fullname = Column(String(62))
    password = Column(String(64))

    addresses = relationship("Address", back_populates='user',  #  这个addresses字段关系到Address类的user字段的back_populates的addresses
                           cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User (name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password
        )


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="addresses")  # 这个user就是User类定义addresses字段时设置的back_populates的user属性

    def __repr__(self):
        return "<Address(email_address='%s)>" % self.email_address


Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

jack = User(name='jack', fullname='Jack Bean', password='giffdd')
session.commit()