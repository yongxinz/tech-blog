# 每周一个 Python 模块 | pathlib

使用面向对象的 API 而不是低级字符串操作来解析，构建，测试和以其他方式处理文件名和路径。

## 构建路径

要创建引用相对于现有路径值的新路径，可以使用 `/` 运算符来扩展路径，运算符的参数可以是字符串或其他路径对象。

```python
import pathlib

usr = pathlib.PurePosixPath('/usr')
print(usr)	# /usr

usr_local = usr / 'local'
print(usr_local)	# /usr/local

usr_share = usr / pathlib.PurePosixPath('share')
print(usr_share)	# /usr/share

root = usr / '..'
print(root)	# /usr/..

etc = root / '/etc/'
print(etc)	# /etc
```

正如`root`示例所示，运算符在给定路径值时将它们组合在一起，并且在包含父目录引用时不会对结果进行规范化 `".."`。但是，如果某段以路径分隔符开头，则会以与之相同的方式将其解释为新的“根”引用 `os.path.join()`，从路径值中间删除额外路径分隔符，如此处的`etc`示例所示。

路径类包括 `resolve()` 方法，通过查看目录和符号链接的文件系统以及生成名称引用的绝对路径来规范化路径。

```python
import pathlib

usr_local = pathlib.Path('/usr/local')
share = usr_local / '..' / 'share'
print(share.resolve())	# /usr/share
```

这里相对路径转换为绝对路径 `/usr/share`。如果输入路径包含符号链接，那么也会扩展这些符号链接以允许已解析的路径直接引用目标。

要在事先不知道段时构建路径，请使用 `joinpath()`，将每个路径段作为单独的参数传递。

```python
import pathlib

root = pathlib.PurePosixPath('/')
subdirs = ['usr', 'local']
usr_local = root.joinpath(*subdirs)
print(usr_local)	# /usr/local
```

与`/`运算符一样，调用`joinpath()`会创建一个新实例。

给定一个现有的路径对象，很容易构建一个具有微小差异的新对象，例如引用同一目录中的不同文件，使用`with_name()`创建替换文件名的新路径。使用 `with_suffix()`创建替换文件扩展名的新路径。

```python
import pathlib

ind = pathlib.PurePosixPath('source/pathlib/index.rst')
print(ind)	# source/pathlib/index.rst

py = ind.with_name('pathlib_from_existing.py')
print(py)	# source/pathlib/pathlib_from_existing.py

pyc = py.with_suffix('.pyc')
print(pyc)	# source/pathlib/pathlib_from_existing.pyc
```

两种方法都返回新对象，原始文件保持不变。

## 解析路径

Path 对象具有从名称中提取部分值的方法和属性。例如，`parts` 属性生成一系列基于路径分隔符解析的路径段。

```python
import pathlib

p = pathlib.PurePosixPath('/usr/local')
print(p.parts)	# ('/', 'usr', 'local')
```

序列是一个元组，反映了路径实例的不变性。

有两种方法可以从给定的路径对象“向上”导航文件系统层次结构。`parent` 属性引用包含路径的目录的新路径实例，通过 `os.path.dirname()` 返回值。`parents` 属性是一个可迭代的，它产生父目录引用，不断地“向上”路径层次结构，直到到达根目录。

```python
import pathlib

p = pathlib.PurePosixPath('/usr/local/lib')

print('parent: {}'.format(p.parent))

print('\nhierarchy:')
for up in p.parents:
    print(up)
    
# output
# parent: /usr/local
# 
# hierarchy:
# /usr/local
# /usr
# /
```

该示例遍历`parents`属性并打印成员值。

可以通过路径对象的属性访问路径的其他部分。`name` 属性保存路径的最后一部分，位于最终路径分隔符（`os.path.basename()` 生成的相同值）之后。`suffix`属性保存扩展分隔符后面的值，`stem`属性保存后缀之前的名称部分。

