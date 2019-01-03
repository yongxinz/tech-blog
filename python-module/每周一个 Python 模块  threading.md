# 每周一个 Python 模块 | threading

其实在 Python 中，多线程是不推荐使用的，除非明确不支持使用多进程的场景，否则的话，能用多进程就用多进程吧。写这篇文章的目的，可以对比多进程的文章来看，有很多相通的地方，看完也许会对并发编程有更好的理解。

## GIL

Python（特指 CPython）的多线程的代码并不能利用多核的优势，而是通过著名的全局解释锁（GIL）来进行处理的。如果是一个计算型的任务，使用多线程 GIL 就会让多线程变慢。我们举个计算斐波那契数列的例子：

```python
# coding=utf-8
import time
import threading


def profile(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        func(*args, **kwargs)
        end   = time.time()
        print 'COST: {}'.format(end - start)
    return wrapper


def fib(n):
    if n<= 2:
        return 1
    return fib(n-1) + fib(n-2)


@profile
def nothread():
    fib(35)
    fib(35)


@profile
def hasthread():
    for i in range(2):
        t = threading.Thread(target=fib, args=(35,))
        t.start()
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()

nothread()
hasthread()

# output
# COST: 5.05716490746
# COST: 6.75599503517
```

运行的结果你猜猜会怎么样？还不如不用多线程！

GIL 是必须的，这是 Python 设计的问题：Python 解释器是非线程安全的。这意味着当从线程内尝试安全的访问Python 对象的时候将有一个全局的强制锁。 在任何时候，仅仅一个单一的线程能够获取 Python 对象或者 C API。每 100 个字节的 Python 指令解释器将重新获取锁，这（潜在的）阻塞了 I/O 操作。因为锁，CPU 密集型的代码使用线程库时，不会获得性能的提高（但是当它使用之后介绍的多进程库时，性能可以获得提高）。

那是不是由于 GIL 的存在，多线程库就是个「鸡肋」呢？当然不是。事实上我们平时会接触非常多的和网络通信或者数据输入/输出相关的程序，比如网络爬虫、文本处理等等。这时候由于网络情况和 I/O 的性能的限制，Python 解释器会等待读写数据的函数调用返回，这个时候就可以利用多线程库提高并发效率了。

## 线程对象

先说一个非常简单的方法，直接使用 Thread 来实例化目标函数，然后调用 `start()` 来执行。

```python
import threading


def worker():
    """thread worker function"""
    print('Worker')


threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
    
# output
# Worker
# Worker
# Worker
# Worker
# Worker
```

生成线程时可以传递参数给线程，什么类型的参数都可以。下面这个例子只传了一个数字：

```python
import threading


def worker(num):
    """thread worker function"""
    print('Worker: %s' % num)


threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
    
# output
# Worker: 0
# Worker: 1
# Worker: 2
# Worker: 3
# Worker: 4
```

还有一种创建线程的方法，通过继承 Thread 类，然后重写 `run()` 方法，代码如下：

```python
import threading
import logging


class MyThread(threading.Thread):

    def run(self):
        logging.debug('running')


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

for i in range(5):
    t = MyThread()
    t.start()
    
# output
# (Thread-1  ) running
# (Thread-2  ) running
# (Thread-3  ) running
# (Thread-4  ) running
# (Thread-5  ) running
```

因为传递给 Thread 构造函数的参数 `args` 和 `kwargs` 被保存成了带 `__` 前缀的私有变量，所以在子线程中访问不到，所以在自定义线程类中，要重新构造函数。

```python
import threading
import logging


class MyThreadWithArgs(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.args = args
        self.kwargs = kwargs

    def run(self):
        logging.debug('running with %s and %s',
                      self.args, self.kwargs)


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

for i in range(5):
    t = MyThreadWithArgs(args=(i,), kwargs={'a': 'A', 'b': 'B'})
    t.start()
    
# output
# (Thread-1  ) running with (0,) and {'b': 'B', 'a': 'A'}
# (Thread-2  ) running with (1,) and {'b': 'B', 'a': 'A'}
# (Thread-3  ) running with (2,) and {'b': 'B', 'a': 'A'}
# (Thread-4  ) running with (3,) and {'b': 'B', 'a': 'A'}
# (Thread-5  ) running with (4,) and {'b': 'B', 'a': 'A'}
```

