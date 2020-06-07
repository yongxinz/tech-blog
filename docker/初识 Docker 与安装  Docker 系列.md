# 初识 Docker 与安装 | Docker 系列

如果想要快速持续开发和部署应用，那么对 Docker 这个词肯定不陌生，2015 年的时候我研究过一段时间，但后来由于工作内容的变更，就没有再关注过了。

今年开始，项目每周都会升级上线，虽然写了很多自动化脚本，但依然感觉很麻烦，所以就想是不是可以通过 Docker 来优化一下这个流程。

说干就干，最近读了两本书：《Docker 技术入门与实战》和《Docker 进阶与实战》，以及在测试环境的验证，也算是有了点心得，所以在这里总结一下，分享给大家。

后续计划把线上环境都迁移到 Docker 上，也会边实践边总结，并且记录在这里。

Docker 是一个开源项目，诞生于 2013 年初，最初是 dotCloud 公司内部的一个业余项目。它基于 Google 公司推出的 Go 语言实现。 项目后来加入了 Linux 基金会，遵从了 Apache 2.0 协议，项目代码在 [GitHub](https://github.com/docker/docker) 上进行维护。

Docker 的口号是：

> Build,Ship,and Run Any App,Anywhere

因此也看得出来，使用 Docker 之后，会使开发和部署变得更加便捷。基本就是镜像在手，到哪都可以运行，再也不用担心环境的问题了。

Docker 涉及到的概念有这么几个：镜像，容器，仓库，容器卷，Dockerfile 等。如果之前接触过，那对这几个概念肯定不会陌生，没接触过也没关系，后续文章会一一进行介绍。

下面来看看 Docker 和传统虚拟化方式的不同之处：

![](https://ww1.sinaimg.cn/large/0061a0TTly1gfjk4102b4j30yh0ljwis.jpg)

可见容器是在操作系统层面上实现虚拟化，直接复用本地主机的操作系统，而传统方式则是在硬件层面实现。

Docker 安装也非常简单，直接到 [Docker 官网](https://docs.docker.com/get-docker/)，不管是 Mac，Windows 还是 Linux，要么是有安装包，要么就是有详细的教程，按着一步一步来就没有问题。

![](https://ww1.sinaimg.cn/large/0061a0TTly1gfjk4z7dfzj30mz0feju5.jpg)

其实啊，在网上看再多的博客，也包括我这篇，都不如直接看官方文档，既实时，又权威。

这篇就到这里吧，下篇来说说镜像。

**参考文档：**

https://docs.docker.com/

**往期精彩：**

