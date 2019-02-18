# 每周一个 Python 模块 | fnmatch

fnmatch 模块主要用于文件名的比较，使用 Unix shell 使用的 glob 样式模式。

## 简单匹配

`fnmatch()` 将单个文件名与模式进行比较并返回布尔值，来看它们是否匹配。当操作系统使用区分大小写的文件系统时，比较区分大小写。

```python
import fnmatch
import os

pattern = 'fnmatch_*.py'
print('Pattern :', pattern)
print()

files = os.listdir('.')
for name in sorted(files):
    print('Filename: {:<25} {}'.format(name, fnmatch.fnmatch(name, pattern)))
    
# output
# Pattern : fnmatch_*.py
# 
# Filename: fnmatch_filter.py         True
# Filename: fnmatch_fnmatch.py        True
# Filename: fnmatch_fnmatchcase.py    True
# Filename: fnmatch_translate.py      True
# Filename: index.rst                 False
```

在此示例中，模式匹配所有以 `'fnmatch_'` 开头和以 `'.py'` 结尾的文件。

要强制进行区分大小写的比较，无论文件系统和操作系统设置如何，请使用 `fnmatchcase()`。

```python
import fnmatch
import os

pattern = 'FNMATCH_*.PY'
print('Pattern :', pattern)
print()

files = os.listdir('.')

for name in sorted(files):
    print('Filename: {:<25} {}'.format(name, fnmatch.fnmatchcase(name, pattern)))
    
# output
# Pattern : FNMATCH_*.PY
# 
# Filename: fnmatch_filter.py         False
# Filename: fnmatch_fnmatch.py        False
# Filename: fnmatch_fnmatchcase.py    False
# Filename: fnmatch_translate.py      False
# Filename: index.rst                 False
```

由于用于测试此程序的 OS X 系统使用区分大小写的文件系统，因此没有文件与修改后的模式匹配。

## 过滤

要测试文件名序列，使用 `filter()`，它返回与 `pattern` 参数匹配的名称列表。

```python
import fnmatch
import os
import pprint

pattern = 'fnmatch_*.py'
print('Pattern :', pattern)

files = list(sorted(os.listdir('.')))

print('\nFiles   :')
pprint.pprint(files)

print('\nMatches :')
pprint.pprint(fnmatch.filter(files, pattern))

# output
# Pattern : fnmatch_*.py
# 
# Files   :
# ['fnmatch_filter.py',
#  'fnmatch_fnmatch.py',
#  'fnmatch_fnmatchcase.py',
#  'fnmatch_translate.py',
#  'index.rst']
# 
# Matches :
# ['fnmatch_filter.py',
#  'fnmatch_fnmatch.py',
#  'fnmatch_fnmatchcase.py',
#  'fnmatch_translate.py']
```

在此示例中，`filter()` 返回与此部分关联的示例源文件的名称列表。

## 翻译模式

在内部，`fnmatch` 将 `glob` 模式转换为正则表达式，并使用 `re` 模块比较名称和模式。`translate()` 函数是将 `glob` 模式转换为正则表达式的公共 API。

```python
import fnmatch

pattern = 'fnmatch_*.py'
print('Pattern :', pattern) # Pattern : fnmatch_*.py
print('Regex   :', fnmatch.translate(pattern))  # Regex   : (?s:fnmatch_.*\.py)\Z
``` 


原文链接：

https://pymotw.com/3/fnmatch/index.html