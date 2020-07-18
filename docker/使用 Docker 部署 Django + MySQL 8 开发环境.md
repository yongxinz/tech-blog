# 使用 Docker 部署 Django + MySQL 8 开发环境

前一段时间重装了系统，然后我还没有备份，导致电脑里的开发环境全都没有了。

一想到又要装 Python 环境，还要装数据库，然后安装过程中还可能报一堆错就头疼。

最近正在学习 Docker，这不正好解决了我当前的痛点了吗？而且，不止这次重装系统，以后再重装都不怕了，只要拿着 Dockerfile 和 docker-compose 文件，不管到什么环境，一条命令轻松跑起来。

之前部署 Python 开发环境，都是用的 virtualenv，或者是 Pipenv。这次使用 Docker 之后，对比下来，还是 Docker 更加方便，下面就来详细介绍。

### Dockerfile

```dockerfile
FROM python:3.6.8

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code
COPY ./requirements.txt /code

WORKDIR /code

RUN sed -i "s/archive.ubuntu./mirrors.aliyun./g" /etc/apt/sources.list
RUN sed -i "s/deb.debian.org/mirrors.aliyun.com/g" /etc/apt/sources.list

RUN apt-get clean && apt-get -y update && \
    apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev libsnmp-dev
RUN pip3 install --index-url https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt

COPY ./* /code/
```

使用 Dockerfile 来创建镜像，Python 版本是 3.6.8，将源代码拷贝到容器中 `/code` 目录。

### docker-compose

```yaml
version: '3'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    image: web
    container_name: web
    hostname: web
    restart: always
    command: python /code/manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/web
    ports:
      - "8000:8000"
    depends_on:
      - mysql  

  mysql:
    image: mysql
    container_name: mysql
    hostname: mysql
    restart: always
    command: --default-authentication-plugin=mysql_native_password --mysqlx=0
    ports:
      - 3306:3306
    volumes:
      - ./db:/var/lib/mysql
    environment:
      - MYSQL_HOST=localhost 
      - MYSQL_PORT=3306 
      - MYSQL_DATABASE=dev
      - MYSQL_USER=dev
      - MYSQL_PASSWORD=123456
      - MYSQL_ROOT_PASSWORD=123456
```

使用 docker-compose 来编排容器，一共启两个服务，`web` 服务就是后台的 Django 服务，`mysql` 是数据库服务。

有三点需要注意：

- `web` 服务使用 `depends_on` 命令，表示依赖于 `mysql` 服务。
- `mysql` 服务一定要加 `--default-authentication-plugin=mysql_native_password` 命令。因为从 MySQL 8.0 开始，默认的加密规则使用的是 caching_sha2_password，而我们的客户端并不支持。之前使用的是 mysql_native_password。
- 使用 `volumes` 来持久化数据，否则容器删除之后，数据就都丢了。

### requirements

```
Django==2.2.11
mysqlclient==1.4.6
```

启动 Django 需要的 pip 包，Django 版本至少要 2.0，否则会报错。

### Django settings

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dev',
        'USER': 'dev',
        'PASSWORD': '123456',
        'HOST': 'mysql',
        'PORT': '3306'
    }
}
```

在 Django settings 文件中配置数据库信息，内容需要与 docker-compose 中一致。

有一点需要注意，HOST 一定要配置成 docker-compose 中的服务名称，在我这里是 `mysql`。配置成其他，比如 localhost 或者 127.0.0.1 会报错。

因为 Docker 启动时会设置一个本地网络，可以将 `mysql` 解析到对应服务的容器，而对应的服务并不在 localhost 上。

### Run

使用如下命令创建镜像。

```shell
$ docker-compose -f ./docker-compose.yml build
```

也可以省略上一步，直接使用如下命令启动服务，如果没有镜像，会先创建镜像，然后再启动服务。

```shell
$ docker-compose -f ./docker-compose.yml up
```

### 排错

在部署过程中，可能会碰到如下这些错误，基本都是配置错误造成的。如果发生了，一定要仔细检查配置，只要和文中相同，是不会有问题的。

- 'Plugin caching_sha2_password could not be loaded: /usr/lib/x86_64-linux-gnu/mariadb19/plugin/caching_sha2_password.so: cannot open shared object file: No such file or directory'
- django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module.
- django.db.utils.OperationalError: (2002, "Can't connect to MySQL server on 'db' (115)")
- django.db.utils.OperationalError: (2002, "Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)")
- django.db.utils.OperationalError: (2002, "Can't connect to MySQL server on '127.0.0.1' (115)")
- django.db.utils.OperationalError: (2002, "Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)")

我还遇到一个比较坑的问题是这个：

[Warning] root@localhost is created with an empty password ! Please consider switching off the --initialize-insecure option.

我以为是我的密码设置不正确，检查了好久都没发现问题，后来在网上找到了解释，直接忽略就行了。

> That is just a warning printed by during database file initialization ([`mysqld --initialize-insecure`](https://github.com/docker-library/mysql/blob/e51083fa7d44e8aba89a3e37ac38d9cb0595b7d9/5.7/docker-entrypoint.sh#L90-L92)). The root user with password is created later while the database is listening only on the unix socket.



**参考文档：**

http://fusionblender.net/django-and-mysql-8-using-docker/

https://github.com/docker-library/mysql/issues/307

https://www.jianshu.com/p/4eafa4f87fd5

**往期精彩：**

