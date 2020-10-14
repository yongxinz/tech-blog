# 使用 docker-compose 部署多机 RabbitMQ 集群

本文介绍 RabbitMQ 集群的 Docker 化部署，最开始是想通过 DockerSwarm 方式来部署的，但是 RabbitMQ 节点加入集群时一直失败，在网上找了很多办法，始终没有解决这个问题，无奈只能放弃。所以最终采用配置 hosts 文件方式来保证节点之间的通信，下面来进行详细说明。

### 部署环境

- 系统：CentOS8
- 两台服务器：10.1.1.1/10.1.1.2

### docker-compose 文件

```python
version: '3'

services:
  rabbit1:
    container_name: rabbit1
    image: rabbitmq:3.7-management-alpine
    restart: always
    hostname: rabbit1
    extra_hosts:
      - "rabbit1:10.1.1.1"
      - "rabbit2:10.1.1.2"
    environment:
      - RABBITMQ_ERLANG_COOKIE=MY_COOKIE
      - RABBITMQ_DEFAULT_USER=MY_USER
      - RABBITMQ_DEFAULT_PASS=MY_PASS
    ports:
      - "4369:4369"
      - "5671:5671"
      - "5672:5672"
      - "15671:15671"
      - "15672:15672"
      - "25672:25672"
```

这样，10.1.1.1 上的 docker-compose 文件就写好了，部署另一台时，只要将 `rabbit1` 改成 `rabbit2` 就可以了。如果是更多台服务器的话，也是同样的道理，将 IP 配置到 `extra_hosts` 参数下即可。

### 启动服务

在两台服务器上分别执行：

```
# docker-compose up -d
```

### 加入集群

如果将 `rabbit1` 作为主节点的话，需要在 `rabbit2` 上执行命令，将其加入到集群，如下：

```
# docker exec -it rabbit2 /bin/bash

rabbit2# rabbitmqctl stop_app
rabbit2# rabbitmqctl reset
rabbit2# rabbitmqctl join_cluster rabbit@rabbit1
rabbit2# rabbitmqctl start_app
```

默认情况下，RabbitMQ 启动后是磁盘节点，如果想以内存节点方式加入，可以加 `--ram` 参数。

如果想要修改节点类型，可以使用命令：

```shell
# rabbitmqctl change_cluster_node_type disc(ram)
```

修改节点类型之前需要先 `rabbitmqctl stop_app`。

通过下面命令来查看集群状态：

```shell
# rabbitmqctl cluster_status
```

注意，由于 RAM 节点仅将内部数据库表存储在内存中，因此在内存节点启动时必须从其他节点同步这些数据，所以一个集群必须至少包含一个磁盘节点。

### HAProxy 负载均衡

ha 同样采用 Docker 方式来部署，先看一下 haproxy.cfg 配置文件：

```python
# Simple configuration for an HTTP proxy listening on port 80 on all
# interfaces and forwarding requests to a single backend "servers" with a
# single server "server1" listening on 127.0.0.1:8000

global
    daemon
    maxconn 256

defaults
    mode http
    timeout connect 5000ms
    timeout client 5000ms
    timeout server 5000ms

listen rabbitmq_cluster
    bind 0.0.0.0:5677
    option tcplog
    mode tcp
    balance leastconn
    server  rabbit1 10.1.1.1:5672 weight 1 check inter 2s rise 2 fall 3
    server  rabbit2 10.2.2.2:5672 weight 1 check inter 2s rise 2 fall 3

listen http_front
    bind 0.0.0.0:8002
    stats uri /haproxy?stats

listen rabbitmq_admin
    bind 0.0.0.0:8001
    server rabbit1 10.1.1.1:15672
    server rabbit2 10.1.1.2:15672
```

再看一下 docker-compose 文件：

```yaml
version: '3'

services:
  haproxy:
    container_name: rabbit-haproxy
    image: haproxy
    restart: always
    hostname: haproxy
    network_mode: rabbitmq_default
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg
    ports:
      - "5677:5677"
      - "8001:8001"
      - "8002:8002"
```

