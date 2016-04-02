#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import redis

# r = redis.Redis(host="127.0.0.1", port=6379)
# r.set("user", "zengchunyun")
# user = r.get("user") # 获取KEY为user的值
# print(user)  # python3获取的是bytes类型数据,使用时需要准换成UTF8类型


pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
r = redis.Redis(connection_pool=pool)
# r.set("user", "python")
# user = r.get("user")
# print(user)
#
# r.set(name="user", value="zengchunyun", ex=100, px=None, nx=True, xx=False)
# user = r.get("user")
# print(user)
# # 当nx为True时,则只有不存在name时,set操作才会执行
# r.set(name="user", value="zengchunyun", ex=100, px=None, nx=False, xx=True)
# user = r.get("user")
# print(user)
#
# # 当 xx为True时,只有name存在时,set操作才会执行
# r.set(name="pwd", value="zengchunyun", ex=100, px=None, nx=True, xx=True)
# user = r.get("pwd")
# print(user)
# # 当nx,xx同时为True时,结果为None

# r.setnx(name="age", value=10)
# age = r.get("age")
# print(age)  # 打印10
# r.setnx(name="age", value=100)
# age = r.get("age")
# print(age)  # 打印10
# # setnx只有name不存在时,才执行操作

# import datetime
#
# date = datetime.timedelta(seconds=100)
# print(date)
# r.setex(name="user", value=111, time=date)
# print(r.get("user"))
#
# date = datetime.timedelta(milliseconds=100)
# r.psetex(name="user", time_ms=date, value=121)
# print(r.get("user"))

# r.mset(k1=110, k2=119) # 设置多个值
# r.mset({"k1": 120, "k2": 121})
# print(r.mget("k2")) # 取单个值
# print(r.mget("k1", "k2"))  # 取多个值,返回的都是列表类型
# print(r.mget(["k1", "k2"]))

# r.set(name="user", value="zcy")
# print(r.get("user"))  # 获取键值
# print(r.getset(name="user", value="newzcy"))  # 设置新值,并获取原来的值,不存在则为none
# print(r.get("user"))  # 打印新值
# # b'zcy'
# # b'zcy'
# # b'newzcy'

#
# user = r.getrange(key="user", start=0, end=-1)
# print(user)
# user = r.getrange(key="user", start=0, end=-2)
# print(user)
# user = r.getrange(key="user", start=1, end=-1)
# print(user)  # 从第1位,也就是下标为1的元素,结束为最后一位
# user = r.getrange(key="user", start=0, end=1)
# print(user)  # 包括开始位置,以及结束位置
# # b'newzcy'
# # b'newzc'
# # b'ewzcy'
# # b'ne'

# print(r.get("user"))
# r.setrange(name="user", offset=1, value="我")  # 从下标1开始修改user的值,如果是汉字,泽占三个字节
# print(r.get("user"))
# # b'n222222'
# # b'n\xe6\x88\x91222'
#
# r.set(name="user", value="110")  # 字符串表示法
# user = r.get("user")  # 打印字符串内容为110
# print(user)
# user_li = list(map(lambda x: ord(x), str(user, "utf8")))
# print(user_li)  # 打印每个字符在计算机中实际的十进制数值 [49, 49, 48]
# print(list(map(lambda x: bin(x), user_li)))  # 打印每个字符在计算机中代表的实际二进制位 ['0b110001', '0b110001', '0b110000']
# print("-" * 20)
# print(r.getbit(name="user", offset=9))  # 查看第二个字节对第二位,也就是下标为1的位,这位显示为0
# r.setbit(name="user", offset=9, value=1)  # 计算机中每个字符范围-127~127,\
# # 即11111111~01111111,最高位也就是下标为0的位代表一个数的正负符号,为1则代表负数,为0则为正数\
# # 故而如果修改一个二进制数的最高位则表示去修改他的正负符号位,字符串是没有符号的,只有整数才有符号之分\
# # ,所以如果使用符号方式,是不能进行将一个负的二进制转换成字符
# print("\xb1")  # 表示+-符号
# user = r.get("user")  # 这里我们修改第二个字节的第二位也就是下标为1,原来这位为0,也就是这位现在的十进制由49变成了\
# # ,64+49=113,第二位二进制表示的十进制数为64,十进制的113对应的字符为q
# print(user)  # 所以这里打印的是1q0
# user_li = list(map(lambda x: ord(x), str(user, "utf8")))
# print(user_li)  # [49, 113, 48]
# print("-" * 20)
# print(list(map(lambda x: bin(x), user_li)))  # ['0b110001', '0b1110001', '0b110000']
# print(r.getbit(name="user", offset=9))  # 查看第二个字节对第二位,也就是下标为1的位,也就是我们刚才设置的位由0变成了1

