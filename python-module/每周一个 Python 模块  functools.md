# 每周一个 Python 模块 | functools

functools 是 Python 中很简单但也很重要的模块，主要是一些 Python 高阶函数相关的函数。 该模块的内容并不多，看 [官方文档](https://docs.python.org/2/library/functools.html) 也就知道了。

说到高阶函数，这是函数式编程范式中很重要的一个概念，简单地说， 就是一个可以接受函数作为参数或者以函数作为返回值的函数，因为 Python 中函数是一类对象， 因此很容易支持这样的函数式特性。

functools 模块中函数只有 `cmp_to_key`、`partial`、`reduce`、`total_ordering`、`update_wrapper`、`wraps`、`lru_cache` 这几个：

## 被发配边疆的 `reduce`

这个 `functools.reduce` 就是 Python 2 内建库中的 `reduce`，它之所以出现在这里就是因为 Guido 的独裁，他并不喜欢函数式编程中的“map-reduce”概念，因此打算将 `map` 和 `reduce` 两个函数移出内建函数库，最后在社区的强烈反对中将 `map` 函数保留在了内建库中， 但是 Python 3 内建的 `map` 函数返回的是一个迭代器对象，而 Python 2 中会 eagerly 生成一个 list，使用时要多加注意。

该函数的作用是将一个序列归纳为一个输出，其原型如下：

```python
reduce(function, sequence, startValue)
```

使用示例：

```python
>>> def foo(x, y):
...     return x + y
...
>>> l = range(1, 10)
>>> reduce(foo, l)
45
>>> reduce(foo, l, 10)
55
```

## 偏函数 `partial` 和 `partialmethod`

用于创建一个偏函数，它用一些默认参数包装一个可调用对象，返回结果是可调用对象，并且可以像原始对象一样对待，这样可以简化函数调用。

一个简单的使用示例：

``` python
from functools import partial

def add(x, y):
    return x + y

add_y = partial(add, 3)  # add_y 是一个新的函数
add_y(4) # 7
```

一个很实用的例子：

```python
def json_serial_fallback(obj):
    """
    JSON serializer for objects not serializable by default json code
    """
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return str(obj)
    if isinstance(obj, bytes):
        return obj.decode("utf-8")
    raise TypeError ("%s is not JSON serializable" % obj)

json_dumps = partial(json.dumps, default=json_serial_fallback)
```

可以在 `json_serial_fallback` 函数中添加类型判断来指定如何 json 序列化一个 Python 对象

[`partialmethod`](https://docs.python.org/3/library/functools.html#functools.partialmethod) 是 Python 3.4 中新引入的装饰器，作用基本类似于 `partial`， 不过仅作用于方法。举个例子就很容易明白：

```python
class Cell(object):
    def __init__(self):
        self._alive = False
    @property
    def alive(self):
        return self._alive
    def set_state(self, state):
        self._alive = bool(state)
        
    set_alive = partialmethod(set_state, True)
    set_dead = partialmethod(set_state, False)

c = Cell()
c.alive         # False
c.set_alive()
c.alive         # True
```

在 Python 2 中使用 partialmethod 可以这样定义：

```python
# Code from https://gist.github.com/carymrobbins/8940382
from functools import partial

class partialmethod(partial):
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return partial(self.func, instance,
                       *(self.args or ()), **(self.keywords or {}))
```

## 装饰器相关

说到“接受函数为参数，以函数为返回值”，在 Python 中最常用的当属装饰器了。 functools 库中装饰器相关的函数是 `update_wrapper`、`wraps`，还搭配 `WRAPPER_ASSIGNMENTS` 和 `WRAPPER_UPDATES` 两个常量使用，作用就是消除 Python 装饰器的一些负面作用。

### `wraps`

例：

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def add(x, y):
    return x + y

add     # <function __main__.wrapper>
```

可以看到被装饰的函数的名称，也就是函数的 `__name__` 属性变成了 `wrapper`， 这就是装饰器带来的副作用，实际上`add` 函数整个变成了 `decorator(add)`，而 `wraps` 装饰器能消除这些副作用：

```python
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def add(x, y):
    return x + y

add     # <function __main__.add>
```

更正的属性定义在 `WRAPPER_ASSIGNMENTS` 中：

```python
>>> functools.WRAPPER_ASSIGNMENTS
('__module__', '__name__', '__doc__')
>>> functools.WRAPPER_UPDATES
('__dict__',)
```

### `update_wrapper`

`update_wrapper` 的作用与 `wraps` 类似，不过功能更加强大，换句话说，`wraps` 其实是 `update_wrapper` 的特殊化，实际上 `wraps(wrapped)` 相当于 `partial(update_wrapper, wrapped=wrapped, **kwargs)`。

因此，上面的代码可以用 `update_wrapper` 重写如下：

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return update_wrapper(wrapper, func)
```

## 用于比较的 `cmp_to_key` 和 `total_ordering`

### `cmp_to_key`

在 `list.sort` 和 内建函数 `sorted ` 中都有一个 key 参数，这个参数用来指定取元素的什么值进行比较，例如按字符串元素的长度进行比较：

```python
>>> x = ['hello','abc','iplaypython.com']
>>> x.sort(key=len)
>>> x
['abc', 'hello', 'iplaypython.com']
```

也就是说排序时会先对每个元素调用 key 所指定的函数，然后再排序。同时，`sorted ` 和 `list.sort` 还提供了 cmp 参数来指定如何比较两个元素，但是在 Python 3 中该参数被去掉了。

`cmp_to_key` 是 Python 2.7 中新增的函数，用于将比较函数转换为 key 函数， 这样就可以应用在接受 key 函数为参数的函数中。比如 `sorted()`、`min()`、 `max()`、 `heapq.nlargest()`、 `itertools.groupby()` 等。

```python
sorted(range(5), key=cmp_to_key(lambda x, y: y-x))      # [4, 3, 2, 1, 0]
```

### `total_ordering`

`total_ordering` 同样是 Python 2.7 中新增函数，用于简化比较函数的写法。如果你已经定义了`__eq__` 方法，以及 `__lt__`、`__le__`、`__gt__` 或者 `__ge__()` 其中之一， 即可自动生成其它比较方法。官方示例：

```python
@total_ordering
class Student:
    def __eq__(self, other):
        return ((self.lastname.lower(), self.firstname.lower()) ==
                (other.lastname.lower(), other.firstname.lower()))
    def __lt__(self, other):
        return ((self.lastname.lower(), self.firstname.lower()) <
                (other.lastname.lower(), other.firstname.lower()))

dir(Student)    # ['__doc__', '__eq__', '__ge__', '__gt__', '__le__', '__lt__', '__module__']
```

再看一个示例：

```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def __eq__(self, other):
        return ((self.lastname.lower(), self.firstname.lower()) ==
                (other.lastname.lower(), other.firstname.lower()))

    def __lt__(self, other):
        return ((self.lastname.lower(), self.firstname.lower()) <
                (other.lastname.lower(), other.firstname.lower()))

print dir(Student)

stu = Student("Huoty", "Kong")
stu2 = Student("Huoty", "Kong")
stu3 = Student("Qing", "Lu")

print stu == stu2
print stu > stu3
```

输出结果：

```python
['__doc__', '__eq__', '__ge__', '__gt__', '__init__', '__le__', '__lt__', '__module__']
True
False
```

## 用于缓存的`lru_cache`

这个装饰器是在 Python3 中新加的，在 Python2 中如果想要使用可以安装第三方库 `functools32`。该装饰器用于缓存函数的调用结果，对于需要多次调用的函数，而且每次调用参数都相同，则可以用该装饰器缓存调用结果，从而加快程序运行。示例：

```python
from functools import lru_cache
@lru_cache(None)
def add(x, y):
    print("calculating: %s + %s" % (x, y))
    return x + y

print(add(1, 2))
print(add(1, 2))  # 直接返回缓存信息
print(add(2, 3))
```

输出结果：

```python
calculating: 1 + 2
3
3
calculating: 2 + 3
5
```

由于该装饰器会将不同的调用结果缓存在内存中，因此需要注意内存占用问题，避免占用过多内存，从而影响系统性能。



相关文档：

https://blog.windrunner.me/python/functools.html

http://kuanghy.github.io/2016/10/26/python-functools

https://pymotw.com/3/