启动之后，就可以通过 ha 的地址来访问 RabbitMQ 集群管理页面了。

如果公司内部有现成的负载均衡，比如 LVS，那么也可以省略这一步。

其实到这里，集群就可以正常使用了，但还有很重要的一点需要做些说明。

### 集群模式

#### 普通模式

- 对于 Queue 来说，消息实体只存在于其中一个节点，A、B 两个节点仅有相同的元数据，即队列结构。
- 当消息进入 A 节点的队列中后，消费者从 B 节点拉取时，RabbitMQ 会临时在 A、B 间进行消息传输，把 A 中的消息实体取出并经过 B 发送给消费者。
- 所以，消费者应尽量连接每一个节点，从中取消息。即对于同一个逻辑队列，要在多个节点建立物理队列，否则，无论消费者连 A 或者连 B，出口总在 A，会产生瓶颈。
- 该模式还存在一个问题就是当 A 节点故障后，B 节点无法取到 A 节点中还未消费的消息实体。
- 如果做了消息持久化，那么得等 A 节点恢复，才可被消费；如果没有持久化的话，消息会丢失。

#### 镜像模式

- 该模式解决了上述问题，其和普通模式不同之处在于，消息实体会主动在镜像节点间同步，而不是在消费者取数据时临时拉取。
- 该模式带来的副作用也很明显，除了降低系统性能外，如果镜像队列数量过多，加之大量的消息进入，集群内部的网络带宽将会被这种同步通讯大大消耗掉。
- 所以，在对可靠性要求较高的场合中适用于该模式。

个人感觉，在生产环境中，还是使用镜像模式比较保险。

要想使用镜像模式，不管是通过管理页面，还是命令行方式，只需要简单配置即可完成。管理页面方式就不过多介绍了，下面说说如何通过命令行来设置，一条命令就搞定。

添加：

```shell
# rabbitmqctl set_policy -p testvhost testha "^" '{"ha-mode":"all","ha-sync-mode":"automatic"}'
Setting policy "testha" for pattern "^" to "{"ha-mode":"all","ha-sync-mode":"automatic"}" with priority "0" for vhost "testvhost" ...
```

清除：

```shell
# rabbitmqctl clear_policy -p testvhost testha
Clearing policy "testha" on vhost "testvhost" ...
```

查看：

```shell
# rabbitmqctl list_policies -p testvhost
Listing policies for vhost "testvhost" ...
vhost   name    pattern apply-to        definition      priority
testvhost       testha  ^       all     {"ha-mode":"all","ha-sync-mode":"automatic"}    0
```

参数说明：

- Virtual host：策略应用的 vhost。

- Name：为策略名称，可以是任何名称，但建议使用不带空格的基于 ASCII 的名称。

- Pattern：与一个或多个 queue（exchange） 名称匹配的正则表达式，可以使用任何正则表达式。只有一个 `^` 代表匹配所有，`^test` 为匹配名称为 "test" 的 exchanges 或者 queue。

- Apply to：Pattern 应用对象。

- Priority：配置多个策略时的优先级，值越大，优先级越高。没有指定优先级的消息会以 0 优先级对待，对于超过队列所定最大优先级的消息，优先级以最大优先级对待。

- Definition：键/值对，将被插入匹配 queues and exchanges 的可选参数映射中。

  `ha-mode`：策略键，分为 3 种模式：

    - `all` ：所有的 queue。
    - `exctly` ：部分（需配置 `ha-params` 参数，此参数为 int 类型。比如 3，众多集群中的随机 3 台机器）。
    - `nodes` ：指定（需配置 `ha-params` 参数，此参数为数组类型。比如 ["rabbit@rabbit2", "rabbit@rabbit3"] 这样指定为 rabbit2 与 rabbit3 这两台机器）。

  `ha-sync-mode`：队列同步：

    - `manual`：手动（默认模式）。新的队列镜像将不会收到现有的消息，它只会接收新的消息。
    - `automatic`：自动同步。当一个新镜像加入时，队列会自动同步。队列同步是一个阻塞操作。

以上就是本篇全部内容，欢迎大家留言交流。