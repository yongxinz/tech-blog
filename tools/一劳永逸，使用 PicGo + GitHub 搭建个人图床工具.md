**原文链接：** [一劳永逸，使用 PicGo + GitHub 搭建个人图床工具](https://mp.weixin.qq.com/s/AMpRm2s_wyLZ48fkRhkqgQ)

经常写博客的同学都知道，有一个稳定又好用的图床是多么重要。我之前用过七牛云 + Mpic 和微博图床，但总感觉配置起来比较麻烦，用起来也不是很顺手。而且更让人担心的是，万一有一天图床服务不能用了怎么办？那之前的图片岂不是都挂了。

直到遇到了 PicGo + GitHub，彻底打消了我的所有顾虑，而且配置简单，使用优雅。背靠 GitHub 和微软，稳定性问题基本不用担心。还有就是支持 Windowns，macOS 和 Linux 平台。

唯一的缺点，如果算的话，就是隐密性问题。因为所有图片都是上传到了 GitHub 的一个公有仓库，如果在意这点的话就不太适合。不过我上传的都是技术文章中的配图，这一点对我来说根本不是问题。

下面就来手把手教大家如何配置，非常简单。

### 配置 GitHub

新建仓库：

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/sc_20211206094511.png)

这里需要注意：仓库得设置为 Public 。因为后面通过客户端访问算是外部访问，因此无法访问 Private ，这样的话图片传上来之后只能存储不能显示。

仓库建好之后，点击页面右上角，进入 Settings：

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/sc_20211206094703.png)

然后进入 Developer settings：

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/sc_20211206094803.png)

点击 Personal access tokens，再点 Generate new token 新建 token。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/sc_20211206095015.png)

填写 Notes 信息，选择 token 过期时间，为了安全，GitHub 会强烈建议不要设置成永久。这个大家根据自己实际情况选择，到期之后重新生成即可。

复选框的话，repo 一定要全选，其他的无所谓，我是都勾选了。

确定之后，就生成我们需要的 token 了。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/sc_20211206095447.png)

### 配置 PicGo

下载 PicGo：点击[下载地址](https://github.com/Molunerfinn/PicGo)，然后安装。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/sc_20211206095654.png)

- 设定仓库名：上文在 GitHub 创建的仓库。
- 设定分支名：main。
- 设定 Token：上文生成的 token。
- 指定存储路径：为空的话会上传到跟目录，也可以指定路径。
- 设定自定义域名：可以为空，这里为了使用 CDN 加快图片的访问速度，按这样格式填写：https://cdn.jsdelivr.net/gh/GitHub 用户名/仓库名

配置完成后就可以使用了。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/sc_20211206095710.png)

直接拖拽，或者点击上传都可以。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/sc_20211206105226.png)

上传成功之后，在 GitHub 的仓库就可以看到了。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/sc_20211206104502.png)

最后，在相册里复制外链，粘贴到我们的 markdown 文档中，就可以看到图片了。

希望各位老板玩的愉快。


---


**热情推荐：**

- **[技术博客](https://github.com/yongxinz/tech-blog)：** 硬核后端技术干货，内容包括 Python、Django、Docker、Go、Redis、ElasticSearch、Kafka、Linux 等。
- **[Go 程序员](https://github.com/yongxinz/gopher)：** Go 学习路线图，包括基础专栏，进阶专栏，源码阅读，实战开发，面试刷题，必读书单等一系列资源。
- **[面试题汇总](https://github.com/yongxinz/backend-interview)：** 包括 Python、Go、Redis、MySQL、Kafka、数据结构、算法、编程、网络等各种常考题。