## 确定当前线程

每个 Thread 都有一个名称，可以使用默认值，也可以在创建线程时指定。

```python
import threading
import time


def worker():
    print(threading.current_thread().getName(), 'Starting')
    time.sleep(0.2)
    print(threading.current_thread().getName(), 'Exiting')


def my_service():
    print(threading.current_thread().getName(), 'Starting')
    time.sleep(0.3)
    print(threading.current_thread().getName(), 'Exiting')


t = threading.Thread(name='my_service', target=my_service)
w = threading.Thread(name='worker', target=worker)
w2 = threading.Thread(target=worker)  # use default name

w.start()
w2.start()
t.start()

# output
# worker Starting
# Thread-1 Starting
# my_service Starting
# worker Exiting
# Thread-1 Exiting
# my_service Exiting
```

## 守护线程

默认情况下，在所有子线程退出之前，主程序不会退出。有些时候，启动后台线程运行而不阻止主程序退出是有用的，例如为监视工具生成“心跳”的任务。

要将线程标记为守护程序，在创建时传递 `daemon=True` 或调用`set_daemon(True)`，默认情况下，线程不是守护进程。

```python
import threading
import time
import logging


def daemon():
    logging.debug('Starting')
    time.sleep(0.2)
    logging.debug('Exiting')


def non_daemon():
    logging.debug('Starting')
    logging.debug('Exiting')


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

d = threading.Thread(name='daemon', target=daemon, daemon=True)

t = threading.Thread(name='non-daemon', target=non_daemon)

d.start()
t.start()

# output
# (daemon    ) Starting
# (non-daemon) Starting
# (non-daemon) Exiting
```

输出不包含守护线程的 `Exiting`，因为在守护线程从 `sleep()` 唤醒之前，其他线程，包括主程序都已经退出了。

如果想等守护线程完成工作，可以使用 `join()` 方法。

```python
import threading
import time
import logging


def daemon():
    logging.debug('Starting')
    time.sleep(0.2)
    logging.debug('Exiting')


def non_daemon():
    logging.debug('Starting')
    logging.debug('Exiting')


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

d = threading.Thread(name='daemon', target=daemon, daemon=True)

t = threading.Thread(name='non-daemon', target=non_daemon)

d.start()
t.start()

d.join()
t.join()

# output
# (daemon    ) Starting
# (non-daemon) Starting
# (non-daemon) Exiting
# (daemon    ) Exiting
```

输出信息已经包括守护线程的 `Exiting`。

默认情况下，`join()`无限期地阻止。也可以传一个浮点值，表示等待线程变为非活动状态的秒数。如果线程未在超时期限内完成，则`join()`无论如何都会返回。

```python
import threading
import time
import logging


def daemon():
    logging.debug('Starting')
    time.sleep(0.2)
    logging.debug('Exiting')


def non_daemon():
    logging.debug('Starting')
    logging.debug('Exiting')


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

d = threading.Thread(name='daemon', target=daemon, daemon=True)

t = threading.Thread(name='non-daemon', target=non_daemon)

d.start()
t.start()

d.join(0.1)
print('d.isAlive()', d.isAlive())
t.join()

# output
# (daemon    ) Starting
# (non-daemon) Starting
# (non-daemon) Exiting
# d.isAlive() True
```

由于传递的超时小于守护程序线程休眠的时间，因此`join()` 返回后线程仍处于“活动”状态。

## 枚举所有线程

`enumerate()` 方法可以返回活动 Thread 实例列表。由于该列表包括当前线程，并且由于加入当前线程会引入死锁情况，因此必须跳过它。

```python
import random
import threading
import time
import logging


def worker():
    """thread worker function"""
    pause = random.randint(1, 5) / 10
    logging.debug('sleeping %0.2f', pause)
    time.sleep(pause)
    logging.debug('ending')


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

for i in range(3):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

main_thread = threading.main_thread()
for t in threading.enumerate():
    if t is main_thread:
        continue
    logging.debug('joining %s', t.getName())
    t.join()
    
# output
# (Thread-1  ) sleeping 0.20
# (Thread-2  ) sleeping 0.30
# (Thread-3  ) sleeping 0.40
# (MainThread) joining Thread-1
# (Thread-1  ) ending
# (MainThread) joining Thread-3
# (Thread-2  ) ending
# (Thread-3  ) ending
# (MainThread) joining Thread-2
```

