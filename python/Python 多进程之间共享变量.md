# Python 多进程之间共享变量

Python 多线程之间共享变量很简单，直接定义全局 global 变量即可。而多进程之间是相互独立的执行单元，这种方法就不可行了。

不过 Python 标准库已经给我们提供了这样的能力，使用起来也很简单。但要分两种情况来看，一种是 Process 多进程，一种是 Pool 进程池的方式。

### Process 多进程

使用 Process 定义的多进程之间共享变量可以直接使用 multiprocessing 下的 Value，Array，Queue 等，如果要共享 list，dict，可以使用强大的 Manager 模块。

```python
import multiprocessing


def func(num):
    # 共享数值型变量
    # num.value = 2

    # 共享数组型变量
    num[2] = 9999


if __name__ == '__main__':
    # 共享数值型变量
    # num = multiprocessing.Value('d', 1)
    # print(num.value)

    # 共享数组型变量
    num = multiprocessing.Array('i', [1, 2, 3, 4, 5])
    print(num[:])

    p = multiprocessing.Process(target=func, args=(num,))
    p.start()
    p.join()

    # 共享数值型变量
    # print(num.value)

    # 共享数组型变量
    print(num[:])
```

### Pool 进程池

进程池之间共享变量是不能使用上文方式的，因为进程池内进程关系并非父子进程，想要共享，必须使用 Manage 模块来定义。

```python
from multiprocessing import Pool, Manager


def func(my_list, my_dict):
    my_list.append(10)
    my_list.append(11)
    my_dict['a'] = 1
    my_dict['b'] = 2


if __name__ == '__main__':
    manager = Manager()
    my_list = manager.list()
    my_dict = manager.dict()

    pool = Pool(processes=2)
    for i in range(0, 2):
        pool.apply_async(func, (my_list, my_dict))
    pool.close()
    pool.join()

    print(my_list)
    print(my_dict)
```

还有一点需要注意，在共享 list 时，像下面这样写 func 是不起作用的。

```python
def func(my_list, my_dict):
    my_list = [10, 11]
    my_dict['a'] = 1
    my_dict['b'] = 2
```

这样写相当于重新定义了一个局部变量，并没有作用到原来的 list 上，必须使用 append，extend 等方法。

**参考文档：**

https://blog.csdn.net/houyanhua1/article/details/78244288

**往期精彩：**