# Python 开发编码规范

最近，团队又来了几个小伙伴，经过一段时间磨合之后，发现彼此之间还是比较默契的，但有一个很大的问题是，每个人的编程风格和习惯都不同，导致现在代码看起来非常混乱。

所以，有一个统一的开发编码规范还是很重要的。我在网上搜索了一些资料，在 PEP8 的基础上，同时结合目前代码的特点，总结出下文，分享给大家。

## 代码布局

### 缩进

每个缩进级别采用 4 个空格，注意不是 Tab。

当一行超出单行最大长度时，采用 Python 隐式续行，即垂直对齐于圆括号、方括号和花括号。

例如：

```python
# 调用函数
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
                         
# 定义列表
my_list = [
    1, 2, 3,
    4, 5, 6,
]

# 定义字典
my_dict = {
    'a': 'hello',
    'b': 'world'
}
```

### 每行最大长度

传统来说一直都是 80，但我觉得以现在的浏览器屏宽来说，设置 120 都没问题，我设置的是 120.

### 二元运算符前换行

例如：

```python
# 更容易匹配运算符与操作数
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

### 空行

- 使用 1 个空行来分隔类中的方法（method）定义。
- 使用 2 个空行来分隔最外层的函数（function）和类（class）定义。

### 模块引用

Imports 应该写在代码文件的开头，并按照下面这样的顺序引用：

1. 标准库 imports
1. 相关第三方 imports
1. 本地应用/库的特定 imports

禁止使用 `import *` 这样的方式。

### 模块级的双下划线命名

模块中的「双下滑线」变量，比如 `__all__`，`__author__`，`__version__` 等，直接写在文件开头。

例如：

```python
"""
This is the example module.
This module does stuff.
"""

from __future__ import barry_as_FLUFL

__all__ = ['a', 'b', 'c']
__version__ = '0.1'
__author__ = 'Cardinal Biggles'

import os
import sys
```

## 字符串引用

使用单引号来表示字符串，对于三引号字符串，使用双引号字符表示。

例如：

```python
# 单引号字符串
a = 'hello'

# 三引号字符串
"""
这是一个三引号字符串
"""
```

## 表达式和语句中的空格

在下列情形中避免使用过多的空白：

1、方括号，圆括号和花括号之后：

```python
# 正确的例子:
spam(ham[1], {eggs: 2})

# 错误的例子：
spam( ham[ 1 ], { eggs: 2 } )
```

2、逗号，分号或冒号之前：

```python
# 正确的例子:
if x == 4: print x, y; x, y = y, x

# 错误的例子:
if x == 4 : print x , y ; x , y = y , x
```

3、切片操作

```python
# 正确的例子:
ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3], ham[1:9:]
ham[lower:upper], ham[lower:upper:], ham[lower::step]
ham[lower+offset : upper+offset]
ham[: upper_fn(x) : step_fn(x)], ham[:: step_fn(x)]
ham[lower + offset : upper + offset]

# 错误的例子:
ham[lower + offset:upper + offset]
ham[1: 9], ham[1 :9], ham[1:9 :3]
ham[lower : : upper]
ham[ : upper]
```

4、赋值

```python
# 正确的例子:
x = 1
y = 2
long_variable = 3

# 错误的例子:
x             = 1
y             = 2
long_variable = 3
```

还有一点需要注意的是，一定要把行尾的空格删掉。

## 注释

对代码进行必要的注释，如果修改代码，还要修改对应的注释内容。

删除无用的注释内容，增加代码可读性。

### 块注释

要使用块注释，禁止使用行内注释，注释时，`#` 和后面的注释内容要有空格。

例如：

```python
# 这是一个注释
x = 1 + 1
```

不要使用下面的注释方式：

```python
x = 1 + 1   # 这是一个注释
```

### TODO 注释

主要包含以下三点内容：

1. 开头包含「TODO」字符串
1. 紧跟着是用括号括起来的你的名字或者 email
1. 再接下来是冒号，然后写接下来要做内容的文字解释

例如：

```python
# TODO(zhangyongxin): 明确需求之后再开发
```

### 文档字符串

对于公共模块，函数，类和方法，使用文档字符串。内容包括三个方面，分别是功能描述、参数、返回值。

例如：

```python
class MyClass:
    """
    这是一个自定义类
    """
    something
    
def func():
    """
    这是一个自定义函数
    
    params:
        params1: 第一个参数
        params2: 第二个参数
        
    return:
        {'data': {}, 'status': 200}
    """
    something    
```

## 命名

1、文件名

采用小写字母和下划线的方式。

例如：

```python
utils.py

mail_lib.py
```

2、函数名

采用小写字母和下划线的方式。

例如：

```python
def func():
    pass

def send_mail():
    pass
```

3、类名

采用大驼峰方式。

例如：

```python
class MyClass:
    pass
```

4、常量和变量：

例如：

```python
# 常量
TOTAL
MAX_COUNT

# 变量
total
max_total
```

参考文章：

https://alvinzhu.xyz/2017/10/07/python-pep-8/