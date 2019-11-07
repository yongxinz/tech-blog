## 简介

随着应用系统规模的不断扩大，对数据的安全性和可靠性也提出更好的要求，rsync 在高端业务系统中也逐渐暴露出了很多不足。

首先，rsync 在同步数据时，需要扫描所有文件后进行比对，进行差量传输。如果文件数量达到了百万甚至千万量级，扫描所有文件将是非常耗时的，并且正在发生变化的往往是其中很少的一部分，这是非常低效的方式。

其次，rsync 不能实时的去监测、同步数据，虽然它可以通过 linux 守护进程的方式进行触发同步，但是两次触发动作一定会有时间差，这样就导致了服务端和客户端数据可能出现不一致，无法在应用故障时完全的恢复数据。

基于以上两种情况，可以使用 rsync+inotify 的组合来解决，可以实现数据的实时同步。

inotify 是一种强大的、细粒度的、异步的文件系统事件控制机制。linux 内核从 2.6.13 起，加入了 inotify 支持。通过 inotify 可以监控文件系统中添加、删除、修改、移动等各种事件，利用这个内核接口，第三方软件就可以监控文件系统下文件的各种变化情况，而 inotify-tools 正是实施监控的软件。在使用 rsync 首次全量同步后，结合 inotify 对源目录进行实时监控，只要有文件变动或新文件产生，就会立刻同步到目标目录下，非常高效实用。

## rsync

### 安装

```python
yum -y install rsync
```

源码方式安装这里不介绍了。

### 常用参数

```python
-v :展示详细的同步信息
-a :归档模式，相当于 -rlptgoD
-r :递归目录
-l :同步软连接文件
-p :保留权限
-t :将源文件的"modify time"同步到目标机器
-g :保持文件属组
-o :保持文件属主
-D :和--devices --specials一样，保持设备文件和特殊文件
-z :发送数据前，先压缩再传输
-H :保持硬链接
-n :进行试运行，不作任何更改
-P same as --partial --progress
    --partial :支持断点续传
    --progress :展示传输的进度
--delete :如果源文件消失，目标文件也会被删除
--delete-excluded :指定要在目的端删除的文件
--delete-after :默认情况下，rsync是先清理目的端的文件再开始数据同步；如果使用此选项，则rsync会先进行数据同步，都完成后再删除那些需要清理的文件。
--exclude=PATTERN :排除匹配PATTERN的文件
--exclude-from=FILE :如果要排除的文件很多，可以统一写在某一文件中
-e ssh :使用SSH加密隧道传输
```

### 部署使用

- 服务器A： 192.168.0.1
- 服务器B： 192.168.0.2

这里有两台 linux 服务器，我们可以先假定 A 作为服务端，B 作为客户端。

1、服务端配置：

修改服务端的配置文件：`/etc/rsyncd.conf`，内容如下：

```python
# rsync 守护进程的用户
uid = www
# 运行 rsync 守护进程的组
gid = www
# 允许 chroot，提升安全性，客户端连接模块，首先 chroot 到模块 path 参数指定的目录下，chroot 为 yes 时必须使用 root 权限，且不能备份 path 路径外的链接文件
use chroot = yes
# 只读
read only = no
# 只写
write only = no
# 设定白名单，可以指定IP段（172.18.50.1/255.255.255.0）,各个Ip段用空格分开
hosts allow = 192.168.0.2
hosts deny = *
# 允许的客户端最大连接数
max connections = 4
# 欢迎文件的路径，非必须
motd file = /etc/rsyncd.motd
# pid文件路径
pid file = /var/run/rsyncd.pid
# 记录传输文件日志
transfer logging = yes
# 日志文件格式
log format = %t %a %m %f %b
# 指定日志文件
log file = /var/log/rsync.log
# 剔除某些文件或目录，不同步
exclude = lost+found/
# 设置超时时间
timeout = 900
ignore nonreadable = yes
# 设置不需要压缩的文件
dont compress   = *.gz *.tgz *.zip *.z *.Z *.rpm *.deb *.bz2

# 模块，可以配置多个
[sync_file]
# 模块的根目录，同步目录，要注意权限
path = /home/test
# 是否允许列出模块内容
list = no
# 忽略错误
ignore errors
# 添加注释
comment = ftp export area
# 模块验证的用户名称，可使用空格或者逗号隔开多个用户名
auth users = sync
# 模块验证密码文件 可放在全局配置里
secrets file = /etc/rsyncd.secrets
```

编辑 `/etc/rsyncd.secrets` 文件，内容如下：

```python
### rsyncd.secrets 文件的配置
# 用户名:密码
sync:123456
```

编辑 `/etc/rsyncd.motd` 文件，内容如下：

```python
### rsyncd.motd  文件配置
++++++++++++++++++
sync zhang : rsync start
++++++++++++++++++
```

