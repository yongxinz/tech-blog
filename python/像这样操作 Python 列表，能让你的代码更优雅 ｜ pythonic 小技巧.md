# 像这样操作 Python 列表，能让你的代码更优雅 ｜ pythonic 小技巧

写 Python 代码，列表的出镜率是相当高的，伴随列表一起出现的往往就是一大堆 `for` 循环，这样的代码多了看起来非常不简洁。作为一名 Python 程序员，怎么能忍受呢？

那有没有什么好办法呢？除了列表表达式之外，其实还有一些小技巧来操作列表，可以使代码更简洁，更优雅。下面介绍几个常见的使用场景，分享给大家。

### 一、列表合并

第一种方式：循环。

```python
>>> a = [1, 2, 3]
>>> b = [4, 5, 6]
>>> for i in b:
...     a.append(i)
...
>>> a
[1, 2, 3, 4, 5, 6]
```

这种方式最不友好了，也不建议使用。

第二种方式：使用 `+`。

```python
>>> a + b
[1, 2, 3, 4, 5, 6]
```

第三种方式：使用 `extend` 关键字。

```python
>>> a.extend(b)
>>> a
[1, 2, 3, 4, 5, 6]
```

后两种方式明显更加优雅，推荐使用。需要说明的一点是，如果列表很大的话，`+` 会比较慢，使用 `extend` 更好。

### 二、列表元素去重

使用 `set()` 对列表元素进行去重。

```python
>>> a = [1, 2, 3, 4, 2, 3]
>>> list(set(a))
[1, 2, 3, 4]
```

### 三、列表排序

使用 `sort()` 或内建函数 `sorted()` 对列表进行排序。它们之间的区别有两点：

1. `sort()` 方法是对原列表进行操作，而 `sorted()` 方法会返回一个新列表，不是在原来的基础上进行操作。
2. `sort()` 是应用在列表上的方法，而 `sorted()` 可以对所有可迭代的对象进行排序操作。

```python
# sort()
>>> a = [1, 2, 3, 4, 2, 3]
>>> a.sort()
>>> a
[1, 2, 2, 3, 3, 4]
>>>
>>> a = [1, 2, 3, 4, 2, 3]
>>> a.sort(reverse=True)
>>> a
[4, 3, 3, 2, 2, 1]

# sorted()
>>> a = [1, 2, 3, 4, 2, 3]
>>> sorted(a)
[1, 2, 2, 3, 3, 4]
>>> a = [1, 2, 3, 4, 2, 3]
>>> sorted(a, reverse=True)
[4, 3, 3, 2, 2, 1]
```

### 四、遍历列表的索引和元素对

使用 `enumerate()` 函数可以同时输出索引和元素值。

```python
>>> a = ['python', 'go', 'java']
>>> for i, v in enumerate(a):
...     print(i, v)

# output
0 python
1 go
2 java
```

### 五、查找列表中出现最频繁的元素

使用 `max()` 函数可以快速查找出一个列表中出现频率最高的某个元素。

```python
>>> a = [1, 2, 3, 4, 3, 4, 5, 4, 4, 2]
>>> b = max(set(a), key=a.count)
>>> b
4
```

需要说明的一点是，当列表中有两个元素出现的次数相同时，会返回第一个出现的元素。

```python
>>> a = [1, 2]
>>> b = max(set(a), key=a.count)
>>> b
1
```

### 六、统计列表中所有元素的出现次数

前面的代码给出了出现最频繁的值。如果想要知道列表中所有元素的出现次数，那么可以使用 collections 模块。collections 是 Python 中的一个宝藏模块，它提供了很多特性。`Counter` 方法正好可以完美解决这个需求。

```python
>>> from collections import Counter
>>>
>>> a = [1, 2, 3, 4, 3, 4, 5, 4, 4, 2]
>>> Counter(a)
Counter({4: 4, 2: 2, 3: 2, 1: 1, 5: 1})
```

### 七、将两个列表合并为词典

使用 `zip()` 函数，可以将两个列表合并成字典。

```python
>>> a = ['one', 'tow', 'three']
>>> b = [1, 2, 3]
>>> dict(zip(a, b))
{'one': 1, 'tow': 2, 'three': 3}
```

以上。

希望对你能有帮助，欢迎关注公众号 **AlwaysBeta**，更多技术干货等你来。

**题图：**

**往期精彩：**

