# 每周一个 Python 模块 | struct

`struct` 模块包括用于在字节串和 Python 数据类型（如数字和字符串）之间进行转换的函数。

## 包装和拆包

Structs 支持将数据打包成字符串，并使用格式说明符从字符串中解压缩数据，格式说明符由表示数据类型的字符、可选计数和字节顺序指示符组成。有关支持的格式说明符的完整列表，请参阅标准库文档。

在此示例中，说明符调用整数或长整数值，双字节字符串和浮点数。格式说明符中的空格用作分隔类型指示符，并在编译格式时忽略。

```python
import struct
import binascii

values = (1, 'ab'.encode('utf-8'), 2.7)
s = struct.Struct('I 2s f')
packed_data = s.pack(*values)

print('Original values:', values)
print('Format string  :', s.format)
print('Uses           :', s.size, 'bytes')
print('Packed Value   :', binascii.hexlify(packed_data))

# output
# Original values: (1, b'ab', 2.7)
# Format string  : b'I 2s f'
# Uses           : 12 bytes
# Packed Value   : b'0100000061620000cdcc2c40'
```

该示例使用函数 `binascii.hexlify()` 将打包值转换为十六进制字节序列以进行打印。

用`unpack()`从打包中提取数据。

```python
import struct
import binascii

packed_data = binascii.unhexlify(b'0100000061620000cdcc2c40')

s = struct.Struct('I 2s f')
unpacked_data = s.unpack(packed_data)
print('Unpacked Values:', unpacked_data)

# output
# Unpacked Values: (1, b'ab', 2.700000047683716)
```

将打包值传递给 `unpack()`，返回基本相同的值（注意浮点值的差异）。

## 字节顺序

默认情况下，使用本机 C 库的字节序对值进行编码 。通过在格式字符串中提供显式字节序指令，可以轻松覆盖该选项。

```python
import struct
import binascii

values = (1, 'ab'.encode('utf-8'), 2.7)
print('Original values:', values)

endianness = [
    ('@', 'native, native'),
    ('=', 'native, standard'),
    ('<', 'little-endian'),
    ('>', 'big-endian'),
    ('!', 'network'),
]

for code, name in endianness:
    s = struct.Struct(code + ' I 2s f')
    packed_data = s.pack(*values)
    print()
    print('Format string  :', s.format, 'for', name)
    print('Uses           :', s.size, 'bytes')
    print('Packed Value   :', binascii.hexlify(packed_data))
    print('Unpacked Value :', s.unpack(packed_data))
    
# output
# Original values: (1, b'ab', 2.7)
# 
# Format string  : b'@ I 2s f' for native, native
# Uses           : 12 bytes
# Packed Value   : b'0100000061620000cdcc2c40'
# Unpacked Value : (1, b'ab', 2.700000047683716)
# 
# Format string  : b'= I 2s f' for native, standard
# Uses           : 10 bytes
# Packed Value   : b'010000006162cdcc2c40'
# Unpacked Value : (1, b'ab', 2.700000047683716)
# 
# Format string  : b'< I 2s f' for little-endian
# Uses           : 10 bytes
# Packed Value   : b'010000006162cdcc2c40'
# Unpacked Value : (1, b'ab', 2.700000047683716)
# 
# Format string  : b'> I 2s f' for big-endian
# Uses           : 10 bytes
# Packed Value   : b'000000016162402ccccd'
# Unpacked Value : (1, b'ab', 2.700000047683716)
# 
# Format string  : b'! I 2s f' for network
# Uses           : 10 bytes
# Packed Value   : b'000000016162402ccccd'
# Unpacked Value : (1, b'ab', 2.700000047683716)
```

## 缓冲区

使用二进制打包数据通常用于对性能要求较高的场景或将数据传入和传出扩展模块。通过避免为每个打包结构分配新缓冲区，可以优化这些情况。`pack_into()`和`unpack_from()`方法支持直接写入预先分配的缓冲区。

```python
import array
import binascii
import ctypes
import struct

s = struct.Struct('I 2s f')
values = (1, 'ab'.encode('utf-8'), 2.7)
print('Original:', values)

print()
print('ctypes string buffer')

b = ctypes.create_string_buffer(s.size)
print('Before  :', binascii.hexlify(b.raw))
s.pack_into(b, 0, *values)
print('After   :', binascii.hexlify(b.raw))
print('Unpacked:', s.unpack_from(b, 0))

print()
print('array')

a = array.array('b', b'\0' * s.size)
print('Before  :', binascii.hexlify(a))
s.pack_into(a, 0, *values)
print('After   :', binascii.hexlify(a))
print('Unpacked:', s.unpack_from(a, 0))

# output
# Original: (1, b'ab', 2.7)
# 
# ctypes string buffer
# Before  : b'000000000000000000000000'
# After   : b'0100000061620000cdcc2c40'
# Unpacked: (1, b'ab', 2.700000047683716)
# 
# array
# Before  : b'000000000000000000000000'
# After   : b'0100000061620000cdcc2c40'
# Unpacked: (1, b'ab', 2.700000047683716)
```

`size`属性告诉我们缓冲区需要多大。

相关文档：

https://pymotw.com/3/struct/index.html