## 计时器线程

`Timer()` 在延迟时间后开始工作，并且可以在该延迟时间段内的任何时间点取消。

```python
import threading
import time
import logging


def delayed():
    logging.debug('worker running')


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

t1 = threading.Timer(0.3, delayed)
t1.setName('t1')
t2 = threading.Timer(0.3, delayed)
t2.setName('t2')

logging.debug('starting timers')
t1.start()
t2.start()

logging.debug('waiting before canceling %s', t2.getName())
time.sleep(0.2)
logging.debug('canceling %s', t2.getName())
t2.cancel()
logging.debug('done')

# output
# (MainThread) starting timers
# (MainThread) waiting before canceling t2
# (MainThread) canceling t2
# (MainThread) done
# (t1        ) worker running
```

此示例中的第二个计时器不会运行，并且第一个计时器似乎在主程序完成后运行的。由于它不是守护线程，因此在完成主线程时会隐式调用它。

## 同步机制

### Semaphore

在多线程编程中，为了防止不同的线程同时对一个公用的资源（比如全部变量）进行修改，需要进行同时访问的数量（通常是 1）。信号量同步基于内部计数器，每调用一次 `acquire()`，计数器减 1；每调用一次 `release()`，计数器加 1。当计数器为 0 时，`acquire()` 调用被阻塞。

```python
import logging
import random
import threading
import time


class ActivePool:

    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running: %s', self.active)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Running: %s', self.active)


def worker(s, pool):
    logging.debug('Waiting to join the pool')
    with s:
        name = threading.current_thread().getName()
        pool.makeActive(name)
        time.sleep(0.1)
        pool.makeInactive(name)


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-2s) %(message)s',
)

pool = ActivePool()
s = threading.Semaphore(2)
for i in range(4):
    t = threading.Thread(
        target=worker,
        name=str(i),
        args=(s, pool),
    )
    t.start()
    
# output
# 2016-07-10 10:45:29,398 (0 ) Waiting to join the pool
# 2016-07-10 10:45:29,398 (0 ) Running: ['0']
# 2016-07-10 10:45:29,399 (1 ) Waiting to join the pool
# 2016-07-10 10:45:29,399 (1 ) Running: ['0', '1']
# 2016-07-10 10:45:29,399 (2 ) Waiting to join the pool
# 2016-07-10 10:45:29,399 (3 ) Waiting to join the pool
# 2016-07-10 10:45:29,501 (1 ) Running: ['0']
# 2016-07-10 10:45:29,501 (0 ) Running: []
# 2016-07-10 10:45:29,502 (3 ) Running: ['3']
# 2016-07-10 10:45:29,502 (2 ) Running: ['3', '2']
# 2016-07-10 10:45:29,607 (3 ) Running: ['2']
# 2016-07-10 10:45:29,608 (2 ) Running: []
```

在这个例子中，`ActivePool()` 类只是为了展示在同一时刻，最多只有两个线程在运行。

### Lock

Lock 也可以叫做互斥锁，其实相当于信号量为 1。我们先看一个不加锁的例子：

```python
import time
from threading import Thread

value = 0


def getlock():
    global value
    new = value + 1
    time.sleep(0.001)  # 使用sleep让线程有机会切换
    value = new


threads = []

for i in range(100):
    t = Thread(target=getlock)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print value	# 16
```

不加锁的情况下，结果会远远的小于 100。那我们加上互斥锁看看：

```python
import time
from threading import Thread, Lock

value = 0
lock = Lock()


def getlock():
    global value
    with lock:
        new = value + 1
        time.sleep(0.001)
        value = new

threads = []

for i in range(100):
    t = Thread(target=getlock)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print value	# 100
```

### RLock

`acquire()` 能够不被阻塞的被同一个线程调用多次。但是要注意的是 `release()` 需要调用与 `acquire()` 相同的次数才能释放锁。

先看一下使用 `Lock` 的情况：

