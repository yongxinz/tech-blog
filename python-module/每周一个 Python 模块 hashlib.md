# 每周一个 Python 模块 | hashlib

`hashlib` 模块定义了用于访问不同加密散列算法的 API。要使用特定的哈希算法，需要先用适当的构造函数或`new()`创建哈希对象。然后，无论使用何种算法，对象都使用相同的 API。

## 散列算法

由于`hashlib` 受 OpenSSL “支持”，因此该库提供的所有算法都可用，包括：

> - MD5
> - SHA1
> - SHA224
> - SHA256
> - SHA384
> - SHA512

有些算法可用于所有平台，有些算法依赖于底层库。对于每个列表，分别查看 `algorithms_guaranteed` 和`algorithms_available` 函数。

```python
import hashlib


print('Guaranteed:\n{}\n'.format(', '.join(sorted(hashlib.algorithms_guaranteed))))
print('Available:\n{}'.format(', '.join(sorted(hashlib.algorithms_available))))

# output
# Guaranteed:
# blake2b, blake2s, md5, sha1, sha224, sha256, sha384, sha3_224,
# sha3_256, sha3_384, sha3_512, sha512, shake_128, shake_256
# 
# Available:
# BLAKE2b512, BLAKE2s256, MD4, MD5, MD5 - SHA1, RIPEMD160, SHA1,
# SHA224, SHA256, SHA384, SHA512, blake2b, blake2b512, blake2s,
# blake2s256, md4, md5, md5 - sha1, ripemd160, sha1, sha224, sha256,
# sha384, sha3_224, sha3_256, sha3_384, sha3_512, sha512,
# shake_128, shake_256, whirlpool
```

## 样本数据

本节中的所有示例都使用相同的示例数据：

```python
# hashlib_data.py 

import hashlib

lorem = '''Lorem ipsum dolor sit amet, consectetur adipisicing
elit, sed do eiusmod tempor incididunt ut labore et dolore magna
aliqua. Ut enim ad minim veniam, quis nostrud exercitation
ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis
aute irure dolor in reprehenderit in voluptate velit esse cillum
dolore eu fugiat nulla pariatur. Excepteur sint occaecat
cupidatat non proident, sunt in culpa qui officia deserunt
mollit anim id est laborum.'''
```

## MD5示例

要计算数据块（此处为转换为字节字符串的 unicode 字符串）的 MD5 哈希或摘要，首先创建哈希对象，然后添加数据并调用 `digest()` 或 `hexdigest()`。

```python
import hashlib

from hashlib_data import lorem

h = hashlib.md5()
h.update(lorem.encode('utf-8'))
print(h.hexdigest())	# 3f2fd2c9e25d60fb0fa5d593b802b7a8
```

此例使用 `hexdigest()` 方法而不是 `digest()`，因为输出已格式化，因此可以清晰地打印。如果二进制摘要值可以接受，请使用`digest()`。

## SHA1示例

SHA1 摘要以相同的方式计算。

```python
import hashlib

from hashlib_data import lorem

h = hashlib.sha1()
h.update(lorem.encode('utf-8'))
print(h.hexdigest())	# ea360b288b3dd178fe2625f55b2959bf1dba6eef
```

摘要值在此示例中是不同的，因为算法从 MD5 更改为 SHA1。

## 按名称创建哈希

有时，在字符串中按名称引用算法比通过直接使用构造函数更方便。例如，将哈希类型存储在配置文件中。在这种情况下，用 `new()` 创建哈希对象。

```python
# hashlib_new.py 

import argparse
import hashlib
import sys

from hashlib_data import lorem


parser = argparse.ArgumentParser('hashlib demo')
parser.add_argument(
    'hash_name',
    choices=hashlib.algorithms_available,
    help='the name of the hash algorithm to use',
)
parser.add_argument(
    'data',
    nargs='?',
    default=lorem,
    help='the input data to hash, defaults to lorem ipsum',
)
args = parser.parse_args()

h = hashlib.new(args.hash_name)
h.update(args.data.encode('utf-8'))
print(h.hexdigest())

# output
# $ python3 hashlib_new.py sha1
# ea360b288b3dd178fe2625f55b2959bf1dba6eef
# 
# $ python3 hashlib_new.py sha256
# 
# 3c887cc71c67949df29568119cc646f46b9cd2c2b39d456065646bc2fc09ffd8
# 
# $ python3 hashlib_new.py sha512
# 
# a7e53384eb9bb4251a19571450465d51809e0b7046101b87c4faef96b9bc904cf7f90
# 035f444952dfd9f6084eeee2457433f3ade614712f42f80960b2fca43ff
# 
# $ python3 hashlib_new.py md5
# 
# 3f2fd2c9e25d60fb0fa5d593b802b7a8
```

## 增量更新

`update()` 可以重复调用哈希计算器的方法。每次，摘要都会根据输入的附加文本进行更新。逐步更新比将整个文件读入内存更有效，并产生相同的结果。

```python
import hashlib

from hashlib_data import lorem

h = hashlib.md5()
h.update(lorem.encode('utf-8'))
all_at_once = h.hexdigest()


def chunkize(size, text):
    "Return parts of the text in size-based increments."
    start = 0
    while start < len(text):
        chunk = text[start:start + size]
        yield chunk
        start += size
    return


h = hashlib.md5()
for chunk in chunkize(64, lorem.encode('utf-8')):
    h.update(chunk)
line_by_line = h.hexdigest()

print('All at once :', all_at_once)	# All at once : 3f2fd2c9e25d60fb0fa5d593b802b7a8
print('Line by line:', line_by_line)  # Line by line: 3f2fd2c9e25d60fb0fa5d593b802b7a8
print('Same        :', (all_at_once == line_by_line))	# Same        : True
```



相关文档：

https://pymotw.com/3/hashlib/index.html