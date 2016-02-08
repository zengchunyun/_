#! /usr/bin/env python3


def main(quit_atm):  # 程序入口
    from ATM import atm_self_service  # 导入自助服务系统平台
    from mall import shop_mall  # 导入商城服务系统
    while not quit_atm:
        print("""欢迎使用一站式购物平台
        ATM自助服务(1)  商城购物(2)""")
        wait_choose = str(input("\n请选择操作:"))
        if wait_choose == "1":
            quit_atm = atm_self_service(quit_atm)  # 进入ATM自助服务系统
        elif wait_choose == "2":
            quit_atm = shop_mall(quit_atm)  # 进入商城购物系统
        elif str(wait_choose).lower() in ['q', 'quit', ]:  # 退出
            quit_atm = True
            print("谢谢使用,再见 !")
            break
        else:
            print("操作有误 !!!")
    return quit_atm

if __name__ == "__main__":
    quit_ATM = False  # 设置退出程序条件
    main(quit_ATM)
