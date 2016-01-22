#!/usr/bin/env python3.5
"""
Created on 2016年1月9日
@author: zengchunyun
"""


def help_doc():
    print("""
    1 查看配置模式
        通过序号方式查询
        可以查看到主区域配置下面的细节配置
        该模式仅允许查看,不允许修改或其他操作

    2 添加配置模式
        进入该模式,直接输入新配置,即可进入对应的操作
        此模式涉及到服务的稳定运行,所以必须严格按照字典方式进行添加配置,
        以防操作不当,影响正常服务的使用,具体使用可以参照README文档

        示例:
        以下示例不保证配置内容的正确性,只是一个写入配置的方式,请结合实际需求进行变更
            2.1 {"backend": "oldboy.org","record":{"option": "forwardfor"}}
                该配置表示
                    在主区域
                        backend oldboy.org
                    下面添加具体的细节配置,如果不存在主区域配置,则会进行添加一条主区域配置记录
                        record
                    只是一个标识键值,无特殊意义,可以使用自定义.
                    最终会在这个主区域配置下面添加一条这样的记录
                        option forwardfor

            2.2 {"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}
                该配置表示
                    在主区域
                        backend test.oldboy.org
                    下面添加如下一条记录
                        server 100.1.7.9 100.1.7.9 weight 20 maxconn 30

            通过两条示例,你应该要明白,这个record的键值实际只针对一条记录的添加,如果想多次添加,也只能多次执行,
            后期会增加多条记录添加功能

    3 修改配置模式
        该模式下,可以对主区域配置下面的任何具体细节配置进行修改操作
        注意: 该模式不能对主区域配置内容进行修改,也是为了避免不必要的错误产生
                如果强行要修改.只能通过下面介绍的删除功能进行删除后再添加

    4 删除配置模式
        该模式与添加模式互斥操作,所以操作过程其实是完全一样的

        区别在于,要删除的具体配置细节精确到每一个空格,所以在配置文件中,我们要养成好习惯,同级配置下,仅使用一个空格隔开

        删除的记录不匹配,则返回 记录不存在操作,只有完全匹配才会进行删除操作

        此删除操作是针对具体配置的一个完整记录,而不是部分记录,如果发现配置存在多余空格,可以通过修改模式进行修改操作

    """)


def action():  # 显示系统主菜单
    print("""
    1.查看配置
    2.添加配置
    3.修改配置
    4.删除配置

    帮助(h)   退出(q)
    """)


def show_first_menu():
    first_menu = haproxy(file_name).main_conf()  # 获取配置文件第一列数据
    for index, value in enumerate(first_menu, 1):
            print(index, value)  # 打印第一列数据
    return first_menu


def show_file_dict():  # 将配置文件格式化成字典形式返回
    file_dict = haproxy(file_name).format_dict()
    return file_dict


def sort_list(ref_list, no_sort_list):  # 传入两个列表,一个为参照列表,一个为打乱顺序的列表
    temp_list = []
    for value in ref_list:
        if value in no_sort_list:
            temp_list.append(value)
    return temp_list  # 返回排序后的列表


