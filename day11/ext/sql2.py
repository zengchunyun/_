#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

engine = create_engine("mysql+pymysql://root:123@localhost:3306/s12", echo=True)


class Host(Base):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(64), unique=True, nullable=False)
    ip_addr = Column(String(128), unique=True, nullable=False)
    port = Column(Integer, default=22)
    # group_id = Column(Integer, ForeignKey("groups.id"))
    # group = relationship("Groups", backref="host_list")
    group = relationship("Groups", back_populates="host_list")


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    # host_id = Column(Integer, ForeignKey("hosts.id"))
    host_list = relationship("Host", back_populates="group")
    # hosts = relationship("Host")


Base.metadata.create_all(engine)

if __name__ == "__main__":
    SessionCls = sessionmaker(bind=engine)
    session = SessionCls()
    # g1 = Groups(name="G1")
    # g2 = Groups(name="G2")
    # session.add_all([g1, g2])
    # session.commit()
    # h1 = Host(hostname="localhost", ip_addr="127.0.0.1", group_id=1)
    # h2 = Host(hostname="ubuntu", ip_addr="127.0.0.2", port=22)

    # session.add(h2)
    # session.add_all([h1, ])
    # session.commit()
    # obj = session.query(Host).filter(Host.hostname=="localhost").first()
    # print(obj)
    # res = session.query(Host).filter(Host.hostname.in)
    session.query(Host).join(Host.group).group_by(Groups.name).all()
