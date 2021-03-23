# Python 高手都这样使用字典，这些高效方法你知道吗？｜pythonic 小技巧

字典（dict）对象是 Python 最常用的数据结构之一。

社区曾有人开玩笑地说：「Python 企图用字典装载整个世界。」

可见其有多重要，不用多说，我平时用的也很多，索性总结一下，把一些常用的方法写下来，分享给大家。

### 一、字典创建

```python
# 1、创建空字典
a = {}
b = dict()

# 2、有初始值，从输入的便利程度来说，我更喜欢第二种
a = {'a': 1, 'b': 2, 'c': 3}
b = dict(a=1, b=2, c=3)

# 3、key 来自一个列表，而 value 相同, 使用 fromkeys，那是相当的优雅
keys = ['a', 'b', 'c']
value = 100
d = dict.fromkeys(keys, value)

# 4、key 来自一个列表，而 value 也是一个列表，使用 zip
keys = ['a', 'b', 'c']
values = [1, 2, 3]
d = dict(zip(keys, values))
```

### 二、字典合并

```python
m = {'a': 1}
n = {'b': 2, 'c': 3}

# 合并，两种方式
# 1、使用 update
m.update(n)
# 2、使用 **
{**m, **n}
```

### 三、判断 key 是否存在

在 Python2 中判断某个 key 是否存在，可以使用 `has_key`，但这个方法在 Python3 中已经被移除了。

另一种方法是使用 `in` 关键字，不仅兼容 Python2 和 Python3，速度还更快，强烈推荐。

```python
d = {'a': 1, 'b': 2}
if 'a' in d:
    print('hello')    
```

### 四、获取字典中的值

```python
d = {'a': 1, 'b': 2}

# 1、直接用 key 取值，但这种方式不好，如果 key 不存在会报错，推荐使用 get
a = d['a']

# 2、使用 get，如果 key 不存在还可以赋默认值
a = d.get('a')
c = d.get('c', 3)
```

### 五、字典遍历

```python
d = {'a': 1, 'b': 2, 'c': 3}

# 遍历 key
for key in d.keys():
    pass

# 遍历 value
for value in d.values():
    pass

# 遍历 key 和 value
for key, value in d.items():
    pass
```

### 六、字典按 key 或 value 排序

```python
d = {'a': 1, 'b': 2, 'e': 9, 'c': 5, 'd': 7}

# 按 key 排序
sorted(d.items(), key=lambda t: t[0])
# 按 key 倒序
sorted(d.items(), key=lambda t: t[0], reverse=True)

# 按 value 排序
sorted(d.items(), key=lambda t: t[1])
```

还有一个需求是我在开发过程经常碰到的，就是有一个列表，列表的元素是字典，然后按字典的 value 对列表进行排序。

```python
l = [{'name': 'a', 'count': 4}, {'name': 'b', 'count': 1}, {'name': 'd', 'count': 2}, {'name': 'c', 'count': 6}]
sorted(l, key=lambda e: e.__getitem__('count'))
# 倒序
sorted(l, key=lambda e: e.__getitem__('count'), reverse=True)
```

### 七、字典推导式

列表推导式和字典推导式是我相当喜欢的功能，简洁高效。`map` 和 `filter` 我都已经快不会用了。

```python
l = [1, 2, 3]
{n: n * n for n in l}
{1: 1, 2: 4, 3: 9}
```

以上。

希望对你能有帮助，欢迎关注公众号 **AlwaysBeta**，更多技术干货等你来。

**题图：** 由 fdsfe67854 在 Pixabay 上发布。

**往期精彩：**

