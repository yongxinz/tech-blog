# 每周一个 Python 模块 | glob

使用 Unix shell 规则查找与模式匹配的文件名。

尽管 `glob` API 不多，但该模块具有很强的功能。当程序需要通过名称与模式匹配的方式查找文件列表时，它很有用。要创建一个文件列表，这些文件名具有特定的扩展名，前缀或中间的任何公共字符串，这个时候，使用`glob`而不是编写自定义代码来扫描目录内容。

`glob` 模式规则与 [`re`](https://pymotw.com/3/re/index.html#module-re) 模块使用的正则表达式不同。相反，它们遵循标准的 Unix 路径扩展规则，只有少数特殊字符用于实现两个不同的通配符和字符范围。模式规则应用于文件名段（在路径分隔符处停止`/`），模式中的路径可以是相对的或绝对的，Shell 变量名和波浪号（`~`）不会展开。

## 示例数据

本节中的示例假定当前工作目录中存在以下测试文件。

```python
dir
dir/file.txt
dir/file1.txt
dir/file2.txt
dir/filea.txt
dir/fileb.txt
dir/file?.txt
dir/file*.txt
dir/file[.txt
dir/subdir
dir/subdir/subfile.txt
```

## 通配符

星号（`*`）匹配名称段中的零个或多个字符。例如，`dir/*`。

```python
import glob
for name in sorted(glob.glob('dir/*')):
    print(name)
    
# output
# dir/file *.txt
# dir/file.txt
# dir/file1.txt
# dir/file2.txt
# dir/file?.txt
# dir/file[.txt
# dir/filea.txt
# dir/fileb.txt
# dir/subdir
```

该模式匹配目录 dir 中的每个路径名（文件或目录），而不会进一步递归到子目录中。返回的数据未排序，因此这里的示例对其进行排序以便更直观地展示结果。

要列出子目录中的文件，子目录必须包含在模式中。

```python
import glob

print('Named explicitly:')
for name in sorted(glob.glob('dir/subdir/*')):
    print('  {}'.format(name))

print('Named with wildcard:')
for name in sorted(glob.glob('dir/*/*')):
    print('  {}'.format(name))
    
# output
# Named explicitly:
#   dir/subdir/subfile.txt
# Named with wildcard:
#   dir/subdir/subfile.txt
```

前面显示的第一种情况明确列出了子目录名称，而第二种情况依赖于通配符来查找目录。

在这种情况下，结果是相同的。如果有另一个子目录，则通配符将匹配两个子目录并包含两者的文件名。

## 单字符通配符

问号（`?`）是另一个通配符。它匹配名称中该位置的任何单个字符。

```python
import glob

for name in sorted(glob.glob('dir/file?.txt')):
    print(name)
    
# output
# dir/file*.txt
# dir/file1.txt
# dir/file2.txt
# dir/file?.txt
# dir/file[.txt
# dir/filea.txt
# dir/fileb.txt
```

示例匹配所有以 `file` 开头的文件名，具有任何类型的单个字符，然后以 `.txt` 结束。

## 字符范围

使用字符范围（`[a-z]`）而不是问号来匹配多个字符之一。此示例在扩展名之前查找名称中带有数字的所有文件。

```python
import glob
for name in sorted(glob.glob('dir/*[0-9].*')):
    print(name)
    
# output
# dir/file1.txt
# dir/file2.txt
```

字符范围`[0-9]`匹配任何单个数字。范围根据每个字母/数字的字符代码排序，短划线表示连续字符的连续范围。可以写入相同的范围值`[0123456789]`。

## 转义元字符

有时需要搜索名称中包含特殊元字符（`glob`用于模式匹配）的文件。`escape()`函数使用特殊字符“转义”构建合适的模式，因此它们不会被扩展或解释为特殊字符。

```python
import glob

specials = '?*['

for char in specials:
    pattern = 'dir/*' + glob.escape(char) + '.txt'
    print('Searching for: {!r}'.format(pattern))
    for name in sorted(glob.glob(pattern)):
        print(name)
    print()
    
# output
# Searching for: 'dir/*[?].txt'
# dir/file?.txt
# 
# Searching for: 'dir/*[*].txt'
# dir/file*.txt
# 
# Searching for: 'dir/*[[].txt'
# dir/file[.txt
```

通过构建包含单个条目的字符范围来转义每个特殊字符。

相关文档：

https://pymotw.com/3/glob/index.html