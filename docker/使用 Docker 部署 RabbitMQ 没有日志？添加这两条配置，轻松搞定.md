# 使用 Docker 部署 RabbitMQ 没有日志？添加这两条配置，轻松搞定

使用 Docker 部署完 RabbitMQ 服务，到 `/var/log/rabbitmq` 目录下一看，空空如也，并没有日志文件生成。

是没有日志吗？并非如此，日志都打在了标准输出上。使用如下命令可以查看：

```shell
# docker logs -f container_name
```

但平时运维的时候不可能这样来看，太麻烦了。

这里就有一个疑问了，为什么打在了标准输出上，而不是输出到文件呢？

RabbitMQ 有两个配置来定义日志输出：

- `RABBITMQ_LOG_BASE`：日志文件输出路径
- `RABBITMQ_LOGS`：具体的日志文件

而在 Docker 中又有些不同，在 [Github](https://github.com/rabbitmq/rabbitmq-server/blob/v3.7.26/scripts/rabbitmq-server) 上查看源码可以看到下面一段代码：

```shell
# If $RABBITMQ_LOGS is '-', send all log messages to stdout. This is
# particularly useful for Docker images.

if [ "$RABBITMQ_LOGS" = '-' ]; then
    SASL_ERROR_LOGGER=tty
    RABBIT_LAGER_HANDLER=tty
    RABBITMQ_LAGER_HANDLER_UPGRADE=tty
else
    SASL_ERROR_LOGGER=false
    RABBIT_LAGER_HANDLER='"'${RABBITMQ_LOGS}'"'
    RABBITMQ_LAGER_HANDLER_UPGRADE='"'${RABBITMQ_UPGRADE_LOG}'"'
fi
```

意思是 `RABBITMQ_LOGS` 如果配置成了 `-`，日志就会输出到标准输出。

到我的容器中打印一看，也的确如此。

```shell
# docker exec -it rabbitmq /bin/bash
bash-5.0# echo $RABBITMQ_LOGS
-
bash-5.0#
```

原因搞清楚之后，解决起来就简单了，只要在 docker-compose 文件中添加两项配置即可。

```yml
version: '2'

services:
  rabbitmq:
    container_name: rabbitmq
    image: rabbitmq:3.7-management-alpine
    restart: always
    environment:
      - RABBITMQ_DEFAULT_USER=username
      - RABBITMQ_DEFAULT_PASS=password
      - RABBITMQ_LOGS=
      - RABBITMQ_LOG_BASE=/var/log/rabbitmq
    volumes:
      - /var/log/rabbitmq:/var/log/rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
```

`RABBITMQ_LOGS` 参数可以直接留空，重启服务之后，就有日志文件了。

**题图：**该图片由 <a href="https://pixabay.com/zh/users/vietnguyenbui-12326427/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=5430070">Văn Long Bùi</a>在  <a href="https://pixabay.com/zh/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=5430070">Pixabay</a> 上发布

**源码文件：**

https://github.com/rabbitmq/rabbitmq-server/blob/v3.7.26/scripts/rabbitmq-server

**参考文档：**

https://blog.csdn.net/fvdfsdafdsafs/article/details/110097643

**往期精彩：**

