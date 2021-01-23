# 使用 Docker 部署 canal 服务，实现 MySQL 数据库 binlog 日志解析

canal 是阿里巴巴开源的一个项目，主要用途是基于 MySQL 数据库 binlog 日志解析，提供增量数据订阅和消费。

基于日志增量订阅和消费的业务包括：

- 数据库镜像
- 数据库实时备份
- 索引构建和实时维护（拆分异构索引、倒排索引等）
- 业务 cache 刷新
- 带业务逻辑的增量数据处理

我这边主要在两个场景下使用：

一个是将变更数据实时同步到 Elasticsearch 和 Redis，这样做的好处还是挺明显的。

这里先说一下我目前的做法，一方面是全量数据定时同步，由于数据量比较大，同步时间比较长，所以数据也就不够实时。第二个方面是针对单条数据的变更，部分更新 Elasticsearch 和 Redis 的逻辑都是直接写在了业务代码中，耦合比较严重。

拆出来之后就可以实现实时增量更新，而且还可以解耦，收益还是很大的。

第二个是保存某些重点关注数据的历史变更。

这个目前用在了「资产管理」模块，通过记录 IP 资产的创建，变更以及删除，实现 IP 生命周期管理，方便历史信息回溯。

### MySQL 配置

修改 MySQL 配置文件 my.cnf，开启 binlog 写入功能，并配置模式为 ROW。

```python
log-bin=mysql-bin # 开启 binlog
binlog-format=ROW # 选择 ROW 模式
server_id=1 # 配置 MySQL replaction 需要定义，不要和 canal 的 slaveId 重复
```

重启数据库，查看配置是否生效。

```sql
mysql> show variables like 'binlog_format';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| binlog_format | ROW   |
+---------------+-------+
1 row in set (0.19 sec)
mysql>
mysql> show variables like 'log_bin';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| log_bin       | ON    |
+---------------+-------+
1 row in set (0.00 sec)
mysql>
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000003 |     4230 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
```

然后创建用户，并授权。

```sql
mysql> CREATE USER canal IDENTIFIED BY 'canal';
mysql> GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'canal'@'%%';
mysql> FLUSH PRIVILEGES;
mysql> show grants for 'canal'@'%%';
+----------------------------------------------------------------------------+
| Grants for canal@%%                                                        |
+----------------------------------------------------------------------------+
| GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO `canal`@`%%` |
+----------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### canal 服务端

拉取镜像：

```python
# docker pull canal/canal-server:v1.1.4
```

然后用官方提供的 shell 脚本直接启动：

```python
# sh run.sh -e canal.auto.scan=false -e canal.destinations=test -e canal.instance.master.address=127.0.0.1:3306 -e canal.instance.dbUsername=canal -e canal.instance.dbPassword=canal -e canal.instance.connectionCharset=UTF-8 -e canal.instance.tsdb.enable=true -e canal.instance.gtidon=false
```

但每次都这样启动还是有点麻烦，我们可以写一个 docker-compose 文件，如下：

```yaml
version: '3'

services:
  canal-server:
    image: canal/canal-server:v1.1.4
    container_name: canal-server
    restart: unless-stopped
    network_mode: host
    ports: 
      - 11111:11111
    environment:
      - canal.auto.scan=false
      - canal.instance.master.address=127.0.0.1:3306
      - canal.instance.dbUsername=canal
      - canal.instance.dbPassword=canal
      - canal.instance.filter.regex=.*\\..*
      - canal.destinations=test
      - canal.instance.connectionCharset=UTF-8
      - canal.instance.tsdb.enable=true
    volumes:
      - /root/canal/test/log/:/home/admin/canal-server/logs/
