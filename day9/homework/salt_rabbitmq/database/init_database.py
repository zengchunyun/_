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
    update_info(get_key, name="minion_info")


def initdb(db):
    """
    :return:
    """
    import shelve
    create_database = shelve.open(db)
    print(create_database["data"])
    # minion_info = {}
    # create_database["data"] = minion_info
    create_database.close()


if __name__ == "__main__":
    db_name = "master"
    initdb(db_name)
    # modify_data(db_name, "data")
