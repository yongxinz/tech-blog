# 每周一个 Python 模块 | copy

`copy` 模块包括两个功能，`copy()` 和 `deepcopy()`，用于复制现有对象。

## 浅拷贝

`copy()` 创建的浅表副本是一个新容器，是对原始对象内容的引用。

```python
import copy
import functools


@functools.total_ordering
class MyClass:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name


a = MyClass('a')
my_list = [a]
dup = copy.copy(my_list)

print('             my_list:', my_list)
print('                 dup:', dup)
print('      dup is my_list:', (dup is my_list))
print('      dup == my_list:', (dup == my_list))
print('dup[0] is my_list[0]:', (dup[0] is my_list[0]))
print('dup[0] == my_list[0]:', (dup[0] == my_list[0]))

# output
#              my_list: [<__main__.MyClass object at 0x101f9c160>]
#                  dup: [<__main__.MyClass object at 0x101f9c160>]
#       dup is my_list: False
#       dup == my_list: True
# dup[0] is my_list[0]: True
# dup[0] == my_list[0]: True
```

对于浅拷贝，`MyClass` 实例并不复制，因此`dup` 和 `my_list` 引用的是同一个对象。

## 深拷贝

将调用替换为 `deepcopy()` 会使输出明显不同。

```python
import copy
import functools


@functools.total_ordering
class MyClass:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name


a = MyClass('a')
my_list = [a]
dup = copy.deepcopy(my_list)

print('             my_list:', my_list)
print('                 dup:', dup)
print('      dup is my_list:', (dup is my_list))
print('      dup == my_list:', (dup == my_list))
print('dup[0] is my_list[0]:', (dup[0] is my_list[0]))
print('dup[0] == my_list[0]:', (dup[0] == my_list[0]))

# output
#              my_list: [<__main__.MyClass object at 0x101e9c160>]
#                  dup: [<__main__.MyClass object at 0x1044e1f98>]
#       dup is my_list: False
#       dup == my_list: True
# dup[0] is my_list[0]: False
# dup[0] == my_list[0]: True
```

列表的第一个元素不再是相同的对象引用，但是当比较两个对象时，它们仍然是相等的。

## 自定义复制行为

可以使用  `__copy__()`和`__deepcopy__()` 方法来自定义复制行为。

- `__copy__()` 不需要参数，返回该对象的浅拷贝副本。
- `__deepcopy__()`使用 memo 字典调用，并返回该对象的深拷贝对象。任何需要深度复制的成员属性，都应与 memo 字典一起传递给 `copy.deepcopy()`。

以下示例说明了如何调用方法。

```python
import copy
import functools


@functools.total_ordering
class MyClass:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name

    def __copy__(self):
        print('__copy__()')
        return MyClass(self.name)

    def __deepcopy__(self, memo):
        print('__deepcopy__({})'.format(memo))
        return MyClass(copy.deepcopy(self.name, memo))


a = MyClass('a')

sc = copy.copy(a)
dc = copy.deepcopy(a)

# output
# __copy__()
# __deepcopy__({})
```

memo 字典用于跟踪已经复制的值，以避免无限递归。

## 深度复制中的递归

为避免重复递归数据结构的问题，`deepcopy()` 使用字典来跟踪已复制的对象。这个字典被传递给`__deepcopy__()` 方法，因此可以在这里检查重复递归问题。

下一个示例显示了互连数据结构（如有向图）如何通过实现`__deepcopy__()`方法来防止递归。

```python
import copy


class Graph:

    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    def add_connection(self, other):
        self.connections.append(other)

    def __repr__(self):
        return 'Graph(name={}, id={})'.format(
            self.name, id(self))

    def __deepcopy__(self, memo):
        print('\nCalling __deepcopy__ for {!r}'.format(self))
        if self in memo:
            existing = memo.get(self)
            print('  Already copied to {!r}'.format(existing))
            return existing
        print('  Memo dictionary:')
        if memo:
            for k, v in memo.items():
                print('    {}: {}'.format(k, v))
        else:
            print('    (empty)')
        dup = Graph(copy.deepcopy(self.name, memo), [])
        print('  Copying to new object {}'.format(dup))
        memo[self] = dup
        for c in self.connections:
            dup.add_connection(copy.deepcopy(c, memo))
        return dup


root = Graph('root', [])
a = Graph('a', [root])
b = Graph('b', [a, root])
root.add_connection(a)
root.add_connection(b)

dup = copy.deepcopy(root)

# output
# Calling __deepcopy__ for Graph(name=root, id=4326183824)
#   Memo dictionary:
#     (empty)
#   Copying to new object Graph(name=root, id=4367233208)
# 
# Calling __deepcopy__ for Graph(name=a, id=4326186344)
#   Memo dictionary:
#     Graph(name=root, id=4326183824): Graph(name=root, id=4367233208)
#   Copying to new object Graph(name=a, id=4367234720)
# 
# Calling __deepcopy__ for Graph(name=root, id=4326183824)
#   Already copied to Graph(name=root, id=4367233208)
# 
# Calling __deepcopy__ for Graph(name=b, id=4326183880)
#   Memo dictionary:
#     Graph(name=root, id=4326183824): Graph(name=root, id=4367233208)
#     Graph(name=a, id=4326186344): Graph(name=a, id=4367234720)
#     4326183824: Graph(name=root, id=4367233208)
#     4367217936: [Graph(name=root, id=4326183824), Graph(name=a, id=4326186344)]
#     4326186344: Graph(name=a, id=4367234720)
#   Copying to new object Graph(name=b, id=4367235000)
```

`Graph` 类包括几个基本的有向图的方法。可以使用名称和与其连接的现有节点列表初始化实例。`add_connection()` 方法用于设置双向连接。它也被深拷贝操作符使用。

`__deepcopy__()`方法打印消息以显示其调用方式，并根据需要管理备忘录字典内容。它不是复制整个连接列表，而是创建一个新列表，并将各个连接的副本添加进去。这确保了备忘录字典在每个新节点被复制时更新，并且它避免了递归问题或节点的额外副本。和以前一样，该方法在完成后返回复制的对象。

![digraph copy_example {“root”;  “a” - >“root”;  “b” - >“root”;  “b” - >“a”;  “root” - >“a”;  “root” - >“b”;  }](https://pymotw.com/3/_images/graphviz-e1d2b289f2182fb32e7d25ab5da793d9fe0c8bec.png)

具有循环的对象图的深层复制

图中显示的图形包括几个周期，但使用备注字典处理递归可防止遍历导致堆栈溢出错误。

第二次根遇到一个节点，而这个节点被复制，`__deepcopy__()`检测该递归和重用来自备忘录字典现有值而不是创建新的对象。

相关文档：

https://pymotw.com/3/copy/index.html