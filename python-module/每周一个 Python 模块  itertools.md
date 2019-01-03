

# 每周一个 Python 模块 | itertools

Python 标准库模块 itertools 提供了很多方便灵活的迭代器工具，熟练的运用可以极大的提高工作效率。

## 无限迭代器

### `itertools.count`

```python
count(start=0, step=1)
```

创建一个迭代器，生成从 n 开始的连续整数，如果忽略 n，则从 0 开始计算。示例：

```python
In [2]: for n in itertools.count():
   ...:     if 100000 < n < 100010:
   ...:         print n
   ...:     if n > 1000000:
   ...:         break
   ...:     
100001
100002
100003
100004
100005
100006
100007
100008
100009
```

### `itertools.cycle`

```python
cycle(iterable)
```

把传入的一个序列无限重复下去。示例：

```python
In [6]: count = 0

In [7]: for c in itertools.cycle("AB"):
   ...:     if count > 4:
   ...:         break
   ...:     print c
   ...:     count += 1
   ...:     
A
B
A
B
A
```

### `itertools.repeat`

```python
repeat(object [,times])
```

创建一个迭代器，重复生成 object，times（如果已提供）指定重复计数，如果未提供 times，将无止尽返回该对象。示例：

```python
In [8]: for x in itertools.repeat("hello world", 5):
   ...:     print x
   ...:     
hello world
hello world
hello world
hello world
hello world
```

## 函数式工具

### `itertools.ifilter`、`itertools.reduce`、`itertools.imap`、`itertools.izip`

与内建函数 `filter()`、`reduce()`、`map()`、`zip()` 有同样的功能，只是返回一个迭代器而不是一个序列。在 Python3 中被去掉，因为默认的内建函数就是返回一个迭代器。

### `itertools.ifilterfalse`

```python
ifilterfalse(function or None, sequence)
```

python3 为：

```python
filterfalse(function or None, sequence)
```

与 filter 类似，但仅生成 sequence 中 function(item) 为 False 的项。示例：

```python
In [25]: for elem in itertools.ifilterfalse(lambda x: x > 5, [2, 3, 5, 6, 7]):
   ....:     print elem
   ....:     
2
3
5
```

### `itertools.izip_longest`

```python
izip_longest(iter1 [,iter2 [...]], [fillvalue=None])
```

Python3 为:

```python
zip_longest(iter1 [,iter2 [...]], [fillvalue=None])
```

与 zip 类似，但不同的是它会把最长的 iter 迭代完才结束，其他 iter 如果有缺失值则用 fillvalue 填充。示例：

```python
In [33]: for item in itertools.izip_longest('abcd', '12', fillvalue='-'):
   ....:     print item
   ....:     
('a', '1')
('b', '2')
('c', '-')
('d', '-')
```

### `itertools.starmap`

```python
starmap(function, sequence)
```

对序列 sequence 的每个元素作为 function 的参数列表执行，即 `function(*item)`, 返回执行结果的迭代器。只有当 iterable 生成的项适用于这种调用函数的方式时，此函数才有效。示例：

```python
In [35]: seq = [(0, 5), (1, 6), (2, 7), (3, 3), (3, 8), (4, 9)]

In [36]: for item in itertools.starmap(lambda x,y:(x, y, x*y), seq):
    ...:     print "%d * %d = %d" % item
    ...:     
0 * 5 = 0
1 * 6 = 6
2 * 7 = 14
3 * 3 = 9
3 * 8 = 24
4 * 9 = 36
```

### `itertools.dropwhile`

```python
dropwhile(predicate, iterable)
```

创建一个迭代器，只要函数 predicate(item) 为 True，就丢弃 iterable 中的项，如果 predicate 返回 False，就会生成 iterable 中的项和所有后续项。即在条件为false之后的第一次, 返回迭代器中剩下来的项。示例：

```python
In [41]: for item in itertools.dropwhile(lambda x: x<1, [ -1, 0, 1, 2, 3, 4, 1, -2 ]):
    ...:     print item
    ...:     
1
2
3
4
1
-2
```

### `itertools.takewhile`

```python
takewhile(predicate, iterable)
```

与 dropwhile 相反。创建一个迭代器，生成 iterable 中 predicate(item) 为 True 的项，只要 predicate 计算为 False，迭代就会立即停止。示例：

```python
In [28]: for item in itertools.takewhile(lambda x: x < 2, [ -1, 0, 1, 2, 3, 4, 1, -2 ]):
   ....:     print item
   ....:     
-1
0
1
```

## 组合工具

### `itertools.chain`

```python
chain(*iterables)
```

把一组迭代对象串联起来，形成一个更大的迭代器。示例：

```python
In [9]: for c in itertools.chain('ABC', 'XYZ'):
   ...:     print c
   ...:     
A
B
C
X
Y
Z
```

### `itertools.product`

```python
product(*iterables, repeat=1)
```

创建一个迭代器，生成多个迭代器集合的笛卡尔积，repeat 参数用于指定重复生成序列的次数。示例：

```python
In [6]: for elem in itertools.product((1, 2), ('a', 'b')):
   ...:     print elem
   ...:     
(1, 'a')
(1, 'b')
(2, 'a')
(2, 'b')

In [7]: for elem in itertools.product((1, 2), ('a', 'b'), repeat=2):
   ...:     print elem
   ...:     
(1, 'a', 1, 'a')
(1, 'a', 1, 'b')
(1, 'a', 2, 'a')
(1, 'a', 2, 'b')
(1, 'b', 1, 'a')
(1, 'b', 1, 'b')
(1, 'b', 2, 'a')
(1, 'b', 2, 'b')
(2, 'a', 1, 'a')
(2, 'a', 1, 'b')
(2, 'a', 2, 'a')
(2, 'a', 2, 'b')
(2, 'b', 1, 'a')
(2, 'b', 1, 'b')
(2, 'b', 2, 'a')
(2, 'b', 2, 'b')
```

