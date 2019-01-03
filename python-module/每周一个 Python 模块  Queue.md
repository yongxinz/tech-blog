# 每周一个 Python 模块 | Queue

Queue 是 Python 标准库中的线程安全的队列（FIFO）实现，提供了一个适用于多线程编程的先进先出的数据结构，即队列，用来在生产者和消费者线程之间的信息传递。

有一点需要注意，Python2 中模块名是 Queue，而 Python3 是 queue。

## 基本 FIFO 队列

**class Queue.Queue(maxsize=0)**

FIFO 即 First in First Out，先进先出。Queue 提供了一个基本的 FIFO 容器，使用方法很简单，maxsize 是个整数，指明了队列中能存放的数据个数的上限。一旦达到上限，插入会导致阻塞，直到队列中的数据被消费掉。如果maxsize 小于或者等于 0，队列大小没有限制。

举个栗子：

```python
import Queue

q = Queue.Queue()

for i in range(5):
    q.put(i)

while not q.empty():
    print q.get()
    
# output
# 0
# 1
# 2
# 3
# 4
```

## LIFO 队列

**class Queue.LifoQueue(maxsize=0)**

LIFO 即 Last in First Out，后进先出。与栈的类似，使用也很简单，maxsize 用法同上。

再举个栗子：

```python
import Queue

q = Queue.LifoQueue()

for i in range(5):
    q.put(i)

while not q.empty():
    print q.get()
    
# output
# 4
# 3
# 2
# 1
# 0
```

可以看到仅仅是将`Queue.Quenu` 类替换为`Queue.LifoQueue` 类。

## 优先级队列

**class Queue.PriorityQueue(maxsize=0)**

构造一个优先队列。maxsize 用法同上。

```python
import Queue
import threading

class Job(object):
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print 'Job:',description
        return
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

q = Queue.PriorityQueue()

q.put(Job(3, 'level 3 job'))
q.put(Job(10, 'level 10 job'))
q.put(Job(1, 'level 1 job'))

def process_job(q):
    while True:
        next_job = q.get()
        print 'for:', next_job.description
        q.task_done()

workers = [threading.Thread(target=process_job, args=(q,)),
        threading.Thread(target=process_job, args=(q,))
        ]

for w in workers:
    w.setDaemon(True)
    w.start()

q.join()

# output
# Job: level 3 job
# Job: level 10 job
# Job: level 1 job
# for: level 1 job
# for: level 3 job
# for: job: level 10 job
```

## 一些常用方法

### **task_done()**

意味着之前入队的一个任务已经完成。由队列的消费者线程调用。每一个 `get()` 调用得到一个任务，接下来的 `task_done()` 调用告诉队列该任务已经处理完毕。

如果当前一个`join()`正在阻塞，它将在队列中的所有任务都处理完时恢复执行（即每一个由`put()`调用入队的任务都有一个对应的`task_done()`调用）。

### **join()**

阻塞调用线程，直到队列中的所有任务被处理掉。

只要有数据被加入队列，未完成的任务数就会增加。当消费者线程调用`task_done()`（意味着有消费者取得任务并完成任务），未完成的任务数就会减少。当未完成的任务数降到 0，`join()` 解除阻塞。

### **put(item[, block[, timeout]])**

将`item`放入队列中。

1. 如果可选的参数`block`为`True`且`timeout`为空对象（默认的情况，阻塞调用，无超时）。
2. 如果`timeout`是个正整数，阻塞调用进程最多`timeout`秒，如果一直无空空间可用，抛出`Full`异常（带超时的阻塞调用）。
3. 如果`block`为`False`，如果有空闲空间可用将数据放入队列，否则立即抛出`Full`异常。

其非阻塞版本为`put_nowait`等同于`put(item, False)`。

### **get([block[, timeout]])**

从队列中移除并返回一个数据。`block`跟`timeout`参数同`put`方法。其非阻塞方法为`get_nowait()`相当与`get(False)`。

### empty()

如果队列为空，返回`True`，反之返回`False`。

相关文档：

https://pymotw.com/3/queue/index.html

https://www.cnblogs.com/itogo/p/5635629.html