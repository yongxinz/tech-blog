# 每周一个 Python 模块 | signal

信号是 Unix 系统中常见的一种进程间通信方式（IPC），例如我们经常操作的 `kill -9 pid`，这里的 `-9`对应的就是 SIGKILL 信号，9 就是这个信号的编号，SIGKILL 是它的名称。 由于不同版本的 *nux 的实现会有差异，具体请参照系统 API，可以使用 `man 7 signal` 查看所有信号的定义。

那么，信号有哪些使用场景呢？与其他进程间通信方式（例如管道、共享内存等）相比，信号所能传递的信息比较粗糙，只是一个整数。但正是由于传递的信息量少，信号也更便于管理和使用，可以用于系统管理相关的任务。例如通知进程终结、中止或者恢复等。每种信号用一个整型常量宏表示，以 SIG 开头，比如 SIGCHLD、SIGINT 等。

## 接收信号

Python 中使用 signal 模块来处理信号相关的操作，定义如下：

```python
signal.signal(signalnum, handler)
```

signalnum 为某个信号，handler 为该信号的处理函数。进程可以无视信号，可以采取默认操作，还可以自定义操作。当 handler 为 signal.SIG_IGN 时，信号被无视（ignore）；当 handler 为 singal.SIG_DFL，进程采取默认操作（default）；当 handler 为一个函数名时，进程采取函数中定义的操作。

写一个小程序，来处理 `ctrl+c`事件和 `SIGHUP`，也就是 1 和 2 信号。

```
#coding:utf-8

import signal
import time
import sys
import os

def handle_int(sig, frame):
    print "get signal: %s, I will quit"%sig
    sys.exit(0)

def handle_hup(sig, frame):
    print "get signal: %s"%sig


if __name__ == "__main__":
    signal.signal(2, handle_int)
    signal.signal(1, handle_hup)
    print "My pid is %s"%os.getpid()
    while True:
        time.sleep(3)
```

我们来测试下，首先启动程序（根据打印的 pid），在另外的窗口输入 `kill -1 21838` 和 `kill -HUP 21838`, 最后使用 `ctrl+c`关闭程序。 程序的输出如下：

```
# python recv_signal.py
My pid is 21838
get signal: 1
get signal: 1
^Cget signal: 2, I will quit
```

再来看另一个函数，可以对信号理解的更加透彻：

```python
signal.getsignal(signalnum)
```

根据 signalnum 返回信号对应的 handler，可能是一个可以调用的 Python 对象，或者是 `signal.SIG_IGN`（表示被忽略）, `signal.SIG_DFL`（默认行为已经被使用）或 `None`（Python 的 handler 还没被定义）。

看下面这个例子，获取 signal 中定义的信号 num 和名称，还有它的 handler 是什么。

```
#coding:utf-8

import signal

def handle_hup(sig, frame):
    print "get signal: %s"%sig

signal.signal(1, handle_hup)

if __name__ == "__main__":

    ign = signal.SIG_IGN
    dfl = signal.SIG_DFL
    print "SIG_IGN", ign
    print "SIG_DFL", dfl
    print "*"*40

    for name in dir(signal):
        if name[:3] == "SIG" and name[3] != "_":
            signum = getattr(signal, name)
            gsig = signal.getsignal(signum)

            print name, signum, gsig
```

运行的结果：可以看到大部分信号都是都有默认的行为。

```
SIG_IGN 1
SIG_DFL 0
****************************************
SIGABRT 6 0
SIGALRM 14 0
SIGBUS 10 0
SIGCHLD 20 0
SIGCONT 19 0
SIGEMT 7 0
SIGFPE 8 0
SIGHUP 1 <function handle_hup at 0x109371c80>
SIGILL 4 0
SIGINFO 29 0
SIGINT 2 <built-in function default_int_handler>
SIGIO 23 0
SIGIOT 6 0
SIGKILL 9 None
SIGPIPE 13 1
SIGPROF 27 0
SIGQUIT 3 0
SIGSEGV 11 0
SIGSTOP 17 None
SIGSYS 12 0
SIGTERM 15 0
SIGTRAP 5 0
SIGTSTP 18 0
SIGTTIN 21 0
SIGTTOU 22 0
SIGURG 16 0
SIGUSR1 30 0
SIGUSR2 31 0
SIGVTALRM 26 0
SIGWINCH 28 0
SIGXCPU 24 0
SIGXFSZ 25 1
```

常用的几个信号：

| 编号 | 名称    | 作用                                                         |
| ---- | ------- | ------------------------------------------------------------ |
| 1    | SIGHUP  | 终端挂起或者终止进程。默认动作为终止进程                     |
| 2    | SIGINT  | 键盘中断 `<ctrl+c>` 经常会用到。默认动作为终止进程           |
| 3    | SIGQUIT | 键盘退出键被按下。一般用来响应 `<ctrl+d>`。 默认动作终止进程 |
| 9    | SIGKILL | 强制退出。 shell中经常使用                                   |
| 14   | SIGALRM | 定时器超时，默认为终止进程                                   |
| 15   | SIGTERM | 程序结束信号，程序一般会清理完状态在退出，我们一般说的优雅的退出 |

## 发送信号

signal 包的核心是设置信号处理函数。除了 `signal.alarm()` 向自身发送信号之外，并没有其他发送信号的功能。但在 os 包中，有类似于 Linux 的 kill 命令的函数，分别为：

```python
os.kill(pid, sid)
os.killpg(pgid, sid)
```