```python
import pathlib

p = pathlib.PurePosixPath('./source/pathlib/pathlib_name.py')
print('path  : {}'.format(p))	# path  : source/pathlib/pathlib_name.py
print('name  : {}'.format(p.name))	# name  : pathlib_name.py
print('suffix: {}'.format(p.suffix))	# suffix: .py
print('stem  : {}'.format(p.stem))	# stem  : pathlib_name
```

虽然`suffix`和`stem`值类似于 `os.path.splitext()` 生成的值，但值仅基于 `name` 而不是完整路径。

## 创建具体路径

`Path ` 可以从引用文件系统上的文件，目录或符号链接名称（或潜在名称）的字符串创建具体类的实例。该类还提供了几种方便的方法，用于使用常用的更改位置（例如当前工作目录和用户的主目录）构建实例。

```python
import pathlib

home = pathlib.Path.home()
print('home: ', home)	# home:  /Users/dhellmann

cwd = pathlib.Path.cwd()
print('cwd : ', cwd)	# cwd :  /Users/dhellmann/PyMOTW
```

## 目录内容

有三种方法可以访问目录列表，以发现文件系统上可用文件的名称。`iterdir()` 是一个生成器，`Path` 为包含目录中的每个项生成一个新实例。

```python
import pathlib

p = pathlib.Path('.')

for f in p.iterdir():
    print(f)
    
# output
# example_link
# index.rst
# pathlib_chmod.py
# pathlib_convenience.py
# pathlib_from_existing.py
# pathlib_glob.py
# pathlib_iterdir.py
# pathlib_joinpath.py
# pathlib_mkdir.py
# pathlib_name.py
```

如果`Path`不引用目录，则`iterdir()` 引发`NotADirectoryError`。

`glob()` 仅查找与模式匹配的文件。

```python
import pathlib

p = pathlib.Path('..')

for f in p.glob('*.rst'):
    print(f)
    
# output
# ../about.rst
# ../algorithm_tools.rst
# ../book.rst
# ../compression.rst
# ../concurrency.rst
# ../cryptographic.rst
# ../data_structures.rst
# ../dates.rst
# ../dev_tools.rst
# ../email.rst
```

glob 处理器支持使用模式前缀进行递归扫描 `**`或通过调用`rglob()`而不是`glob()`。

```python
import pathlib

p = pathlib.Path('..')

for f in p.rglob('pathlib_*.py'):
    print(f)
    
# output
# ../pathlib/pathlib_chmod.py
# ../pathlib/pathlib_convenience.py
# ../pathlib/pathlib_from_existing.py
# ../pathlib/pathlib_glob.py
# ../pathlib/pathlib_iterdir.py
# ../pathlib/pathlib_joinpath.py
# ../pathlib/pathlib_mkdir.py
# ../pathlib/pathlib_name.py
# ../pathlib/pathlib_operator.py
# ../pathlib/pathlib_ownership.py
# ../pathlib/pathlib_parents.py
```

由于此示例从父目录开始，因此需要进行递归搜索以查找匹配的示例文件 `pathlib_*.py`。

## 读写文件

每个 `Path` 实例都包含用于处理它所引用的文件内容的方法。要读取内容，使用 `read_bytes()` 或 `read_text()`。要写入文件，使用 `write_bytes()` 或 `write_text()`。

使用 `open()` 方法打开文件并保留文件句柄，而不是将名称传递给内置 `open()` 函数。

```python
import pathlib

f = pathlib.Path('example.txt')

f.write_bytes('This is the content'.encode('utf-8'))

with f.open('r', encoding='utf-8') as handle:
    print('read from open(): {!r}'.format(handle.read()))

print('read_text(): {!r}'.format(f.read_text('utf-8')))

# output
# read from open(): 'This is the content'
# read_text(): 'This is the content'
```

## 操作目录和符号链接

