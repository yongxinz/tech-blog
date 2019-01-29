# 每周一个 Python 模块 | os.path

本文基于 Python3 编写测试。

`os.path` 模块是跨平台的，即使不打算在平台之间移植自己的程序也应该用 `os.path`，好处多多。

## 解析路径

第一组 `os.path` 函数可用于将表示文件名的字符串解析为其组成部分。重要的是要意识到这些功能不依赖于实际存在的路径。

路径解析取决于以下定义的一些 `os` 变量：

- `os.sep`- 路径部分之间的分隔符（例如，“ `/`”或“ `\`”）。
- `os.extsep`- 文件名和文件“扩展名”之间的分隔符（例如，“ `.`”）。
- `os.pardir`- 路径组件，意味着将目录树向上遍历一级（例如，“ `..`”）。
- `os.curdir`- 引用当前目录的路径组件（例如，“ `.`”）。

`split()` 函数将路径分成两个独立的部分，并返回一个`tuple`结果。第二个元素是路径的最后一个元素，第一个元素是它之前的所有元素。

```python
import os.path

PATHS = [
    '/one/two/three',
    '/one/two/three/',
    '/',
    '.',
    '',
]

for path in PATHS:
    print('{!r:>17} : {}'.format(path, os.path.split(path)))
    
# output
# '/one/two/three' : ('/one/two', 'three')
# '/one/two/three/' : ('/one/two/three', '')
#               '/' : ('/', '')
#               '.' : ('', '.')
#                '' : ('', '')
```

当输入参数以 `os.sep` 结束时，路径的最后一个元素是一个空字符串。

`basename()`函数返回一个等于 `split()` 返回值的第二部分的值。

```python
import os.path

PATHS = [
    '/one/two/three',
    '/one/two/three/',
    '/',
    '.',
    '',
]

for path in PATHS:
    print('{!r:>17} : {!r}'.format(path, os.path.basename(path)))
    
# output
# '/one/two/three' : 'three'
# '/one/two/three/' : ''
#               '/' : ''
#               '.' : '.'
#                '' : ''
```

完整路径被剥离到最后一个元素，无论是指文件还是目录。

`dirname()`函数返回拆分路径的第一部分：

```python
import os.path

PATHS = [
    '/one/two/three',
    '/one/two/three/',
    '/',
    '.',
    '',
]

for path in PATHS:
    print('{!r:>17} : {!r}'.format(path, os.path.dirname(path)))
    
# output
# '/one/two/three' : '/one/two'
# '/one/two/three/' : '/one/two/three'
#               '/' : '/'
#               '.' : ''
#                '' : ''
```

结合`basename()` 和 `dirname()` 的结果可以返回原始路径。

`splitext()`类似于`split()`，但在扩展分隔符上划分路径，而不是目录分隔符。

```python
import os.path

PATHS = [
    'filename.txt',
    'filename',
    '/path/to/filename.txt',
    '/',
    '',
    'my-archive.tar.gz',
    'no-extension.',
]

for path in PATHS:
    print('{!r:>21} : {!r}'.format(path, os.path.splitext(path)))
    
# output
#        'filename.txt' : ('filename', '.txt')
#            'filename' : ('filename', '')
# '/path/to/filename.txt' : ('/path/to/filename', '.txt')
#                   '/' : ('/', '')
#                    '' : ('', '')
#   'my-archive.tar.gz' : ('my-archive.tar', '.gz')
#       'no-extension.' : ('no-extension', '.')
```

`os.extsep`在查找扩展名时仅匹配最后一次出现的分隔符，因此如果文件名具有多个扩展名，则会按照最后一个扩展名进行拆分。

`commonprefix()`将路径列表作为参数，并返回表示所有路径中存在的公共前缀的单个字符串。该值还可以表示实际上不存在的路径，并且路径分隔符不包括在考虑中。

```python
import os.path

paths = ['/one/two/three/four',
         '/one/two/threefold',
         '/one/two/three/',
         ]
for path in paths:
    print('PATH:', path)

print()
print('PREFIX:', os.path.commonprefix(paths))

# output
# PATH: /one/two/three/four
# PATH: /one/two/threefold
# PATH: /one/two/three/
# 
# PREFIX: /one/two/three
```

在此示例中，公共前缀字符串是`/one/two/three`，即使一个路径不包含名为的目录`three`。

`commonpath()` 考虑路径分隔符，并返回不包含部分路径值的前缀。

```python
import os.path

paths = ['/one/two/three/four',
         '/one/two/threefold',
         '/one/two/three/',
         ]
for path in paths:
    print('PATH:', path)

print()
print('PREFIX:', os.path.commonpath(paths))

# output
# PATH: /one/two/three/four
# PATH: /one/two/threefold
# PATH: /one/two/three/
# 
# PREFIX: /one/two
```

## 构建路径

除了将现有路径分开之外，经常需要从其他字符串构建路径。要将多个路径组合为单个值，可以使用`join()`：

```python
import os.path

PATHS = [
    ('one', 'two', 'three'),
    ('/', 'one', 'two', 'three'),
    ('/one', '/two', '/three'),
]

