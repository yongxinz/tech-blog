# 每周一个 Python 模块 | json

**目的：**将 Python 对象编码为 JSON 字符串，并将 JSON 字符串解码为 Python 对象。

`json` 模块提供了一个类似于 pickle 的 API，将内存中的 Python 对象转换为 JSON 序列。与 pickle 不同，JSON 具有以多种语言（尤其是 JavaScript）实现的优点。它在 REST API 中 Web 服务端和客户端之间的通信被广泛应用，同时对于应用程序间通信需求也很有用。

## 编码和解码简单数据类型

Python 的默认原生类型（`str`，`int`，`float`，`list`， `tuple`，和`dict`）。

```python
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA:', repr(data))	# DATA: [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

data_string = json.dumps(data)
print('JSON:', data_string)	# JSON: [{"a": "A", "b": [2, 4], "c": 3.0}]
```

表面上看，类似于 Python `repr()` 的输出。

编码，然后重新解码可能不会给出完全相同类型的对象。

```python
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA   :', data)	# DATA   : [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

data_string = json.dumps(data)
print('ENCODED:', data_string)	# ENCODED: [{"a": "A", "b": [2, 4], "c": 3.0}]

decoded = json.loads(data_string)
print('DECODED:', decoded)	# [{'a': 'A', 'b': [2, 4], 'c': 3.0}]

print('ORIGINAL:', type(data[0]['b']))	# ORIGINAL: <class 'tuple'>
print('DECODED :', type(decoded[0]['b']))	# DECODED : <class 'list'>
```

特别是，元组成为了列表。

## 格式化输出

JSON 的结果是更易于阅读的。`dumps()` 函数接受几个参数以使输出更易读结果。例如，`sort_keys` 标志告诉编码器以排序而不是随机顺序输出字典的键。

```python
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA:', repr(data))	# DATA: [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

unsorted = json.dumps(data)
print('JSON:', json.dumps(data))	# JSON: [{"a": "A", "b": [2, 4], "c": 3.0}]
print('SORT:', json.dumps(data, sort_keys=True))	# SORT: [{"a": "A", "b": [2, 4], "c": 3.0}]

first = json.dumps(data, sort_keys=True)
second = json.dumps(data, sort_keys=True)

print('UNSORTED MATCH:', unsorted == first)	# UNSORTED MATCH: True
print('SORTED MATCH  :', first == second)	# SORTED MATCH  : True
```

对于高度嵌套的数据结构，可以指定 `indent` 参数来格式化输出。

```python
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA:', repr(data))

print('NORMAL:', json.dumps(data, sort_keys=True))
print('INDENT:', json.dumps(data, sort_keys=True, indent=2))

# output
# DATA: [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
# NORMAL: [{"a": "A", "b": [2, 4], "c": 3.0}]
# INDENT: [
#   {
#     "a": "A",
#     "b": [
#       2,
#       4
#     ],
#     "c": 3.0
#   }
# ]
```

当 indent 是非负整数时，输出接近于 pprint，与数据结构的每个级别的前导空格匹配缩进级别。

```python
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
print('DATA:', repr(data))

print('repr(data)             :', len(repr(data)))

plain_dump = json.dumps(data)
print('dumps(data)            :', len(plain_dump))

small_indent = json.dumps(data, indent=2)
print('dumps(data, indent=2)  :', len(small_indent))

with_separators = json.dumps(data, separators=(',', ':'))
print('dumps(data, separators):', len(with_separators))

# output
# DATA: [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
# repr(data)             : 35
# dumps(data)            : 35
# dumps(data, indent=2)  : 73
# dumps(data, separators): 29
```

`dumps()` 的 `separators` 参数是一个元组，可以分开列表中的元素和字典中的键值对，默认是 `(', ', ': ')`。通过移除空白，可以产生更紧凑的输出。

## 编码字典

JSON 格式要求字典的键是字符串，如果使用非字符串类型作为键对字典进行编码，会报错 `TypeError`。解决该限制的一种方法是使用 `skipkeys` 参数告诉编码器跳过非字符串键：

``` python
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0, ('d',): 'D tuple'}]

print('First attempt')
try:
    print(json.dumps(data))
except TypeError as err:
    print('ERROR:', err)

print()
print('Second attempt')
print(json.dumps(data, skipkeys=True))

# output
# First attempt
# ERROR: keys must be str, int, float, bool or None, not tuple
# 
# Second attempt
# [{"a": "A", "b": [2, 4], "c": 3.0}]
```

