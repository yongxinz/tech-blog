# 每周一个 Python 模块 | multiprocessing

multiprocessing 是 Python 的标准模块，它既可以用来编写多进程，也可以用来编写多线程。如果是多线程的话，用 multiprocessing.dummy 即可，用法与 multiprocessing 基本相同。

## 基础

利用 multiprocessing.Process 对象可以创建一个进程，Process 对象与 Thread 对象的用法相同，也有 `start()`， `run()`， `join()` 等方法。Process 类适合简单的进程创建，如需资源共享可以结合 multiprocessing.Queue 使用；如果想要控制进程数量，则建议使用进程池 Pool 类。

Process 介绍：

构造方法：

- Process([group [, target [, name [, args [, kwargs]]]]])
- group: 线程组，目前还没有实现，库引用中提示必须是 None；
- target: 要执行的方法；
- name: 进程名；
- args/kwargs: 要传入方法的参数。

实例方法：

- is_alive()：返回进程是否在运行。
- join([timeout])：阻塞当前上下文环境的进程程，直到调用此方法的进程终止或到达指定的 timeout（可选参数）。
- start()：进程准备就绪，等待 CPU 调度。
- run()：strat() 调用 run 方法，如果实例进程时未制定传入 target，start 执行默认 run() 方法。
- terminate()：不管任务是否完成，立即停止工作进程。

属性：