### `itertools.permutations`

```python
permutations(iterable[, r])
```

返回 iterable 中任意取 r 个元素做**排列**的元组的迭代器，如果不指定 r，那么序列的长度与 iterable 中的项目数量相同。示例：

```python
In [7]: for elem in itertools.permutations('abc', 2):
   ...:     print elem
   ...:     
('a', 'b')
('a', 'c')
('b', 'a')
('b', 'c')
('c', 'a')
('c', 'b')

In [8]: for elem in itertools.permutations('abc'):
   ...:     print elem
   ...:     
('a', 'b', 'c')
('a', 'c', 'b')
('b', 'a', 'c')
('b', 'c', 'a')
('c', 'a', 'b')
('c', 'b', 'a')
```

### `itertools.combinations`

```python
combinations(iterable, r)
```

与 permutations 类似，但组合不分顺序，即如果 iterable 为 "abc"，r 为 2 时，ab 和 ba 则视为重复，此时只放回 ab. 示例：

```python
In [10]: for elem in itertools.combinations('abc', 2):
   ....:     print elem
   ....:     
('a', 'b')
('a', 'c')
('b', 'c')
```

### `itertools.combinations_with_replacement`

```python
combinations_with_replacement(iterable, r)
```

与 combinations 类似，但允许重复值，即如果 iterable 为 "abc"，r 为 2 时，会多出 aa, bb, cc. 示例：

```python
In [14]: for elem in itertools.combinations_with_replacement('abc', 2):
   ....:     print elem
   ....:     
('a', 'a')
('a', 'b')
('a', 'c')
('b', 'b')
('b', 'c')
('c', 'c')
```

## 其他工具

### `itertools.compress`

```python
compress(data, selectors)
```

相当于 bool 选取，只有当 selectors 对应位置的元素为 true 时，才保留 data 中相应位置的元素，否则去除。示例：

```python
In [39]: list(itertools.compress('abcdef', [1, 1, 0, 1, 0, 1]))
Out[39]: ['a', 'b', 'd', 'f']

In [40]: list(itertools.compress('abcdef', [True, False, True]))
Out[40]: ['a', 'c']
```

### `itertools.groupby`

```python
groupby(iterable[, keyfunc])
```

对 iterable 中的元素进行分组。keyfunc 是分组函数，用于对 iterable 的**连续项**进行分组，如果不指定，则默认对 iterable 中的连续相同项进行分组，返回一个 (key, sub-iterator) 的迭代器。示例：

```python
In [45]: for key, value_iter in itertools.groupby('aaabbbaaccd'):
   ....:     print key, list(value_iter)
   ....:     
a ['a', 'a', 'a']
b ['b', 'b', 'b']
a ['a', 'a']
c ['c', 'c']
d ['d']

In [48]: data = ['a', 'bb', 'cc', 'ddd', 'eee', 'f']

In [49]: for key, value_iter in itertools.groupby(data, len):
   ....:     print key, list(value_iter)
   ....:     
1 ['a']
2 ['bb', 'cc']
3 ['ddd', 'eee']
1 ['f']
```

注意，注意，注意：必须先排序后才能分组，因为 `groupby` 是通过比较相邻元素来分组的。可以看第二个例子，因为 a 和 f 没有排在一起，所以最后没有分组到同一个列表中。

### `itertools.islice`

```python
islice(iterable, [start,] stop [, step])
```

切片选择，start 是开始索引，stop 是结束索引，step 是步长，start 和 step 可选。示例：

```python
In [52]: list(itertools.islice([10, 6, 2, 8, 1, 3, 9], 5))
Out[52]: [10, 6, 2, 8, 1]

In [53]: list(itertools.islice(itertools.count(), 6))
Out[53]: [0, 1, 2, 3, 4, 5]

In [54]: list(itertools.islice(itertools.count(), 3, 10))
Out[54]: [3, 4, 5, 6, 7, 8, 9]

In [55]: list(itertools.islice(itertools.count(), 3, 10, 2))
Out[55]: [3, 5, 7, 9]
```

### `itertools.tee`

```python
tee(iterable, n=2)
```

从 iterable 创建 n 个独立的迭代器，以元组的形式返回。示例：

```python
In [57]: itertools.tee("abcedf")
Out[57]: (<itertools.tee at 0x7fed7b8f59e0>, <itertools.tee at 0x7fed7b8f56c8>)

In [58]: iter1, iter2 = itertools.tee("abcedf")

In [59]: list(iter1)
Out[59]: ['a', 'b', 'c', 'e', 'd', 'f']

In [60]: list(iter2)
Out[60]: ['a', 'b', 'c', 'e', 'd', 'f']

In [61]: itertools.tee("abcedf", 3)
Out[61]:
(<itertools.tee at 0x7fed7b8f5cf8>,
 <itertools.tee at 0x7fed7b8f5cb0>,
 <itertools.tee at 0x7fed7b8f5b00>)
```

相关文档：

http://blog.konghy.cn/2017/04/25/python-itertools/

https://juejin.im/post/5af56230f265da0b93485cca#heading-15