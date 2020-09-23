# Python 中 \x00 和空字符串的区别，以及在 Django 中的坑

事情是这样的，我有一个守护进程，不停地从 RabbitMQ 消费数据，然后保存到 MySQL。操作数据库使用的是 Django 的 ORM 语法。

最近一段时间，频繁发生一个问题，就是有一类数据，守护进程从后台使用 `create` 方法，直接入库完全没问题。但是，在页面上，通过表单来修改这条数据，无论如何都无法保存成功，报错信息提示某一个字段不能为空。但是这个字段明明是有值的，很让人费解。

仔细分析了代码之后，感觉可能发生问题的只有这一句：

```python
serializer = self.get_serializer(data=request.data)
serializer.is_valid(raise_exception=True)
```

因为打印 `serializer` 是有值的，所以肯定是 `is_valid` 做表单验证时给过滤掉了。但是为什么会过滤就需要更深一步去探索了。

通过单步调试，走到函数的调用关系中，发现了问题的关键所在。

```python
​```python
# django/forms/fields.py

class CharField(Field):
    def __init__(self, *, max_length=None, min_length=None, strip=True, empty_value='', **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        self.strip = strip
        self.empty_value = empty_value
        super().__init__(**kwargs)
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(int(min_length)))
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(int(max_length)))
        self.validators.append(validators.ProhibitNullCharactersValidator())
        ...
​```
```

这段代码只截取了一部分，是对 Model `CharField` 字段的一些定义，比如最小长度，最大长度等等。除了这些，最后还有一句验证，其中调用了下面这个类：

```python
# django/core/validators.py

@deconstructible
class ProhibitNullCharactersValidator:
    """Validate that the string doesn't contain the null character."""
    message = _('Null characters are not allowed.')
    code = 'null_characters_not_allowed'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if '\x00' in str(value):
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.message == other.message and
            self.code == other.code
        )
```

而在这个类中，有一个 `__call__`  方法，如果有 `\x00` 在需要保存的字段值里，就会抛异常。不知道源码里为什么会有这样的判断。

再回过头来看提示我为空的那个字段的值，其中的确有不可见字符 `\x00`。

到这里，这个问题也就明确了，那怎么解决呢？其实很简单，在后台保存数据时，直接将 `\x00` 替换掉成空就可以了。

问题是解决了，但是 `\x00` 和空有什么区别呢？这就又涉及到 Python 的编码问题了。虽然两者都是空，但在很多方面都不相同，下面用一段简单的代码来表现一下：

```python
>>> a = '\x00'
>>> b = ''
>>>
>>> print(a)

>>> print(b)

>>> a == b
False
>>>
>>> len(a)
1
>>> len(b)
0
>>> print('hello\x00world')
helloworld
>>> a = 'hello\x00world'
>>> if '\x00' in a:
...     print('111')
...
111
>>>
```

以上。

**特别鸣谢：**发现了关键问题，我的同事杨小黑

**往期精彩：**

