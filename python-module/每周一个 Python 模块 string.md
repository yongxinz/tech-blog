# 每周一个 Python 模块 | string

目的：包含用于处理文本的常量和类。

string 模块可以追溯到最早的 Python 版本。先前在此模块中实现的许多功能已移至 str 对象方法。string 模块保留了几个有用的常量和类来处理 str 对象。

## 函数 `capwords()`
直接看下面的事例：

```python
import string

s = 'The quick brown fox jumped over the lazy dog.'

print(s)    # The quick brown fox jumped over the lazy dog.
print(string.capwords(s))   # The Quick Brown Fox Jumped Over The Lazy Dog.
```

## 模板
字符串模板作为 PEP 292 一部分添加，旨在替代内置插值语法。通过 `string.Template` 插值，在名称前加上 $（例如，`$`）来标识变量。或者，如果需要将它们从周围的文本中设置出来，它们也可以用花括号包裹（例如：`${var}`）。

```python
import string

values = {'var': 'foo'}

t = string.Template("""
Variable        : $var
Escape          : $$
Variable in text: ${var}iable
""")

print('TEMPLATE:', t.substitute(values))

s = """
Variable        : %(var)s
Escape          : %%
Variable in text: %(var)siable
"""

print('INTERPOLATION:', s % values)

s = """
Variable        : {var}
Escape          : {{}}
Variable in text: {var}iable
"""

print('FORMAT:', s.format(**values))

# output
# TEMPLATE:
# Variable        : foo
# Escape          : $
# Variable in text: fooiable
# 
# INTERPOLATION:
# Variable        : foo
# Escape          : %
# Variable in text: fooiable
# 
# FORMAT:
# Variable        : foo
# Escape          : {}
# Variable in text: fooiable
```

在前两种情况下，触发字符（$或%）通过重复两次来转义。对于语法格式，`{` 和 `}` 都需要通过重复它们进行转义。

模板和字符串插值或格式化之间的一个关键区别是不考虑参数类型。这些值将转换为字符串，并将字符串插入到结果中，没有可用的格式选项。例如，无法控制用于表示浮点值的位数。

有一个好处是，如果并非模板所需的所有值都作为参数提供，则使用 `safe_substitute()` 方法可以避免异常。

```python
import string

values = {'var': 'foo'}

t = string.Template("$var is here but $missing is not provided")

try:
    print('substitute()     :', t.substitute(values))
except KeyError as err:
    print('ERROR:', str(err))

print('safe_substitute():', t.safe_substitute(values))

# output
# ERROR: 'missing'
# safe_substitute(): foo is here but $missing is not provided
```

由于字典中没有 `missing` 值，引发了一个 `KeyError`，`safe_substitute()` 捕获它并在文本中单独保留变量表达式。

## 高级模板
可以通过调整用于在模板主体中查找变量名称的正则表达式模式来更改默认语法。一种简单的方法是更改 `delimiter` 和 `idpattern` 类属性。

```python
import string


class MyTemplate(string.Template):
    delimiter = '%'
    idpattern = '[a-z]+_[a-z]+'


template_text = '''
  Delimiter : %%
  Replaced  : %with_underscore
  Ignored   : %notunderscored
'''

d = {
    'with_underscore': 'replaced',
    'notunderscored': 'not replaced',
}

t = MyTemplate(template_text)
print('Modified ID pattern:')
print(t.safe_substitute(d))

# output
# Modified ID pattern:
# 
#   Delimiter : %
#   Replaced  : replaced
#   Ignored   : %notunderscored
```

在此示例中，替换规则已更改，以分隔符%代替，而变量名必须在中间某处包含下划线。该模式 `%notunderscored` 不会被任何内容替换，因为它不包含下划线字符。

对于更复杂的更改，可以覆盖 `pattern` 属性并定义全新的正则表达式。提供的模式必须包含四个命名组，用于捕获转义分隔符，命名变量，变量名称的支撑版本以及无效分隔符模式。

```python
import string

t = string.Template('$var')
print(t.pattern.pattern)

# output
# \$(?:
#   (?P<escaped>\$) |                # two delimiters
#   (?P<named>[_a-z][_a-z0-9]*)    | # identifier
#   {(?P<braced>[_a-z][_a-z0-9]*)} | # braced identifier
#   (?P<invalid>)                    # ill-formed delimiter exprs
# )
```

`t.pattern` 是一个已编译的正则表达式，但原始字符串可通过其 `pattern` 属性获得。

此示例使用 `{{var}}` 作为变量语法定义用于创建新类型模板的新模式。

```python
import re
import string


class MyTemplate(string.Template):
    delimiter = '{{'
    pattern = r'''
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    '''


t = MyTemplate('''
{{{{
{{var}}
''')

print('MATCHES:', t.pattern.findall(t.template))
print('SUBSTITUTED:', t.safe_substitute(var='replacement'))

# output
# MATCHES: [('{{', '', '', ''), ('', 'var', '', '')]
# SUBSTITUTED:
# {{
# replacement
```

无论是 `named` 和 `braced` 模式必须单独提供，即使它们是相同的。

## 常数
string 模块包含许多与 ASCII 和数字字符集相关的常量。

```python
import inspect
import string


def is_str(value):
    return isinstance(value, str)


for name, value in inspect.getmembers(string, is_str):
    if name.startswith('_'):
        continue
    print('%s=%r\n' % (name, value))
    
# output
# ascii_letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
# 
# ascii_lowercase='abcdefghijklmnopqrstuvwxyz'
# 
# ascii_uppercase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# 
# digits='0123456789'
# 
# hexdigits='0123456789abcdefABCDEF'
# 
# octdigits='01234567'
# 
# printable='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQ
# RSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
# 
# punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
# 
# whitespace=' \t\n\r\x0b\x0c'
```

这些常量在处理 ASCII 数据时很有用，但由于在某种形式的 Unicode 中遇到非 ASCII 文本越来越常见，因此它们的应用受到限制。

相关文档：

https://pymotw.com/3/string/index.html