```python
import pathlib

p = pathlib.Path('example_dir')

print('Creating {}'.format(p))
p.mkdir()

# output
# Creating example_dir
# Traceback (most recent call last):
#   File "pathlib_mkdir.py", line 16, in <module>
#     p.mkdir()
#   File ".../lib/python3.6/pathlib.py", line 1226, in mkdir
#     self._accessor.mkdir(self, mode)
#   File ".../lib/python3.6/pathlib.py", line 387, in wrapped
#     return strfunc(str(pathobj), *args)
# FileExistsError: [Errno 17] File exists: 'example_dir'
```

如果路径已存在，则 `mkdir()` 引发 `FileExistsError`。

使用 `symlink_to()` 创建符号链接，链接将根据路径的值命名，并将引用作为 `symlink_to()` 参数给出的名称。

```python
import pathlib

p = pathlib.Path('example_link')

p.symlink_to('index.rst')

print(p)	# example_link
print(p.resolve().name)	# index.rst
```

此示例创建一个符号链接，然后用 `resolve()` 读取链接来查找它指向的内容，并打印名称。

## 文件类型

此示例创建了几种不同类型的文件，并测试这些文件以及本地操作系统上可用的一些其他特定于设备的文件。

```python
import itertools
import os
import pathlib

root = pathlib.Path('test_files')

# Clean up from previous runs.
if root.exists():
    for f in root.iterdir():
        f.unlink()
else:
    root.mkdir()

# Create test files
(root / 'file').write_text('This is a regular file', encoding='utf-8')
(root / 'symlink').symlink_to('file')
os.mkfifo(str(root / 'fifo'))

# Check the file types
to_scan = itertools.chain(
    root.iterdir(),
    [pathlib.Path('/dev/disk0'), pathlib.Path('/dev/console')],
)
hfmt = '{:18s}' + ('  {:>5}' * 6)
print(hfmt.format('Name', 'File', 'Dir', 'Link', 'FIFO', 'Block', 'Character'))
print()

fmt = '{:20s}  ' + ('{!r:>5}  ' * 6)
for f in to_scan:
    print(fmt.format(
        str(f),
        f.is_file(),
        f.is_dir(),
        f.is_symlink(),
        f.is_fifo(),
        f.is_block_device(),
        f.is_char_device(),
    ))
    
# output
# Name                 File    Dir   Link   FIFO  Block  Character
# 
# test_files/fifo       False  False  False   True  False  False
# test_files/file        True  False  False  False  False  False
# test_files/symlink     True  False   True  False  False  False
# /dev/disk0            False  False  False  False   True  False
# /dev/console          False  False  False  False  False   True
```

每一种方法，`is_dir()`，`is_file()`， `is_symlink()`，`is_socket()`，`is_fifo()`， `is_block_device()` 和 `is_char_device()`，都不带任何参数。

## 文件属性

可以使用方法 `stat()` 或 `lstat()`（用于检查可能是符号链接的某些内容的状态）访问有关文件的详细信息 。这些方法与 `os.stat()`和 `os.lstat()` 产生相同的结果。

```python
# pathlib_stat.py 

import pathlib
import sys
import time

if len(sys.argv) == 1:
    filename = __file__
else:
    filename = sys.argv[1]

p = pathlib.Path(filename)
stat_info = p.stat()

print('{}:'.format(filename))
print('  Size:', stat_info.st_size)
print('  Permissions:', oct(stat_info.st_mode))
print('  Owner:', stat_info.st_uid)
print('  Device:', stat_info.st_dev)
print('  Created      :', time.ctime(stat_info.st_ctime))
print('  Last modified:', time.ctime(stat_info.st_mtime))
print('  Last accessed:', time.ctime(stat_info.st_atime))

# output
# $ python3 pathlib_stat.py
# 
# pathlib_stat.py:
#   Size: 607
#   Permissions: 0o100644
#   Owner: 527
#   Device: 16777220
#   Created      : Thu Dec 29 12:38:23 2016
#   Last modified: Thu Dec 29 12:38:23 2016
#   Last accessed: Sun Mar 18 16:21:41 2018
# 
# $ python3 pathlib_stat.py index.rst
# 
# index.rst:
#   Size: 19569
#   Permissions: 0o100644
#   Owner: 527
#   Device: 16777220
#   Created      : Sun Mar 18 16:11:31 2018
#   Last modified: Sun Mar 18 16:11:31 2018
#   Last accessed: Sun Mar 18 16:21:40 2018
```