def repl_conf(args):
    global quit_HA  # 设置全局变量,控制程序退出操作
    while not quit_HA:
        get_list = show_first_menu()  # 显示主配置
        get_action = str(input('\n\t返回(b)\t退出(q)\n请选择')).strip()
        if get_action.isdigit() and (int(get_action) - 1) in range(len(get_list)):
            get_key = get_list[int(get_action) - 1]
            while not quit_HA:
                if str(args) == 'show':
                    os.system('clear')
                print('%s 具体配置如下:\n' % get_key)
                second_menu = haproxy(file_name).format_dict(get_key)[get_key]  # 获取详细配置
                for index, menu in enumerate(second_menu, 1):
                    print(index, menu)
                print('')
                if str(args) == 'replace':
                    second_get_action = str(input('\n\t返回(b)\t退出(q)\n请选择需要修改的内容: ')).strip()
                    if second_get_action.isdigit() and (int(second_get_action) - 1) in range(len(second_menu)) and str(args) == 'replace':
                        get_value = second_menu[int(second_get_action) - 1]
                        print('确定要修改\n\t%s\n' % get_value)
                        third_get_action = str(input('请输入需要变更的新配置:'))
                        if third_get_action:  # 只要输入的内容不为空,则进入确认修改状态
                            while not quit_HA:
                                re_get_action = str(input('yes/no:')).strip()
                                if re_get_action.lower() in ['y', 'yes']:
                                    get_file_dict = show_file_dict()
                                    get_file_dict[get_key][int(second_get_action) - 1] = third_get_action
                                    ref_list = haproxy(file_name).main_conf()  # 获取配置文件第一列数据作为参照
                                    haproxy(file_name).format_write(*ref_list, **get_file_dict)  # 格式化写入文件
                                    print('\t返回(b)\t退出(q)\n任意键继续 ...')
                                    wait_action = str(input('>>'))
                                    if wait_action.lower() in ['b', 'back', ]:
                                        break
                                    elif wait_action.lower() in ['q', 'quit', ]:
                                        quit_HA = True
                                    break
                                else:
                                    print('\t返回(b)\t退出(q)\n任意键继续 ...')
                                    wait_action = str(input('>>'))
                                    if wait_action.lower() in ['b', 'back', ]:
                                        break
                                    elif wait_action.lower() in ['q', 'quit', ]:
                                        quit_HA = True
                                    break

                    elif str(second_get_action).lower() in ['b', 'back', ]:  # 返回上一层菜单
                        os.system('clear')
                        break
                    elif str(second_get_action).lower() in ['q', 'quit', ]:  # 退出程序
                        quit_HA = True
                        break
                    else:
                        os.system('clear')
                        print('输入错误 !!!')
                else:
                    break  # 当查看模式下就直接终止本次循环
        elif str(get_action).lower() in ['b', 'back', ]:  # 返回主菜单
            os.system('clear')
            break
        elif str(get_action).lower() in ['q', 'quit', ]:  # 退出程序
            quit_HA = True
            break
        else:
            os.system('clear')
            print('输入错误 !!!')


