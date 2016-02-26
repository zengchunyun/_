#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""


def initdb():
    """以下密码都是123,是根据用户名进行加密得到的,避免即使密码一样,但是用户名不同,得到的密码也不同
    :return:
    """
    import shelve
    show_list = {"login": "\n登陆(l)   注册(r)   退出(q)\n",
                 "name": "\n请输入用户名:\n",
                 "password": "\n请输入密码:\n",
                 "welcome": "\n欢迎进入魔兽世界\n",
                 "continue": "\n继续游戏(c)   新的征程(n)   退出(q)\n",
                 "new": "\n新的征程(n)   退出(q)\n",
                 "failed": "\n登陆失败\n",
                 "role": "\n请输入角色名称:\n",
                 "role_job": "\n请选择职业\n1\t战士\n2\t魔法师\n",
                 "role_info": "\n等级{}  EXP{}  HP{}  \n",
                 "over": "\n珍爱生命,远离游戏\n",
                 "play": "历史",
                 "error": "\n输入错误\n",
                 }
    skills = {"soldier": [{"name": "狂暴", "attr": "Battle Shout", "hurt": "-0.05", "sleep": 0.01},
                          {"name": "英勇一击", "attr": "Heroic Strike", "hurt": "-0.1", "sleep": 0.05},
                          {"name": "割裂", "attr": "Rend", "hurt": "-0.12", "sleep": 0.08},
                          {"name": "防御姿势", "attr": "Defensiv", "hurt": "0.1", "sleep": 0.03},
                          {"name": "血性狂暴", "attr": "Bloodrage", "hurt": "0.18", "sleep": 0.1},
                          {"name": "嘲讽", "attr": "Taunt", "hurt": "0.06", "sleep": 0.01}],
              "magic": [{"name": "火球术", "attr": "Fireball", "hurt": "-0.2", "sleep": 0.04},
                        {"name": "烈火冲击", "attr": "Fire Blast", "hurt": "-0.22", "sleep": 0.08},
                        {"name": "火之守护", "attr": "Fire Ward", "hurt": "0.35", "sleep": 0.2}],
              }
    create_database = shelve.open("database")
    user_info = {"oldboy": {"password": "484d81f3893c04df63dc6bd2aedc917c", "store": True},
                 "zengchunyun": {"password": "86a5897e933c466bb2b6c945845ab76b", "store": False}}
    print(create_database["data"])
    # create_database["data"] = user_info
    create_database["skills"] = skills
    create_database["show_list"] = show_list
    create_database.close()


if __name__ == '__main__':
    initdb()
