### Python 函数式编程

### lambda

lambda 这个关键词在很多语言中都存在。简单地说，它可以实现函数创建的功能。

如下便是 lambda 的两种使用方式。

```python
func1 = lambda : <expression()>
func2 = lambda x : <expression(x)>
func3 = lambda x,y : <expression(x,y)>
```

在第一条语句中，采用 lambda 创建了一个无参的函数 func1。这和下面采用 `def `创建函数的效果是相同的。

```python
def func1():
    <expression()>
```

在第二条和第三条语句中，分别采用 lambda 创建了需要传入 1 个参数的函数 func2，以及传入 2 个参数的函数 func3。这和下面采用`def`创建函数的效果是相同的。

```Python
def func2(x):
    <expression(x)>

def func3(x,y):
    <expression(x,y)>
```

需要注意的是，调用 func1 的时候，虽然不需要传入参数，但是必须要带有括号`()`，否则返回的只是函数的定义，而非函数执行的结果。

```Python
>>> func = lambda : 123
>>> func
<function <lambda> at 0x100f4e1b8>
>>> func()
123
```

另外，虽然在上面例子中都将 lambda 创建的函数赋值给了一个函数名，但这并不是必须的。从下面的例子中大家可以看到，很多时候我们都是直接调用 lambda 创建的函数，而并没有命名一个函数，这也是我们常听说的匿名函数的由来。

### map()

`map()`函数的常见调用形式如下所示：

```Python
map(func, iterable)
```

`map()`需要两个必填参数，第一个参数是一个函数名，第二个参数是一个可迭代的对象，如列表、元组等。

`map()`实现的功能很简单，就是将第二个参数（iterable）中的每一个元素分别传给第一个参数（func），依次执行函数得到结果，并将结果组成一个新的`list`对象后进行返回。返回结果永远都是一个`list`。

简单示例如下：

```Python
>>> double_func = lambda s : s * 2
>>> map(double_func, [1,2,3,4,5])
[2, 4, 6, 8, 10]
```

除了传入一个可迭代对象这种常见的模式外，`map()`还支持传入多个可迭代对象。

```Python
map(func, iterable1, iterable2)
```

在传入多个可迭代对象的情况下，`map()`会依次从所有可迭代对象中依次取一个元素，组成一个元组列表，然后将元组依次传给 func；若可迭代对象的长度不一致，则会以 None 进行补上。

通过以下示例应该就比较容易理解。

```Python
>>> plus = lambda x,y : (x or 0) + (y or 0)
>>> map(plus, [1,2,3], [4,5,6])
[5, 7, 9]
>>> map(plus, [1,2,3,4], [4,5,6])
[5, 7, 9, 4]
>>> map(plus, [1,2,3], [4,5,6,7])
[5, 7, 9, 7]
```

在上面的例子中，之所以采用`x or 0`的形式，是为了防止`None + int`出现异常。

需要注意的是，可迭代对象的个数应该与 func 的参数个数一致，否则就会出现异常，因为传参个数与函数参数个数不一致了，这个应该比较好理解。

```Python
>>> plus = lambda x,y : x + y
>>> map(plus, [1,2,3])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: <lambda>() takes exactly 2 arguments (1 given)
```

另外，`map()`还存在一种特殊情况，就是 func 为 None。这个时候，`map()`仍然是从所有可迭代对象中依次取一个元素，组成一个元组列表，然后将这个元组列表作为结果进行返回。

```Python
>>> map(None, [1,2,3,4])
[1, 2, 3, 4]
>>> map(None, [1,2,3,4], [5,6,7,8])
[(1, 5), (2, 6), (3, 7), (4, 8)]
>>> map(None, [1,2,3,4], [5,6,7])
[(1, 5), (2, 6), (3, 7), (4, None)]
>>> map(None, [1,2,3,4], [6,7,8,9], [11,12])
[(1, 6, 11), (2, 7, 12), (3, 8, None), (4, 9, None)]
```

### reduce()

`reduce()`函数的调用形式如下所示：

```
reduce(func, iterable[, initializer])
```

`reduce()`函数的功能是对可迭代对象（iterable）中的元素从左到右进行累计运算，最终得到一个数值。第三个参数 initializer 是初始数值，可以空置，空置为 None 时就从可迭代对象（iterable）的第二个元素开始，并将第一个元素作为之前的结果。

文字描述可能不大清楚，看下`reduce()`的源码应该就比较清晰了。

```Python
def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        try:
            initializer = next(it)
        except StopIteration:
            raise TypeError('reduce() of empty sequence with no initial value')
    accum_value = initializer
    for x in it:
        accum_value = function(accum_value, x)
    return accum_value
```

再加上如下示例，对`reduce()`的功能应该就能掌握了。

```Python
>>> plus = lambda x, y : x + y
>>> reduce(plus, [1,2,3,4,5])
15
>>> reduce(plus, [1,2,3,4,5], 10)
25
```

### filter()

`filter()`函数的调用形式如下：

```python
filter(func, iterable)
```

`filter()`有且仅有两个参数，第一个参数是一个函数名，第二个参数是一个可迭代的对象，如列表、元组等。

`filter()`函数的调用形式与`map()`比较相近，都是将第二个参数（iterable）中的每一个元素分别传给第一个参数（func），依次执行函数得到结果；差异在于，`filter()`会判断每次执行结果的`bool`值，并只将`bool`值为`true`的筛选出来，组成一个新的列表并进行返回。

```Python
>>> mode2 = lambda x : x % 2
>>> filter(mode2, [1,2,3,4,5,6,7,8,9,10])
[1, 3, 5, 7, 9]
```

### zip()

`zip()`函数的调用形式如下：

```Python
zip([iterable, ...])
```

`zip()`函数接收一个或多个可迭代对象，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。

```Python
>>> zip([1, 2, 3], ["a", "b", "c"])
[(1, 'a'), (2, 'b'), (3, 'c')]
>>> dict(zip([1, 2, 3], ["a", "b", "c"]))
{1: 'a', 2: 'b', 3: 'c'}
>>> dict(zip([1, 2, 3], ["a", "b"]))
{1: 'a', 2: 'b'}
```

打包元组个数与最短列表个数一致。

### enumerate()

`enumerate()`函数的调用形式如下：

```Python
enumerate(iterable, [start=0])
```

`enumerate()`函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。

```Python
>>> enumerate(['Spring', 'Summer', 'Fall', 'Winter'])
<enumerate object at 0x1031780>
>>> list(enumerate(['Spring', 'Summer', 'Fall', 'Winter']))
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
```

### all()、any()

`all()`、`any()`函数的调用形式如下：

```Python
all(iterable)
any(iterable)
```

这两个函数比较简单，即判定一个可迭代对象是否全为 True 或者有为 True 的。

```Python
>>> all([0, 1, 2])
False
>>> any([0, 1, 2])
True
```



相关文档：

https://zhuanlan.zhihu.com/p/23384430

https://coolshell.cn/articles/10822.html

https://debugtalk.com/post/python-functional-programming-getting-started/