# 每周一个 Python 模块 | operator

operator 模块是 Python 中内置的操作符函数接口，它定义了算术，比较和与标准对象 API 相对应的其他操作的内置函数。

operator 模块是用 C 实现的，所以执行速度比 Python 代码快。

## 逻辑运算

```python
from operator import *

a = -1
b = 5

print('a =', a)
print('b =', b)
print()

print('not_(a)     :', not_(a))       # False
print('truth(a)    :', truth(a))	  # True		
print('is_(a, b)   :', is_(a, b))	  # False
print('is_not(a, b):', is_not(a, b))  # True
```

`not_()`包括尾随下划线，因为`not` 是 Python 的关键字。 `truth()`作为判断表达式用在`if`语句中，或者将一个表达式转换成`bool`。 `is_()`和`is`关键字的用法一样，`is_not()`用法相同，只不过返回相反的答案。

## 比较运算符

```python
from operator import *

a = 1
b = 5.0

print('a =', a)
print('b =', b)
for func in (lt, le, eq, ne, ge, gt):
    print('{}(a, b): {}'.format(func.__name__, func(a, b)))
    
# a = 1
# b = 5.0
# lt(a, b): True
# le(a, b): True
# eq(a, b): False
# ne(a, b): True
# ge(a, b): False
# gt(a, b): False    
```

功能是等同于使用表达式语法`<`， `<=`，`==`，`>=`，和`>`。

## 算术运算符

```python
from operator import *

a = -1
b = 5.0
c = 2
d = 6

print('\nPositive/Negative:')
print('abs(a):', abs(a))	# abs(a): 1
print('neg(a):', neg(a))	# neg(a): 1
print('neg(b):', neg(b))	# neg(b): -5.0
print('pos(a):', pos(a))	# pos(a): -1
print('pos(b):', pos(b))	# pos(b): 5.0

print('\nArithmetic:')
print('add(a, b)     :', add(a, b))			# add(a, b)     : 4.0
print('floordiv(a, b):', floordiv(a, b))	# floordiv(a, b): -1.0
print('floordiv(d, c):', floordiv(d, c))	# floordiv(d, c): 3
print('mod(a, b)     :', mod(a, b))			# mod(a, b)     : 4.0
print('mul(a, b)     :', mul(a, b))			# mul(a, b)     : -5.0
print('pow(c, d)     :', pow(c, d))			# pow(c, d)     : 64
print('sub(b, a)     :', sub(b, a))			# sub(b, a)     : 6.0
print('truediv(a, b) :', truediv(a, b))		# truediv(a, b) : -0.2
print('truediv(d, c) :', truediv(d, c))		# truediv(d, c) : 3.0

print('\nBitwise:')
print('and_(c, d)  :', and_(c, d))		# and_(c, d)  : 2		
print('invert(c)   :', invert(c))		# invert(c)   : -3
print('lshift(c, d):', lshift(c, d))	# lshift(c, d): 128
print('or_(c, d)   :', or_(c, d))		# or_(c, d)   : 6
print('rshift(d, c):', rshift(d, c))	# rshift(d, c): 1
print('xor(c, d)   :', xor(c, d))		# xor(c, d)   : 4
```

## 序列运算符

使用序列的运算符可以分为四组：构建序列，搜索项目，访问内容以及从序列中删除项目。

```python
from operator import *

a = [1, 2, 3]
b = ['a', 'b', 'c']

print('\nConstructive:')
print('  concat(a, b):', concat(a, b))		# concat(a, b): [1, 2, 3, 'a', 'b', 'c']

print('\nSearching:')
print('  contains(a, 1)  :', contains(a, 1))	# contains(a, 1)  : True
print('  contains(b, "d"):', contains(b, "d"))	# contains(b, "d"): False
print('  countOf(a, 1)   :', countOf(a, 1))		# countOf(a, 1)   : 1
print('  countOf(b, "d") :', countOf(b, "d"))	# countOf(b, "d") : 0
print('  indexOf(a, 5)   :', indexOf(a, 1))		# indexOf(a, 5)   : 0

print('\nAccess Items:')
print(getitem(b, 1))	# b
print(getitem(b, slice(1, 3))) # ['b', 'c']
print(setitem(b, 1, "d")	# None
print(b)	# ['a', 'd', 'c']
print(setitem(a, slice(1, 3), [4, 5])）	# None
print(a)	# [1, 4, 5]

print('\nDestructive:')
print(delitem(b, 1)）	# None
print(b)	# ['a', 'c']
print(delitem(a, slice(1, 3))	# None
print(a)	# [1]
```

