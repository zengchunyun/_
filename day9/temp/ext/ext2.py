#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import pymysql
"""
show databases;  # 查看数据库
CREATE SCHEMA `mydb` DEFAULT CHARACTER SET utf8 ;  # 创建库
use mydb;  # 使用mydb,之后才能对mydb库进行操作
create database [dbname]  # 也可以这样创建库
use mydb2;
show tables;
create table students(
id int not null auto_increment primary key,
name char(64) not null,
sex char(4) not null,
age tinyint unsigned not null,
tel char(13) null default "-"
);
"""

conn = pymysql.connect(host="127.0.0.1", user="root", passwd="123", db="mydb2")  # 连接数据库

cur = conn.cursor()  # 创建游标

# 执行SQL语句
re_count = cur.execute("insert into students(Name, sex, age, tel) values(%s, %s, %s, %s)",("zengchunyun", "M", 18, 187))

conn.commit()  # 提交
cur.close()  # 关闭游标
conn.close()  # 关闭连接

print(re_count)  # 打印影响行数

