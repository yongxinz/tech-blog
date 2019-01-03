# 每周一个 Python 模块 | collections

Python 作为一个“内置电池”的编程语言，标准库里面拥有非常多好用的模块。比如今天想给大家 介绍的 `collections` 就是一个非常好的例子。

## 基本介绍

我们都知道，Python 拥有一些内置的数据类型，比如 str, int, list, tuple, dict 等， collections 模块在这些内置数据类型的基础上，提供了几个额外的数据类型：

- `ChainMap`：将多个字典组成一个新的单元，Python3 新特性；
- `Counter`：计数器，主要用来计数；
- `deque`：双端队列，可以快速的从另外一侧追加和推出对象；
- `namedtuple`：生成可以使用名字来访问元素内容的 tuple 子类；
- `defaultdict`：带有默认值的字典；
- `OrderedDict`：有序字典。

## ChainMap

用 `ChainMap` 来管理字典序列，并且通过顺序搜索来找到 `key` 对应的值。

### 访问值

`ChainMap` 和普通字典一样，支持相同的 API 访问现有的值。

```python
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)

print('Individual Values')
print('a = {}'.format(m['a']))
print('b = {}'.format(m['b']))
print('c = {}'.format(m['c']))
print()

print('Keys = {}'.format(list(m.keys())))
print('Values = {}'.format(list(m.values())))
print()

print('Items:')
for k, v in m.items():
    print('{} = {}'.format(k, v))
print()

print('"d" in m: {}'.format(('d' in m)))

# output
# Individual Values
# a = A
# b = B
# c = C
# 
# Keys = ['c', 'b', 'a']
# Values = ['C', 'B', 'A']
# 
# Items:
# c = C
# b = B
# a = A
# 
# "d" in m: False
```

`ChainMap` 按照传递给它的顺序进行搜索，所以键 `c` 对应的值来自字典 `a`。

### 重新排序

可以通过 `maps` 属性将结果以列表形式返回。由于列表是可变的，所以可以对这个列表重新排序，或者添加新的值。

```python
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)

print(m.maps)	# [{'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'}]
print('c = {}\n'.format(m['c']))	# c = C

# reverse the list
m.maps = list(reversed(m.maps))

print(m.maps)	# [{'b': 'B', 'c': 'D'}, {'a': 'A', 'c': 'C'}]
print('c = {}'.format(m['c']))	# c = D
```

### 更新值

`ChainMap` 不会给子映射创建一个单独的空间，所以对子映射修改时，结果也会反馈到 `ChainMap` 上。

```python
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)
print('Before: {}'.format(m['c']))	# Before: C
a['c'] = 'E'
print('After : {}'.format(m['c']))	# After : E
```

也可以通过 `ChainMap` 直接设置值，实际上只修改了第一个字典中的值。

```python
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)
print('Before:', m)	# Before: ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
m['c'] = 'E'
print('After :', m)	# After : ChainMap({'a': 'A', 'c': 'E'}, {'b': 'B', 'c': 'D'})
print('a:', a)	# a: {'a': 'A', 'c': 'E'}
```

`ChainMap`提供了一个简单的方法，用于在`maps`列表的前面创建一个新实例，这样做的好处是可以避免修改现有的底层数据结构。

```python
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m1 = collections.ChainMap(a, b)
m2 = m1.new_child()

print(m1)	# ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
print(m2)	# ChainMap({}, {'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})

m2['c'] = 'E'

print(m1)	# ChainMap({'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
print(m2)	# ChainMap({'c': 'E'}, {'a': 'A', 'c': 'C'}, {'b': 'B', 'c': 'D'})
```

这种堆叠行为使得将`ChainMap` 实例用作模板或应用程序上下文变得非常方便。具体来说，在一次迭代中很容易添加或更新值，然后丢弃下一次迭代的更改。

对于新上下文已知或预先构建的情况，也可以将映射传递给`new_child()`。

```python
import collections

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}
c = {'c': 'E'}

m1 = collections.ChainMap(a, b)
m2 = m1.new_child(c)

print('m1["c"] = {}'.format(m1['c']))	# m1["c"] = C
print('m2["c"] = {}'.format(m2['c']))	# m2["c"] = E
```

这相当于：

```python
m2 = collections.ChainMap(c, *m1.maps)
```