其中一些操作（例如`setitem()`和`delitem()`）修改了序列并且不返回值。

## 原地操作符

除了标准运算符之外，许多类型的对象还支持通过特殊运算符进行“原地”修改 ，`+=`同样具有就地修改的功能：

```python
from operator import *

a = -1
b = 5.0
c = [1, 2, 3]
d = ['a', 'b', 'c']

a = iadd(a, b)
print('a = iadd(a, b) =>', a)	# a = iadd(a, b) => 4.0

c = iconcat(c, d)
print('c = iconcat(c, d) =>', c)	# c = iconcat(c, d) => [1, 2, 3, 'a', 'b', 'c']
```

## 属性和元素的获取方法

operator 模块最特别的特性之一就是获取方法的概念，获取方法是运行时构造的一些可回调对象，用来获取对象的属性或序列的内容，获取方法在处理迭代器或生成器序列的时候特别有用，它们引入的开销会大大降低 lambda 或 Python 函数的开销。

```python
from operator import *


class MyObj:
    """example class for attrgetter"""

    def __init__(self, arg):
        super().__init__()
        self.arg = arg

    def __repr__(self):
        return 'MyObj({})'.format(self.arg)


l = [MyObj(i) for i in range(5)]
print(l)	# [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]

# Extract the 'arg' value from each object
g = attrgetter('arg')
vals = [g(i) for i in l]
print('arg values:', vals)	# arg values: [0, 1, 2, 3, 4]

# Sort using arg
l.reverse()
print(l)	# [MyObj(4), MyObj(3), MyObj(2), MyObj(1), MyObj(0)]
print(sorted(l, key=g))	# [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]
```

## 结合操作符和定制类

`operator`模块中的函数通过标准 Python 接口进行操作，因此它可以使用用户定义的类以及内置类型。

```python
from operator import *


class MyObj:
    """Example for operator overloading"""

    def __init__(self, val):
        super(MyObj, self).__init__()
        self.val = val

    def __str__(self):
        return 'MyObj({})'.format(self.val)

    def __lt__(self, other):
        """compare for less-than"""
        print('Testing {} < {}'.format(self, other))
        return self.val < other.val

    def __add__(self, other):
        """add values"""
        print('Adding {} + {}'.format(self, other))
        return MyObj(self.val + other.val)


a = MyObj(1)
b = MyObj(2)

print('Comparison:')
print(lt(a, b))		
# Comparison:
# Testing MyObj(1) < MyObj(2)
# True

print('\nArithmetic:')
print(add(a, b))	
# Arithmetic:
# Adding MyObj(1) + MyObj(2)
# MyObj(3)
```

## 类型检查

operator 模块还包含一些函数用来测试映射、数字和序列类型的 API 兼容性。

```python
from operator import *

class NoType(object):
    pass

class MultiType(object):
    def __len__(self):
        return 0

    def __getitem__(self, name):
        return "mapping"

    def __int__(self):
        return 0

o = NoType()
t = MultiType()

for func in [isMappingType, isNumberType, isSequenceType]:
    print "%s(o):" % func.__name__, func(o)
    print "%s(t):" % func.__name__, func(t)

# isMappingType(o): False
# isMappingType(t): True
# isNumberType(o): False
# isNumberType(t): True
# isSequenceType(o): False
# isSequenceType(t): True    
```

## 获取对象方法

使用 methodcaller 可以获取对象的方法。

```python
from operator import methodcaller

class Student(object):
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

stu = Student("Jim")
func = methodcaller('getName')
print func(stu)   # 输出Jim
```

还可以给方法传递参数：

```python
f = methodcaller('name', 'foo', bar=1)
f(b)    # return   b.name('foo', bar=1)
```

methodcaller方法等价于下面这个函数：

```python
def methodcaller(name, *args,  **kwargs):
      def caller(obj):
            return getattr(obj, name)(*args, **kwargs)
      return caller
```

相关文档：

https://pymotw.com/3/operator/index.html

https://www.jianshu.com/p/1a3a2ae01c06

https://blog.csdn.net/lilong117194/article/details/76950993