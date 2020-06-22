# 操作 Docker 容器 | Docker 系列

前文回顾：

- [初识 Docker 与安装 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/初识 Docker 与安装  Docker 系列.md>)
- [使用 Docker 镜像 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/使用 Docker 镜像  Docker 系列.md>)

有了镜像的基础，下面就开始创建容器吧。Docker 容器非常轻量级，随时都可以创建和删除，非常方便。

### 创建并启动容器

使用 `docker run` 命令来创建并启动一个容器：

```shell
$ docker run -it centos /bin/echo 'hello world'
hello world
```

`-t` 参数让 Docker 分配一个伪终端，并绑定到容器的标准输入上，`-i` 参数让容器的标准输入持续打开。

```shell
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                     PORTS               NAMES
df84684c3888        centos              "/bin/echo 'hello wo…"   10 seconds ago      Exited (0) 7 seconds ago                       admiring_noyce
```

`docker ps` 命令列出当前的容器，可以看到，刚刚执行的容器输出完信息之后就直接退出了。那有没有办法让容器在后台执行呢？答案当然是可以的。

使用 `-d` 参数让容器在后台，以守护进程的方式执行，这也是在工作中最常用到的。

```shell
$ docker run -d centos /bin/sh -c "while true; do echo hello world; sleep 1; done"
fcb07a324388d58883e212ff5675ad7947a22c731f677d1a37ff7bc3d8bfa9a7

$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
fcb07a324388        centos              "/bin/sh -c 'while t…"   6 seconds ago       Up 5 seconds                            beautiful_northcutt
```

这样容器就在后台运行了。

还有一种方式，使用 `docker create` 命令创建容器，然后使用 `docker start` 来启动容器，两条命令相当于 `docker run` 一条，这种方式不常用，就不做更多介绍了。

下面聊聊 `docker run` 背后的故事，到底这一条命令背后，Docker 都为我们做了哪些操作呢？

- 检查本地是否存在指定镜像，不存在就从公有仓库下载；
- 使用镜像创建并启动一个容器；
- 分配一个文件系统，并在只读的镜像层外面挂载一层可读写层；
- 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中；
- 从地址池配置一个 IP 地址给容器；
- 执行用户指定的命令或应用程序；
- 执行完毕后容器被终止。

### 进入容器

当容器以后台方式执行时，使用 `docker exec` 命令进入到容器中。

```shell
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
fcb07a324388        centos              "/bin/sh -c 'while t…"   6 seconds ago       Up 5 seconds                            beautiful_northcutt

$ docker exec -it fcb07a324388 /bin/bash
[root@fcb07a324388 /]# ls
bin  dev  etc  home  lib  lib64  lost+found  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
[root@fcb07a324388 /]#
```

进入到容器之后，就是一个 Linux 系统，Linux 支持的命令，容器也基本都支持。

这条命令还是比较重要的，有时候我们的应用出问题了，单纯通过 logs 看不出问题的话，就需要我们进入容器，来看看实际情况。

想退出的话，直接 `exit` 命令就可以了。

还有一个命令是 `docker attach`，但是它有一个缺点。当多个窗口同时 attach 到同一个容器时，所有窗口都会同步显示，当某个窗口因命令阻塞时，其他窗口也无法执行操作。

所以，这个命令现在基本也不用了。

### 停止容器

使用 `docker stop` 命令来停止一个容器。

```shell
$ docker stop fcb
fcb
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                       PORTS               NAMES
fcb07a324388        centos              "/bin/sh -c 'while t…"   23 minutes ago      Exited (137) 4 seconds ago                       beautiful_northcutt
```

如果再想启动的话，使用 `docker start`。

### 查看容器

上文已经介绍过了，使用 `docker ps` 命令查看当前容器。

使用 `docker logs` 查看容器日志输出。

使用 `docker container inspect` 命令查看容器的详细信息。

使用 `docker top` 命令查看容器内进程信息，类似 Linux 下的 top 命令。

使用 `docker stats` 命令查看容器 CPU，内存，储存等信息。

使用 `docker container port` 查看容器的端口映射情况。

### 导入和导出容器

使用 `docker export` 命令导出一个容器到文件。

```shell
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
fcb07a324388        centos              "/bin/sh -c 'while t…"   34 minutes ago      Up 9 minutes                            beautiful_northcutt
$ docker export -o centos.tar fcb
$ ls
centos.tar
```

使用 `docker import` 命令将容器文件导入成本地镜像。

```shell
$ docker import centos.tar test/centos
sha256:f994c062dae063ffb8c97191d951b9beaac73d99023120191dbbc9741d725578
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
test/centos         latest              f994c062dae0        6 seconds ago       237MB
```

在上一篇文章中介绍了一个 `docker load` 命令，同样是将文件导入成本地镜像，那二者有什么区别呢？

容器快照文件将丢弃所有历史记录和元数据信息，而镜像存储文件将保存完整记录，但体积更大。

### 删除容器

使用 `docker rm` 命令来删除已经停止的容器，如果容器正在运行，可以加 `-f` 参数进行强制删除。

**参考文档：**

书籍《Docker 技术入门与实战》

[http://www.dockerinfo.net/docker%e5%ae%b9%e5%99%a8-2](http://www.dockerinfo.net/docker容器-2)

**往期精彩：**

