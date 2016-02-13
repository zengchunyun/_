#!/usr/bin/env python3


def shop_mall(quit_atm):  # 商城购物中心
    while not quit_atm:
        print("""欢迎使用 建都网上商城
        返回(b)    退出(q)
        """)
        wait_choose = str(input("请选择操作:"))
        if str(wait_choose).lower() in ['q', 'quit', ]:
            quit_atm = True
            print("谢谢使用,再见 !")
            break
        elif str(wait_choose).lower() in ['b', 'back', ]:
            break
        else:
            print("操作有误 !!!")
    return quit_atm
