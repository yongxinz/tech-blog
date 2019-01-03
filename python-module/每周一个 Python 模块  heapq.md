# 每周一个 Python 模块 | heapq

heapq 实现了适用于 Python 列表的最小堆排序算法。

堆是一个树状的数据结构，其中的子节点与父节点属于排序关系。可以使用列表或数组来表示二进制堆，使得元素 N 的子元素位于 2 * *N* + 1 和 2 * *N* + 2 的位置（对于从零开始的索引）。这种布局使得可以在适当的位置重新排列堆，因此在添加或删除数据时无需重新分配内存。

max-heap 确保父级大于或等于其子级。min-heap 要求父项小于或等于其子级。Python 的`heapq`模块实现了一个 min-heap。

## 示例数据

本节中的示例使用数据`heapq_heapdata.py`。

```python
# heapq_heapdata.py 
# This data was generated with the random module.

data = [19, 9, 4, 10, 11]
```

堆输出使用打印`heapq_showtree.py`。

```python
# heapq_showtree.py 
import math
from io import StringIO


def show_tree(tree, total_width=36, fill=' '):
    """Pretty-print a tree."""
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i + 1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write('\n')
        columns = 2 ** row
        col_width = int(math.floor(total_width / columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print(output.getvalue())
    print('-' * total_width)
    print()
```

## 创建堆

创建堆有两种基本方法：`heappush()` 和 `heapify()`。

```python
import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data

heap = []
print('random :', data)
print()

for n in data:
    print('add {:>3}:'.format(n))
    heapq.heappush(heap, n)
    show_tree(heap)
    
# output
# random : [19, 9, 4, 10, 11]
# 
# add  19:
# 
#                  19
# ------------------------------------
# 
# add   9:
# 
#                  9
#         19
# ------------------------------------
# 
# add   4:
# 
#                  4
#         19                9
# ------------------------------------
# 
# add  10:
# 
#                  4
#         10                9
#     19
# ------------------------------------
# 
# add  11:
# 
#                  4
#         10                9
#     19       11
# ------------------------------------
```

当使用`heappush()`时，当新元素添加时，堆得顺序被保持了。

如果数据已经在内存中，则使用 `heapify()` 来更有效地重新排列列表中的元素。

```python
import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data

print('random    :', data)
heapq.heapify(data)
print('heapified :')
show_tree(data)

# output
# random    : [19, 9, 4, 10, 11]
# heapified :
# 
#                  4
#         9                 19
#     10       11
# ------------------------------------
```

## 访问堆的内容

正确创建堆后，使用`heappop()`删除具有最小值的元素。

```python
import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data

print('random    :', data)
heapq.heapify(data)
print('heapified :')
show_tree(data)
print()

for i in range(2):
    smallest = heapq.heappop(data)
    print('pop    {:>3}:'.format(smallest))
    show_tree(data)
    
# output
# random    : [19, 9, 4, 10, 11]
# heapified :
# 
#                  4
#         9                 19
#     10       11
# ------------------------------------
# 
# 
# pop      4:
# 
#                  9
#         10                19
#     11
# ------------------------------------
# 
# pop      9:
# 
#                  10
#         11                19
# ------------------------------------
```

在这个例子中，使用 `heapify()` 和 `heappop()` 进行排序。

要删除现有元素，并在一次操作中用新值替换它们，使用`heapreplace()`。

```python
import heapq
from heapq_showtree import show_tree
from heapq_heapdata import data

heapq.heapify(data)
print('start:')
show_tree(data)

for n in [0, 13]:
    smallest = heapq.heapreplace(data, n)
    print('replace {:>2} with {:>2}:'.format(smallest, n))
    show_tree(data)
    
# output
# start:
# 
#                  4
#         9                 19
#     10       11
# ------------------------------------
# 
# replace  4 with  0:
# 
#                  0
#         9                 19
#     10       11
# ------------------------------------
# 
# replace  0 with 13:
# 
#                  9
#         10                19
#     13       11
# ------------------------------------
```

替换元素可以维护固定大小的堆，例如按优先级排序的 jobs 队列。

## 堆的数据极值

`heapq` 还包括两个函数来检查 iterable 并找到它包含的最大或最小值的范围。

```python
import heapq
from heapq_heapdata import data

print('all       :', data)
print('3 largest :', heapq.nlargest(3, data))
print('from sort :', list(reversed(sorted(data)[-3:])))
print('3 smallest:', heapq.nsmallest(3, data))
print('from sort :', sorted(data)[:3])

# output
# all       : [19, 9, 4, 10, 11]
# 3 largest : [19, 11, 10]
# from sort : [19, 11, 10]
# 3 smallest: [4, 9, 10]
# from sort : [4, 9, 10]
```

使用`nlargest()`和`nsmallest()`仅对 `n > 1` 的相对较小的值有效，但在少数情况下仍然可以派上用场。

## 有效地合并排序序列

将几个排序的序列组合成一个新序列对于小数据集来说很容易。

```python
list(sorted(itertools.chain(*data)))
```

对于较大的数据集，将会占用大量内存。不是对整个组合序列进行排序，而是使用 `merge()` 一次生成一个新序列。

```python
import heapq
import random


random.seed(2016)

data = []
for i in range(4):
    new_data = list(random.sample(range(1, 101), 5))
    new_data.sort()
    data.append(new_data)

for i, d in enumerate(data):
    print('{}: {}'.format(i, d))

print('\nMerged:')
for i in heapq.merge(*data):
    print(i, end=' ')
print()

# output
# 0: [33, 58, 71, 88, 95]
# 1: [10, 11, 17, 38, 91]
# 2: [13, 18, 39, 61, 63]
# 3: [20, 27, 31, 42, 45]
# 
# Merged:
# 10 11 13 17 18 20 27 31 33 38 39 42 45 58 61 63 71 88 91 95
```

因为`merge()`使用堆的实现，它根据被合并的序列元素个数消耗内存，而不是所有序列中的元素个数。

相关文档：

https://pymotw.com/3/heapq/index.html