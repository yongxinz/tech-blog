# 每周一个 Python 模块 | array

这个模块定义了一个看起来很像 `list` 的数据结构，只不过它要求所有成员的类型都要相同。

可以用下表做一个简单参考，`array` 标准库文档包含完整的类型代码列表。

| Code | Type               | Minimum size (bytes) |
| ---- | ------------------ | -------------------- |
| `b`  | int                | 1                    |
| `B`  | int                | 1                    |
| `h`  | signed short       | 2                    |
| `H`  | unsigned short     | 2                    |
| `i`  | signed int         | 2                    |
| `I`  | unsigned int       | 2                    |
| `l`  | signed long        | 4                    |
| `L`  | unsigned long      | 4                    |
| `q`  | signed long long   | 8                    |
| `Q`  | unsigned long long | 8                    |
| `f`  | float              | 4                    |
| `d`  | double float       | 8                    |

## 初始化

`array` 需要两个参数，第一个参数是数据类型，第二个是要传入的数据。

```python
import array
import binascii

s = b'This is the array.'
a = array.array('b', s)

print('As byte string:', s)
print('As array      :', a)
print('As hex        :', binascii.hexlify(a))

# output
# As byte string: b'This is the array.'
# As array      : array('b', [84, 104, 105, 115, 32, 105, 115, 32,
#  116, 104, 101, 32, 97, 114, 114, 97, 121, 46])
# As hex        : b'54686973206973207468652061727261792e'
```

## 操作 Arrays

可以采用像操作 Python 其他序列同样的方式来操作 `array`，支持的操作包括切片，迭代和添加元素到最后等。

```python
import array
import pprint

a = array.array('i', range(3))
print('Initial :', a)

a.extend(range(3))
print('Extended:', a)

print('Slice   :', a[2:5])

print('Iterator:')
print(list(enumerate(a)))

# output
# Initial : array('i', [0, 1, 2])
# Extended: array('i', [0, 1, 2, 0, 1, 2])
# Slice   : array('i', [2, 0, 1])
# Iterator:
# [(0, 0), (1, 1), (2, 2), (3, 0), (4, 1), (5, 2)]
```

## Arrays 和 Files

可以将数组中内容写入文件，也可以将文件中内容读取出来存到数组。

```python
import array
import binascii
import tempfile

a = array.array('i', range(5))
print('A1:', a)

# Write the array of numbers to a temporary file
output = tempfile.NamedTemporaryFile()
a.tofile(output.file)  # must pass an *actual* file
output.flush()

# Read the raw data
with open(output.name, 'rb') as input:
    raw_data = input.read()
    print('Raw Contents:', binascii.hexlify(raw_data))

    # Read the data into an array
    input.seek(0)
    a2 = array.array('i')
    a2.fromfile(input, len(a))
    print('A2:', a2)
    
# output
# A1: array('i', [0, 1, 2, 3, 4])
# Raw Contents: b'0000000001000000020000000300000004000000'
# A2: array('i', [0, 1, 2, 3, 4])
```

此示例说明直接从二进制文件读取数据“raw”，而不是将其读入新数组并将字节转换为适当的类型。

`tofile()`用 `tobytes()`格式化数据，然后 `fromfile()` 用`frombytes()`将其转换回数组实例。

```python
import array
import binascii

a = array.array('i', range(5))
print('A1:', a)

as_bytes = a.tobytes()
print('Bytes:', binascii.hexlify(as_bytes))

a2 = array.array('i')
a2.frombytes(as_bytes)
print('A2:', a2)

# output
# A1: array('i', [0, 1, 2, 3, 4])
# Bytes: b'0000000001000000020000000300000004000000'
# A2: array('i', [0, 1, 2, 3, 4])
```

`tobytes()` 和 `frombytes()` 都操作的字节字符串，而不是Unicode字符串。

相关文档：

https://pymotw.com/3/array/index.html