## Counter

`Counter` 函数用来统计一个容器中相等值出现的次数。

### 初始化

`Counter ` 支持三种初始化形式：

```python
import collections

print(collections.Counter(['a', 'b', 'c', 'a', 'b', 'b']))
print(collections.Counter({'a': 2, 'b': 3, 'c': 1}))
print(collections.Counter(a=2, b=3, c=1))

# output
# Counter({'b': 3, 'a': 2, 'c': 1})
# Counter({'b': 3, 'a': 2, 'c': 1})
# Counter({'b': 3, 'a': 2, 'c': 1})
```

`Counter` 初始化时也可以不传参数，然后通过`update()`方法更新。

```python
import collections

c = collections.Counter()
print('Initial :', c)	# Initial : Counter()

c.update('abcdaab')
print('Sequence:', c)	# Sequence: Counter({'a': 3, 'b': 2, 'c': 1, 'd': 1})

c.update({'a': 1, 'd': 5})
print('Dict    :', c)	# Dict    : Counter({'d': 6, 'a': 4, 'b': 2, 'c': 1})
```

计数值基于新数据而不是替换而增加。在上例中，计数`a`从`3`到 `4`。

### 访问计数

`Counter` 中的值，可以使用字典 API 获取它的值。

```python
import collections

c = collections.Counter('abcdaab')

for letter in 'abcde':
    print('{} : {}'.format(letter, c[letter]))
    
# output
# a : 3
# b : 2
# c : 1
# d : 1
# e : 0
```

对于 `Counter` 中没有的键，不会报 `KeyError`。如本例中的 `e`，将其计数为`0`。

`elements()`方法返回一个迭代器，遍历它可以获得 `Counter` 中的值。

```python
import collections

c = collections.Counter('extremely')
c['z'] = 0
print(c)	# Counter({'e': 3, 'x': 1, 't': 1, 'r': 1, 'm': 1, 'l': 1, 'y': 1, 'z': 0})
print(list(c.elements()))	# ['e', 'e', 'e', 'x', 't', 'r', 'm', 'l', 'y']
```

不保证元素的顺序，并且不包括计数小于或等于零的值。

使用`most_common()`产生序列最常遇到的输入值和它们各自的计数。

```python
import collections

c = collections.Counter()
with open('/usr/share/dict/words', 'rt') as f:
    for line in f:
        c.update(line.rstrip().lower())

print('Most common:')
for letter, count in c.most_common(3):
    print('{}: {:>7}'.format(letter, count))
    
# output
# Most common:
# e:  235331
# i:  201032
# a:  199554
```

此示例计算在系统字典所有单词中的字母生成频率分布，然后打印三个最常见的字母。如果没有参数的话，会按频率顺序生成所有项目的列表。

### 算术

`Counter`实例支持算术和聚合结果。这个例子显示了标准的操作符计算新的`Counter`实例，就地操作符 `+=`，`-=`，`&=`，和`|=`也支持。

```python
import collections

c1 = collections.Counter(['a', 'b', 'c', 'a', 'b', 'b'])
c2 = collections.Counter('alphabet')

print('C1:', c1)
print('C2:', c2)

print('\nCombined counts:')
print(c1 + c2)

print('\nSubtraction:')
print(c1 - c2)

print('\nIntersection (taking positive minimums):')
print(c1 & c2)

print('\nUnion (taking maximums):')
print(c1 | c2)

# output
# C1: Counter({'b': 3, 'a': 2, 'c': 1})
# C2: Counter({'a': 2, 'l': 1, 'p': 1, 'h': 1, 'b': 1, 'e': 1, 't': 1})
# 
# Combined counts:
# Counter({'a': 4, 'b': 4, 'c': 1, 'l': 1, 'p': 1, 'h': 1, 'e': 1, 't': 1})
# 
# Subtraction:
# Counter({'b': 2, 'c': 1})
# 
# Intersection (taking positive minimums):
# Counter({'a': 2, 'b': 1})
# 
# Union (taking maximums):
# Counter({'b': 3, 'a': 2, 'c': 1, 'l': 1, 'p': 1, 'h': 1, 'e': 1, 't': 1})
```

