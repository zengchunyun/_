#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import queue

# q = queue.Queue(maxsize=4)  # 先进先出
# q = queue.LifoQueue(maxsize=4)  # 后进先出
q = queue.PriorityQueue(maxsize=4) # 优先级越高越先出,按数字形式,越小优先级越大,以元组形式(优先级,数据)放入队列

# q.put([1, 2, 3])
# q.put_nowait(2)  # 当队列满时,放入直接异常
# q.put(3, timeout=3)  # 当队列满时,超过3秒还是未放入则异常
# q.full()  # 判断队列是否满了
# q.empty()  # 如果队列为空,则返回True
# q.get(timeout=1)  # 当设置timeout,取不到则空异常
# q.get_nowait()  # 当队列为空,取不到值,直接异常
# q.put(33)  # 当不设置超时,队列满了,会阻塞,直到队列可以放入数据
# q.get()  # 当队列为,不设置超时,则一直阻塞,等待有数据
q.put((1, [1, 2, 3]))  # 针对优先级队列设置优先级,元组的第一个数值为优先级,数值越小优先级越大
q.put((2, 33))  # 该数值比1大,所以优先级低,所以后取
q.put((2, 44))  # 同等优先级,,必须放入大数据类型也要一样,否则报错.就按照先进先出原则取数据
print(q.get())
print(q.get())
print(q.get())