```python
import threading

lock = threading.Lock()

print('First try :', lock.acquire())
print('Second try:', lock.acquire(0))

# output
# First try : True
# Second try: False
```

在这种情况下，第二次调用将 `acquire()` 被赋予零超时以防止它被阻塞，因为第一次调用已获得锁定。

再看看用`RLock`替代的情况。

```python
import threading

lock = threading.RLock()

print('First try :', lock.acquire())
print('Second try:', lock.acquire(0))

# output
# First try : True
# Second try: True
```

### Condition

一个线程等待特定条件，而另一个线程发出特定条件满足的信号。最好说明的例子就是「生产者/消费者」模型：

```python
import time
import threading

def consumer(cond):
    t = threading.currentThread()
    with cond:
        cond.wait()  # wait()方法创建了一个名为waiter的锁，并且设置锁的状态为locked。这个waiter锁用于线程间的通讯
        print '{}: Resource is available to consumer'.format(t.name)


def producer(cond):
    t = threading.currentThread()
    with cond:
        print '{}: Making resource available'.format(t.name)
        cond.notifyAll()  # 释放waiter锁，唤醒消费者


condition = threading.Condition()

c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
c2 = threading.Thread(name='c2', target=consumer, args=(condition,))
p = threading.Thread(name='p', target=producer, args=(condition,))

c1.start()
time.sleep(1)
c2.start()
time.sleep(1)
p.start()

# output
# p: Making resource available
# c2: Resource is available to consumer
# c1: Resource is available to consumer
```

可以看到生产者发送通知之后，消费者都收到了。

### Event

一个线程发送/传递事件，另外的线程等待事件的触发。我们同样的用「生产者/消费者」模型的例子：

```python
# coding=utf-8
import time
import threading
from random import randint


TIMEOUT = 2

def consumer(event, l):
    t = threading.currentThread()
    while 1:
        event_is_set = event.wait(TIMEOUT)
        if event_is_set:
            try:
                integer = l.pop()
                print '{} popped from list by {}'.format(integer, t.name)
                event.clear()  # 重置事件状态
            except IndexError:  # 为了让刚启动时容错
                pass


def producer(event, l):
    t = threading.currentThread()
    while 1:
        integer = randint(10, 100)
        l.append(integer)
        print '{} appended to list by {}'.format(integer, t.name)
        event.set()	 # 设置事件
        time.sleep(1)


event = threading.Event()
l = []

threads = []

for name in ('consumer1', 'consumer2'):
    t = threading.Thread(name=name, target=consumer, args=(event, l))
    t.start()
    threads.append(t)

p = threading.Thread(name='producer1', target=producer, args=(event, l))
p.start()
threads.append(p)

for t in threads:
    t.join()
    
# output
# 77 appended to list by producer1
# 77 popped from list by consumer1
# 46 appended to list by producer1
# 46 popped from list by consumer2
# 43 appended to list by producer1
# 43 popped from list by consumer2
# 37 appended to list by producer1
# 37 popped from list by consumer2
# 33 appended to list by producer1
# 33 popped from list by consumer2
# 57 appended to list by producer1
# 57 popped from list by consumer1
```

可以看到事件被 2 个消费者比较平均的接收并处理了。如果使用了 `wait()` 方法，线程就会等待我们设置事件，这也有助于保证任务的完成。

### Queue

队列在并发开发中最常用的。我们借助「生产者/消费者」模式来理解：生产者把生产的「消息」放入队列，消费者从这个队列中对去对应的消息执行。

大家主要关心如下 4 个方法就好了：

1. put: 向队列中添加一个项。
2. get: 从队列中删除并返回一个项。
3. task_done: 当某一项任务完成时调用。
4. join: 阻塞直到所有的项目都被处理完。

```python
# coding=utf-8
import time
import threading
from random import random
from Queue import Queue

q = Queue()


def double(n):
    return n * 2


def producer():
    while 1:
        wt = random()
        time.sleep(wt)
        q.put((double, wt))


def consumer():
    while 1:
        task, arg = q.get()
        print arg, task(arg)
        q.task_done()


for target in(producer, consumer):
    t = threading.Thread(target=target)
    t.start()
```

这就是最简化的队列架构。