每次`Counter`通过操作产生新的时，任何具有零或负计数的项目都将被丢弃。计数`a` 在`c1`和`c2`中是相同的，因此相减之后变为零。

## deque

双端队列，支持在队列的任意一端添加和删除元素，常用的堆栈和队列可以看做是它的简化形式。

```python
import collections

d = collections.deque('abcdefg')
print('Deque:', d)	# Deque: deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
print('Length:', len(d))	# Length: 7
print('Left end:', d[0])	# Left end: a
print('Right end:', d[-1])	# Right end: g

d.remove('c')
print('remove(c):', d)	# remove(c): deque(['a', 'b', 'd', 'e', 'f', 'g'])
```

`deques` 是一种序列容器，它们支持一些类似于 `list` 的操作，例如求长度，从中删除某个元素等。

### 填充

可以从任一端填充双端队列，在 Python 实现中称为“左”和“右”。

```python
import collections

# Add to the right
d1 = collections.deque()
d1.extend('abcdefg')
print('extend    :', d1)	# extend    : deque(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
d1.append('h')
print('append    :', d1)  # append    : deque(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])

# Add to the left
d2 = collections.deque()
d2.extendleft(range(6))
print('extendleft:', d2)	# extendleft: deque([5, 4, 3, 2, 1, 0])
d2.appendleft(6)
print('appendleft:', d2)	# appendleft: deque([6, 5, 4, 3, 2, 1, 0])
```

`extendleft()` 函数迭代其输入，相当于对每一项执行 `appendleft()`。最终结果是以`deque`相反的顺序插入序列。

### 消费

类似地，`deque`取决于所应用的算法，可以从两端或任一端消耗元素。

```python
import collections

print('From the right:')
d = collections.deque('abcdefg')
while True:
    try:
        print(d.pop(), end='')
    except IndexError:
        break
print()

print('\nFrom the left:')
d = collections.deque(range(6))
while True:
    try:
        print(d.popleft(), end='')
    except IndexError:
        break
print()

# output
# From the right:
# gfedcba

# From the left:
# 012345
```

用`pop()`从“右”端移除项目，用 `popleft()`从“左”端获取项目。

由于`deques`是线程安全的，所以可以用不同线程同时从双端取数据。

```python
import collections
import threading
import time

candle = collections.deque(range(5))


def burn(direction, nextSource):
    while True:
        try:
            next = nextSource()
        except IndexError:
            break
        else:
            print('{:>8}: {}'.format(direction, next))
            time.sleep(0.1)
    print('{:>8} done'.format(direction))
    return


left = threading.Thread(target=burn, args=('Left', candle.popleft))
right = threading.Thread(target=burn, args=('Right', candle.pop))

left.start()
right.start()

left.join()
right.join()

# output
# Left: 0
# Right: 4
# Right: 3
#  Left: 1
# Right: 2
#  Left done
# Right done
```

删除项目直到`deque` 为空。

### 旋转

另一个有用的方面是 `deque` 能够在任一方向上旋转，可以通过这个方法跳过一些项目。

```python
import collections

d = collections.deque(range(10))
print('Normal        :', d)	# Normal        : deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

d = collections.deque(range(10))
d.rotate(2)
print('Right rotation:', d)	# Right rotation: deque([8, 9, 0, 1, 2, 3, 4, 5, 6, 7])

d = collections.deque(range(10))
d.rotate(-2)
print('Left rotation :', d)	# Left rotation : deque([2, 3, 4, 5, 6, 7, 8, 9, 0, 1])
```

`deque`向右旋转（使用正向旋转）从右端获取项目并将它们移动到左端。向左旋转（带负值）从左端获取项目并将它们移动到右端。

### 约束队列大小

一个`deque`实例可以设置最大长度。当队列达到指定长度时，将在添加新项目时丢弃现有项目。

```python
import collections
import random

# Set the random seed so we see the same output each time
# the script is run.
random.seed(1)

d1 = collections.deque(maxlen=3)
d2 = collections.deque(maxlen=3)

for i in range(5):
    n = random.randint(0, 100)
    print('n =', n)
    d1.append(n)
    d2.appendleft(n)
    print('D1:', d1)
    print('D2:', d2)
    
# output
# n = 17
# D1: deque([17], maxlen=3)
# D2: deque([17], maxlen=3)
# n = 72
# D1: deque([17, 72], maxlen=3)
# D2: deque([72, 17], maxlen=3)
# n = 97
# D1: deque([17, 72, 97], maxlen=3)
# D2: deque([97, 72, 17], maxlen=3)
# n = 8
# D1: deque([72, 97, 8], maxlen=3)
# D2: deque([8, 97, 72], maxlen=3)
# n = 32
# D1: deque([97, 8, 32], maxlen=3)
# D2: deque([32, 8, 97], maxlen=3)
```