# print(~127)
# print(bin(127))
# print(bin(-128))
#
# print(~126)
# print(bin(126))
# print(bin(-127))
#
# print(~-126)
# print(bin(-126))
# print(bin(125))
#
# print(~12)
# print(bin(12))
# print(bin(255))
# print(bin(-13))
#
# print(~16)
# print(bin(16))
# print(bin(-17))
#
# print(~-16)
# print(bin(-16))
# print(bin(15))


# source = "曾春云"
# for i in source:
#     num = ord(i)
#     print(num)
#     print(bin(num).replace('b', ''))
#     r.set(name=num, value=bin(num))
#     print(r.bitcount("num"))

# r.setbit(name="count", offset=1, value=1)
# r.setbit(name="count", offset=2, value=1)
# r.setbit(name="count", offset=3, value=1)
# print(r.bitcount(key="count"))  # 统计一个二进制数有多少位是1
# r.mset({"k1": bin(1), "k2": bin(6)})
# print(r.mget(["k1", "k2"]))
# print(r.bitop("AND", "new_name", "k1", "k2"))
# print(r.bitop("OR", "new_name", "k1", "k2"))
# print(r.bitop("xor", "new_name", "k1", "k2"))
# print(r.bitop("AND", 'new_name', 'n1', 'n2', 'n3'))
# r.set(name="user", value="曾")
# print(r.strlen(name="user"))
# r.set(name="user", value="1")
# print(r.strlen(name="user"))
# r.set(name="user", value=12)
# print(r.strlen(name="user"))
#
# r.set(name="user", value=1)
# r.incr(name="user", amount=1)
# print(r.get("user"))
# r.incr(name="user", amount=1)
# print(r.get("user"))
# r.incr(name="user", amount=1)
# print(r.get("user"))
# # b'2'
# # b'3'
# b'4'



# r.set(name="user", value=1.1)
# r.incrbyfloat(name="user", amount=1.2)
# print(r.get("user"))
# r.incrbyfloat(name="user", amount=1)
# print(r.get("user"))
# r.incrbyfloat(name="user", amount=1)
# print(r.get("user"))
# # b'2.3'
# # b'3.3'
# # b'4.3'
# r.set(name="user", value=3)
# r.decr(name="user", amount=1)
# print(r.get("user"))
# r.decr(name="user", amount=1)
# print(r.get("user"))
# r.decr(name="user", amount=1)
# print(r.get("user"))
# # b'2'
# # b'1'
# # b'0'

# r.set(name="user", value="1")
# r.append(key="user", value="21")  # 将21追加到到键值
# print(r.get("user"))
#
# r.hset(name="info", key="name", value="zengchunyun")
# print(r.hget(name="info", key="name"))
# r.hmset(name="info",mapping={"k1": 1, "k2": 23})
# print(r.hmget(name="info", keys="k1"))
# print(r.hmget("info", ["k1", "k2", "k3"]))
# print(r.hgetall(name="info"))
# print(r.hlen(name="info"))
# print(r.hkeys("info"))
# print(r.hvals("info"))
# print(r.exists("hello"))
# print(r.exists("info"))
# print(r.hdel("info","k3"))  # 删除指定键
# print(r.hkeys("info"))
# print(r.hincrby(name="info", key="count", amount=1))
# print(r.hincrby(name="info", key="count", amount=1))
# print(r.hincrbyfloat(name="info", key="count_f", amount=1.1))
# print(r.hincrbyfloat(name="info", key="count_f", amount=1.1))
# print(r.hincrbyfloat(name="info", key="count_f", amount=1.1))
# print(r.hscan(name="info"))
# print(r.hscan(name="info", count=2, match="k2"))
#
#
# # b'zengchunyun'
# # [b'1']
# # [b'1', b'23', None]
# # {b'k2': b'23', b'k1': b'1', b'count': b'15', b'count_f': b'19.8', b'name': b'zengchunyun'}
# # 5
# # [b'name', b'k1', b'k2', b'count', b'count_f']
# # [b'zengchunyun', b'1', b'23', b'15', b'19.8']
# # False
# # True
# # 0
# # [b'name', b'k1', b'k2', b'count', b'count_f']
# # 16
# # 17
# # 20.9
# # 22.0
# # 23.1
# # (0, {b'k2': b'23', b'k1': b'1', b'count': b'17', b'count_f': b'23.1', b'name': b'zengchunyun'})
# # (0, {b'k2': b'23'})

