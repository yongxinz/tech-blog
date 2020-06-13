# 使用 Docker 镜像 | Docker 系列

前文回顾：

- [初识 Docker 与安装 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/初识 Docker 与安装  Docker 系列.md>)

今天来说说镜像，镜像是 Docker 中特别重要的概念，是容器运行的基础，没有镜像，后面的一切都不成立。

典型的镜像表示方法分三部分，用 `/` 分隔：

```python
remote image hub/namespace/name:tag
```

- remote image hub：存储镜像的 Web 服务器地址；
- namespace：命名空间，表示一个用户或组织下的所有镜像；
- name：镜像名称；
- tag：镜像标签。

其实，我们常看到的镜像是长这样的 `name:tag`，因为从 Docker 官方仓库拉下来的镜像，是可以省略前两部分的。

### 获取镜像

使用 `docker pull name[:tag]` 命令来下载镜像，如果不显式指定 tag，则默认会选择 latest 标签。

```shell
$ docker pull busybox
Using default tag: latest
latest: Pulling from library/busybox
76df9210b28c: Pull complete
Digest: sha256:95cf004f559831017cdf4628aaf1bb30133677be8702a8c5f2994629f637a209
Status: Downloaded newer image for busybox:latest
docker.io/library/busybox:latest
```

### 查看镜像信息

使用 `docker images` 命令列出本机镜像。

```shell
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
busybox             latest              1c35c4412082        6 days ago          1.22MB
```

镜像 ID 十分重要，它唯一标识了镜像。

使用 `docker tag` 命令来给本地镜像添加新的标签。

```shell
$ docker tag busybox:latest mybusybox:latest

$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
busybox             latest              1c35c4412082        6 days ago          1.22MB
mybusybox           latest              1c35c4412082        6 days ago          1.22MB
```

可以看到，现在本地的两个镜像 ID 是相同的，表示它们指向了同一个镜像，只是标签不同而已。

使用 `docker inspect` 命令来获取镜像的详细信息。

使用 `docker history` 命令列出镜像各层的创建信息。

### 搜索镜像

使用 `docker search` 命令来搜索镜像。

```shell
$ docker search centos
NAME                               DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
centos                             The official build of CentOS.                   6039                [OK]
ansible/centos7-ansible            Ansible on Centos7                              130                                     [OK]
consol/centos-xfce-vnc             Centos container with "headless" VNC session…   116                                     [OK]
jdeathe/centos-ssh                 OpenSSH / Supervisor / EPEL/IUS/SCL Repos - …   114                                     [OK]
centos/mysql-57-centos7            MySQL 5.7 SQL database server                   76
imagine10255/centos6-lnmp-php56    centos6-lnmp-php56                              58                                      [OK]
```

### 删除和清理镜像

使用 `docker rmi` 命令来删除镜像，分两种方式：一种是通过镜像名和标签来删除；一种是通过镜像 ID 来删除。平时使用过程中，大部分都是通过镜像 ID 来删除。

```shell
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
busybox             latest              1c35c4412082        8 days ago          1.22MB
mybusybox           latest              1c35c4412082        8 days ago          1.22MB

$ docker rmi mybusybox:latest
# 或者
$ docker rmi 1c35c4412082
```

如果镜像被容器引用了的话，是无法删除的，需要先删除依赖该镜像的容器，然后再删除镜像。或者比较暴力的话，直接使用 `-f` 参数来删除，也能达到效果，但还是不推荐这种做法。

使用 `docker image prune` 命令来清理系统中遗留的一些临时镜像，以及一些没有被使用的镜像。

### 创建镜像

创建镜像有三种方式：

- 基于已有容器创建
- 基于本地模板导入
- 基于 Dockerfile 创建

1、基于已有容器创建

```shell
# 运行一个容器
$ docker run -it centos /bin/bash

# 在容器中创建一个文件，然后退出
[root@f0767e2e8964 /]# touch text.txt
[root@f0767e2e8964 /]# exit
exit

# 查看容器
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                     PORTS               NAMES
f0767e2e8964        centos              "/bin/bash"         17 seconds ago      Exited (0) 4 seconds ago                       stupefied_ptolemy

# 基于容器创建镜像
$ docker commit -a 'add file' f0767e2e8964 centos:1.0
sha256:a651491d9bfe6d00eef7a23bd290be839d59efafa31183ef2038399271dee459

# 查看除了原有镜像，还有新生成的镜像，标签不同
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
centos              1.0                 a651491d9bfe        4 seconds ago       237MB
centos              latest              470671670cac        4 months ago        237MB
```

2、基于本地模板导入

使用 `docker import` 命令将模板导入成镜像。

3、基于 Dockerfile 创建

这是在实际工作中使用最多的方法，先卖个关子，后续单独写一篇来详细介绍。

### 存出和载入镜像

使用 `docker save` 命令保存镜像到文件。

```shell
$ docker save -o busybox.tar busybox
```

执行之后，在当前目录下就会有 busybox.tar 文件了，然后可以把这个文件分享给其他人。

收到文件之后，使用 `docker load` 命令来载入镜像。

```shell
$ docker load < busybox.tar
```

### 上传镜像

使用 `docker push` 命令将镜像上传到镜像仓库，这样在其他服务器上想用这个镜像，直接 `docker pull` 一下就可以了，非常方便。

默认的话，会上传到 Docker Hub 官方仓库，我们也可以搭建自己的私有仓库。一般来说，公司内部都会有自己的镜像仓库，我们根据需求来使用就可以了。

这篇就到这里吧，下篇来说说容器。

**参考书籍：**

- 《Docker 技术入门与实战》
- 《Docker 进阶与实战》

**往期精彩：**

[初识 Docker 与安装 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/初识 Docker 与安装  Docker 系列.md>)