for parts in PATHS:
    print('{} : {!r}'.format(parts, os.path.join(*parts)))
    
# output
# ('one', 'two', 'three') : 'one/two/three'
# ('/', 'one', 'two', 'three') : '/one/two/three'
# ('/one', '/two', '/three') : '/three'
```

如果有任何一个参数是以 `os.sep` 开头的，则先前所有的参数都会被丢弃，并将该值作为返回值的开头。

也可以使用包含可以自动扩展的“可变”组件的路径。例如，`expanduser()` 将 `~` 字符转换为用户主目录的名称。

```python
import os.path

for user in ['', 'dhellmann', 'nosuchuser']:
    lookup = '~' + user
    print('{!r:>15} : {!r}'.format(lookup, os.path.expanduser(lookup)))
    
# output
#             '~' : '/Users/dhellmann'
#    '~dhellmann' : '/Users/dhellmann'
#   '~nosuchuser' : '~nosuchuser'
```

如果找不到用户的主目录，则返回字符串不变，如`~nosuchuser`。

`expandvars()` 更通用，扩展路径中存在的任何 shell 环境变量。

```python
import os.path
import os

os.environ['MYVAR'] = 'VALUE'

print(os.path.expandvars('/path/to/$MYVAR'))	# /path/to/VALUE
```

并不会验证文件或路径是否存在。

## 规范化路径

使用`join()` 组合的路径可能会有额外的分隔符或相对路径。用 `normpath()`来清理它们：

```python
import os.path

PATHS = [
    'one//two//three',
    'one/./two/./three',
    'one/../alt/two/three',
]

for path in PATHS:
    print('{!r:>22} : {!r}'.format(path, os.path.normpath(path)))
    
# output
#      'one//two//three' : 'one/two/three'
#    'one/./two/./three' : 'one/two/three'
# 'one/../alt/two/three' : 'alt/two/three'
```

要将相对路径转换为绝对文件名，请使用 `abspath()`。

```python
import os
import os.path

os.chdir('/usr')

PATHS = [
    '.',
    '..',
    './one/two/three',
    '../one/two/three',
]

for path in PATHS:
    print('{!r:>21} : {!r}'.format(path, os.path.abspath(path)))
    
# output
#                   '.' : '/usr'
#                  '..' : '/'
#     './one/two/three' : '/usr/one/two/three'
#    '../one/two/three' : '/one/two/three'
```

## 文件时间

除了使用路径之外，`os.path`还包括用于检索文件属性的函数，类似于 `os.stat()`：

```python
import os.path
import time

print('File         :', __file__)
print('Access time  :', time.ctime(os.path.getatime(__file__)))
print('Modified time:', time.ctime(os.path.getmtime(__file__)))
print('Change time  :', time.ctime(os.path.getctime(__file__)))
print('Size         :', os.path.getsize(__file__))

# output
# File         : ospath_properties.py
# Access time  : Sun Mar 18 16:21:22 2018
# Modified time: Fri Nov 11 17:18:44 2016
# Change time  : Fri Nov 11 17:18:44 2016
# Size         : 481
```

`os.path.getatime()`返回访问时间， `os.path.getmtime()`返回修改时间，`os.path.getctime()`返回创建时间。 `os.path.getsize()`返回文件中的数据量，以字节为单位表示。

## 测试文件

当程序遇到路径名时，通常需要知道路径是指文件，目录还是符号链接以及它是否存在。 `os.path`包括测试所有这些条件的功能。

```python
import os.path

FILENAMES = [
    __file__,
    os.path.dirname(__file__),
    '/',
    './broken_link',
]

for file in FILENAMES:
    print('File        : {!r}'.format(file))
    print('Absolute    :', os.path.isabs(file))
    print('Is File?    :', os.path.isfile(file))
    print('Is Dir?     :', os.path.isdir(file))
    print('Is Link?    :', os.path.islink(file))
    print('Mountpoint? :', os.path.ismount(file))
    print('Exists?     :', os.path.exists(file))
    print('Link Exists?:', os.path.lexists(file))
    print()
    
# output
# File        : 'ospath_tests.py'
# Absolute    : False
# Is File?    : True
# Is Dir?     : False
# Is Link?    : False
# Mountpoint? : False
# Exists?     : True
# Link Exists?: True
# 
# File        : ''
# Absolute    : False
# Is File?    : False
# Is Dir?     : False
# Is Link?    : False
# Mountpoint? : False
# Exists?     : False
# Link Exists?: False
# 
# File        : '/'
# Absolute    : True
# Is File?    : False
# Is Dir?     : True
# Is Link?    : False
# Mountpoint? : True
# Exists?     : True
# Link Exists?: True
# 
# File        : './broken_link'
# Absolute    : False
# Is File?    : False
# Is Dir?     : False
# Is Link?    : True
# Mountpoint? : False
# Exists?     : False
# Link Exists?: True
```

所有测试函数都返回布尔值。



相关文档：

https://pymotw.com/3/os.path/index.html