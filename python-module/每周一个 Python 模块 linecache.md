# 每周一个 Python 模块 | linecache

从文件或导入的 Python 模块中检索文本行，保存结果缓存，以便更高效地从同一文件中读取多行。

linecache 在处理 Python 源文件时，该模块用于 Python 标准库的其他部分。缓存实现在内存中将文件内容分解为单独的行。API 通过索引请求的行到一个列表中，节省了重复读取文件和解析行以找到所需行的时间。这在查找同一文件中的多行时尤其有用，例如在为错误报告生成回溯时。

## 测试数据

由 Lorem Ipsum 生成器生成的该文本用作样本输入。

```python
# linecache_data.py 

import os
import tempfile

lorem = '''Lorem ipsum dolor sit amet, consectetuer
adipiscing elit.  Vivamus eget elit. In posuere mi non
risus. Mauris id quam posuere lectus sollicitudin
varius. Praesent at mi. Nunc eu velit. Sed augue massa,
fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur
eros pede, egestas at, ultricies ac, apellentesque eu,
tellus.

Sed sed odio sed mi luctus mollis. Integer et nulla ac augue
convallis accumsan. Ut felis. Donec lectus sapien, elementum
nec, condimentum ac, interdum non, tellus. Aenean viverra,
mauris vehicula semper porttitor, ipsum odio consectetuer
lorem, ac imperdiet eros odio a sapien. Nulla mauris tellus,
aliquam non, egestas a, nonummy et, erat. Vivamus sagittis
porttitor eros.'''


def make_tempfile():
    fd, temp_file_name = tempfile.mkstemp()
    os.close(fd)
    with open(temp_file_name, 'wt') as f:
        f.write(lorem)
    return temp_file_name


def cleanup(filename):
    os.unlink(filename)
```

## 读取特定行

linecache 模块读取的文件行数以 1 开头，通常数组索引都是从 0 开始。

```python
import linecache
from linecache_data import *

filename = make_tempfile()

# Pick out the same line from source and cache.
# (Notice that linecache counts from 1)
print('SOURCE:')
print('{!r}'.format(lorem.split('\n')[4]))
print()
print('CACHE:')
print('{!r}'.format(linecache.getline(filename, 5)))

cleanup(filename)

# output
# SOURCE:
# 'fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur'
#
# CACHE:
# 'fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur\n'
```

返回的每一行都包含一个尾随换行符。

## 处理空行
返回值始终包含行尾的换行符，因此如果行为空，则返回值只是换行符。

```python
import linecache
from linecache_data import *

filename = make_tempfile()

# Blank lines include the newline
print('BLANK : {!r}'.format(linecache.getline(filename, 8)))    # BLANK : '\n'

cleanup(filename)
```

输入文件的第八行不包含文本。

## 错误处理

如果请求的行号超出文件中有效行的范围，则 `getline()` 返回空字符串。

```python
import linecache
from linecache_data import *

filename = make_tempfile()

# The cache always returns a string, and uses
# an empty string to indicate a line which does
# not exist.
not_there = linecache.getline(filename, 500)
print('NOT THERE: {!r} includes {} characters'.format(not_there, len(not_there)))    # NOT THERE: '' includes 0 characters

cleanup(filename)
```

输入文件只有 15 行，因此请求行 500 就像尝试读取文件末尾一样。

从不存在的文件读取以相同的方式处理。

```python
import linecache

# Errors are even hidden if linecache cannot find the file
no_such_file = linecache.getline(
    'this_file_does_not_exist.txt', 1,
)
print('NO FILE: {!r}'.format(no_such_file)) # NO FILE: ''
```

当调用者尝试读取数据时，模块永远不会引发异常。

## 阅读 Python 源文件

由于 linecache 在生成回溯时使用得非常多，因此其关键特性之一是能够通过指定模块的基本名称在导入路径中查找 Python 源模块。

```python
import linecache
import os

# Look for the linecache module, using
# the built in sys.path search.
module_line = linecache.getline('linecache.py', 3)
print('MODULE:')
print(repr(module_line))

# Look at the linecache module source directly.
file_src = linecache.__file__
if file_src.endswith('.pyc'):
    file_src = file_src[:-1]
print('\nFILE:')
with open(file_src, 'r') as f:
    file_line = f.readlines()[2]
print(repr(file_line))

# output
# MODULE:
# 'This is intended to read lines from modules imported -- hence if a filename\n'
# 
# FILE:
# 'This is intended to read lines from modules imported -- hence if a filename\n'
```

如果命名模块在当前目录中找不到具有该名称的文件，则 linecache 会搜索 `sys.path`。这个例子是寻找的  `linecache.py`，由于当前目录中没有，因此会找到标准库中的文件。


原文链接：

https://pymotw.com/3/linecache/index.html