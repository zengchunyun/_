#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
# from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
#
# metadata = MetaData()
#
# user = Table('user', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String(20)),
# )
#
# color = Table('color', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String(20)),
# )
# engine = create_engine("mysql+pymysql://root:123@localhost:3306/s12", max_overflow=5)
#
# metadata.create_all(engine)
import time
print(time.ctime())