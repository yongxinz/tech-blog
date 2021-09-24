**原文链接：** [被 Docker 日志坑惨了](https://mp.weixin.qq.com/s/3Tkc15dTCEDUAZaZ88pcSQ)

最近在读《计算机程序的构造和解释》，里面有一句话：代码必须能够被人阅读，只是机器恰巧可以执行。

我也想到了一句话：BUG 一定能够被人写出，只是恰好我写的多而已。

说多了都是泪，来看看我最近遇到的一个问题。

### 问题

普通的一天，打开普通的电脑，登录一台普通的服务器，敲下一条普通的命令。

在我使用命令补全时，出现了一条不普通的提示：

```
-bash: cannot create temp file for here-document: No space left on device ls -bash
```

怎么磁盘满了？

使用 `df -h` 一看还真是。

什么原因呢？

### 解决

首先，查找一下系统里的大文件，看看是哪个小可爱搞的鬼。

```
du -sh /* | grep G
```

很快就定位到了这个目录：`/var/lib/docker/containers`。

原来是 Docker 这家伙，这个目录下存放的都是容器运行过程中产生的日志。

使用下面命令来给这些文件按大小排个序：

```
du -d1 -h /var/lib/docker/containers | sort -h

32K	/var/lib/docker/containers/d607c06e475191fff1abd0c2b4b672e7fe8a96cb197f4e8557b18600de2e60af
36K	/var/lib/docker/containers/0d4321106721b9d26335fefef7b9e8e23629691684a4da2f953ac8223c8240c3
36K	/var/lib/docker/containers/7525aab4aa917aa1016169114762261726ac7b9cc712bef35cdc7035b50d20ce
36K	/var/lib/docker/containers/9252e1c373d59ef5613c2b6122eb6e43aa2bd822bd2c199aa67d6eb659c4adb7
142M	/var/lib/docker/containers
142M	/var/lib/docker/containers/15700ee92cd2831554b9a1e78127df0f07248c1498d35c17525407bc8a98bc1a
```

文件名称就是容器 ID，每个文件对应一个容器，也就可以定位到，具体是哪个容器产生了大量的日志。

使用这个命令可以将大文件快速清空：

```
sh -c "cat /dev/null > ${log_file_name}"
```

但是清空了文件哪算解决问题，新的日志还在源源不断往日志里打呢。看了看日志内容，很熟悉。前两天为了调试程序，刚加的一条 `print`。

编辑代码，删除 `print`，重启容器。好了，日志不再疯狂追加了。

为什么 `print` 语句将日志都输出到文件里了呢？别着急，后面再来详细介绍。

先处理一下眼前的问题，放任日志无限增长是肯定不行的，需要有一个单个文件大小限制。否则，明天张三再加一条 `print`，磁盘又满了。

这里有两个方案：

1. 单一容器配置
2. 全局配置

#### 单一容器配置

启动容器时，通过参数来控制日志的文件个数和单个文件的大小：

```
docker run -it --log-opt max-size=10m --log-opt max-file=3 redis
```

但这样做是比较麻烦的，更多的采用的是全局配置的方式。

#### 全局配置

编辑 `/etc/docker/daemon.json`：

```json
{
    "log-driver":"json-file",
    "log-opts":{
        "max-size" :"50m",
        "max-file":"3"
    }
}
```

重启 Docker 服务：

```
systemctl daemon-reload
systemctl restart docker
```

**注意：** 已存在的容器不会生效，需要重建才可以。

接下来再说说上文提到的 `print` 问题。

### Docker 日志

Docker  日志分为两类：

- Docker 引擎日志（也就是 dockerd 运行时的日志）
- 容器的日志，容器内的服务产生的日志

#### 引擎日志

Docker 引擎日志一般是交给了 Upstart(Ubuntu 14.04) 或者 systemd (CentOS 7, Ubuntu 16.04)。前者一般位于 /var/log/upstart/docker.log 下，后者一般通过 `journalctl -u docker` 进行查看。

不同系统的位置都不一样，网上有人总结了一份列表，我修正了一下，可以参考：

系统 | 日志位置
---|---
Ubuntu(14.04) | /var/log/upstart/docker.log
Ubuntu(16.04) |	journalctl -u docker.service
CentOS 7/RHEL 7/Fedora |	journalctl -u docker.service
CoreOS |	journalctl -u docker.service
OpenSuSE |	journalctl -u docker.service
OSX |	~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-
Debian GNU/Linux 7 |	/var/log/daemon.log
Debian GNU/Linux 8 |	journalctl -u docker.service
Boot2Docker |	/var/log/docker.log

#### 容器日志

使用下面命令可以显示当前运行的容器的日志信息：

```
docker logs CONTAINER
```

UNIX 和 Linux 命令有三种输入输出，分别是 STDIN、STDOUT 和 STDERR。`docker logs` 显示的内容包含 STDOUT 和 STDERR。

在生产环境下，如果我们的应用输出到日志文件里，那么我们在使用 `docker logs` 时一般收集不到太多重要的信息。

这里来看一下 nginx 和 httpd 是怎么做的：

- nginx 官方镜像，使用了一种方式，让日志输出到 STDOUT，也就是创建一个符号链接 /var/log/nginx/access.log 到 /dev/stdout。
- httpd 使用的是让其输出到指定文件，正常日志输出到 /proc/self/fd/1 (STDOUT) ，错误日志输出到 /proc/self/fd/2 (STDERR)。

当日志量比较大的时候，使用 `docker logs` 来查看日志，会对 docker daemon 造成比较大的压力，容易导致容器创建慢等一系列问题。

只有使用了 local 、json-file、journald 日志驱动的容器才可以使用 `docker logs` 捕获日志，使用其他日志驱动无法使用 `docker logs`。

Docker 默认使用 json-file 作为日志驱动。

除此之外，Docker 还提供了很多其他日志驱动，这里就不过多介绍。还有日志管理方案，我也不是很有经验，大家如果感兴趣的话自己搜搜看吧。


---


**参考文章：**

1. https://www.cnblogs.com/zhangmingcheng/p/13960496.html
2. https://www.cnblogs.com/operationhome/p/10907591.html

文章中的脑图和源码都上传到了 GitHub，有需要的同学可自行下载。

**地址：** [https://github.com/yongxinz/tech-blog](https://github.com/yongxinz/tech-blog)

关注公众号 **AlwaysBeta**，回复「**goebook**」领取 Go 编程经典书籍。

<center class="half">
    <img src="https://github.com/yongxinz/gopher/blob/main/alwaysbeta.JPG" width="300"/>
</center>

**Go 专栏文章列表：**

1. [Go 专栏｜开发环境搭建以及开发工具 VS Code 配置](https://mp.weixin.qq.com/s/x1OW--3mwSTjgB2HaKGVVA)
2. [Go 专栏｜变量和常量的声明与赋值](https://mp.weixin.qq.com/s/cIceTj02bGa0BYqu-JN1Bg)
3. [Go 专栏｜基础数据类型：整数、浮点数、复数、布尔值和字符串](https://mp.weixin.qq.com/s/aotpxglSGRFfl6A1xPN-dw)
4. [Go 专栏｜复合数据类型：数组和切片 slice](https://mp.weixin.qq.com/s/MnjIeJPUAA6n48o4yns3hg)
5. [Go 专栏｜复合数据类型：字典 map 和 结构体 struct](https://mp.weixin.qq.com/s/1unl6K9xHxy4V3KukORC3A)
6. [Go 专栏｜流程控制，一网打尽](https://mp.weixin.qq.com/s/TbjT1dmTvwiKCzzbWc23kA)
7. [Go 专栏｜函数那些事](https://mp.weixin.qq.com/s/RKpyVrhtSk9pXMWNVpWYjQ)
8. [Go 专栏｜错误处理：defer，panic 和 recover](https://mp.weixin.qq.com/s/qYZXfAifBxwl1cDDaP0FNA)
9. [Go 专栏｜说说方法](https://mp.weixin.qq.com/s/qvFipY0pnmqxok6CVKquvg)
10. [Go 专栏｜接口 interface](https://mp.weixin.qq.com/s/g7ngRIxxbd-M8K_sL_M4KQ)
11. [Go 专栏｜并发编程：goroutine，channel 和 sync](https://mp.weixin.qq.com/s/VG4CSfT2OfxA6nfygWLSyw)