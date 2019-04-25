所用 Python 依赖包：`kafka-python      1.3.3`

## 生产者：
```python
# -*- coding:utf-8 -*-

from kafka import KafkaProducer

# 此处ip可以是多个['0.0.0.1:9092','0.0.0.2:9092','0.0.0.3:9092' ]
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

for i in range(3):
    msg = "msg%d" % i
    producer.send('test', msg)

producer.close()
```

## 生产者-压缩消息发送
```python
# -*- coding:utf-8 -*-

from kafka import KafkaProducer

# 此处ip可以是多个['0.0.0.1:9092','0.0.0.2:9092','0.0.0.3:9092' ]
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], compression_type='gzip')

for i in range(3):
    msg = "msg%d" % i
    producer.send('test', msg)

producer.close()
```
若消息过大，可压缩消息发送，可选值为 `gzip`, `snappy`, `lz4`。

## 生产者-json 数据
```python
# -*- coding:utf-8 -*-

import json

from kafka import KafkaProducer

# 此处ip可以是多个['0.0.0.1:9092','0.0.0.2:9092','0.0.0.3:9092' ]
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))

for i in range(3):
    msg = "msg%d" % i
    producer.send('test', {msg: msg})

producer.close()
```


## 消费者：
```python
# -*- coding:utf-8 -*-

from kafka import KafkaConsumer

consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])
for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
```

先启动消费者，再启动生产者，可以看到消费者程序可以正常消费消息。

## 消费者-json 数据
```python
# -*- coding:utf-8 -*-

import json

from kafka import KafkaConsumer

consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('ascii')))
for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
```

key 同样支持 json 格式生产和消费，只需指定 `key_serializer` 和 `key_deserializer`。

## 消费者-读取最早可读消息
```python
# -*- coding:utf-8 -*-

from kafka import KafkaConsumer

consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')
for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
```

earliest 移到最早的可用消息，latest 最新的消息。

## 消费者-手动设置偏移量
```python
# -*- coding:utf-8 -*-

from kafka import KafkaConsumer
from kafka.structs import TopicPartition

consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])

# 获取test主题的分区信息
print consumer.partitions_for_topic('test')
# 获取主题列表
print consumer.topics()
# 获取当前消费者订阅的主题
print consumer.subscription()
# 获取当前消费者topic、分区信息
print consumer.assignment()
# 获取当前主题的最新偏移量
print consumer.position(TopicPartition(topic='test', partition=0))
# 重置偏移量，从第1个偏移量消费
consumer.seek(TopicPartition(topic='test', partition=0), 1)
for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
```

## 消费者-订阅多个主题
```python
# -*- coding:utf-8 -*-

from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'])

# 订阅要消费的主题
consumer.subscribe(topics=['test', 'test0'])
for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
```

## 消费者-手动拉取消息
```python
# -*- coding:utf-8 -*-

import time

from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'])

# 订阅要消费的主题
consumer.subscribe(topics=['test', 'test0'])
while True:
    msg = consumer.poll(timeout_ms=5)
    print msg
    time.sleep(1)
```

## 消费者-消息挂起与恢复
```python
# -*- coding:utf-8 -*-

import time

from kafka import KafkaConsumer
from kafka.structs import TopicPartition

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'])

# 订阅要消费的主题
consumer.subscribe(topics=['test'])
# 这句要有，否则报 KeyError: TopicPartition(topic='test', partition=0)
consumer.topics()
consumer.pause(TopicPartition(topic='test', partition=0))

num = 0
while True:
    print num
    # 获取当前挂起的消费者
    print consumer.paused()

    msg = consumer.poll(timeout_ms=5)
    print msg
    time.sleep(1)

    num = num + 1
    if num == 10:
        consumer.resume(TopicPartition(topic='test', partition=0))
        print "resume...... "
```


## 消费者组：
```python
# -*- coding:utf-8 -*-

from kafka import KafkaConsumer

consumer = KafkaConsumer('test', group_id='my-group', bootstrap_servers=['localhost:9092'])
for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
```
启动多个消费者，消费组可以横向扩展提高处理能力。

启动程序之后，执行下面命令，即可看到消费者组列表：
```
/usr/local/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```