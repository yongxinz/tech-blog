# 解决 Django 多进程下，logging 记录日志错乱问题

之前写过一篇文章 [Django 中如何优雅的记录日志]([<https://github.com/yongxinz/tech-blog/blob/master/django/Django%20%E4%B8%AD%E5%A6%82%E4%BD%95%E4%BC%98%E9%9B%85%E7%9A%84%E8%AE%B0%E5%BD%95%E6%97%A5%E5%BF%97.md>])，本以为代码上线之后，就可以愉快的看日志，通过日志来分析问题了，但现实总是跟想象不同，两个异常现象纷纷挥起大手，啪啪地打在我的脸上。

两个异常如下：

1. 日志写入错乱；
2. 日志并没有按天分割，而且还会丢失。

在网上查找一些资料，发现了原因所在：

> Django logging 是基于 Python logging 模块实现的，logging 模块是线程安全的，但不能保证多进程安全。我的 Django 项目是通过 uwsgi 启的多进程，所以就发生了上述两个问题。

下面来详细描述一下这个异常过程，假设我们每天生成一个日志文件 error.log，每天凌晨进行日志分割。那么，在单进程环境下是这样的：

1. 生成 error.log 文件；
2. 写入一天的日志；
3. 零点时，判断 error.log-2020-05-15 是否存在，如果存在则删除；如果不存在，将 error.log 文件重命名为 error.log-2020-05-15；
4. 重新生成 error.log 文件，并将 logger 句柄指向新的 error.log。

再来看看多进程的情况：

1. 生成 error.log 文件；
2. 写入一天的日志；
3. 零点时，1 号进程判断 error.log-2020-05-15 是否存在，如果存在则删除；如果不存在，将 error.log 文件重命名为 error.log-2020-05-15；
4. 此时，2 号进程可能还在向 error.log 文件进行写入，由于写入文件句柄已经打开，所以会向 error.log-2020-05-15 进行写入；
5. 2 号进程进行文件分割操作，由于 error.log-2020-05-15 已经存在，所以 2 号进程会将它删除，然后再重命名 error.log，这样就导致了日志丢失；
6. 由于 2 号进程将 error.log 重命名为 error.log-2020-05-15，也会导致 1 号进程继续向 error.log-2020-05-15 写入，这样就造成了写入错乱。

原因清楚了，那么，有什么解决办法呢？两个方案：

## 使用 concurrent-log-handler 包

这个包通过加锁的方式实现了多进程安全，并且可以在日志文件达到特定大小时，分割文件，但是不支持按时间分割。

包的源码我并没有仔细研究，也就没办法再细说了，大家如果感兴趣的话可以自己找来看。

由于我的需求是按时间进行分割，显然就不能用了，自己写吧。

## 重写 TimedRotatingFileHandler

通过上面的分析可以知道，出问题的点就是发生在日志分割时，一是删文件，二是没有及时更新写入句柄。

所以针对这两点，我的对策就是：一是去掉删文件的逻辑，二是在切割文件时，及时将写入句柄更新到最新。

**代码如下：** 

```python
# 解决多进程日志写入混乱问题


import os
import time
from logging.handlers import TimedRotatingFileHandler


class CommonTimedRotatingFileHandler(TimedRotatingFileHandler):

    @property
    def dfn(self):
        currentTime = int(time.time())
        # get the time that this sequence started at and make it a TimeTuple
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." + time.strftime(self.suffix, timeTuple))

        return dfn

    def shouldRollover(self, record):
        """
        是否应该执行日志滚动操作：
        1、存档文件已存在时，执行滚动操作
        2、当前时间 >= 滚动时间点时，执行滚动操作
        """
        dfn = self.dfn
        t = int(time.time())
        if t >= self.rolloverAt or os.path.exists(dfn):
            return 1
        return 0

    def doRollover(self):
        """
        执行滚动操作
        1、文件句柄更新
        2、存在文件处理
        3、备份数处理
        4、下次滚动时间点更新
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple

        dfn = self.dfn

        # 存档log 已存在处理
        if not os.path.exists(dfn):
            self.rotate(self.baseFilename, dfn)

        # 备份数控制
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)

        # 延迟处理
        if not self.delay:
            self.stream = self._open()

        # 更新滚动时间点
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval

        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            dstNow = time.localtime(currentTime)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
```

在 settings handles 中引入上面 class 即可。

生产环境已经上线了两周，运行稳定，没有再发生异常。

以上。

**参考文档：** 

https://www.jianshu.com/p/665694966025

https://juejin.im/post/5e1303026fb9a0482c4ea59f#heading-5

**往期精彩：**

