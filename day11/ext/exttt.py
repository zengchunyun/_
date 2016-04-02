#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
'''
from sqlalchemy import create_engine, Table, Column, Integer,String,MetaData, ForeignKey, select

metadata = MetaData()
user = Table('User', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String(20)),
             )

color = Table('color', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(20)),
              )

engine = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/day11", encoding="utf8", max_overflow=5)

conn = engine.connect()

#insert
# conn.execute(user.insert(), {'id': 7, 'name': 'seven'})
# conn.close()
# sql = user.insert().values(id=123, name='wu')
# conn.execute(sql)

# delete
sql = user.delete().where(user.c.id > 3)
conn.execute(sql)

# update
sql = user.update().values(name=user.c.name)
print(sql)
sql = user.update().where(user.c.name == 'ly').values(name='zcy')
print(sql)
conn.execute(sql)

sql = select([user,])
print(sql)
ret = conn.execute(sql)
print(ret)
print(ret.fetchone())
print(ret.fetchall())
print(ret.fetchmany())

sql = select([user.c.id,])
print(sql)

sql = select([user.c.name]).order_by(user.c.name)
print(sql)
print(conn.execute(sql).fetchall())

sql = select([user]).group_by(user.c.name)
print(sql)
print(conn.execute(sql))
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:123@127.0.0.1:3306/day11')

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __repr__(self):
        return self.name

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# insert
u = Users(name='sb')
session.add(u)
session.add_all([
    Users(name='za'),
    Users(name='sd'),
    Users(name='es'),
])
session.commit()


# delete
# session.query(Users).filter(Users.id > 4).delete()
# session.commit()

# update
# session.query(Users).filter(Users.id > 2).update({'name': 22})
# session.commit()

# select
ret = session.query(Users).filter_by(name='sb').all()  # 打印的是列表
print(ret)

ret = session.query(Users).filter_by(name='sb').first()  # 打印的是字符串
print(ret)

ret = session.query(Users).filter(Users.name.in_(['sb', 'za'])).all()
print(ret)
ret = session.query(Users.name.label('name_label')).all()
print(ret, type(ret))

ret = session.query(Users).order_by(Users.id)[1:3]
print(ret)

session.query(Users).add_column('pwd')
session.commit()

from sqlalchemy.sql import func

stmt = session.query(Users.id, func.count('*').label('user')).group_by(Users.name).subquery()
print(stmt)
session.commit()