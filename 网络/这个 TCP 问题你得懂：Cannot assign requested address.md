**原文链接：** [这个 TCP 问题你得懂：Cannot assign requested address](https://mp.weixin.qq.com/s/-cThzr5N2w3IEYYf-duCDA)

微信群里一阵骚动，响声震天。

我心想，虽然是周五，并且到了下班点，但也不至于这么兴奋吧。

打开微信一看，心凉半截，全是报系统 `403` 错误的消息。别说下班了，怕是老板会让我永远下班吧。

别慌，在长期的团队协作训练中，我明白了一个道理：稳住我们能赢。

冷静下来之后，我仔细分析了一下问题的原因。

`403` 说明权限不足，也就是说我们的子系统到鉴权中心拉取权限失败了。直接登录到子系统服务器，手动执行拉取权限程序，的确是拉不到。

我的推测没有问题，难道网络不通了？`telnet` 目标端口试试，然后 Linux 给我返回了这个错误信息：

> Cannot assign requested address

### 原因

产生这个错误的原因是由于 Linux 分配的客户端连接端口用尽，无法建立 socket 连接导致的。

我们都知道，建立一个连接需要四个部分：目标 IP，目标端口，客户端 IP 和客户端端口。其中前三项是不变的，只有客户端端口不断变化。

那么在大量频繁建立连接时，而端口又不是立即释放，默认是 60s，就会出现客户端端口不够用的情况。

这就是这个问题的本质。

接下来使用两个命令来验证一下：

查看连接数：

```shell
# netstat -ae | wc -l
# netstat -ae | grep TIME_WAIT | wc -l
```

查看可用端口范围：

```shell
# sysctl -a | grep port_range
net.ipv4.ip_local_port_range = 50000    65000
```

结果就是连接数是远大于可用端口数的。

### 解决

怎么解决呢？有两个方案：

1. 调低 TIME_WAIT 时间
2. 调高可用端口范围

#### 调低 TIME_WAIT 时间

编辑内核文件 `/etc/sysctl.conf`，增加以下内容：

```
// 表示开启 SYN Cookies。当出现 SYN 等待队列溢出时，启用 cookies 来处理，
// 可防范少量 SYN 攻击，默认为 0，表示关闭；
net.ipv4.tcp_syncookies = 1 
// 表示开启重用。允许将 TIME-WAIT sockets 重新用于新的 TCP 连接，默认为 0，表示关闭；
net.ipv4.tcp_tw_reuse = 1 
// 表示开启 TCP 连接中 TIME-WAIT sockets 的快速回收，默认为 0，表示关闭。
net.ipv4.tcp_tw_recycle = 1 
// 修改系默认的 TIMEOUT 时间，默认为 60s 
net.ipv4.tcp_fin_timeout = 30
```

#### 调高可用端口范围

编辑内核文件 `/etc/sysctl.conf`，增加以下内容：

```
// 表示用于向外连接的端口范围。设置为 1024 到 65535。
net.ipv4.ip_local_port_range = 1024 65535 
```

最后，执行 `sysctl -p` 使参数生效。

### 复盘

我通过增加可用端口范围，顺利将问题解决，看来可以正常下班了。

但是还没完，为什么会突然有这么多连接呢？通过分析日志发现，过去一段时间，我的一个同事疯狂请求系统接口，应该就是这个操作引起的，问了一下原来是在爬数据。好家伙直接来硬的，找我提供一个 API 不香吗？

不过这也反应了我们的系统也太过脆弱，一个小爬虫就给搞挂了。分析了线上代码，觉得有三个地方应该优化：

1. 每次请求鉴权中心不应该都建立新的连接，而是应该复用之前的连接，比如单例模式；
2. 权限相对来说是变化不频繁的，子系统应该建立本地缓存，而不是每次实时请求；
3. 不止要对 `POST` 接口设置频率限制，`GET` 接口也应该限制。

剩下的事就是优化代码了，不过，先开心的过个周末再说。

---

文章中的脑图和源码都上传到了 GitHub，有需要的同学可自行下载。

**地址：** https://github.com/yongxinz/tech-blog

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