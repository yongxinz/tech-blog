# 使用 docker-compose 部署 Redis 服务

项目 Docker 化部署的最后一步，就差 Redis 了。本来以为是一件很简单的事，没想到折腾了我大半天的时间，下面就来分享分享我的采坑经历。

docker-compose 文件：

```yml
version: '3'

services:
  redis:
    image: redis:3.2.12
    container_name: redis
    restart: always
    network_mode: host
    command: redis-server /etc/redis.conf
    ports:
      - 6379:6379
    volumes:
      - /data:/data
      - ./redis.conf:/etc/redis.conf
```

当前目录下执行：

```shell
# docker-compose up
```

本来以为服务一启，事情就这么愉快的结束了，但是，报错。

> Can't open the log file: No such file or directory

原因就是 redis.conf 文件直接用的是在物理机上部署时用的，`logfile` 参数配的是 `/var/lib/redis`，但 docker 容器里没有这个目录，但是有 `/data` 目录，所以，把 `logfile` 配置成 `/data` 即可。

改完之后再一启，没有任何信息输出，看来是成功了。

`docker ps` 看看，没有容器。

这下给我整懵了，咋回事呢？其实报错都不怕，就怕启动不成功，还没有报错信息。

就这个问题给我折腾了好久，突然灵光一闪，想到 redis 会不会是以后台进程起的，导致容器直接退出。

检查一下配置文件中的 `daemonize` 参数，果然是 `yes`。改成 `no` 之后，就可以正常启动了。

就这么个破问题，卡了这么长时间，而且这类问题之前还遇到过，真是让人郁闷。

至此，项目中的所有服务就都 Docker 化部署了。

**往期精彩：**

