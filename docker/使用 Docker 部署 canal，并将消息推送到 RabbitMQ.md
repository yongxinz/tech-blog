# 使用 Docker 部署 canal，并将消息推送到 RabbitMQ

上一篇已经介绍了使用 Docker 部署 canal 服务，实现 MySQL 数据库 binlog 日志解析，并且用官方提供的客户端程序成功读到了消息。但在生产环境下还不能这么用，更好的做法是将消息发送到消息队列，然后再从消息队列消费。

这里我选择的是 RabbitMQ。

原来看官方文档发现只支持 Kafka 和 RocketMQ，但好在最新版 1.1.5 也支持了 RabbitMQ，而且镜像也已经打好了。

如果使用 Docker 部署的话，直接拉取最新的镜像即可。

### 配置 canal

第一步拉取镜像：

```shell
# docker pull canal/canal-server:latest
```

然后启动容器，从容器中拷贝出配置文件：

```shell
# docker cp canal-server:/home/admin/canal-server/conf/canal.properties ./
# docker cp canal-server:/home/admin/canal-server/conf/test/instance.properties ./
```

修改 `canal.properties` 文件，配置输出到 RabbitMQ，有以下几处要改：

```python
# 指定 RabbitMQ
canal.serverMode = rabbitMQ

# RabbitMQ 配置
rabbitmq.host = 127.0.0.1
rabbitmq.virtual.host = /
rabbitmq.exchange = exchange.canal
rabbitmq.username = xxxx
rabbitmq.password = xxxx
```

这里有两点需要说明，一是我在网上找的很多文章，关于 RabbitMQ 的配置都是这样的：

```python
canal.mq.servers = xxx
canal.mq.vhost = /
canal.mq.exchange = exchange.canal
canal.mq.username = admin
canal.mq.password = admin
```

但是我这样配置并不成功，也可能是版本的问题，我没有更多去验证。

第二个是目前 RabbitMQ 的配置还不支持端口，只能使用默认端口 5672。

接下来修改 `instance.properties` 文件：

```python
# MySQL 地址 + 端口
canal.instance.master.address=host:port
canal.instance.dbUsername=xxxx
canal.instance.dbPassword=xxxx
# 对应到 RabbitMQ 的话是 Routing key
canal.mq.topic=canal-routing-key
```

docker-compose 文件：

```yaml
version: '3'

services:
  canal-server:
    image: canal/canal-server
    container_name: canal-server
    restart: unless-stopped
    network_mode: host
    ports: 
      - 11111:11111
    volumes:
      - ./canal.properties:/home/admin/canal-server/conf/canal.properties
      - ./instance.properties:/home/admin/canal-server/conf/test/instance.properties
      - ./log/:/home/admin/canal-server/logs/
```

一切就绪，启动服务：

```shell
# docker-compose up -d
```

### 配置 RabbitMQ

首先新建 exchange：

![sc_20201220103714](/Users/zhangyongxin/zyx/alwaysbeta/canal/sc_20201220103714.png)

然后新建队列：

![sc_20201220104505](/Users/zhangyongxin/zyx/alwaysbeta/canal/sc_20201220104505.png)

最后绑定队列：

![sc_20201220103833](/Users/zhangyongxin/zyx/alwaysbeta/canal/sc_20201220103833.png)

这里要注意，Routing key 一定要和之前配置的一致。

到这里，如果顺利的话队列里就应该有消息了。

**参考文档：**

https://www.siques.cn/doc/340

**往期精彩：**

