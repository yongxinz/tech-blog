# 使用 Dockerfile 创建镜像 | Docker 系列

前文回顾：

- [初识 Docker 与安装 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/初识 Docker 与安装  Docker 系列.md>)
- [使用 Docker 镜像 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/使用 Docker 镜像  Docker 系列.md>)
- [操作 Docker 容器 | Docker 系列](<https://github.com/yongxinz/tech-blog/blob/master/docker/操作 Docker 容器  Docker 系列.md>)

之前写镜像的时候说到创建镜像最常用的方式是使用 Dockerfile，这篇就来重点说一下，到底是怎么使用 Dockerfile 来创建的。

### 基本结构

```dockerfile
# 1、第一行必须是 FROM 基础镜像信息
FROM ubuntu
 
# 2、维护者信息
MAINTAINER docker_user docker_user@email.com
 
# 3、镜像操作指令
RUN echo "deb http://archive.ubuntu.com/ubuntu/ raring main universe" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y nginx
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
 
# 4、容器启动执行指令
CMD /usr/sbin/nginx
```

Dockerfile 基本就长这样，当然这是一个很简单的例子，还有很多其他命令会在下个小节介绍。

有几点需要注意，第一行必须是 FROM 命令，表示是基于哪个基础镜像来创建镜像的。第二行一般是 MAINTAINER 命令，表示维护人信息，但不做硬性要求。最后一行是 CMD 命令，表示启动容器执行的命令，CMD 命令必须在最后一行，如果有多个 CMD 命令，则只有最后一个生效。

### 常用指令

**FROM：** 必须是 Dockerfile 的首个命令，定义了使用哪个基础镜像启动构建流程。

**MAINTAINER：** 声明镜像作者。

**COPY：** 将宿主机的文件拷贝到镜像内的指定路径。

**ADD：** 作用类似于 **COPY**。

**COPY** 和 **ADD** 的区别是：**ADD** 命令功能更多，比如拷贝一个压缩包，**ADD** 可以将压缩包解压到镜像内，如果是下载链接，**ADD** 会先下载文件，然后再拷贝。

但现在 docker 官方更推荐使用 **COPY** 命令，一个命令只做一件事。

**WORKDIR：** 指定 Dockerfile 中该命令下的操作所在的工作目录。

**RUN：** 执行命令行命令。

**ENV：** 设置环境变量。

**VOLUME：** 挂载数据卷。

**EXPOSE：** 暴露端口。

**CMD：** 服务启动命令。

### 创建镜像

有了 Dockerfile 之后，在 Dockerfile 所在目录执行命令：

```shell
# docker build -t <image_name> .
```

就这么简单，镜像就创建好了。



**往期精彩：**

