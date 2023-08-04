# 使用 Redis 有序集合实现 IP 归属地查询

工作中经常遇到一类需求，根据 IP 地址段来查找 IP 对应的归属地信息。如果把查询过程放到关系型数据库中，会带来很大的 IO 消耗，速度也不能满足，显然是不合适的。

那有哪些更好的办法呢？为此做了一些尝试，下面来详细说明。

## 构建索引文件
在 GitHub 上看到一个 [ip2region](https://github.com/lionsoul2014/ip2region) 项目，作者通过生成一个包含有二级索引的文件来实现快速查询，查询速度足够快，毫秒级别。但如果想更新地址段或归属地信息，每次都要重新生成文件，并不是很方便。

不过还是推荐大家看看这个项目，其中建索引的思想还是很值得学习的。作者的开源项目中只有查询的相关代码，并没有生成索引文件的代码，我依照原理图写了一段生成索引文件的代码，如下：

```python
# -*- coding:utf-8 -*-


import time
import socket
import struct

IP_REGION_FILE = './data/ip_to_region.db'

SUPER_BLOCK_LENGTH = 8
INDEX_BLOCK_LENGTH = 12
HEADER_INDEX_LENGTH = 8192


def generate_db_file():
    pointer = SUPER_BLOCK_LENGTH + HEADER_INDEX_LENGTH

    region, index = '', ''

    # 文件格式
    # 1.0.0.0|1.0.0.255|澳大利亚|0|0|0|0
    # 1.0.1.0|1.0.3.255|中国|0|福建省|福州市|电信
    with open('./ip.merge.txt', 'r') as f:
        for line in f.readlines():
            item = line.strip().split('|')
            print item[0], item[1], item[2], item[3], item[4], item[5], item[6]
            start_ip = struct.pack('I', struct.unpack('!L', socket.inet_aton(item[0]))[0])
            end_ip = struct.pack('I', struct.unpack('!L', socket.inet_aton(item[1]))[0])
            region_item = '|'.join([item[2], item[3], item[4], item[5], item[6]])
            region += region_item

            ptr = struct.pack('I', int(bin(len(region_item))[2:].zfill(8) + bin(pointer)[2:].zfill(24), 2))
            index += start_ip + end_ip + ptr
            pointer += len(region_item)

    index_start_ptr = pointer
    index_end_ptr = pointer + len(index) - 12
    super_block = struct.pack('I', index_start_ptr) + struct.pack('I', index_end_ptr)

    n = 0
    header_index = ''
    for index_block in range(pointer, index_end_ptr, 8184):
        header_index_block_ip = index[n * 8184:n * 8184 + 4]
        header_index_block_ptr = index_block
        header_index += header_index_block_ip + struct.pack('I', header_index_block_ptr)

        n += 1

    header_index += index[len(index) - 12: len(index) - 8] + struct.pack('I', index_end_ptr)

    with open(IP_REGION_FILE, 'wb') as f:
        f.write(super_block)
        f.write(header_index)
        f.seek(SUPER_BLOCK_LENGTH + HEADER_INDEX_LENGTH, 0)
        f.write(region)
        f.write(index)


if __name__ == '__main__':
    start_time = time.time()
    generate_db_file()

    print 'cost time: ', time.time() - start_time
```

## 使用 Redis 缓存

目前有两种方式对 IP 以及归属地信息进行缓存：

第一种是将起始 IP，结束 IP 以及中间所有 IP 转换成整型，然后以字符串方式，用转换后的 IP 作为 key，归属地信息作为 value 存入 Redis；

第二种是采用有序集合和散列方式，首先将起始 IP 和结束 IP 添加到有序集合 ip2cityid，城市 ID 作为成员，转换后的 IP 作为分值，然后再将城市 ID 和归属地信息添加到散列 cityid2city，城市 ID 作为 key，归属地信息作为 value。

第一种方式就不多做介绍了，简单粗暴，非常不推荐。查询速度当然很快，毫秒级别，但缺点也十分明显，我用 1000 条数据做了测试，缓存时间长，大概 20 分钟，占用空间大，将近 1G。

下面介绍第二种方式，直接看代码：

```python
# generate_to_redis.py
# -*- coding:utf-8 -*-

import time
import json
from redis import Redis


def ip_to_num(x):
    return sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])


# 连接 Redis
conn = Redis(host='127.0.0.1', port=6379, db=10)

start_time = time.time()

# 文件格式
# 1.0.0.0|1.0.0.255|澳大利亚|0|0|0|0
# 1.0.1.0|1.0.3.255|中国|0|福建省|福州市|电信
with open('./ip.merge.txt', 'r') as f:
    i = 1
    for line in f.readlines():
        item = line.strip().split('|')
        # 将起始 IP 和结束 IP 添加到有序集合 ip2cityid
        # 成员分别是城市 ID 和 ID + #, 分值是根据 IP 计算的整数值
        conn.zadd('ip2cityid', str(i), ip_to_num(item[0]), str(i) + '#', ip_to_num(item[1]) + 1)
        # 将城市信息添加到散列 cityid2city，key 是城市 ID，值是城市信息的 json 序列
        conn.hset('cityid2city', str(i), json.dumps([item[2], item[3], item[4], item[5]]))

        i += 1

end_time = time.time()

print 'start_time: ' + str(start_time) + ', end_time: ' + str(end_time) + ', cost time: ' + str(end_time - start_time)
```

```python
# test.py
# -*- coding:utf-8 -*-

import sys
import time
import json
import socket
import struct
from redis import Redis

# 连接 Redis
conn = Redis(host='127.0.0.1', port=6379, db=10)

# 将 IP 转换成整数
ip = struct.unpack("!L", socket.inet_aton(sys.argv[1]))[0]

start_time = time.time()
# 将有序集合从大到小排序，取小于输入 IP 值的第一条数据
cityid = conn.zrevrangebyscore('ip2cityid', ip, 0, start=0, num=1)
# 如果返回 cityid 是空，或者匹配到了 # 号，说明没有找到对应地址段
if not cityid or cityid[0].endswith('#'):
    print 'no city info...'
else:
    # 根据城市 ID 到散列表取出城市信息
    ret = json.loads(conn.hget('cityid2city', cityid[0]))
    print ret[0], ret[1], ret[2]

end_time = time.time()
print 'start_time: ' + str(start_time) + ', end_time: ' + str(end_time) + ', cost time: ' + str(end_time - start_time)
```

```python
# python generate_to_redis.py 
start_time: 1554300310.31, end_time: 1554300425.65, cost time: 115.333260059
```
```python
# python test_2.py 1.0.16.0
日本 0 0
start_time: 1555081532.44, end_time: 1555081532.45, cost time: 0.000912189483643
```
测试数据大概 50 万条，缓存所用时间不到 2 分钟，占用内存 182M，查询速度毫秒级别。显而易见，这种方式更值得尝试。

`zrevrangebyscore` 方法的时间复杂度是 O(log(N)+M)， `N` 为有序集的基数， `M` 为结果集的基数。可见当 N 的值越大，查询效率越慢，具体在多大的数据量还可以高效查询，这个有待验证。不过这个问题我觉得并不用担心，遇到了再说吧。

以上。