```

启动服务：

```python
# docker-compose up
Recreating canal-server ... done
Attaching to canal-server
canal-server    | DOCKER_DEPLOY_TYPE=VM
canal-server    | ==> INIT /alidata/init/02init-sshd.sh
canal-server    | ==> EXIT CODE: 0
canal-server    | ==> INIT /alidata/init/fix-hosts.py
canal-server    | ==> EXIT CODE: 0
canal-server    | ==> INIT DEFAULT
canal-server    | Generating SSH1 RSA host key: [  OK  ]
canal-server    | Starting sshd: [  OK  ]
canal-server    | Starting crond: [  OK  ]
canal-server    | ==> INIT DONE
canal-server    | ==> RUN /home/admin/app.sh
canal-server    | ==> START ...
canal-server    | start canal ...
canal-server    | start canal successful
canal-server    | ==> START SUCCESSFUL ...
```

### canal Python 客户端

直接 Copy 官方提供的客户端代码：

```python
import time

from canal.client import Client
from canal.protocol import EntryProtocol_pb2
from canal.protocol import CanalProtocol_pb2

client = Client()
client.connect(host='127.0.0.1', port=11111)
client.check_valid(username=b'', password=b'')
client.subscribe(client_id=b'1001', destination=b'test', filter=b'.*\\..*')

while True:
    message = client.get(100)
    entries = message['entries']
    for entry in entries:
        entry_type = entry.entryType
        if entry_type in [EntryProtocol_pb2.EntryType.TRANSACTIONBEGIN, EntryProtocol_pb2.EntryType.TRANSACTIONEND]:
            continue
        row_change = EntryProtocol_pb2.RowChange()
        row_change.MergeFromString(entry.storeValue)
        event_type = row_change.eventType
        header = entry.header
        database = header.schemaName
        table = header.tableName
        event_type = header.eventType
        for row in row_change.rowDatas:
            format_data = dict()
            if event_type == EntryProtocol_pb2.EventType.DELETE:
                for column in row.beforeColumns:
                    format_data = {
                        column.name: column.value
                    }
            elif event_type == EntryProtocol_pb2.EventType.INSERT:
                for column in row.afterColumns:
                    format_data = {
                        column.name: column.value
                    }
            else:
                format_data['before'] = format_data['after'] = dict()
                for column in row.beforeColumns:
                    format_data['before'][column.name] = column.value
                for column in row.afterColumns:
                    format_data['after'][column.name] = column.value
            data = dict(
                db=database,
                table=table,
                event_type=event_type,
                data=format_data,
            )
            print(data)
    time.sleep(1)

