上一篇介绍了在 [Mac 环境下，RabbitMQ 的安装](<https://github.com/yongxinz/tech-blog/blob/master/rabbitmq/Mac%20%E7%8E%AF%E5%A2%83%E4%B8%8B%20RabbitMQ%20%E7%9A%84%E5%AE%89%E8%A3%85.md>)，这篇来详细介绍一下 RabbitMQ 的六种工作模式。

其实，这篇文章中的大部分内容都可以从 RabbitMQ 官网得到，包括每种工作模式的说明，以及多种语言的代码实例。

但是，如果你没有时间看英文文档，或者想看到一些总结性的内容，还是可以继续读下去的。

![rabbitmq-framework.jpg](https://ww1.sinaimg.cn/large/0061a0TTly1gdlck40tjwj30fe04ewfb.jpg)

首先，来看一下整体的架构图，并介绍一些基本概念：

- **channel：** 信道是生产者，消费者和 RabbitMQ 通信的渠道，是建立在 TCP 连接上的虚拟连接。一个 TCP 连接上可以建立成百上千个信道，通过这种方式，可以减少系统开销，提高性能。
- **Broker：** 接收客户端连接，实现 AMQP 协议的消息队列和路由功能的进程。
- **Virtual Host：** 虚拟主机的概念，类似权限控制组，一个 Virtual Host 里可以有多个 Exchange 和 Queue，权限控制的最小粒度是 Virtual Host。
- **Exchange：** 交换机，接收生产者发送的消息，并根据 Routing Key 将消息路由到服务器中的队列 Queue。
- **ExchangeType：** 交换机类型决定了路由消息的行为，RabbitMQ 中有三种 Exchange 类型，分别是 direct、fanout、topic。
- **Message Queue：** 消息队列，用于存储还未被消费者消费的消息，由 Header 和 body 组成。Header 是由生产者添加的各种属性的集合，包括 Message 是否被持久化、优先级是多少、由哪个 Message Queue 接收等，body 是真正需要发送的数据内容。
- **BindingKey：** 绑定关键字，将一个特定的 Exchange 和一个特定的 Queue 绑定起来。

了解了基本概念之后，就开始写代码吧。本文使用 Python 开发，需要先安装 Pika，版本信息如下：

- RabbitMQ：3.8.3
- Python：3.7.3
- Pika：1.1.0

## 简单模式 Hello World

![hello_world.png](https://ww1.sinaimg.cn/large/0061a0TTly1gdlcfpi4phj308002s3yj.jpg)

**说明：** 最简单的一对一模式，一个生产者，一个消费者，这个没什么可多说的。

**生产者代码：**

```python
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
```

![management.png](https://ww1.sinaimg.cn/large/0061a0TTly1gdld1cd7sij31400f0mzb.jpg)

执行完代码之后，通过管理控制台可以看到，已经有一个叫 hello 的队列了，而且里面有一条消息，就是我们刚才发送过去的。

**消费者代码：**

```python
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
```


## 工作队列模式 Work Queues

![worker_queues.png](https://ww1.sinaimg.cn/large/0061a0TTly1gdlcktkzrlj3098033glq.jpg)

**说明：**一对多模式，一个生产者，多个消费者，一个队列，每个消费者从队列中获取唯一的消息。

有两种消息分发机制，轮询分发和公平分发：

轮询分发的特点是将消息轮流发送给每个消费者，在实际情况中，多个消费者，难免有的处理得快，有的处理得慢，如果都要等到一个消费者处理完，才把消息发送给下一个消费者，效率就大大降低了。

而公平分发的特点是，只要有消费者处理完，就会把消息发送给目前空闲的消费者，这样就提高消费效率了。

**生产者代码：**

```python
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ))
print(" [x] Sent %r" % message)
connection.close()
```

**消费者代码：**

```python
#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 公平分发
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
```

## 发布/订阅模式 Publish/Subscribe

![pub.png](https://ww1.sinaimg.cn/large/0061a0TTly1gdlcoxe33jj309504g74g.jpg)

**说明：**生产者将消息发送给 broker，由交换机将消息转发到绑定此交换机的每个队列，每个绑定交换机的队列都将接收到消息。消费者监听自己的队列并进行消费。

**生产者代码：**

```python
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()
```

**消费者代码：**

```python
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
```

## 路由模式 Routing

![routing.png](https://ww1.sinaimg.cn/large/0061a0TTly1gdlcpb6aubj30br04r74k.jpg)

**说明：**生产者将消息发送给 broker，由交换机根据 `routing_key` 分发到不同的消息队列，然后消费者同样根据 `routing_key` 来消费对应队列上的消息。

**生产者代码：**

```python
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message)
print(" [x] Sent %r:%r" % (severity, message))

connection.close()
```

**消费者代码：**

```python
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
```

## 主题模式 Topics

![topic.png](https://ww1.sinaimg.cn/large/0061a0TTly1gdlcpp1ypmj30bs04r3yr.jpg)

**说明：**其实，主题模式应该算是路由模式的一种，也是通过 `routing_key` 来分发，只不过是 `routing_key` 支持了正则表达式，更加灵活。

**生产者代码：**

```python
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(
    exchange='topic_logs', routing_key=routing_key, body=message)
print(" [x] Sent %r:%r" % (routing_key, message))

connection.close()
```

**消费者代码：**

```python
#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
```

## RPC 模式 RPC

![rpc.png](https://ww1.sinaimg.cn/large/0061a0TTly1gdlcq346wlj30g005k0t3.jpg)

**说明：**通过消息队列来实现 RPC 功能，客户端发送消息到消费队列，消息内容其实就是服务端执行需要的参数，服务端消费消息内容，执行程序，然后将结果返回给客户端。

**生产者代码：**

```python
#!/usr/bin/env python
import pika
import uuid


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %r" % response)
```

**消费者代码：**

```python
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
```

## 总结

以上就是本文的全部内容，其中 Publish/Subscribe，Routing，Topics 三种模式可以统一归为 Exchange 模式，只是创建时交换机的类型不一样，分别是 fanout、direct、topic。

如果有一些概念不是很懂，把代码运行一下也许就都明白了，动手是十分重要的。文中源码都是可以直接运行的，并且会上传到 GitHub 上，文末会有链接。

以上。



**源码链接：**

https://github.com/yongxinz/tech-blog/tree/master/rabbitmq/src



**参考文档：**

https://www.rabbitmq.com/getstarted.html

https://juejin.im/post/5d627d1f51882540df07e430

https://www.jianshu.com/p/80eefec808e5

https://www.cnblogs.com/frankyou/p/5283539.html