def modify_conf(args):  # 添加或删除配置,需要按照字典方式输入,必须严格按住README说明修改
    global quit_HA
    while not quit_HA:
        get_list = show_first_menu()
        get_action = str(input("\n\t返回(b)\t退出(q)\n请输入配置:")).strip()
        get_file_dict = show_file_dict()
        flag = False
        if re.match('^\'', get_action):
            get_action = re.sub('\'', '\"', get_action)  # 把输入的单引号替换成双引号
        all_keys_list = re.findall('\w+.:', str(get_action))  # 在用户输入数据格式化JSON前,提取用户输入的顺序
        all_keys_list = re.sub('\W', ' ', str(all_keys_list)).split()  # 对数据进行列表处理
        try:
            get_action = json.loads(get_action)  # 将用户输入转化为json
        except json.JSONDecodeError:
            pass
        if type(get_action) == dict:  # 如果用户输入的是一个字典
            first_keys_list = list(get_action.keys())  # 将用户输入的字典键临时存到一个列表,用于判断输入是否正确
            new_set_list = list(set(all_keys_list).symmetric_difference(first_keys_list))
            second_keys_list = sort_list(all_keys_list, new_set_list)  # 对用户输入的字典键进行排序
            if len(first_keys_list) <= 2:  # 判断输入的字典是否符合要求
                for value in get_list:  # 将配置文件对应的第一列数据取出
                    if flag:
                        break
                    for key in get_action.keys():  # 对输入的字典键进行迭代查询判断
                        if flag:
                            break
                        if key in value:  # 如果输入的键在第一列配置文件里,仅匹配第一列的第0个下标元素
                            if get_action[key] in str(value).split():  # 将字典的键对应的值继续匹配对应的配置文件第一列数据
                                insert_key = value
                            else:
                                insert_key = '%s %s' % (key, get_action[key])
                            if first_keys_list.count(key):  # 如果列表存在这个元素,则删除
                                first_keys_list.remove(key)
                            second_key_to_value = get_action[first_keys_list[0]]  # 将另一个键的值临时保存起来
                            if type(second_key_to_value) == dict:
                                second_values_to_list = []  # 将字典所对应的匹配键的值存入一个列表
                                for key in second_keys_list:
                                    if str(key) == 'server':
                                        second_values_to_list.append('%s {%s} {%s}' % (key, key, key))
                                    else:
                                        second_values_to_list.append('%s {%s}' % (key, key))
                                insert_value = ' '.join(eval(str(tuple(second_values_to_list)).format(
                                        **second_key_to_value)))
                                if insert_value in get_file_dict[insert_key] and str(args) == 'del':
                                    get_file_dict[insert_key].remove(insert_value)  # 删除键对应列表的元素,再判断列表是否为空
                                    if not get_file_dict[insert_key].count('') and not get_file_dict[insert_key]:
                                        get_file_dict.pop(insert_key)
                                elif str(args) == 'del':  # 如果是删除操作,且记录不存在,则终止循环
                                    flag = True
                                    print('此记录不存在 !!!\n')
                                    break
                                if not get_file_dict[insert_key].count(insert_value) and str(args) == 'add':
                                    get_file_dict[insert_key].append(insert_value)  # 更新字典,对键值内容追加新配置
                                elif str(args) == 'add':
                                    flag = True
                                    print('请勿重复输入相同的配置内容 !!!\n')
                                    break
                                ref_list = haproxy(file_name).main_conf()  # 获取配置文件第一列数据作为参照
                                haproxy(file_name).format_write(*ref_list, **get_file_dict)  # 格式化写入文件
                                print('配置修改成功 !!!\n')
                                flag = True
                                break
                            else:
                                print('输入错误 !!!')
                                break
            else:
                print('输入错误 !!!')
        elif str(get_action).lower() in ['q', 'quit', ]:  # 退出程序
            quit_HA = True
            break
        elif str(get_action).lower() in ['b', 'back', ]:  # 返回主菜单
            os.system('clear')
            break
        else:
            os.system('clear')
            print('输入错误 !!!')


def main_menu():
    global quit_HA
    while not quit_HA:  # 当不是退出操作时,一直循环
        action()
        get_action = str(input('请选择操作:')).strip()  # 获取用户输入,并去除输入字段两边的空格
        if get_action == '1':  # 进入查看配置模式,仅查看,不能修改
            os.system('clear')
            repl_conf('show')
        elif get_action == '2':  # 进入添加配置模式,进添加,不能修改
            os.system('clear')
            modify_conf('add')
        elif get_action == '3':  # 进入修改模式,只能修改具体配置,主区域配置不允许修改,不能删除,只能修改
            os.system('clear')
            repl_conf('replace')
        elif get_action == '4':  # 进入删除模式,只能删除,如果主区域配置下面买药具体细节配置,则主区域配置也会删除
            os.system('clear')
            modify_conf('del')
        elif str(get_action).lower() in ['h', 'help', ]:  # 打印帮助信息
            help_doc()
        elif str(get_action).lower() in ['q', 'quit', ]:  # 退出程序
            quit_HA = True
            break
        else:
            os.system('clear')
            print('输入错误 !!!')

if __name__ == '__main__':
    import os
    import json
    import re
    from HAproxy.HAproxy import HAproxy
    haproxy = HAproxy  # 创建一个新对象
    quit_HA = False  # 设置退出条件
    file_name = 'haproxy.conf'  # 配置文件名称
    os.system('clear')
    main_menu()  # 进入主程序