"""
# r.lpush("user", [11, 22, 33])
print(r.delete("oo"))  # 返回删除的列表个数
print(r.lpush('oo', 11,22,33))  # 返回的是列表的长度,从右向左添加每个元素,也就是['33', '22', '11']
print(r.lrange(name="oo", start=0, end=-1))

print(r.lpushx(name="oo", value=44))  # 在对应的列表中添加元素,如果name已经存在,则添加到列表的最左边,[b'44', b'33', b'22', b'11']
print(r.lrange(name="oo", start=0, end=-1))

print(r.llen(name="oo"))
print(r.rpush("oo", 55, 66)) # 在列表oo中从左向右添加元素, [b'44', b'33', b'22', b'11', b'55', b'66']
print(r.lrange(name="oo", start=0, end=-1))

print(r.rpushx(name="oo", value=41))  # 只有name存在时,则在列表从左向右添加数据, [b'44', b'33', b'22', b'11', b'55', b'66', b'41']
print(r.lrange(name="oo", start=0, end=-1))

print(r.rpushx(name="too", value=41))  # 只有name存在时,则在列表从左向右添加数据
print(r.lrange(name="too", start=0, end=-1))

print(r.linsert(name="oo", where="BEFORE", refvalue="41", value=12))  # 在列表oo里,如果存在41这个元素,则在第一次找到的41元素前\
# 插入新元素12,不存在则返回-1, [b'44', b'33', b'22', b'11', b'55', b'66', b'12', b'41']
print(r.lrange(name="oo", start=0, end=-1))

print(r.linsert(name="oo", where="AFTER", refvalue="41", value=12))  # 在列表oo里,如果存在41这个元素,则在第一次找到的41元素后\
# 插入新元素12,不存在则返回-1, [b'44', b'33', b'22', b'11', b'55', b'66', b'12', b'41', b'12']
print(r.lrange(name="oo", start=0, end=-1))

print(r.lset(name="oo", index=2, value=13))  # 对列表oo下标为2的元素修改值为13,修改成功为True,否则异常,
# [b'44', b'33', b'13', b'11', b'55', b'66', b'12', b'41', b'12']
print(r.lrange(name="oo", start=0, end=-1))

print(r.lrem(name="oo", value=41, num=1))  # 找到列表元素为41的对象,num=0,则删除所有元素为41的对象,num=3,则表示从前到后删除3个元素\
# num=-3表示从后向前删除3个,返回删除的个数,[b'44', b'33', b'13', b'11', b'55', b'66', b'12', b'12']
print(r.lrange(name="oo", start=0, end=-1))

print(r.lpop(name="oo"))  # 在列表中,从左侧获取第一个元素从列表移除,返回第一个移除的元素
print(r.lrange(name="oo", start=0, end=-1))  # [b'33', b'13', b'11', b'55', b'66', b'12', b'12']

print(r.rpop(name="oo"))  # 在列表中,从右侧获取最后一个元素从列表移除,返回最后一个元素
print(r.lrange(name="oo", start=0, end=-1))  # [b'33', b'13', b'11', b'55', b'66', b'12']


print(r.lindex(name="oo", index=2))  # 获取列表里下标为2的元素
print(r.lrange(name="oo", start=0, end=-1))  # [b'33', b'13', b'11', b'55', b'66', b'12']


print(r.ltrim(name="oo", start=1, end=4))  # 移除下标为1元素之前的元素,不包括下标1,以及移除下标4之后的元素,但不包括下标4
print(r.lrange(name="oo", start=0, end=-1))  # [b'13', b'11', b'55', b'66']
"""
# print(r.delete("userli"))
# print(r.delete("newli"))
# print(r.lpush("userli", 11, 22, 33, 44, 33, 22))  # 从右向左添加元素,[b'22', b'33', b'44', b'33', b'22', b'11']
# print(r.lrange(name="userli", start=0, end=-1))
#
# print(r.lpush("newli", 23))
#
# print(r.rpoplpush(src="userli", dst="newli"))  # 从一个列表移除最右边的元素,添加到另一个列表的最左边,同时返回移除的元素
# print(r.lrange(name="userli", start=0, end=-1))  # [b'22', b'33', b'44', b'33', b'22']
# print(r.lrange(name="newli", start=0, end=-1))  # [b'11', b'23']
#
#
# print(r.blpop(keys="userli", timeout=100))  # 删除和获取列表中第一个元素,或阻塞直到有可用, (b'userli', b'22')
# print(r.lrange(name="userli", start=0, end=-1))  # [b'33', b'44', b'33', b'22']
#
# print(r.brpop(keys="userli", timeout=0))  # 删除并获取列表最后一个元素,或阻塞直到有可用元素,(b'userli', b'22')
# print(r.lrange(name="userli", start=0, end=-1))  # [b'33', b'44', b'33']
# print(r.blpop(keys="userl", timeout=5))  # 删除和获取列表中第一个元素,或阻塞直到有可用, (b'userl', b'33')
# print(r.lrange(name="userl", start=0, end=-1))
#
# print(r.brpoplpush(src="userli", dst="userl", timeout=0))  # 取出列表最右侧的元素并移除返回,增加到目标列表
# print(r.lrange(name="userli", start=0, end=-1))  # [b'33', b'44']
# print(r.lrange(name="userl", start=0, end=-1))  # [b'33']
#
#
# # 1
# # 1
# # 6
# # [b'22', b'33', b'44', b'33', b'22', b'11']
# # 1
# # b'11'
# # [b'22', b'33', b'44', b'33', b'22']
# # [b'11', b'23']
# # (b'userli', b'22')
# # [b'33', b'44', b'33', b'22']
# # (b'userli', b'22')
# # [b'33', b'44', b'33']
# # (b'userl', b'33')
# # []
# # b'33'
# # [b'33', b'44']
# # [b'33']