分别向进程和进程组发送信号。sid 为信号所对应的整数或者 singal.SIG*。

## 定时发出 SIGALRM 信号

它被用于在一定时间之后，向进程自身发送 SIGALRM 信号，这对于避免无限期地阻塞 I/O 操作或其他系统调用很有用。

```python
import signal
import time


def receive_alarm(signum, stack):
    print('Alarm :', time.ctime())


# Call receive_alarm in 2 seconds
signal.signal(signal.SIGALRM, receive_alarm)
signal.alarm(2)

print('Before:', time.ctime())
time.sleep(4)
print('After :', time.ctime())

# output
# Before: Sat Apr 22 14:48:57 2017
# Alarm : Sat Apr 22 14:48:59 2017
# After : Sat Apr 22 14:49:01 2017
```

在此示例中，调用 `sleep()` 被中断，但在信号处理后继续，因此`sleep()`返回后打印的消息显示程序执行时间与睡眠持续时间一样长。

## 忽略信号

要忽略信号，请注册 SIG_IGN 为处理程序。

下面这个例子注册了两个程序，分别是 SIGINT 和 SIGUSR1，然后用 `signal.pause()` 等待接收信号。

```python
import signal
import os
import time


def do_exit(sig, stack):
    raise SystemExit('Exiting')


signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGUSR1, do_exit)

print('My PID:', os.getpid())

signal.pause()

# output
# My PID: 72598
# ^C^C^C^CExiting
```

通常 SIGINT（当用户按下 `Ctrl-C` 时由 shell 发送到程序的信号）会引发 `KeyboardInterrupt`。这个例子在它看到 SIGINT 时直接忽略了。输出中的每个 `^C` 表示尝试从终端终止脚本。

从另一个终端使用 `kill -USR1 72598` 将脚本退出。

## 信号与线程

多线程环境下使用信号，只有 main thread 可以设置 signal 的 handler，也只有它能接收到 signal. 下面用一个例子看看效果，在一个线程中等待信号，并从另一个线程发送信号。

```python
#coding:utf-8
#orangleliu py2.7
#thread_signal.py

import signal
import threading
import os
import time

def usr1_handler(num, frame):
    print "received signal %s %s"%(num, threading.currentThread())

signal.signal(signal.SIGUSR1, usr1_handler)

def thread_get_signal():
    #如果在子线程中设置signal的handler 会报错
    #ValueError: signal only works in main thread
    #signal.signal(signal.SIGUSR2, usr1_handler)

    print "waiting for signal in", threading.currentThread()
    #sleep 进程直到接收到信号
    signal.pause()
    print "waiting done"

receiver = threading.Thread(target=thread_get_signal, name="receiver")
receiver.start()
time.sleep(0.1)

def send_signal():
    print "sending signal in ", threading.currentThread()
    os.kill(os.getpid(), signal.SIGUSR1)

sender = threading.Thread(target=send_signal, name="sender")
sender.start()
sender.join()

print 'pid', os.getpid()
# 这里是为了让程序结束，唤醒 pause
signal.alarm(2)
receiver.join()

# output
# waiting for signal in <Thread(receiver, started 123145306509312)>
# sending signal in  <Thread(sender, started 123145310715904)>
# received signal 30 <_MainThread(MainThread, started 140735138967552)>
# pid 23188
# [1]    23188 alarm      python thread_signal.py
```

Python 的 signal 模块要求，所有的 handlers 必需在 main thread 中注册，即使底层平台支持线程和信号混合编程。即使接收线程调用了 `signal.pause()`，但还是没有接收到信号。代码结尾处的 `signal.alarm(2)` 是为了唤醒接收线程的 `pause()`，否则接收线程永远不会退出。

尽管 alarms 可以在任意的线程中设置，但他们只能在 main thread 接收。

```python
import signal
import time
import threading


def signal_handler(num, stack):
    print(time.ctime(), 'Alarm in',
          threading.currentThread().name)


signal.signal(signal.SIGALRM, signal_handler)


def use_alarm():
    t_name = threading.currentThread().name
    print(time.ctime(), 'Setting alarm in', t_name)
    signal.alarm(1)
    print(time.ctime(), 'Sleeping in', t_name)
    time.sleep(3)
    print(time.ctime(), 'Done with sleep in', t_name)


# Start a thread that will not receive the signal
alarm_thread = threading.Thread(
    target=use_alarm,
    name='alarm_thread',
)
alarm_thread.start()
time.sleep(0.1)

# Wait for the thread to see the signal (not going to happen!)
print(time.ctime(), 'Waiting for', alarm_thread.name)
alarm_thread.join()

print(time.ctime(), 'Exiting normally')

# output
# Sat Apr 22 14:49:01 2017 Setting alarm in alarm_thread
# Sat Apr 22 14:49:01 2017 Sleeping in alarm_thread
# Sat Apr 22 14:49:01 2017 Waiting for alarm_thread
# Sat Apr 22 14:49:02 2017 Alarm in MainThread
# Sat Apr 22 14:49:04 2017 Done with sleep in alarm_thread
# Sat Apr 22 14:49:04 2017 Exiting normally
```

alarm 并没有中断 `use_alarm()` 中的 `sleep`。

相关文档：

https://pymotw.com/3/signal/index.html

http://orangleliu.info/2016/03/06/python-signal-module-simple-use/

http://www.cnblogs.com/vamei/archive/2012/10/06/2712683.html