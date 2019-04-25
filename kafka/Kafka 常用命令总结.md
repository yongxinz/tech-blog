在 0.9.0.0 之后的 Kafka，出现了几个新变动，一个是在 Server 端增加了 GroupCoordinator 这个角色，另一个较大的变动是将 topic 的 offset 信息由之前存储在 zookeeper 上改为存储到一个特殊的 topic（__consumer_offsets）中。

本文测试版本：kafka_2.11-2.2.0

## 启动 Kafka 
后台常驻方式，带上参数 `-daemon`，如： 
```
/usr/local/kafka/bin/kafka-server-start.sh -daemon /usr/local/kafka/config/server.properties
```

指定 JMX port 端口启动，指定 jmx，可以方便监控 Kafka 集群
```
JMX_PORT=9991 /usr/local/kafka/bin/kafka-server-start.sh -daemon /usr/local/kafka/config/server.properties
```

## 停止 Kafka
```
/usr/local/kafka/bin/kafka-server-stop.sh
```

## Topic
### 创建 Topic
参数 `--topic` 指定 Topic 名，`--partitions` 指定分区数，`--replication-factor` 指定备份数：
```
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
```

注意，如果配置文件 server.properties 指定了 Kafka 在 zookeeper 上的目录，则参数也要指定，否则会报无可用的 brokers（下面部分命令也有同样的情况），如：
```
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181/kafka --replication-factor 1 --partitions 1 --topic test
```

### 列出所有 Topic
```
/usr/local/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181 
```

### 查看 Topic
```
/usr/local/kafka/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test 
```

### 增加 Topic 的 partition 数
```
/usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic test --partitions 5 
```

### 查看 topic 指定分区 offset 的最大值或最小值
time 为 -1 时表示最大值，为 -2 时表示最小值： 
```
/usr/local/kafka/bin/kafka-run-class.sh kafka.tools.GetOffsetShell --topic test --time -1 --broker-list 127.0.0.1:9092 --partitions 0 
```

### 删除 Topic
```
/usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --topic test --delete 
```

## 生产消息 
```
/usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test 
```

## 消费消息

### 从头开始
```
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```
### 从尾部开始
从尾部开始取数据，必需要指定分区：
```
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --offset latest --partition 0
```
### 指定分区
```
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --offset latest --partition 0
```
### 取指定个数
```
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --offset latest --partition 0 --max-messages 1 
```

## 消费者 Group
### 指定 Group
```
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test -group test_group --from-beginning
```
### 消费者 Group 列表
```
/usr/local/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

### 查看 Group 详情
```
/usr/local/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test_group --describe
```

输出：
```
Consumer group 'test_group' has no active members.

TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID     HOST            CLIENT-ID
test            0          5               5               0               -               -               -

# CURRENT-OFFSET: 当前消费者群组最近提交的 offset，也就是消费者分区里读取的当前位置
# LOG-END-OFFSET: 当前最高水位偏移量，也就是最近一个读取消息的偏移量，同时也是最近一个提交到集群的偏移量
# LAG：消费者的 CURRENT-OFFSET 与 broker 的 LOG-END-OFFSET 之间的差距
```

### 删除 Group 中 Topic
```
/usr/local/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test_group --topic test --delete
```

### 删除 Group 
```
/usr/local/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test_group --delete
```

## 平衡 leader 

```
/usr/local/kafka/bin/kafka-preferred-replica-election.sh --bootstrap-server localhost:9092
```

## 自带压测工具
```
/usr/local/kafka/bin/kafka-producer-perf-test.sh --topic test --num-records 100 --record-size 1 --throughput 100 --producer-props bootstrap.servers=localhost:9092 
```