输出将根据示例代码的安装方式而有所不同，尝试在命令行上传递不同的文件名 `pathlib_stat.py`。

为了更简单地访问有关文件所有者的信息，使用 `owner()`和`group()`。

```python
import pathlib

p = pathlib.Path(__file__)

print('{} is owned by {}/{}'.format(p, p.owner(), p.group()))

# output
# pathlib_ownership.py is owned by dhellmann/dhellmann
```

`touch()` 方法类似于 Unix 的 `touch` 命令，创建文件或更新现有文件的修改时间和权限。

```python
# pathlib_touch.py 

import pathlib
import time

p = pathlib.Path('touched')
if p.exists():
    print('already exists')
else:
    print('creating new')

p.touch()
start = p.stat()

time.sleep(1)

p.touch()
end = p.stat()

print('Start:', time.ctime(start.st_mtime))
print('End  :', time.ctime(end.st_mtime))

# output
# $ python3 pathlib_touch.py
# 
# creating new
# Start: Sun Mar 18 16:21:41 2018
# End  : Sun Mar 18 16:21:42 2018
# 
# $ python3 pathlib_touch.py
# 
# already exists
# Start: Sun Mar 18 16:21:42 2018
# End  : Sun Mar 18 16:21:43 2018
```

运行多次此示例会在后续运行中更新现有文件。

## 权限

在类 Unix 系统上，可以使用 `chmod()` 更改文件权限，将模式作为整数传递。可以使用`stat`模块中定义的常量构造模式值。此示例切换用户的执行权限位。

```python
import os
import pathlib
import stat

# Create a fresh test file.
f = pathlib.Path('pathlib_chmod_example.txt')
if f.exists():
    f.unlink()
f.write_text('contents')

# Determine what permissions are already set using stat.
existing_permissions = stat.S_IMODE(f.stat().st_mode)
print('Before: {:o}'.format(existing_permissions))	# Before: 644

# Decide which way to toggle them.
if not (existing_permissions & os.X_OK):
    print('Adding execute permission')	# Adding execute permission
    new_permissions = existing_permissions | stat.S_IXUSR
else:
    print('Removing execute permission')
    # use xor to remove the user execute permission
    new_permissions = existing_permissions ^ stat.S_IXUSR

# Make the change and show the new value.
f.chmod(new_permissions)
after_permissions = stat.S_IMODE(f.stat().st_mode)
print('After: {:o}'.format(after_permissions))	# After: 744
```

## 删除

有两种方法可以从文件系统中删除内容，具体取决于类型。要删除空目录，使用 `rmdir()`。

```python
import pathlib

p = pathlib.Path('example_dir')

print('Removing {}'.format(p))
p.rmdir()

# output
# Removing example_dir
# Traceback (most recent call last):
#   File "pathlib_rmdir.py", line 16, in <module>
#     p.rmdir()
#   File ".../lib/python3.6/pathlib.py", line 1270, in rmdir
#     self._accessor.rmdir(self)
#   File ".../lib/python3.6/pathlib.py", line 387, in wrapped
#     return strfunc(str(pathobj), *args)
# FileNotFoundError: [Errno 2] No such file or directory: 'example_dir'
```

如果目录不存在会引发错误 `FileNotFoundError`，尝试删除非空目录也是错误的。

对于文件，符号链接和大多数其他路径类型使用 `unlink()`。

```python
import pathlib

p = pathlib.Path('touched')

p.touch()

print('exists before removing:', p.exists())	# exists before removing: True

p.unlink()

print('exists after removing:', p.exists())	# exists after removing: False
```

用户必须具有删除文件，符号链接，套接字或其他文件系统对象的权限。

相关文档：

https://pymotw.com/3/pathlib/index.html