- authkey
- daemon：和线程的 setDeamon 功能一样（将父进程设置为守护进程，当父进程结束时，子进程也结束）。
- exitcode(进程在运行时为 None、如果为 –N，表示被信号 N 结束）。
- name：进程名字。
- pid：进程号。

下面看一个简单的例子：

```python
import multiprocessing


def worker():
    """worker function"""
    print('Worker')


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker)
        jobs.append(p)
        p.start()

# 输出
# Worker
# Worker
# Worker
# Worker
# Worker        
```

输出结果是打印了五次 Worker，我们并不知道哪个 Worker 是由哪个进程打印的，具体取决于执行顺序，因为每个进程都在竞争访问输出流。

那怎样才能知道具体执行顺序呢？可以通过给进程传参来实现。与 threading 不同，传递给 `multiprocessing` `Process` 的参数必需是可序列化的，来看一下代码：

```python
import multiprocessing


def worker(num):
    """thread worker function"""
    print('Worker:', num)


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()
        
# 输出
# Worker: 1
# Worker: 0
# Worker: 2
# Worker: 3
# Worker: 4
```

## 可导入的目标函数

threading 和 multiprocessing 的一处区别是在 `__main__` 中使用时的额外保护。由于进程已经启动，子进程需要能够导入包含目标函数的脚本。在 `__main__` 中包装应用程序的主要部分，可确保在导入模块时不会在每个子项中递归运行它。另一种方法是从单独的脚本导入目标函数。例如：`multiprocessing_import_main.py`使用在第二个模块中定义的 worker 函数。

```python
# multiprocessing_import_main.py 
import multiprocessing
import multiprocessing_import_worker

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(
            target=multiprocessing_import_worker.worker,
        )
        jobs.append(p)
        p.start()
        
# 输出
# Worker
# Worker
# Worker
# Worker
# Worker
```

worker 函数定义于`multiprocessing_import_worker.py`。

```python
# multiprocessing_import_worker.py 
def worker():
    """worker function"""
    print('Worker')
    return
```

## 确定当前进程

传参来识别或命名进程非常麻烦，也不必要。每个`Process`实例都有一个名称，其默认值可以在创建进程时更改。命名进程对于跟踪它们非常有用，尤其是在同时运行多种类型进程的应用程序中。

```python
import multiprocessing
import time


def worker():
    name = multiprocessing.current_process().name
    print(name, 'Starting')
    time.sleep(2)
    print(name, 'Exiting')


def my_service():
    name = multiprocessing.current_process().name
    print(name, 'Starting')
    time.sleep(3)
    print(name, 'Exiting')


if __name__ == '__main__':
    service = multiprocessing.Process(
        name='my_service',
        target=my_service,
    )
    worker_1 = multiprocessing.Process(
        name='worker 1',
        target=worker,
    )
    worker_2 = multiprocessing.Process(  # default name
        target=worker,
    )

    worker_1.start()
    worker_2.start()
    service.start()
    
# output
# worker 1 Starting
# worker 1 Exiting
# Process-3 Starting
# Process-3 Exiting
# my_service Starting
# my_service Exiting
```

## 守护进程

默认情况下，在所有子进程退出之前，主程序不会退出。有些时候，启动后台进程运行而不阻止主程序退出是有用的，例如为监视工具生成“心跳”的任务。

要将进程标记为守护程序很简单，只要将`daemon`属性设置为 `True` 就可以了。

```python
import multiprocessing
import time
import sys


def daemon():
    p = multiprocessing.current_process()
    print('Starting:', p.name, p.pid)
    sys.stdout.flush()
    time.sleep(2)
    print('Exiting :', p.name, p.pid)
    sys.stdout.flush()


def non_daemon():
    p = multiprocessing.current_process()
    print('Starting:', p.name, p.pid)
    sys.stdout.flush()
    print('Exiting :', p.name, p.pid)
    sys.stdout.flush()


if __name__ == '__main__':
    d = multiprocessing.Process(
        name='daemon',
        target=daemon,
    )
    d.daemon = True

    n = multiprocessing.Process(
        name='non-daemon',
        target=non_daemon,
    )
    n.daemon = False

    d.start()
    time.sleep(1)
    n.start()
    
# output
# Starting: daemon 41838
# Starting: non-daemon 41841
# Exiting : non-daemon 41841
```

输出不包括来自守护进程的“退出”消息，因为所有非守护进程（包括主程序）在守护进程从两秒休眠状态唤醒之前退出。

守护进程在主程序退出之前自动终止，这避免了孤立进程的运行。这可以通过查找程序运行时打印的进程 ID 值来验证，然后使用 `ps` 命令检查该进程。

## 等待进程

要等到进程完成其工作并退出，请使用 `join()`方法。

```python
import multiprocessing
import time
import sys


def daemon():
    name = multiprocessing.current_process().name
    print('Starting:', name)
    time.sleep(2)
    print('Exiting :', name)


def non_daemon():
    name = multiprocessing.current_process().name
    print('Starting:', name)
    print('Exiting :', name)


if __name__ == '__main__':
    d = multiprocessing.Process(
        name='daemon',
        target=daemon,
    )
    d.daemon = True

    n = multiprocessing.Process(
        name='non-daemon',
        target=non_daemon,
    )
    n.daemon = False

    d.start()
    time.sleep(1)
    n.start()

    d.join()
    n.join()
    
# output
# Starting: non-daemon
# Exiting : non-daemon
# Starting: daemon
# Exiting : daemon
```

由于主进程使用 `join()` 等待守护进程退出，因此此时将打印“退出”消息。

默认情况下，`join()`无限期地阻止。也可以传递一个超时参数（一个浮点数表示等待进程变为非活动状态的秒数）。如果进程未在超时期限内完成，则`join()`无论如何都要返回。

```python
import multiprocessing
import time
import sys


def daemon():
    name = multiprocessing.current_process().name
    print('Starting:', name)
    time.sleep(2)
    print('Exiting :', name)


def non_daemon():
    name = multiprocessing.current_process().name
    print('Starting:', name)
    print('Exiting :', name)


if __name__ == '__main__':
    d = multiprocessing.Process(
        name='daemon',
        target=daemon,
    )
    d.daemon = True

    n = multiprocessing.Process(
        name='non-daemon',
        target=non_daemon,
    )
    n.daemon = False

    d.start()
    n.start()

    d.join(1)
    print('d.is_alive()', d.is_alive())
    n.join()
    
# output
# Starting: non-daemon
# Exiting : non-daemon
# d.is_alive() True
```

由于传递的超时时间小于守护进程休眠的时间，因此`join()`返回后进程仍处于“活动”状态。

## 终止进程

如果想让一个进程退出，最好使用「poison pill」方法向它发送信号，如果进程出现挂起或死锁，那么强制终止它是有用的。 调用 `terminate()` 来杀死子进程。

```python
import multiprocessing
import time


def slow_worker():
    print('Starting worker')
    time.sleep(0.1)
    print('Finished worker')


if __name__ == '__main__':
    p = multiprocessing.Process(target=slow_worker)
    print('BEFORE:', p, p.is_alive())

    p.start()
    print('DURING:', p, p.is_alive())

    p.terminate()
    print('TERMINATED:', p, p.is_alive())

    p.join()
    print('JOINED:', p, p.is_alive())
    
# output
# BEFORE: <Process(Process-1, initial)> False
# DURING: <Process(Process-1, started)> True
# TERMINATED: <Process(Process-1, started)> True
# JOINED: <Process(Process-1, stopped[SIGTERM])> False
```

在终止它之后对该进程使用 `join()` 很重要，可以为进程管理代码提供时间来更新对象状态，用以反映终止效果。

## 处理退出状态

可以通过`exitcode`属性访问进程退出时生成的状态代码。允许的范围列于下表中。

| 退出代码 | 含义                                     |
| -------- | ---------------------------------------- |
| `== 0`   | 没有产生错误                             |
| `> 0`    | 该进程出错，并退出该代码                 |
| `< 0`    | 这个过程被一个信号杀死了 `-1 * exitcode` |

```python
import multiprocessing
import sys
import time


def exit_error():
    sys.exit(1)


def exit_ok():
    return


def return_value():
    return 1


def raises():
    raise RuntimeError('There was an error!')


def terminated():
    time.sleep(3)


if __name__ == '__main__':
    jobs = []
    funcs = [
        exit_error,
        exit_ok,
        return_value,
        raises,
        terminated,
    ]
    for f in funcs:
        print('Starting process for', f.__name__)
        j = multiprocessing.Process(target=f, name=f.__name__)
        jobs.append(j)
        j.start()

    jobs[-1].terminate()

    for j in jobs:
        j.join()
        print('{:>15}.exitcode = {}'.format(j.name, j.exitcode))
        
# output
# Starting process for exit_error
# Starting process for exit_ok
# Starting process for return_value
# Starting process for raises
# Starting process for terminated
# Process raises:
# Traceback (most recent call last):
#   File ".../lib/python3.6/multiprocessing/process.py", line 258,
# in _bootstrap
#     self.run()
#   File ".../lib/python3.6/multiprocessing/process.py", line 93,
# in run
#     self._target(*self._args, **self._kwargs)
#   File "multiprocessing_exitcode.py", line 28, in raises
#     raise RuntimeError('There was an error!')
# RuntimeError: There was an error!
#      exit_error.exitcode = 1
#         exit_ok.exitcode = 0
#    return_value.exitcode = 0
#          raises.exitcode = 1
#      terminated.exitcode = -15
```

## 记录日志

在调试并发问题时，访问 `multiprocessing` 对象的内部结构很有用。有一个方便的模块级功能来启用被调用的日志，叫 `log_to_stderr()`。它使用[`logging`](https://pymotw.com/3/logging/index.html#module-logging)并添加处理程序来设置记录器对象 ，以便将日志消息发送到标准错误通道。

```python
import multiprocessing
import logging
import sys


def worker():
    print('Doing some work')
    sys.stdout.flush()


if __name__ == '__main__':
    multiprocessing.log_to_stderr(logging.DEBUG)
    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()
    
# output
# [INFO/Process-1] child process calling self.run()
# Doing some work
# [INFO/Process-1] process shutting down
# [DEBUG/Process-1] running all "atexit" finalizers with priority >= 0
# [DEBUG/Process-1] running the remaining "atexit" finalizers
# [INFO/Process-1] process exiting with exitcode 0
# [INFO/MainProcess] process shutting down
# [DEBUG/MainProcess] running all "atexit" finalizers with priority >= 0
# [DEBUG/MainProcess] running the remaining "atexit" finalizers
```

默认情况下，日志记录级别设置为`NOTSET`不生成任何消息。传递不同的级别以将记录器初始化为所需的详细程度。

要直接操作记录器（更改其级别设置或添加处理程序），请使用`get_logger()`。

```python
import multiprocessing
import logging
import sys


def worker():
    print('Doing some work')
    sys.stdout.flush()


if __name__ == '__main__':
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()
    
# output
# [INFO/Process-1] child process calling self.run()
# Doing some work
# [INFO/Process-1] process shutting down
# [INFO/Process-1] process exiting with exitcode 0
# [INFO/MainProcess] process shutting down    
```

## 子类化过程

虽然在单独的进程中启动子进程的最简单方法是使用`Process`并传递目标函数，但也可以使用自定义子类。

```python
import multiprocessing


class Worker(multiprocessing.Process):

    def run(self):
        print('In {}'.format(self.name))
        return


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = Worker()
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()
        
# output
# In Worker-1
# In Worker-3
# In Worker-2
# In Worker-4
# In Worker-5
```

派生类应该重写`run()`以完成其工作。

## 向进程传递消息

与线程一样，多个进程的常见使用模式是将作业划分为多个工作并行运行。有效使用多个流程通常需要在它们之间进行一些通信，以便可以划分工作并汇总结果。在进程之间通信的一种简单方法是使用 `Queue`来传递消息。任何可以通过 [`pickle`](https://pymotw.com/3/pickle/index.html#module-pickle) 序列化的对象都可以传递给 `Queue`。

```python
import multiprocessing


class MyFancyClass:

    def __init__(self, name):
        self.name = name

    def do_something(self):
        proc_name = multiprocessing.current_process().name
        print('Doing something fancy in {} for {}!'.format(proc_name, self.name))


def worker(q):
    obj = q.get()
    obj.do_something()


if __name__ == '__main__':
    queue = multiprocessing.Queue()

    p = multiprocessing.Process(target=worker, args=(queue,))
    p.start()

    queue.put(MyFancyClass('Fancy Dan'))

    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    p.join()
    
# output
# Doing something fancy in Process-1 for Fancy Dan!
```

这个简短的示例仅将单个消息传递给单个工作程序，然后主进程等待工作程序完成。

下面看一个更复杂例子，它显示了如何管理多个从 `JoinableQueue` 消耗数据的 worker，并将结果传递回父进程。「poison pill」技术用来终止 workers。设置实际任务后，主程序会将每个工作程序的一个“停止”值添加到队列中。当 worker 遇到特殊值时，它会从循环中跳出。主进程使用任务队列的`join()`方法在处理结果之前等待所有任务完成。

```python
import multiprocessing
import time


class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print('{}: Exiting'.format(proc_name))
                self.task_queue.task_done()
                break
            print('{}: {}'.format(proc_name, next_task))
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)


class Task:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(0.1)  # pretend to take time to do the work
        return '{self.a} * {self.b} = {product}'.format(
            self=self, product=self.a * self.b)

    def __str__(self):
        return '{self.a} * {self.b}'.format(self=self)


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print('Creating {} consumers'.format(num_consumers))
    consumers = [
        Consumer(tasks, results)
        for i in range(num_consumers)
    ]
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = 10
    for i in range(num_jobs):
        tasks.put(Task(i, i))

    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    while num_jobs:
        result = results.get()
        print('Result:', result)
        num_jobs -= 1
        
# output
# Creating 8 consumers
# Consumer-1: 0 * 0
# Consumer-2: 1 * 1
# Consumer-3: 2 * 2
# Consumer-4: 3 * 3
# Consumer-5: 4 * 4
# Consumer-6: 5 * 5
# Consumer-7: 6 * 6
# Consumer-8: 7 * 7
# Consumer-3: 8 * 8
# Consumer-7: 9 * 9
# Consumer-4: Exiting
# Consumer-1: Exiting
# Consumer-2: Exiting
# Consumer-5: Exiting
# Consumer-6: Exiting
# Consumer-8: Exiting
# Consumer-7: Exiting
# Consumer-3: Exiting
# Result: 6 * 6 = 36
# Result: 2 * 2 = 4
# Result: 3 * 3 = 9
# Result: 0 * 0 = 0
# Result: 1 * 1 = 1
# Result: 7 * 7 = 49
# Result: 4 * 4 = 16
# Result: 5 * 5 = 25
# Result: 8 * 8 = 64
# Result: 9 * 9 = 81
```

尽管作业按顺序进入队列，但它们的执行是并行化的，因此无法保证它们的完成顺序。

## 进程间通信

`Event`类提供一种简单的方式进行进程之间的通信。可以在设置和未设置状态之间切换事件。事件对象的用户可以使用可选的超时值等待它从未设置更改为设置。

```python
import multiprocessing
import time


def wait_for_event(e):
    """Wait for the event to be set before doing anything"""
    print('wait_for_event: starting')
    e.wait()
    print('wait_for_event: e.is_set()->', e.is_set())


def wait_for_event_timeout(e, t):
    """Wait t seconds and then timeout"""
    print('wait_for_event_timeout: starting')
    e.wait(t)
    print('wait_for_event_timeout: e.is_set()->', e.is_set())


if __name__ == '__main__':
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(
        name='block',
        target=wait_for_event,
        args=(e,),
    )
    w1.start()

    w2 = multiprocessing.Process(
        name='nonblock',
        target=wait_for_event_timeout,
        args=(e, 2),
    )
    w2.start()

    print('main: waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    print('main: event is set')
    
# output
# main: waiting before calling Event.set()
# wait_for_event: starting
# wait_for_event_timeout: starting
# wait_for_event_timeout: e.is_set()-> False
# main: event is set
# wait_for_event: e.is_set()-> True
```

如果`wait()`超时，不会返回错误。调用者可以使用 `is_set()` 检查事件的状态。

## 控制对资源的访问

在多个进程之间共享单个资源的情况下，可以用 `Lock` 来避免访问冲突。

```python
import multiprocessing
import sys


def worker_with(lock, stream):
    with lock:
        stream.write('Lock acquired via with\n')


def worker_no_with(lock, stream):
    lock.acquire()
    try:
        stream.write('Lock acquired directly\n')
    finally:
        lock.release()


lock = multiprocessing.Lock()
w = multiprocessing.Process(
    target=worker_with,
    args=(lock, sys.stdout),
)
nw = multiprocessing.Process(
    target=worker_no_with,
    args=(lock, sys.stdout),
)

w.start()
nw.start()

w.join()
nw.join()

# output
# Lock acquired via with
# Lock acquired directly
```

在此示例中，如果两个进程不同步它们对标准输出的访问与锁定，则打印到控制台的消息可能混杂在一起。

## 同步操作

`Condition` 对象可用于同步工作流的一部分，可以使某些对象并行运行，但其他对象顺序运行，即使它们位于不同的进程中。

```python
import multiprocessing
import time


def stage_1(cond):
    """
    perform first stage of work,
    then notify stage_2 to continue
    """
    name = multiprocessing.current_process().name
    print('Starting', name)
    with cond:
        print('{} done and ready for stage 2'.format(name))
        cond.notify_all()


def stage_2(cond):
    """wait for the condition telling us stage_1 is done"""
    name = multiprocessing.current_process().name
    print('Starting', name)
    with cond:
        cond.wait()
        print('{} running'.format(name))


if __name__ == '__main__':
    condition = multiprocessing.Condition()
    s1 = multiprocessing.Process(name='s1',
                                 target=stage_1,
                                 args=(condition,))
    s2_clients = [
        multiprocessing.Process(
            name='stage_2[{}]'.format(i),
            target=stage_2,
            args=(condition,),
        )
        for i in range(1, 3)
    ]

    for c in s2_clients:
        c.start()
        time.sleep(1)
    s1.start()

    s1.join()
    for c in s2_clients:
        c.join()
        
# output
# Starting stage_2[1]
# Starting stage_2[2]
# Starting s1
# s1 done and ready for stage 2
# stage_2[1] running
# stage_2[2] running
```

在此示例中，两个进程并行运行 `stage_2`，但仅在 `stage_1 ` 完成后运行。

## 控制对资源的并发访问

有时，允许多个 worker 同时访问资源是有用的，同时仍限制总数。例如，连接池可能支持固定数量的并发连接，或者网络应用程序可能支持固定数量的并发下载。`Semaphore` 是管理这些连接的一种方法。

```python
import random
import multiprocessing
import time


class ActivePool:

    def __init__(self):
        super(ActivePool, self).__init__()
        self.mgr = multiprocessing.Manager()
        self.active = self.mgr.list()
        self.lock = multiprocessing.Lock()

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)

    def __str__(self):
        with self.lock:
            return str(self.active)


def worker(s, pool):
    name = multiprocessing.current_process().name
    with s:
        pool.makeActive(name)
        print('Activating {} now running {}'.format(name, pool))
        time.sleep(random.random())
        pool.makeInactive(name)


if __name__ == '__main__':
    pool = ActivePool()
    s = multiprocessing.Semaphore(3)
    jobs = [
        multiprocessing.Process(
            target=worker,
            name=str(i),
            args=(s, pool),
        )
        for i in range(10)
    ]

    for j in jobs:
        j.start()

    while True:
        alive = 0
        for j in jobs:
            if j.is_alive():
                alive += 1
                j.join(timeout=0.1)
                print('Now running {}'.format(pool))
        if alive == 0:
            # all done
            break

# output            
# Activating 0 now running ['0', '1', '2']
# Activating 1 now running ['0', '1', '2']
# Activating 2 now running ['0', '1', '2']
# Now running ['0', '1', '2']
# Now running ['0', '1', '2']
# Now running ['0', '1', '2']
# Now running ['0', '1', '2']
# Activating 3 now running ['0', '1', '3']
# Activating 4 now running ['1', '3', '4']
# Activating 6 now running ['1', '4', '6']
# Now running ['1', '4', '6']
# Now running ['1', '4', '6']
# Activating 5 now running ['1', '4', '5']
# Now running ['1', '4', '5']
# Now running ['1', '4', '5']
# Now running ['1', '4', '5']
# Activating 8 now running ['4', '5', '8']
# Now running ['4', '5', '8']
# Now running ['4', '5', '8']
# Now running ['4', '5', '8']
# Now running ['4', '5', '8']
# Now running ['4', '5', '8']
# Activating 7 now running ['5', '8', '7']
# Now running ['5', '8', '7']
# Activating 9 now running ['8', '7', '9']
# Now running ['8', '7', '9']
# Now running ['8', '9']
# Now running ['8', '9']
# Now running ['9']
# Now running ['9']
# Now running ['9']
# Now running ['9']
# Now running []            
```

在此示例中，`ActivePool` 类仅用作跟踪在给定时刻正在运行的进程的便捷方式。实际资源池可能会为新活动的进程分配连接或其他值，并在任务完成时回收该值。这里，pool 只用于保存活动进程的名称，以显示只有三个并发运行。

## 管理共享状态

在前面的示例中，首先通过 `Manager` 创建特殊类型的列表，然后活动进程列表通过 `ActivePool` 在实例中集中维护。`Manager`负责协调所有用户之间共享信息的状态。

```python
import multiprocessing
import pprint


def worker(d, key, value):
    d[key] = value


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    d = mgr.dict()
    jobs = [
        multiprocessing.Process(
            target=worker,
            args=(d, i, i * 2),
        )
        for i in range(10)
    ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print('Results:', d)
    
# output
# Results: {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 10, 6: 12, 7: 14, 8: 16, 9: 18}
```

通过管理器创建列表，它将被共享，并且可以在所有进程中看到更新。字典也支持。

## 共享命名空间

除了字典和列表，`Manager`还可以创建共享`Namespace`。

```python
import multiprocessing


def producer(ns, event):
    ns.value = 'This is the value'
    event.set()


def consumer(ns, event):
    try:
        print('Before event: {}'.format(ns.value))
    except Exception as err:
        print('Before event, error:', str(err))
    event.wait()
    print('After event:', ns.value)


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    namespace = mgr.Namespace()
    event = multiprocessing.Event()
    p = multiprocessing.Process(
        target=producer,
        args=(namespace, event),
    )
    c = multiprocessing.Process(
        target=consumer,
        args=(namespace, event),
    )

    c.start()
    p.start()

    c.join()
    p.join()
    
# output
# Before event, error: 'Namespace' object has no attribute 'value'
# After event: This is the value
```

只要添加到命名空间`Namespace`，那么所有接收`Namespace`实例的客户端都可见。

重要的是，要知道命名空间中可变值内容的更新不会自动传播。

```python
import multiprocessing


def producer(ns, event):
    # DOES NOT UPDATE GLOBAL VALUE!
    ns.my_list.append('This is the value')
    event.set()


def consumer(ns, event):
    print('Before event:', ns.my_list)
    event.wait()
    print('After event :', ns.my_list)


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    namespace = mgr.Namespace()
    namespace.my_list = []

    event = multiprocessing.Event()
    p = multiprocessing.Process(
        target=producer,
        args=(namespace, event),
    )
    c = multiprocessing.Process(
        target=consumer,
        args=(namespace, event),
    )

    c.start()
    p.start()

    c.join()
    p.join()
    
# output
# Before event: []
# After event : []
```

要更新列表，需要再次将其添加到命名空间。

## 进程池

`Pool`类可用于管理固定数量 workers 的简单情况。返回值作为列表返回。`Pool` 参数包括进程数和启动任务进程时要运行的函数（每个子进程调用一次）。

```python
import multiprocessing


def do_calculation(data):
    return data * 2


def start_process():
    print('Starting', multiprocessing.current_process().name)


if __name__ == '__main__':
    inputs = list(range(10))
    print('Input   :', inputs)

    builtin_outputs = map(do_calculation, inputs)
    print('Built-in:', builtin_outputs)

    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(
        processes=pool_size,
        initializer=start_process,
    )
    pool_outputs = pool.map(do_calculation, inputs)
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    print('Pool    :', pool_outputs)
    
# output
# Input   : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# Built-in: <map object at 0x1007b2be0>
# Starting ForkPoolWorker-3
# Starting ForkPoolWorker-4
# Starting ForkPoolWorker-5
# Starting ForkPoolWorker-6
# Starting ForkPoolWorker-1
# Starting ForkPoolWorker-7
# Starting ForkPoolWorker-2
# Starting ForkPoolWorker-8
# Pool    : [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

除了各个任务并行运行外，`map()`方法的结果在功能上等同于内置`map()`。由于 `Pool` 并行处理其输入，`close()` 和 `join()`可用于主处理与任务进程进行同步，以确保完全清除。

默认情况下，`Pool`创建固定数量的工作进程并将 jobs 传递给它们，直到没有其他 jobs  为止。设置 `maxtasksperchild`参数会告诉 `Pool` 在完成一些任务后重新启动工作进程，从而防止长时间运行 workers  消耗更多的系统资源。

```python
import multiprocessing


def do_calculation(data):
    return data * 2


def start_process():
    print('Starting', multiprocessing.current_process().name)


if __name__ == '__main__':
    inputs = list(range(10))
    print('Input   :', inputs)

    builtin_outputs = map(do_calculation, inputs)
    print('Built-in:', builtin_outputs)

    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(
        processes=pool_size,
        initializer=start_process,
        maxtasksperchild=2,
    )
    pool_outputs = pool.map(do_calculation, inputs)
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    print('Pool    :', pool_outputs)
    
# output
# Input   : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# Built-in: <map object at 0x1007b21d0>
# Starting ForkPoolWorker-1
# Starting ForkPoolWorker-2
# Starting ForkPoolWorker-4
# Starting ForkPoolWorker-5
# Starting ForkPoolWorker-6
# Starting ForkPoolWorker-3
# Starting ForkPoolWorker-7
# Starting ForkPoolWorker-8
# Pool    : [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

即使没有更多工作，`Pool` 也会在完成分配的任务后重新启动 workers。在此输出中，即使只有 10 个任务，也会创建 8 个 workers，并且每个 worker 可以一次完成其中两个任务。

## 实现 MapReduce

`Pool`类可以用来创建一个简单的单台服务器的 MapReduce 实现。虽然它没有给出分布式处理的全部好处，但它确实说明了将一些问题分解为可分配的工作单元是多么容易。

在基于 MapReduce 的系统中，输入数据被分解为块以供不同的工作实例处理。使用简单的变换将每个输入数据块 映射到中间状态。然后将中间数据收集在一起并基于键值进行分区，以使所有相关值在一起。最后，分区数据减少到结果。

```python
# multiprocessing_mapreduce.py
import collections
import itertools
import multiprocessing


class SimpleMapReduce:

    def __init__(self, map_func, reduce_func, num_workers=None):
        """
        map_func

          Function to map inputs to intermediate data. Takes as
          argument one input value and returns a tuple with the
          key and a value to be reduced.

        reduce_func

          Function to reduce partitioned version of intermediate
          data to final output. Takes as argument a key as
          produced by map_func and a sequence of the values
          associated with that key.

        num_workers

          The number of workers to create in the pool. Defaults
          to the number of CPUs available on the current host.
        """
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.pool = multiprocessing.Pool(num_workers)

    def partition(self, mapped_values):
        """Organize the mapped values by their key.
        Returns an unsorted sequence of tuples with a key
        and a sequence of values.
        """
        partitioned_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()

    def __call__(self, inputs, chunksize=1):
        """Process the inputs through the map and reduce functions
        given.

        inputs
          An iterable containing the input data to be processed.

        chunksize=1
          The portion of the input data to hand to each worker.
          This can be used to tune performance during the mapping
          phase.
        """
        map_responses = self.pool.map(
            self.map_func,
            inputs,
            chunksize=chunksize,
        )
        partitioned_data = self.partition(
            itertools.chain(*map_responses)
        )
        reduced_values = self.pool.map(
            self.reduce_func,
            partitioned_data,
        )
        return reduced_values
```

下面的示例脚本使用 SimpleMapReduce 来计算本文的 reStructuredText 源中的“words”，忽略了一些标记。

```python
# multiprocessing_wordcount.py 
import multiprocessing
import string

from multiprocessing_mapreduce import SimpleMapReduce


def file_to_words(filename):
    """Read a file and return a sequence of
    (word, occurences) values.
    """
    STOP_WORDS = set([
        'a', 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if',
        'in', 'is', 'it', 'of', 'or', 'py', 'rst', 'that', 'the',
        'to', 'with',
    ])
    TR = str.maketrans({
        p: ' '
        for p in string.punctuation
    })

    print('{} reading {}'.format(
        multiprocessing.current_process().name, filename))
    output = []

    with open(filename, 'rt') as f:
        for line in f:
            # Skip comment lines.
            if line.lstrip().startswith('..'):
                continue
            line = line.translate(TR)  # Strip punctuation
            for word in line.split():
                word = word.lower()
                if word.isalpha() and word not in STOP_WORDS:
                    output.append((word, 1))
    return output


def count_words(item):
    """Convert the partitioned data for a word to a
    tuple containing the word and the number of occurences.
    """
    word, occurences = item
    return (word, sum(occurences))


if __name__ == '__main__':
    import operator
    import glob

    input_files = glob.glob('*.rst')

    mapper = SimpleMapReduce(file_to_words, count_words)
    word_counts = mapper(input_files)
    word_counts.sort(key=operator.itemgetter(1))
    word_counts.reverse()

    print('\nTOP 20 WORDS BY FREQUENCY\n')
    top20 = word_counts[:20]
    longest = max(len(word) for word, count in top20)
    for word, count in top20:
        print('{word:<{len}}: {count:5}'.format(
            len=longest + 1,
            word=word,
            count=count)
        )
```

`file_to_words()` 函数将每个输入文件转换为包含单词和数字`1`（表示单个匹配项）的元组序列。通过`partition()` 使用单词作为键来划分数据，因此得到的结构由一个键和`1`表示每个单词出现的值序列组成。`count_words()`在缩小阶段，分区数据被转换为一组元组，其中包含一个单词和该单词的计数。

```python
$ python3 -u multiprocessing_wordcount.py

ForkPoolWorker-1 reading basics.rst
ForkPoolWorker-2 reading communication.rst
ForkPoolWorker-3 reading index.rst
ForkPoolWorker-4 reading mapreduce.rst

TOP 20 WORDS BY FREQUENCY

process         :    83
running         :    45
multiprocessing :    44
worker          :    40
starting        :    37
now             :    35
after           :    34
processes       :    31
start           :    29
header          :    27
pymotw          :    27
caption         :    27
end             :    27
daemon          :    22
can             :    22
exiting         :    21
forkpoolworker  :    21
consumer        :    20
main            :    18
event           :    16
```

相关文档：

https://pymotw.com/3/multiprocessing/index.html

https://thief.one/2016/11/23/Python-multiprocessing/

http://www.dongwm.com/archives/%E4%BD%BF%E7%94%A8Python%E8%BF%9B%E8%A1%8C%E5%B9%B6%E5%8F%91%E7%BC%96%E7%A8%8B-%E8%BF%9B%E7%A8%8B%E7%AF%87/