不会引发异常，而是忽略非字符串键。

## 使用自定义类型

目前为止，所有的例子都是用的 Python 的内置类型，`json` 原生就支持它们。不过有时我们也想编码一些自定义类，这里我们有两种方式来实现它。

尝试把下面的类编码：

```python
# json_myobj.py 
class MyObj:

    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return '<MyObj({})>'.format(self.s)
```

编码 `MyObj` 实例最简单的方法是定义一个函数，把未知的类型转换成已知类型。它不需要进行编码操作，它只是把一个对象转换成另一个对象。

```python
import json
import json_myobj

obj = json_myobj.MyObj('instance value goes here')

print('First attempt')
try:
    print(json.dumps(obj))
except TypeError as err:
    print('ERROR:', err)


def convert_to_builtin_type(obj):
    print('default(', repr(obj), ')')
    # Convert objects to a dictionary of their representation
    d = {
        '__class__': obj.__class__.__name__,
        '__module__': obj.__module__,
    }
    d.update(obj.__dict__)
    return d


print()
print('With default')
print(json.dumps(obj, default=convert_to_builtin_type))

# output
# First attempt
# ERROR: Object of type MyObj is not JSON serializable
# 
# With default
# default( <MyObj(instance value goes here)> )
# {"__class__": "MyObj", "__module__": "json_myobj", "s": "instance value goes here"}
```

在 `convert_to_bulitin_type()` 中不能被 `json` 识别的对象被转换成携带其信息的字典，如果程序有必要访问这个 Python 的模块，转换后的信息足够对其进行重建。

我们要想根据解码结果重建 `MyObj()` 实例，需要使用 `loads()` 的 `object_hook` 参数，这样在处理时就可以从模块中导入并用此来创建实例。

数据流中的每个字典都会调用 `object_hook`，这样就不会错过要转换的字典。hook 函数处理后的结果应是应用程序想要的对象。

```python
import json


def dict_to_object(d):
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        print('MODULE:', module.__name__)
        class_ = getattr(module, class_name)
        print('CLASS:', class_)
        args = {
            key: value
            for key, value in d.items()
        }
        print('INSTANCE ARGS:', args)
        inst = class_(**args)
    else:
        inst = d
    return inst


encoded_object = '''
    [{"s": "instance value goes here",
      "__module__": "json_myobj", "__class__": "MyObj"}]
    '''

myobj_instance = json.loads(
    encoded_object,
    object_hook=dict_to_object,
)
print(myobj_instance)

# output
# MODULE: json_myobj
# CLASS: <class 'json_myobj.MyObj'>
# INSTANCE ARGS: {'s': 'instance value goes here'}
# [<MyObj(instance value goes here)>]
```

由于 `json` 会将字符串转成 Unicode 对象，在把它们作为类构造器的关键字参数之前我们还需要把它们重新编码为 ASCII 。

类似的 hook 还能用在内置类型整数，浮点数和其他常量的转换上。

## 编码器和解码器类

除了已经涵盖的简便函数外，`json` 模块还提供用于解码和编码的类。使用类可以对自定义行为直接提供额外的 API。

`JSONEncoder` 使用的是可迭代的接口，可以生成编码数据的「块」，我们使用它可以更容易得将数据写入文件或网络套接字中而无需将整个数据结构放到内存中。

```python
import json

encoder = json.JSONEncoder()
data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

for part in encoder.iterencode(data):
    print('PART:', part)
    
# output
# PART: [
# PART: {
# PART: "a"
# PART: :
# PART: "A"
# PART: ,
# PART: "b"
# PART: :
# PART: [2
# PART: , 4
# PART: ]
# PART: ,
# PART: "c"
# PART: :
# PART: 3.0
# PART: }
# PART: ]
```

输出以单个逻辑单位生成，不管之前是何种数据。

`encode()` 方法基本上等同于 `''.join(encoder.iterencode())`，除了一些额外的错误检测。

要编码任何想要编码的对象，我们需要覆盖 `default()` 方法并实现类似于 `convert_to_bulitin_type()` 功能的代码。.

```python
import json
import json_myobj


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        print('default(', repr(obj), ')')
        # Convert objects to a dictionary of their representation
        d = {
            '__class__': obj.__class__.__name__,
            '__module__': obj.__module__,
        }
        d.update(obj.__dict__)
        return d


obj = json_myobj.MyObj('internal data')
print(obj)
print(MyEncoder().encode(obj))

# output
# <MyObj(internal data)>
# default( <MyObj(internal data)> )
# {"__class__": "MyObj", "__module__": "json_myobj", "s": "internal data"}
```