无论项目添加到哪一端，都会保持双端队列长度。

## namedtuple

标准`tuple`使用数字索引来访问其成员。

```python
bob = ('Bob', 30, 'male')
print('Representation:', bob)

jane = ('Jane', 29, 'female')
print('\nField by index:', jane[0])

print('\nFields by index:')
for p in [bob, jane]:
    print('{} is a {} year old {}'.format(*p))
    
# output
# Representation: ('Bob', 30, 'male')
# 
# Field by index: Jane
# 
# Fields by index:
# Bob is a 30 year old male
# Jane is a 29 year old female
```

但通过索引来访问的方式可能会引起错误，特别是当 `tuple` 有很多字段的时候。使用 `namedtuple` 的好处就是为每个成员分配了名称和索引。

### 定义

`namedtuple` 和常用元组的效率是一样的，由 `namedtuple()`工厂函数创建。参数是新类的名称和包含元素名称的字符串。

```python
import collections

Person = collections.namedtuple('Person', 'name age')

bob = Person(name='Bob', age=30)
print('\nRepresentation:', bob)

jane = Person(name='Jane', age=29)
print('\nField by name:', jane.name)

print('\nFields by index:')
for p in [bob, jane]:
    print('{} is {} years old'.format(*p))
    
# output
# Representation: Person(name='Bob', age=30)
# 
# Field by name: Jane
# 
# Fields by index:
# Bob is 30 years old
# Jane is 29 years old
```

如示例所示，`namedtuple` 可以使用点式表示法（`obj.attr`）按名称来访问字段。

就像普通的`tuple`，`namedtuple` 也是不可改变的。

```python
import collections

Person = collections.namedtuple('Person', 'name age')

pat = Person(name='Pat', age=12)
print('\nRepresentation:', pat)

pat.age = 21

# output
# Representation: Person(name='Pat', age=12)
# Traceback (most recent call last):
#   File "collections_namedtuple_immutable.py", line 17, in
# <module>
#     pat.age = 21
# AttributeError: can't set attribute
```

尝试通过其命名属性更改值会导致 `AttributeError`。

### 无效的字段名称

如果字段名称重复或与 Python 关键字冲突，则字段名称无效。

```python
import collections

try:
    collections.namedtuple('Person', 'name class age')
except ValueError as err:
    print(err)

try:
    collections.namedtuple('Person', 'name age age')
except ValueError as err:
    print(err)
    
# output
# Type names and field names cannot be a keyword: 'class'
# Encountered duplicate field name: 'age'
```

在解析字段名称时，无效值会导致 `ValueError`异常。

将`rename`选项设置为`True`来重命名无效字段。

```python
import collections

with_class = collections.namedtuple(
    'Person', 'name class age',
    rename=True)
print(with_class._fields)	# ('name', '_1', 'age')

two_ages = collections.namedtuple(
    'Person', 'name age age',
    rename=True)
print(two_ages._fields)	# ('name', 'age', '_2')
```

重命名字段的新名称取决于它们在元组中的索引，因此，名称字段`class`将变为`_1`，重复字段 `age`将更改为`_2`。

### 特殊属性

`namedtuple`提供了几个有用的属性和方法来处理子类和实例。所有这些内置属性都有一个下划线（`_`）为前缀的名称，在大多数 Python 程序中，按照惯例表示私有属性。对于 `namedtuple`，前缀是为了防止名称和用户提供的属性名称冲突。

传递给`namedtuple`定义新类的字段名称保存在`_fields`属性中。

```python
import collections

Person = collections.namedtuple('Person', 'name age')

bob = Person(name='Bob', age=30)
print('Representation:', bob)	# Representation: Person(name='Bob', age=30)
print('Fields:', bob._fields)	# Fields: ('name', 'age')
```