Queue 模块还自带了 PriorityQueue（带有优先级）和 LifoQueue（后进先出）2 种特殊队列。我们这里展示下线程安全的优先级队列的用法，PriorityQueue 要求我们 put 的数据的格式是`(priority_number, data)`，我们看看下面的例子：

```python
import time
import threading
from random import randint
from Queue import PriorityQueue


q = PriorityQueue()


def double(n):
    return n * 2


def producer():
    count = 0
    while 1:
        if count > 5:
            break
        pri = randint(0, 100)
        print 'put :{}'.format(pri)
        q.put((pri, double, pri))  # (priority, func, args)
        count += 1


def consumer():
    while 1:
        if q.empty():
            break
        pri, task, arg = q.get()
        print '[PRI:{}] {} * 2 = {}'.format(pri, arg, task(arg))
        q.task_done()
        time.sleep(0.1)


t = threading.Thread(target=producer)
t.start()
time.sleep(1)
t = threading.Thread(target=consumer)
t.start()

# output
# put :84
# put :86
# put :16
# put :93
# put :14
# put :93
# [PRI:14] 14 * 2 = 28
# 
# [PRI:16] 16 * 2 = 32
# [PRI:84] 84 * 2 = 168
# [PRI:86] 86 * 2 = 172
# [PRI:93] 93 * 2 = 186
# [PRI:93] 93 * 2 = 186
```

其中消费者是故意让它执行的比生产者慢很多，为了节省篇幅，只随机产生 5 次随机结果。可以看到 put 时的数字是随机的，但是 get 的时候先从优先级更高（数字小表示优先级高）开始获取的。

## 线程池

面向对象开发中，大家知道创建和销毁对象是很费时间的，因为创建一个对象要获取内存资源或者其它更多资源。无节制的创建和销毁线程是一种极大的浪费。那我们可不可以把执行完任务的线程不销毁而重复利用呢？仿佛就是把这些线程放进一个池子，一方面我们可以控制同时工作的线程数量，一方面也避免了创建和销毁产生的开销。

线程池在标准库中其实是有体现的，只是在官方文章中基本没有被提及：

```python
In : from multiprocessing.pool import ThreadPool
In : pool = ThreadPool(5)
In : pool.map(lambda x: x**2, range(5))
Out: [0, 1, 4, 9, 16]
```

当然我们也可以自己实现一个：

```python
# coding=utf-8
import time
import threading
from random import random
from Queue import Queue


def double(n):
    return n * 2


class Worker(threading.Thread):
    def __init__(self, queue):
        super(Worker, self).__init__()
        self._q = queue
        self.daemon = True
        self.start()
    def run(self):
        while 1:
            f, args, kwargs = self._q.get()
            try:
                print 'USE: {}'.format(self.name)  # 线程名字
                print f(*args, **kwargs)
            except Exception as e:
                print e
            self._q.task_done()


class ThreadPool(object):
    def __init__(self, num_t=5):
        self._q = Queue(num_t)
        # Create Worker Thread
        for _ in range(num_t):
            Worker(self._q)
    def add_task(self, f, *args, **kwargs):
        self._q.put((f, args, kwargs))
    def wait_complete(self):
        self._q.join()


pool = ThreadPool()
for _ in range(8):
    wt = random()
    pool.add_task(double, wt)
    time.sleep(wt)
pool.wait_complete()

# output
# USE: Thread-1
# 1.58762376489
# USE: Thread-2
# 0.0652918738849
# USE: Thread-3
# 0.997407997138
# USE: Thread-4
# 1.69333900685
# USE: Thread-5
# 0.726900613676
# USE: Thread-1
# 1.69110052253
# USE: Thread-2
# 1.89039743989
# USE: Thread-3
# 0.96281118122
```

线程池会保证同时提供 5 个线程工作，但是我们有 8 个待完成的任务，可以看到线程按顺序被循环利用了。

相关文档：

https://pymotw.com/3/threading/index.html

http://www.dongwm.com/archives/%E4%BD%BF%E7%94%A8Python%E8%BF%9B%E8%A1%8C%E5%B9%B6%E5%8F%91%E7%BC%96%E7%A8%8B-%E7%BA%BF%E7%A8%8B%E7%AF%87/