输出与先前的实现相同。

解码文本，然后转换字典到对象需要比之前稍多的步骤。

```python
import json


class MyDecoder(json.JSONDecoder):

    def __init__(self):
        json.JSONDecoder.__init__(
            self,
            object_hook=self.dict_to_object,
        )

    def dict_to_object(self, d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            print('MODULE:', module.__name__)
            class_ = getattr(module, class_name)
            print('CLASS:', class_)
            args = {
                key: value
                for key, value in d.items()
            }
            print('INSTANCE ARGS:', args)
            inst = class_(**args)
        else:
            inst = d
        return inst


encoded_object = '''
[{"s": "instance value goes here",
  "__module__": "json_myobj", "__class__": "MyObj"}]
'''

myobj_instance = MyDecoder().decode(encoded_object)
print(myobj_instance)

# output
# MODULE: json_myobj
# CLASS: <class 'json_myobj.MyObj'>
# INSTANCE ARGS: {'s': 'instance value goes here'}
# [<MyObj(instance value goes here)>]
```

输出与前面的例子相同。

## 使用流和文件

到目前为止，所有示例都假设整个数据结构可以一次保存在内存中。对于大型数据结构，最好将其直接写入类文件对象。`load()` 和 `dump()`接受对类似文件的对象的引用以用于读取或写入。

```python
import io
import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]

f = io.StringIO()
json.dump(data, f)

print(f.getvalue())	# [{"a": "A", "b": [2, 4], "c": 3.0}]
```

套接字或普通文件句柄的工作方式与本示例中使用的 `StringIO` 缓冲区相同 。

```python
import io
import json

f = io.StringIO('[{"a": "A", "c": 3.0, "b": [2, 4]}]')
print(json.load(f))	# [{'a': 'A', 'c': 3.0, 'b': [2, 4]}]
```

就像 `dump()`，任何类似文件的对象都可以传递给 `load()`。

## 混合数据流

``JSONDecoder` 包含一个叫 `raw_decode()` 的方法，这个方法用于解码跟在有结构的数据之后的数据，比如带有尾文本的 JSON 数据。返回的值是由解码后的输入数据所创建的对象和解码结束的位置的索引。

```python
import json

decoder = json.JSONDecoder()


def get_decoded_and_remainder(input_data):
    obj, end = decoder.raw_decode(input_data)
    remaining = input_data[end:]
    return (obj, end, remaining)


encoded_object = '[{"a": "A", "c": 3.0, "b": [2, 4]}]'
extra_text = 'This text is not JSON.'

print('JSON first:')
data = ' '.join([encoded_object, extra_text])
obj, end, remaining = get_decoded_and_remainder(data)

print('Object              :', obj)
print('End of parsed input :', end)
print('Remaining text      :', repr(remaining))

print()
print('JSON embedded:')
try:
    data = ' '.join([extra_text, encoded_object, extra_text])
    obj, end, remaining = get_decoded_and_remainder(data)
except ValueError as err:
    print('ERROR:', err)
    
# output
# JSON first:
# Object              : [{'a': 'A', 'c': 3.0, 'b': [2, 4]}]
# End of parsed input : 35
# Remaining text      : ' This text is not JSON.'
# 
# JSON embedded:
# ERROR: Expecting value: line 1 column 1 (char 0)
```

不过，它只能在 JSON 对象在数据首部的时候才能正常工作，否则就会发生异常。

## 命令行中的 JSON

`json.tool` 模块实现了一个命令行程序，用于重新格式化 JSON 数据以便于阅读。

```python
[{"a": "A", "c": 3.0, "b": [2, 4]}]
```

输入文件 `example.json` 包含按字母顺序排列的键映射。下面的第一个示例按顺序显示重新格式化的数据，第二个示例用 `--sort-keys`，在打印输出之前对映射键进行排序。

```python
$ python3 -m json.tool example.json

[
    {
        "a": "A",
        "c": 3.0,
        "b": [
            2,
            4
        ]
    }
]

$ python3 -m json.tool --sort-keys example.json

[
    {
        "a": "A",
        "b": [
            2,
            4
        ],
        "c": 3.0
    }
]
```

原文链接：

https://pymotw.com/3/json/index.html