client.disconnect()
```

### 功能验证

首先在 MySQL 里边创建一张测试表，然后再增删改几条测试数据：

```sql
mysql> create database test;
mysql> use test;
mysql> CREATE TABLE `role` (   `id` int unsigned NOT NULL AUTO_INCREMENT,   `role_name` varchar(255)
DEFAULT NULL,   PRIMARY KEY (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
mysql> insert into role (id, role_name) values (10, 'admin');
Query OK, 1 row affected (0.01 sec)

mysql> update role set role_name='hh' where id = 10;
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> delete from role where id = 10;
Query OK, 1 row affected (0.01 sec)
```

客户端打印输出：

```python
$ python canal_client.py
connected to 127.0.0.1:11111
Auth succed
Subscribe succed


header {
  version: 1
  logfileName: "mysql-bin.000003"
  logfileOffset: 5497
  serverId: 1
  serverenCode: "UTF-8"
  executeTime: 1607843285000
  sourceType: MYSQL
  eventLength: 75
}
entryType: TRANSACTIONBEGIN
storeValue: " \217\001"

header {
  version: 1
  logfileName: "mysql-bin.000003"
  logfileOffset: 5630
  serverId: 1
  serverenCode: "UTF-8"
  executeTime: 1607843285000
  sourceType: MYSQL
  schemaName: "test"
  tableName: "role"
  eventLength: 47
  eventType: INSERT
  props {
    key: "rowsCount"
    value: "1"
  }
}
entryType: ROWDATA
storeValue: "\010\322\001\020\001P\000bN\022 \010\000\020\004\032\002id \001(\0010\000B\00210R\014int unsigned\022*\010\001\020\014\032\trole_name \000(\0010\000B\005adminR\014varchar(255)"

{'db': 'test', 'table': 'role', 'event_type': 1, 'data': {'role_name': 'admin'}}
header {
  version: 1
  logfileName: "mysql-bin.000003"
  logfileOffset: 5677
  serverId: 1
  serverenCode: "UTF-8"
  executeTime: 1607843285000
  sourceType: MYSQL
  eventLength: 31
}
entryType: TRANSACTIONEND
storeValue: "\022\003440"
```

变更一条数据，输出内容分三部分，分别是：TRANSACTIONBEGIN，ROWDATA 和 TRANSACTIONEND。然后我们比较关注的内容都在 ROWDATA 中，解析出来之后就是我们需要的，包括数据库名，表名和变更内容。

其中 event_type 字段 1 表示新增，2 表示更新，3 表示删除。

`update` 对应输出：

```python
{'db': 'test', 'table': 'role', 'event_type': 2, 'data': {'before': {'id': '10', 'role_name': 'hh'}, 'after': {'id': '10', 'role_name': 'hh'}}}
```

`delete` 对应输出：

```python
{'db': 'test', 'table': 'role', 'event_type': 3, 'data': {'role_name': 'hh'}}
```

canal 服务端启动之后，在 `/home/admin/canal-server/logs/test` 目录下会生成两个日志文件，分别是：meta.log 和 test.log，可以查看服务是不是正常，有没有报错信息。其中 test 是启动 Docker 时 `canal.destinations` 设置的名称。

```python
# cat meta.log
2020-12-13 14:55:18.051 - clientId:1001 cursor:[mysql-bin.000003,4805,1607842360000,1,] address[/127.0.0.1:3306]
2020-12-13 14:55:33.051 - clientId:1001 cursor:[mysql-bin.000003,5096,1607842531000,1,] address[127.0.0.1:3306]
2020-12-13 14:57:07.051 - clientId:1001 cursor:[mysql-bin.000003,5387,1607842625000,1,] address[127.0.0.1:3306]

# cat test.log
2020-12-13 14:55:09.067 [main] INFO  c.a.otter.canal.instance.core.AbstractCanalInstance - start successful....
2020-12-13 14:55:09.144 [destination = test , address = /127.0.0.1:3306 , EventParser] WARN  c.a.o.c.p.inbound.mysql.rds.RdsBinlogEventParserProxy - ---> begin to find start position, it will be long time for reset or first position
2020-12-13 14:55:09.144 [destination = test , address = /127.0.0.1:3306 , EventParser] WARN  c.a.o.c.p.inbound.mysql.rds.RdsBinlogEventParserProxy - prepare to find start position just show master status
2020-12-13 14:55:09.693 [destination = test , address = /127.0.0.1:3306 , EventParser] WARN  c.a.o.c.p.inbound.mysql.rds.RdsBinlogEventParserProxy - ---> find start position successfully, EntryPosition[included=false,journalName=mysql-bin.000003,position=4699,serverId=1,gtid=,timestamp=1607842360000] cost : 538ms , the next step is binlog dump
```

### 踩坑记录

在我自己搭建的测试环境一切正常，但放到项目 beta 环境上还是遇到了一个问题：

> [fetch failed by table meta:`schemeName`.`tableName`]

查了一下说是由于表删除，或者是表结构变更引起的解析错误，增加一条配置就可以解决：

```python
canal.instance.filter.table.error=true
```

加上之后，报错信息的确都没有了，但消费出来的数据没有 ROWDATA，这个地方确实困扰了我很长时间。

说实话，有的时候调试程序，并不怕碰到报错，怕的是没有报错，然后程序还不正常。

后来，我把忽略表错误的配置删除，又仔细看了一遍日志，发现还有一个报错：

> Caused by: java.io.IOException: ErrorPacket [errorNumber=1142, fieldCount=-1, message=SHOW command denied to user 

这明显就是权限不够嘛，问了一下我们的 DBA，果然如此，我们的 binlog 账号默认是没有 select 权限的，加上之后，问题就成功解决了。

静下心来仔细看日志是多么重要。

以上，下篇会说说对接 MQ 的事。

**参考文档：**

https://github.com/alibaba/canal

https://github.com/haozi3156666/canal-python

**往期精彩：**

