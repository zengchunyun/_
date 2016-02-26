#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import time


class Role(object):
    def __init__(self, name, level=0, exp=0, hp=100):
        """
        :param name: 角色名
        :param level: 等级
        :param exp: 经验
        :param hp: 血量
        :return:
        """
        self.name = name
        get_attr = self.low_level(level, exp, hp)
        if get_attr:
            self.level, self.exp = get_attr
            self.hp = 100
        else:
            self.level, self.exp = self.up_level(level, exp)
            self.hp = hp

    def up_level(self, level, exp):
        """
        :param level: 当前级别
        :param exp: 当前经验
        :return: 级别
        """
        self.level = level
        if exp >= 100:
            level_count, exp_remains = divmod(exp, 100)
            self.level += level_count
            self.exp = exp_remains
        return self.level, self.exp

    def low_level(self, level, exp, hp):
        """
        :param level: 当前级别
        :param exp: 当前经验
        :param hp: 血量
        :return: 级别
        """
        self.exp = exp
        self.level = level
        if self.level < 1:
            return False
        if hp <= 0:
            self.level -= 1
            self.exp += 100
            self.exp -= 5  # 每次死亡一次,减5点经验
            level_count, exp_remains = divmod(self.exp, 100)
            self.level += level_count
            self.exp = exp_remains
            return self.level, self.exp
        return False

    def plus_attr(self, level, attr, value):
        """
        :param level: 等级
        :param attr: 游戏角色属性
        :param value: 增长数
        :return: 角色属性
        """
        self.level = level
        for level_count in range(self.level):
            attr += level_count * value
        return attr


class Soldier(Role):
    def __init__(self, name, level, exp, hp, strength=100, hurt=1):
        """
        :param name: 角色名
        :param level:等级
        :param exp: 经验
        :param hp: 血量
        :param strength:战斗力
        :param hurt: 伤害值,初始为1点伤害
        :return:
        """
        super(Soldier, self).__init__(name, level, exp, hp)
        self.strength = self.plus_attr(level, strength, 4)
        self.hurt = hurt

    def skills_hurt(self, skill_db, strength):
        """
        :param skill_db: 技能库
        :param strength: 战斗力
        :return: 伤害值
        """
        self.strength = strength
        hurt = skill_db.get("hurt")
        sleep = skill_db.get("sleep")
        self.hurt = self.strength * float(hurt)
        time.sleep(sleep)
        return self.hurt


class MagicMaster(Role):
    def __init__(self, name, level, exp, hp, magic=100, hurt=2):
        """
        :param name: 角色名
        :param level: 等级
        :param exp: 经验
        :param hp: 血量
        :param magic: 魔法值
        :param hurt: 伤害值,初始为2点伤害
        :return:
        """
        super(MagicMaster, self).__init__(name, level, exp, hp)
        self.magic = self.plus_attr(level, magic, 2)
        self.hurt = hurt

    def skills_hurt(self, skill_db, magic):
        """
        :param skill_db: 魔法师技能库
        :param magic: 魔法值
        :return: 伤害值
        """
        self.magic = magic
        hurt = skill_db.get("hurt")
        sleep = skill_db.get("sleep")
        self.hurt = self.magic * float(hurt)
        time.sleep(sleep)
        return self.hurt
