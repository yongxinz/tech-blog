# 使用数据卷管理数据 | Docker 系列

前文回顾：

- [初识 Docker 与安装 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/初识 Docker 与安装  Docker 系列.md>)
- [使用 Docker 镜像 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/使用 Docker 镜像  Docker 系列.md>)
- [操作 Docker 容器 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/操作 Docker 容器  Docker 系列.md>)

众所周知，容器是随时创建随时删除的，那删除时容器里的数据怎么办呢？每次手动备份出来？当然不需要，Docker 非常贴心的提供了数据持久化方案，叫数据卷 volume。

使用 volume 有四大优势：

- volume 可以在容器之间以及容器和主机之间共享和重用。

- volume 在某一挂载的位置被修改，所有使用该 volume 的地方都会同时更新。

- volume 的更新不会影响镜像。

- volume 会一直存在，直到没有任何容器使用它，才能使用 `docker volume rm [volumes名字]` 命令删除。

可以看到，除了数据持久化之外，还有很重要的一个点是同步主机的文件到容器，并能够实时更新。这样就可以把源代码目录挂载到容器中，当有代码需要修改时，直接改本地代码就自动同步到容器了，在开发测试时非常方便。

### 创建数据卷

使用 `docker volume create` 命令创建数据卷：

```shell
$ docker volume create --name test
```

### 查看数据卷

使用 `docker volume ls` 命令查看数据卷列表：

```shell
$ docker volume ls
DRIVER              VOLUME NAME
local               test
```

使用 `docker volume inspect` 查看数据卷详情：

```shell
$ docker volume inspect test
[
    {
        "CreatedAt": "2020-06-22T10:25:46Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/test/_data",
        "Name": "test",
        "Options": {},
        "Scope": "local"
    }
]
```

从详情就能看出来，持久化的数据都在 `/var/lib/docker/volumes` 目录下了。

测试这个地方的时候还出现了一点小插曲，在 Linux 下完全没问题，但在我自己的 Mac 电脑上，虽然详情已经显示挂载目录了，但 `cd` 过去却怎么也找不到这个目录。

原因在于，在 Mac 上，Docker 启了一个虚拟机来运行实际的 Docker 进程，那么怎么登录到 Docker 虚拟机呢？使用下面这条命令：

```shell
$ screen ~/Library/Containers/com.docker.docker/Data/vms/0/tty
```

如果 docker 版本小于 18.06，使用下面的命令：

```shell
$ screen ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty
```

执行完命令之后会到一个新的界面，按回车键就进入 Docker 虚拟机了，这下目录就找到了。

```shell
docker-desktop:~#
docker-desktop:~# cd /var/lib/docker/volumes/
docker-desktop:/var/lib/docker/volumes# ls
metadata.db  test
```

### 绑定数据卷

启动容器时可以使用 `-v 主机:容器` 进行数据卷绑定：

```shell
$ docker run -d -v test:/root centos /bin/sh -c "while true; do echo hello world; sleep 1; done"

$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
75f5a72a2f21        centos              "/bin/sh -c 'while t…"   44 hours ago        Up 44 hours                             charming_curie
```

查看容器详情，可以看到具体的绑定信息：

```shell
$ docker inspect 75f

...
			 "Mounts": [
            {
                "Type": "volume",
                "Name": "test",
                "Source": "/var/lib/docker/volumes/test/_data",
                "Destination": "/root",
                "Driver": "local",
                "Mode": "z",
                "RW": true,
                "Propagation": ""
            }
        ],
...
```

其中，主机目录可以是 volume 名称，也可以具体路径，例如：

```shell
$ docker run -d -v /home/test:/root centos /bin/sh -c "while true; do echo hello world; sleep 1; done"
```

这样，对应目录下的文件变更都会得到同步。

### 删除数据卷

使用 `docker volume rm` 命令来删除数据卷。

使用 `docker volume prune` 命令来清理无用的数据卷。

### 数据卷容器

如果要在多个容器之间共享数据，可以使用数据卷容器。说白了就是启一个容器，这个容器专门来供其他容器挂载使用。

首先，创建一个容器 dbdata，并创建一个数据卷挂载到 dbdata：

```shell
$ docker run -it -v /dbdata --name dbdata centos
```

使用 `--volumes-from` 参数启动其他容器：

```shell
$ docker run -it --volumes-from dbdata --name db1 centos

$ docker run -it --volumes-from dbdata --name db2 centos
```

这样就可以了，三个容器，只要有一个容器的 dbdata 目录有变化，其他容器都可以同步。

**参考文档：**

https://www.jianshu.com/p/8c22cdfc0ffd

书籍《Docker 技术入门与实战》

**往期精彩：**

- [初识 Docker 与安装 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/初识 Docker 与安装  Docker 系列.md>)
- [使用 Docker 镜像 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/使用 Docker 镜像  Docker 系列.md>)
- [操作 Docker 容器 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/操作 Docker 容器  Docker 系列.md>)

