#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""


def update_info(user_info_dict, file_path="conf.py", name="user_info"):
    """
    :param user_info_dict: 包含用户信息的字典
    :param file_path: 写入文件的位置
    :param name: 键名,方便调取写入的字典
    :return:
    """
    import re
    write_data = re.findall('["\'\[\]\w,:\s=\d@.\-]+\{*|\}', name + " = " + str(user_info_dict).replace("'", '"'))
    count = 0
    with open(file_path, 'w') as database:
        for content in write_data:
            if content.find('{') != -1:
                database.write('%s%s\n' % (str(count * '\t').expandtabs(4), content))
                count += 1
            elif content.find('}') != -1:
                database.write('%s%s\n' % (str(count * '\t').expandtabs(4), content))
                count -= 1
            else:
                database.write('%s%s\n' % (str(count * '\t').expandtabs(4), content))
    database.close()
    return True


def modify_data(shelve_file, key):
    import shelve
    open_database = shelve.open(shelve_file)
    get_key = open_database.get(key)
    print(get_key)
    update_info(get_key, name="user_info")


def initdb():
    """以下密码都是123,是根据用户名进行加密得到的,避免即使密码一样,但是用户名不同,得到的密码也不同
    :return:
    """
    import shelve
    create_database = shelve.open("database")
    user_info = {"oldboy": {"password": "484d81f3893c04df63dc6bd2aedc917c",
                            "qutota": 1000000,
                            "used": 0,
                            "avail": 1000000,
                            "type": "None",
                            },
                 "zengchunyun": {"password": "86a5897e933c466bb2b6c945845ab76b",
                                 "qutota": 10000000000,
                                 "used": 0,
                                 "avail": 10000000000.
                                 },
                 }
    create_database["data"] = user_info
    create_database.close()


if __name__ == "__main__":
    initdb()
    modify_data("database", "data")