# r.delete("s")
# r.delete('s2')
# print(r.sadd("s", "a", 'b'))  # 添加数据到集合's'
# print(r.smembers('s'))  # 查看集合成员
# print(r.scard('s'))  # 判定集合长度,不存在则为0
# print(r.sismember('s', 'a'))  # 判定对象是否存在集合里
# print(r.sadd('s2', 'a'))
# print(r.sinter('s', 's2'))  # 获取两个集合的交集,{b'a'}
# print(r.sinterstore('s3', 's', 's2'))  # 求交集,并把结果付给s3,返回交集个数
# print(r.smembers('s3'))
#
# print(r.smembers('s'))  # {b'b', b'a'}
# print(r.smembers('s2'))  # {b'a'}
# print(r.sunion('s', 's2'))  # {b'b', b'a'}求并集,返回两个集合的所有元素,不重复
#
# print(r.sunionstore('s4', 's', 's2'))  # 将两个集合的并集赋值给s4
# print(r.smembers('s4'))
#
# print(r.sdiff('s', 's2'))  # 求集合s里有,但是集合s2里没有的元素
# print(r.sdiffstore('s5', 's', 's2'))  # 将两个集合的差集赋值给S5
# print(r.smembers('s5'))
#
# print(r.srandmember('s'))  # 取随机元素
#
# print(r.smove(src='s', dst='s6', value='b'))  # 将集合成员b移到另一个集合,成功为True,否则False
# print(r.smembers('s6'))
# print(r.smembers('s'))
#
# print(r.sadd('s', 11, 33, 44))
# print(r.smembers('s'))
# print(r.spop('s'))  # 移除尾部一个成员,并将其返回
# print(r.srem('s', 11))  # 删除集合成员11
# print(r.smembers('s'))
#
#
# # 2
# # {b'a', b'b'}
# # 2
# # True
# # 1
# # {b'a'}
# # 1
# # {b'a'}
# # {b'a', b'b'}
# # {b'a'}
# # {b'a', b'b'}
# # 2
# # {b'a', b'b'}
# # {b'b'}
# # 1
# # {b'b'}
# # b'a'
# # True
# # {b'b'}
# # {b'a'}
# # 3
# # {b'11', b'a', b'44', b'33'}
# # b'44'
# # 1
# # {b'a', b'33'}
#
# print(r.sadd('s', 11, 22, 33, 11, 10))
# print(r.sscan(name='s', count=1, match="1*"))  # 匹配集合1*的成员
# print(r.sscan_iter('s', match='1*'))  # 返回一个迭代器,用于增量分批获取元素,避免内存消耗太大


