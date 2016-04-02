#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Float, create_engine

from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/day12", echo=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    fullname = Column(String(64))
    password = Column(String(64))

    addresses = relationship()