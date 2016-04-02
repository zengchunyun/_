#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref


Base = declarative_base()

engine = create_engine("mysql+pymysql://root:123@localhost:3306/day11", echo=False)

Host2Group = Table("host_2_group", Base.metadata,
                   Column("host_id", ForeignKey("host.id"), primary_key=True),
                   Column("group_id", ForeignKey("groups.id"), primary_key=True),
                   )

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(User.id))

    hosts = relationship(User, backref=backref('groupses', uselist=True))

    hosts_list = relationship(
        'Host',
        secondary=Host2Group,
    )

    def __repr__(self):
        return "name:{} ".format(self.name)


class Host(Base):
    __tablename__ = "host"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(64), unique=True, nullable=False)
    ip_addr = Column(String(128), unique=True, nullable=False)
    port = Column(Integer, default=22)

    groupses = relationship(
        'Group',
        secondary=Host2Group
    )
    # groups = relationship('Group', backref=backref('group', uselist=True))

    def __repr__(self):
        return "hostname: {}, ip_addr: {}, port: {}".format(self.hostname, self.ip_addr, self.port)





Base.metadata.create_all(engine)

if __name__ == "__main__":
    DBSession = sessionmaker()
    DBSession.configure(bind=engine)
    session = DBSession()
    h1 = Host(hostname='localhost', ip_addr="1.1.1.1",port=22, )
    session.add(h1)
    get_port = session.query(Host).filter(Host.port == 22).first()
    print(get_port)
    zcy = User(name='zcy')
    session.add(zcy)
    sss = Group(hosts=session.query(User).filter(User.name == 'zcy').one())
    sss.hosts_list.append(get_port)
    session.add(sss)
    session.commit()
    # SessionCls = sessionmaker(bind=engine)
    # session = SessionCls()
    # g1 = Group(name="g1")
    # g2 = Group(name="g2")
    # g3 = Group(name="g3")
    # g4 = Group(name="g4")
    # session.add_all([g1, g2, g3, g4])
    #
    # h1 = Group(name="g1", hosts_list=Host(hostname="h1", ip_addr="192.168.11.1", port=222))
    # session.add(h1)
    # h2 = Host(hostname="h2", ip_addr="192.168.11.2", port=223, host_list=Group(name="g1"))
    # h3 = Host(hostname="h3", ip_addr="192.168.11.3")
    #
    # session.add_all([h1, h2, h3])

    # groups = session.query(Group).all()
    # print("".ljust(60, "-"))
    # print(groups)
    # g1 = session.query(Group).first()
    # print(g1)
    # g2 = session.query(Group).all()[2]
    # print(g2)
    #
    # h2 = session.query(Host).filter(Host.hostname == "h2").first()
    # print(h2)
    # print(h2.groups)
    # print(groups[1:-1])
    # h2.groups = groups
    # print(g1.host_list)
    # session.commit()