# 有序集合,在集合的基础上,为每元素排序,元素的排序需要根据另外一个值来进行比较,所以有序集合每一个元素有两个值
# 即,值和分数,分数专门用来做排序

# print(r.delete('zs'))
# print(r.zadd('zs', 'h1', 1, 'h2', 2))
# print(r.zadd('zs', n1=11, n2=22))

# print(r.zcard('zs'))  # 获取集合长度,也就是成员个数
# print(r.zcount('zs', 1, 23))  # 获取集合分数在1到23之间,包含1和23的个数
#
# print(r.zincrby('zs', 11, amount=1))  # 自增集合对应成员的有序集合的对应分数
# print(r.zincrby('zs', 11, amount=1))
# print(r.zrange(name='zs', start=0, end=-1))  # 获取集合范围内的有序集合成员
# # 参数：
#     # name，redis的name
#     # start，有序集合索引起始位置（非分数）
#     # end，有序集合索引结束位置（非分数）
#     # desc，排序规则，默认按照分数从小到大排序
#     # withscores，是否获取元素的分数，默认只获取元素的值
#     # score_cast_func，对分数进行数据转换的函数
#
# print(r.zrevrange(name='zs', start=0, end=-1))  # 按照分数从大到小排序集合
#
# print(r.zrangebyscore(name='zs', min=1, max=11))  # 获取集合分数内的成员
# print(r.zrevrangebyscore(name='zs', max=13, min=1))  # 按照分数从大到小排序集合成员
#
# print(r.zrank(name='zs', value='h2'))  # 获取某个成员在集合中的排行
# print(r.zrevrank(name='zs', value='n1'))  # 从大到小排序,获取某个成员排行位置
#
#
# print(r.zrem('zs', 'n1'))  # 删除集合对应的成员
# print(r.zrange('zs', 0, -1))
#
# print(r.zremrangebyrank(name='zs', min=1, max=2))  # 删除指定排序范围成员,即删除下标1,不包含1,到下标2,包含2
# print(r.zrange('zs', 0, -1))

# print(r.zremrangebyscore(name='zs', min=1, max=20))  # 删除指定分数范围内的集合成员
# print(r.zrange(name='zs', start=0, end=-1))
#
# print(r.zscore(name='zs', value='n2'))  # 返回集合成员对应的分数,浮点数
#
# r.delete('s2')
# print(r.zadd('s2', n3=222, n2=222))
# print(r.zinterstore(dest='news', keys=['zs', 's2']))  # 求两个有序集合的并集
# print(r.zrange(name='news', start=0, end=-1))
#
# print(r.zunionstore(dest='nn', keys=['zs', 's2']))  # 求两个集合的并集,如果遇到不同值分数,则按照aggregate进行操作
# # aggregate值为:SUM,MIN,MAX
# print(r.zrange(name='nn', start=0, end=-1))
#
# print(r.zscan(name='zs', count=1))  # 同字符串类似,新增score_cast_func用来进行对分数进行操作
#
#
# print(r.delete('test'))  # 删除任意数据类型
# print(r.exists(name="test"))  # 判断name是否存在
#
# print(r.keys(pattern="*"))  # 打印所有匹配对KEY
# # KEYS * 匹配数据库中所有 key 。
#     # KEYS h?llo 匹配 hello ， hallo 和 hxllo 等。
#     # KEYS h*llo 匹配 hllo 和 heeeeello 等。
#     # KEYS h[ae]llo 匹配 hello 和 hallo ，但不匹配 hillo
# print(r.expire(name='zs', time=2))  # 为某个name设置超时时间
#
# print(r.rename(src='zs', dst='ns'))  # 重命名某个name
#
# print(r.move(name='zs', db=2))  # 将某个name移到到指定DB下,前提name存在,否则返回False
#
# print(r.randomkey())  # 随机获取一个name,不删除
#
# print(r.type("zs"))  # 获取name对应对类型

import redis
pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
r = redis.Redis(connection_pool=pool)
pipe = r.pipeline(transaction=True)
r.set('name', 'zengchunyun')
r.set('role', 'master')
pipe.execute()