**原文链接：** [使用 RediSearch 在 Redis 中进行全文检索](https://mp.weixin.qq.com/s/X1qKL0jMaklGw6GLcrkp2g)

Redis 大家肯定都不陌生了，作为一种快速、高性能的键值存储数据库，广泛应用于缓存、队列、会话存储等方面。

然而，Redis 在原生状态下并不支持全文检索功能，这使得处理文本数据变得相对困难。但是在有一些场景下还需要这样的功能，有什么好办法呢？答案就是 RediSearch。

RediSearch 是 Redis 的一个插件，它为 Redis 数据库添加了全文搜索和查询功能，使开发人员能够在 Redis 中高效地执行全文检索操作。

它基于 Redis Module API 构建，通过使用自定义的数据结构和索引算法，实现了高效的全文搜索功能。

## 安装

如果单纯用来测试的话，可以直接通过 docker 来启动；如果是生产环境，就需要根据公司的实际情况来支持了。

```shell
$ docker run -p 6379:6379 redis/redis-stack-server:latest
```

启动服务之后，可以使用 `FT.*` 命令集来体验搜索功能。

## 概览

为了使用全文搜索功能，我们必须将文档存储在哈希中，使用命令 `FT.CREATE` 创建索引并使用 `FT.SEARCH` 做文本搜索。

这样说可能会比较懵，看下面的示意图就明白了：

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/2.webp)

现在，让我们插入两条文档：

```shell
redis-cli 'hset post:1 title "hello world" body "this is a cool document"'
redis-cli 'hset post:2 title "goodbye everybody" body "this is the best document"'
```

上面命令创建两个哈希值，分别是 `post:1` 和 `post:2`，其中包含的字段是 `title` 和 `body`。

## 创建索引

接下来创建索引：

```shell
FT.CREATE post_index prefix 1 post: SCHEMA title TEXT body text
```

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/redisearch-3.png)

在这里，我们创建了 `post_index` 索引，它将索引以 `post:` 前缀开头的所有 Redis 哈希键。只有 `title` 和 `body` 字段才会被索引，并且索引立即生效。

## 搜索索引

使用 `FT.SEARCH` 命令，参数是索引名称和需要搜索的关键词：

```shell
FT.SEARCH post_index "world"
```

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/data/4.webp)

### 实时索引

当新增一个文档时，它会被自动添加到索引：

```shell
redis-cli 'hset post:3 title "really?" body "yeah"'
```

立即可以被搜索到：

```shell
> ft.search post_index "really"
1) (integer) 1
2) "post:3"
3) 1) "title"
   2) "really?"
   3) "body"
   4) "yeah"
```

### 搜索特定字段

可以选择要搜索的字段，比如 `title`：

```shell
ft.search post_index "@title:world"
```

### 按列表中的任何单词搜索

类似于逻辑 `OR` 操作，比如要查找与 `hello` 或 `goodbye` 匹配的所有文档：

```shell
ft.search post_index "hello|goodbye"
```

### 搜索结果分页

和 SQL 是一样的，使用 `LIMIT` 关键词，比如：

```shell
ft.search post_index "world" LIMIT 10, 5
```

### 反向搜索

在搜索关键词前使用 `-` 来排除结果中包含该字段的信息：

```shell
ft.search post_index "-foo"
```

### 部分搜索

还可以使用 `*` 只搜索单词的一部分，比如要查找以 `good` 开头的单词的所有文档：

```shell
ft.search post_index "good*"
```

需要注意的是，这样做仅限于前缀，比如关键词是这样的话 `*good`，是不支持的。

### 模糊匹配

这个功能很强大，它是一种近似的搜索手段，使用 `%`。

假设你把想要查找的单词写错了，把 `world` 写成了 `wold`，它依然能查出来，比如：

```shell
ft.search post_index "%wold%"
```

## 总结

最近在工作中遇到了一个问题，因为数据都存储在了 Redis 中，而且大部分功能都可以满足。但其中有一个接口需要模糊查询，这在 Redis 原生方法中是不容易的。

所以查找了一些资料，了解到 RediSearch，使用一下还是挺方便的，并且完美地解决了我的问题。也把这篇文章分享给大家，希望对大家有帮助。

以上就是本文的全部内容，如果觉得还不错的话欢迎**点赞**，**转发**和**关注**，感谢支持。

***

**参考文章：**

- https://github.com/RediSearch
- https://medium.com/datadenys/full-text-search-in-redis-using-redisearch-31df0deb4f3e

**推荐阅读：**

*   [Go 语言切片是如何扩容的？](https://mp.weixin.qq.com/s/VVM8nqs4mMGdFyCNJx16_g)