设置文件权限，这一步不能少：

```python
chmod 600 /etc/rsyncd.secrets
```


启动：

```python
rsync --daemon --config=/etc/rsyncd.conf
```

加入开机自启：

```python
echo 'rsync --daemon --config=/etc/rsyncd.conf' >> /etc/rc.d/rc.local
```

2、客户端配置：

创建密码文件 `/etc/rsyncd.pass`，直接写密码即可，内容如下：

```python
### rsyncd.pass 文件的配置
123456
```

设置文件权限，这一步不能少：

```python
chmod 600 /etc/rsyncd.pass
```

现在就可以在客户端执行命令来同步文件了。

从 服务端=>客户端 同步数据：

```python
rsync -avzP --delete sync@192.168.0.1::sync_file /home/test --password-file=/etc/rsyncd.pass
```

从 客户端=>服务端 同步数据：

```python
rsync -avzP --delete /home/test sync@192.168.0.1::sync_file --password-file=/etc/rsyncd.pass
```

到目前为止，rsync 就配置完成了，如果想实现双向同步，只要将 B 配置成服务端，A 配置成客户端，分别启对应的服务即可。

接下来介绍 inotify 监控文件变动，来实现实时同步。

## inotify

### 安装

```python
yum install -y inotify-tools
```

### 常用参数

1、inotifywait 参数说明：

```python
-m,–monitor：始终保持事件监听状态   # 重要参数
-r,–recursive：递归查询目录     # 重要参数
-q,–quiet：只打印监控事件的信息     # 重要参数
–excludei：排除文件或目录时，不区分大小写
-t,–timeout：超时时间
–timefmt：指定时间输出格式  # 重要参数
–format：指定时间输出格式       # 重要参数
-e,–event：后面指定删、增、改等事件 # 重要参数
```

2、inotifywait events 事件说明：

```python
access：读取文件或目录内容
modify：修改文件或目录内容
attrib：文件或目录的属性改变
close_write：修改真实文件内容   # 重要参数
close_nowrite：文件或目录关闭，在只读模式打开之后关闭的
close：文件或目录关闭，不管读或是写模式
open：文件或目录被打开
moved_to：文件或目录移动到
moved_from：文件或目录从移动
move：移动文件或目录移动到监视目录  # 重要参数
create：在监视目录下创建文件或目录  # 重要参数
delete：删除监视目录下的文件或目录  # 重要参数
delete_self：文件或目录被删除，目录本身被删除
unmount：卸载文件系统
```

### 常用命令

1、创建事件

```python
inotifywait -mrq  /data --timefmt "%d-%m-%y %H:%M" --format "%T %w%f 事件信息: %e" -e create
```

2、删除事件

```python
inotifywait -mrq  /data --timefmt "%d-%m-%y %H:%M" --format "%T %w%f 事件信息: %e" -e delete
```

3、修改事件

```python
inotifywait -mrq  /data --timefmt "%d-%m-%y %H:%M" --format "%T %w%f 事件信息: %e" -e close_write
```

### 脚本监控

```sh
#!/bin/bash

Path=/home/test
Server=192.168.0.2
User=sync
module=sync_file

monitor() {
  /usr/bin/inotifywait -mrq --format '%w%f' -e create,close_write,delete $1 | while read line; do
    if [ -f $line ]; then
      rsync -avz $line --delete ${User}@${Server}::${module} --password-file=/etc/rsyncd.pass
    else
      cd $1 &&
        rsync -avz ./ --delete ${User}@${Server}::${module} --password-file=/etc/rsyncd.pass
    fi
  done
}

monitor $Path;

```

直接将脚本在后台启动，就可以监控文件的变化了，从而实现服务器之间的文件同步。

那么，如果想同步多个目录该怎么办呢？我能想到的办法就是写多个 shell 脚本，每个脚本负责一个目录，但总感觉这种方法不是很好，大家有何高见？

参考文章：

https://www.jianshu.com/p/bd3ae9d8069c <br>
http://www.mengzhaoxu.xyz/2018/12/24/rsync%E5%AE%89%E8%A3%85%E4%B8%8E%E4%BD%BF%E7%94%A8/ <br>
https://www.cnblogs.com/bigberg/p/7886486.html <br>
https://cloud.tencent.com/developer/article/1008061 <br>
https://blog.csdn.net/chenghuikai/article/details/50668805 <br>
https://www.devopssec.cn/2018/08/23/%E6%95%B0%E6%8D%AE%E5%90%8C%E6%AD%A5%E5%B7%A5%E5%85%B7-RSYNC%E7%BB%93%E5%90%88INOTIFY-TOOLS%E5%AE%9E%E7%8E%B0%E6%95%B0%E6%8D%AE%E5%AE%9E%E6%97%B6%E5%90%8C%E6%AD%A5/