虽然参数是单个空格分隔的字符串，但存储的值是各个名称的序列。

`namedtuple`实例可以使用 `_asdict()` 转换为`OrderedDict` 实例。

```python
import collections

Person = collections.namedtuple('Person', 'name age')

bob = Person(name='Bob', age=30)
print('Representation:', bob)
print('As Dictionary:', bob._asdict())

# output
# Representation: Person(name='Bob', age=30)
# As Dictionary: OrderedDict([('name', 'Bob'), ('age', 30)])
```

`OrderedDict` 的键与 `namedtuple` 字段的顺序相同。

`_replace()`方法构建一个新实例，替换进程中某些字段的值。

```python
import collections

Person = collections.namedtuple('Person', 'name age')

bob = Person(name='Bob', age=30)
print('\nBefore:', bob)	# Before: Person(name='Bob', age=30)
bob2 = bob._replace(name='Robert')
print('After:', bob2)	# After: Person(name='Robert', age=30)
print('Same?:', bob is bob2)	# Same?: False
```

虽然名称暗示它在修改现有对象，但由于`namedtuple`实例是不可变的，实际上，该方法返回了一个新对象。

## defaultdict

标准字典包括 `setdefault()` 方法，用于检索值并在值不存在时建立默认值。相反，`defaultdict` 让初始化容器时，调用者可以预先指定默认值。

```python
import collections


def default_factory():
    return 'default value'


d = collections.defaultdict(default_factory, foo='bar')
print('d:', d)	
print('foo =>', d['foo'])
print('bar =>', d['bar'])

# output
# d: defaultdict(<function default_factory at 0x101341950>, {'foo': 'bar'})
# foo => bar
# bar => default value
```

所有键具有相同的默认值。如果默认值是聚合或累加类型的话（比如：`list`、`set`、`int`），尤其有用。

```python
In[88]: from collections import defaultdict
In[89]: d = defaultdict(int)
In[90]: d['a']
Out[90]: 0
In[91]: d = defaultdict(dict)
In[92]: d['a']
Out[92]: {}
```

如果初始化时没有加入默认工厂，则会抛出 `KeyError` 错误：

```python
In[93]: d = defaultdict()
In[94]: d['a']
Traceback (most recent call last):
    d['a']
KeyError: 'a'
```

## OrderedDict

`OrderedDict`是一个字典子类，它会记住添加内容的顺序。

```python
import collections

print('Regular dictionary:')
d = {}
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)

print('\nOrderedDict:')
d = collections.OrderedDict()
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print(k, v)
    
# output
# Regular dictionary:
# c C
# b B
# a A
# 
# OrderedDict:
# a A
# b B
# c C
```

###  相等

`dict`在测试相等性时，只是查看其内容。但 `OrderedDict` 还考虑了添加项目的顺序。

```python
import collections

print('dict       :', end=' ')
d1 = {}
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = {}
d2['c'] = 'C'
d2['b'] = 'B'
d2['a'] = 'A'

print(d1 == d2)

print('OrderedDict:', end=' ')

d1 = collections.OrderedDict()
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'

d2 = collections.OrderedDict()
d2['c'] = 'C'
d2['b'] = 'B'
d2['a'] = 'A'

print(d1 == d2)

# output
# dict       : True
# OrderedDict: False
```

在这种情况下，由于两个有序词典是以不同顺序的值创建的，因此它们被认为是不同的。

### 重新排序

可以通过使用 `move_to_end()` 将键移动到序列的开头或结尾。

```python
import collections

d = collections.OrderedDict(
    [('a', 'A'), ('b', 'B'), ('c', 'C')]
)

print('Before:')
for k, v in d.items():
    print(k, v)

d.move_to_end('b')

print('\nmove_to_end():')
for k, v in d.items():
    print(k, v)

d.move_to_end('b', last=False)

print('\nmove_to_end(last=False):')
for k, v in d.items():
    print(k, v)
    
# output
# Before:
# a A
# b B
# c C
# 
# move_to_end():
# a A
# c C
# b B
# 
# move_to_end(last=False):
# b B
# a A
# c C
```

`last` 参数指示`move_to_end()`是否将键移动到序列中的最后一项（`True`）或第一项（`False`）。

相关文档：

https://pymotw.com/3/collections/index.html