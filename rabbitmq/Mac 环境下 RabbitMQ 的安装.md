技术博客：[https://github.com/yongxinz/tech-blog](https://github.com/yongxinz/tech-blog)

同时，也欢迎关注我的微信公众号 **AlwaysBeta**，更多精彩内容等你来。

![](https://user-gold-cdn.xitu.io/2020/1/17/16fb0d4a31ae61a6?w=258&h=258&f=jpeg&s=20946)

几个月之前，手上的一个项目开始使用 RabbitMQ，没错，就是跟兔子跑得一样快的一个消息队列。

之前并没有做系统的学习，只是了解一些简单用法，网上找一些例子，加上自己的加工，基本也可以满足常规的使用需求。

但有一个问题是，队列有时会出现积压的情况，但我却不能及时知道。所以必须得时不时去看看队列是否还在正常消费，让人十分烦躁。

于是决定痛定思痛，系统学习一下，包括环境搭建，消息消费的几种模式，监控等内容，并整理成文章分享到这里。

不会有太多理论上的知识，更多是从实战出发，直接通过代码来说明问题，希望对大家能有帮助。

本篇文章先介绍一下在 Mac 环境下，怎么安装 RabbitMQ。

一般来说，安装分为两种方式：

1. 下载 RabbitMQ 源文件，解压源文件之后进行安装。
1. 通过 brew 命令安装。

在这里，我当然是推荐使用 brew 来安装，非常强大的 Mac 端包管理工具。

如果还没安装 brew 的小伙伴，可以先安装 brew，这是官网，首页上就有安装命令。

![](https://ww1.sinaimg.cn/large/0061a0TTly1gd8glvkiw9j31gv0r2go9.jpg)

有了 brew 之后，只需要一个简单的命令就搞定了。

```python
brew install rabbitmq
```

这样就表示安装成功了。

![](https://ww1.sinaimg.cn/large/0061a0TTly1gd7rbicqquj31400c2mz8.jpg)

安装的路径是 `/usr/local/Cellar/rabbitmq/3.8.3`，具体情况要视版本而定，我安装的版本是 3.8.3。

接下来就可以启动了，进入安装目录，执行命令：

```python
./sbin/rabbitmq-server
```

启动成功，就是这么简单。

![](https://ww1.sinaimg.cn/large/0061a0TTly1gd7rc63rxvj31400a1gnf.jpg)

接下来可以在浏览器打开 http://localhost:15672，可以看到 RabbitMQ 的管理页面。

![](https://ww1.sinaimg.cn/large/0061a0TTly1gd7rct2b2uj31400m4774.jpg)

管理页面还是包含很多内容和功能的，如果我们向队列里发消息，便可以通过管理页面来查看消息消费情况。后续文章中还会涉及到这点，到时候再来说明。

以上。

**参考连接：**

- RabbitMQ 官网：https://www.rabbitmq.com/
- Homebrew 官网：https://brew.sh/
