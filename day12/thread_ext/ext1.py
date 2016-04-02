#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import threading
import time


def show(i):
    print("[{:^100}]".format("doubi"))
    time.sleep(22)
    print(i)

t = threading.Thread(target=show, args=(1,))
t.start()
t.join(11)  # 设置join,等待线程执行完毕才继续,如果设置超时时间.则在这个时间内,如果线程未执行完毕,则不继续等待,执行后面的代码
# , 如果后面的代码执行完毕,线程还未执行完成,依旧等待线程执行
print(123)