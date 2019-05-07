## 简介

引用官方说法：ZMQ（以下 ZeroMQ 简称 ZMQ）是一个简单好用的传输层，像框架一样的一个 socket library，他使得 Socket 编程更加简单、简洁和性能更高。

是一个消息处理队列库，可在多个线程、内核和主机盒之间弹性伸缩。

ZMQ 的明确目标是“成为标准网络协议栈的一部分，之后进入 Linux 内核”。现在还未看到它们的成功。但是，它无疑是极具前景的、并且是人们更加需要的“传统” BSD 套接字之上的一 层封装。ZMQ 让编写高性能网络应用程序极为简单和有趣。

它跟 RabbitMQ，ActiveMQ 之类有着相当本质的区别，ZeroMQ 根本就不是一个消息队列服务器，更像是一组底层网络通讯库，对原有的 Socket API 加上一层封装，使我们操作更简便。

## 三种工作模式
### Request-Reply 模式：

说到“请求-应答”模式，不得不说的就是它的消息流动模型。消息流动模型指的是该模式下，必须严格遵守“一问一答”的方式。

发出消息后，若没有收到回复，再发出第二条消息时就会抛出异常。同样的，对于 Rep 也是，在没有接收到消息前，不允许发出消息。

基于此构成“一问一答”的响应模式。

**server:**

```python
# -*- coding=utf-8 -*-

import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print("Received: %s" % message)
    socket.send("I am OK!")
```

**client:**

```python
# -*- coding=utf-8 -*-

import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

socket.send('Are you OK?')
response = socket.recv()
print("response: %s" % response)
```

### Publish-Subscribe 模式：

“发布-订阅”模式下，“发布者”绑定一个指定的地址，例如“192.168.10.1：5500”，“订阅者”连接到该地址。该模式下消息流是单向的，只允许从“发布者”流向“订阅者”。且“发布者”只管发消息，不理会是否存在“订阅者”。一个“发布者”可以拥有多个订阅者，同样的，一个“订阅者”也可订阅多个发布者。

虽然我们知道“发布者”在发送消息时是不关心“订阅者”的存在于否，所以先启动“发布者”，再启动“订阅者”是很容易导致部分消息丢失的。那么可能会提出一个说法“我先启动‘订阅者’，再启动‘发布者’，就能解决这个问题了？”

对于 ZeroMQ 而言，这种做法也并不能保证 100% 的可靠性。在 ZeroMQ 领域中，有一个叫做“慢木匠”的术语，就是说即使我是先启动了“订阅者”，再启动“发布者”，“订阅者”总是会丢失第一批数据。因为在“订阅者”与端点建立 TCP 连接时，会包含几毫秒的握手时间，虽然时间短，但是是存在的。再加上 ZeroMQ 后台 IO 是以一部方式执行的，所以若不在双方之间施加同步策略，消息丢失是不可避免的。

关于“发布-订阅”模式在 ZeroMQ 中的一些其他特点：

1. 公平排队，一个“订阅者”连接到多个发布者时，会均衡的从每个“发布者”读取消息，不会出现一个“发布者”淹没其他“发布者”的情况。
1. ZMQ3.0 以上的版本，过滤规则发生在“发布方”。 ZMQ3.0 以下的版本，过滤规则发生在“订阅方”。其实也就是处理消息的位置。

**server:**
```python
# -*- coding=utf-8 -*-

import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

for i in range(10):
    print('send message...' + str(i))
    socket.send('message' + str(i))
    time.sleep(1)
```

**client:**
```python
# -*- coding=utf-8 -*-

import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, '')
while True:
    response = socket.recv()
    print("response: %s" % response)
```

### Parallel Pipeline 模式：

在说明“管道模式”前，需要明确的是在 ZeroMQ 中并没有绝对的服务端与客户端之分，所有的数据接收与发送都是以连接为单位的，只区分 ZeroMQ 定义的类型。就像套接字绑定地址时，可以使用 `bind`，也可以使用 `connect`，只是通常我们将理解中的服务端 `bind` 到一个地址，而理解中的客户端 `connec` 到该地址。

“管道模式”一般用于任务分发与结果收集，由一个任务发生器来产生任务，“公平”的派发到其管辖下的所有 worker，完成后再由结果收集器来回收任务的执行结果。

整体流程比较好理解，worker 连接到任务发生器上，等待任务的产生，完成后将结果发送至结果收集器。如果要以客户端服务端的概念来区分，这里的任务发生器与结果收集器是服务端，而 worker 是客户端。

前面说到了这里任务的派发是“公平的”，因为内部采用了 LRU 的算法来找到最近最久未工作的闲置 worker。但是公平在这里是相对的，当任务发生器启动后，第一个连接到它的 worker 会在一瞬间承受整个任务发生器产生的 tasks。

总结来说由三部分组成，push 进行数据推送，work 进行数据缓存，pull 进行数据竞争获取处理。区别于 Publish-Subscribe 存在一个数据缓存和处理负载。

当连接被断开，数据不会丢失，重连后数据继续发送到对端。

**server:**
```python
# -*- coding=utf-8 -*-

import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5557")

for i in range(10):
    socket.send('message' + str(i))
    # 没启 worker 时不会发消息
    print('send message...' + str(i))
    time.sleep(1)
```

**work:**
```python
# -*- coding=utf-8 -*-

import zmq

context = zmq.Context()
receive = context.socket(zmq.PULL)
receive.connect('tcp://127.0.0.1:5557')

sender = context.socket(zmq.PUSH)
sender.connect('tcp://127.0.0.1:5558')

while True:
    data = receive.recv()
    print('transform...' + data)
    sender.send(data)
```

**client:**

```python
# -*- coding=utf-8 -*-

import zmq

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5558")

while True:
    response = socket.recv()
    print("response: %s" % response)
```

参考文档：

https://www.2cto.com/kf/201606/514211.html

https://segmentfault.com/a/1190000012010573