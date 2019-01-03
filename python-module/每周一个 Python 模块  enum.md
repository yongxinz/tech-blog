# 每周一个 Python 模块 | enum

枚举类型可以看作是一种标签或是一系列常量的集合，通常用于表示某些特定的有限集合，例如星期、月份、状态等。Python 的原生类型（Built-in types）里并没有专门的枚举类型，但是我们可以通过很多方法来实现它，例如字典、类等：

```python
WEEKDAY = {
    'MON': 1,
    'TUS': 2,
    'WEN': 3,
    'THU': 4,
    'FRI': 5
}
class Color:
    RED   = 0
    GREEN = 1
    BLUE  = 2
```

上面两种方法可以看做是简单的枚举类型的实现，如果只在局部范围内用到这样的枚举变量是没有问题的，但问题在于它们都是可变的（mutable），也就是说可以在其它地方被修改，从而影响其正常使用：

```python
WEEKDAY['MON'] = WEEKDAY['FRI']
print(WEEKDAY) # {'FRI': 5, 'TUS': 2, 'MON': 5, 'WEN': 3, 'THU': 4}
```

通过类定义的枚举甚至可以实例化，变得不伦不类：

```python
c = Color()
print(c.RED)	# 0
Color.RED = 2
print(c.RED)	# 2
```

当然也可以使用不可变类型（immutable），例如元组，但是这样就失去了枚举类型的本意，将标签退化为无意义的变量：

```python
COLOR = ('R', 'G', 'B')
print(COLOR[0], COLOR[1], COLOR[2])	# R G B
```

为了提供更好的解决方案，Python 通过 [PEP 435](https://www.python.org/dev/peps/pep-0435) 在 3.4 版本中添加了 [enum](https://github.com/rainyear/cpython/blob/master/Lib/enum.py) 标准库，3.4 之前的版本也可以通过 `pip install enum` 下载兼容支持的库。`enum` 提供了 `Enum`/`IntEnum`/`unique` 三个工具，用法也非常简单，可以通过继承 `Enum`/`IntEnum` 定义枚举类型，其中 `IntEnum` 限定枚举成员必须为（或可以转化为）整数类型，而 `unique` 方法可以作为修饰器限定枚举成员的值不可重复。

## 创建枚举

通过子类化 enum 类来定义枚举，代码如下：

```python
import enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


print('\nMember name: {}'.format(BugStatus.wont_fix.name))
print('Member value: {}'.format(BugStatus.wont_fix.value))

# output
# Member name: wont_fix
# Member value: 4
```

在解析 Enum 类时，会将每个成员转换成实例，每个实例都有 name 和 value 属性，分别对应成员的名称和值。

## 迭代枚举

直接看代码：

```python
import enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))
    
# output
# new             = 7
# incomplete      = 6
# invalid         = 5
# wont_fix        = 4
# in_progress     = 3
# fix_committed   = 2
# fix_released    = 1
```

成员按照在类中的定义顺序生成。

## 比较枚举

由于枚举成员未被排序，因此它们仅支持通过 `is` 和 `==` 进行比较。

```python
import enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


actual_state = BugStatus.wont_fix
desired_state = BugStatus.fix_released

print('Equality:',
      actual_state == desired_state,
      actual_state == BugStatus.wont_fix)
print('Identity:',
      actual_state is desired_state,
      actual_state is BugStatus.wont_fix)
print('Ordered by value:')
try:
    print('\n'.join('  ' + s.name for s in sorted(BugStatus)))
except TypeError as err:
    print('  Cannot sort: {}'.format(err))
    
# output
# Equality: False True
# Identity: False True
# Ordered by value:
#   Cannot sort: '<' not supported between instances of 'BugStatus' and 'BugStatus'
```

大小比较引发 `TypeError` 异常。

继承 `IntEnum` 类创建的枚举类，成员间支持大小比较，代码如下：

```python
import enum


class BugStatus(enum.IntEnum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


print('Ordered by value:')
print('\n'.join('  ' + s.name for s in sorted(BugStatus)))

# output
# Ordered by value:
#   fix_released
#   fix_committed
#   in_progress
#   wont_fix
#   invalid
#   incomplete
#   new
```

## 唯一枚举值

具有相同值的枚举成员将作为对同一成员对象的别名引用，在迭代过程中，不会被打印出来。

```python
import enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1

    by_design = 4
    closed = 1


for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))

print('\nSame: by_design is wont_fix: ',
      BugStatus.by_design is BugStatus.wont_fix)
print('Same: closed is fix_released: ',
      BugStatus.closed is BugStatus.fix_released)

# output
# new             = 7
# incomplete      = 6
# invalid         = 5
# wont_fix        = 4
# in_progress     = 3
# fix_committed   = 2
# fix_released    = 1
# 
# Same: by_design is wont_fix:  True
# Same: closed is fix_released:  True
```

因为 by_design 和 closed 是其他成员的别名，所以没有被打印。在枚举中，第一个出现的值是有效的。

如果想让每一个成员都有唯一值，可以使用 `@unique` 装饰器。

```python
import enum


@enum.unique
class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1

    # This will trigger an error with unique applied.
    by_design = 4
    closed = 1
    
# output
# Traceback (most recent call last):
#   File "enum_unique_enforce.py", line 11, in <module>
#     class BugStatus(enum.Enum):
#   File ".../lib/python3.6/enum.py", line 834, in unique
#     (enumeration, alias_details))
# ValueError: duplicate values found in <enum 'BugStatus'>:
# by_design -> wont_fix, closed -> fix_released
```

如果成员中有重复值，会有 `ValueError` 的报错。

## 以编程方式创建枚举

在一些情况下，通过编程的方式创建枚举，比直接在类中硬编码更方便。如果采用这种方式，还可以传递成员的 name 和 value 到类的构造函数。

```python
import enum


BugStatus = enum.Enum(
    value='BugStatus',
    names=('fix_released fix_committed in_progress '
           'wont_fix invalid incomplete new'),
)

print('Member: {}'.format(BugStatus.new))

print('\nAll members:')
for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))
    
# output
# Member: BugStatus.new
# 
# All members:
# fix_released    = 1
# fix_committed   = 2
# in_progress     = 3
# wont_fix        = 4
# invalid         = 5
# incomplete      = 6
# new             = 7
```

参数 `value `代表枚举的名称，`names` 表示成员。如果给 name 传递的参数是字符串，那么会对这个字符串从空格和逗号处进行拆分，将拆分后的单个字符串作为成员的名称，然后再对其赋值，从 1 开始，以此类推。

为了更好地控制与成员关联的值， `names`可以使用元组或将名称映射到值的字典替换字符串。什么意思，看下面的代码：

```python
import enum


BugStatus = enum.Enum(
    value='BugStatus',
    names=[
        ('new', 7),
        ('incomplete', 6),
        ('invalid', 5),
        ('wont_fix', 4),
        ('in_progress', 3),
        ('fix_committed', 2),
        ('fix_released', 1),
    ],
)

print('All members:')
for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))
    
# output
# All members:
# new             = 7
# incomplete      = 6
# invalid         = 5
# wont_fix        = 4
# in_progress     = 3
# fix_committed   = 2
# fix_released    = 1
```

在这里例子中，`names` 是一个列表，列表中的元素是元组。

## 非整数成员值

枚举成员值不限于整数。实际上，任何类型的对象都可以作为枚举值。如果值是元组，则成员将作为单独的参数传递给`__init__()`。

```python
import enum


class BugStatus(enum.Enum):

    new = (7, ['incomplete', 'invalid', 'wont_fix', 'in_progress'])
    incomplete = (6, ['new', 'wont_fix'])
    invalid = (5, ['new'])
    wont_fix = (4, ['new'])
    in_progress = (3, ['new', 'fix_committed'])
    fix_committed = (2, ['in_progress', 'fix_released'])
    fix_released = (1, ['new'])

    def __init__(self, num, transitions):
        self.num = num
        self.transitions = transitions

    def can_transition(self, new_state):
        return new_state.name in self.transitions


print('Name:', BugStatus.in_progress)
print('Value:', BugStatus.in_progress.value)
print('Custom attribute:', BugStatus.in_progress.transitions)
print('Using attribute:', BugStatus.in_progress.can_transition(BugStatus.new))

# output
# Name: BugStatus.in_progress
# Value: (3, ['new', 'fix_committed'])
# Custom attribute: ['new', 'fix_committed']
# Using attribute: True
```

在此示例中，每个成员值是一个元组，其中包含数字和列表。

对于更复杂的情况，元组可能就不那么方便了。由于成员值可以是任何类型的对象，因此如果有大量需要键值对数据结构的枚举值场景，字典就派上用场了。

```python
import enum


class BugStatus(enum.Enum):

    new = {
        'num': 7,
        'transitions': [
            'incomplete',
            'invalid',
            'wont_fix',
            'in_progress',
        ],
    }
    incomplete = {
        'num': 6,
        'transitions': ['new', 'wont_fix'],
    }
    invalid = {
        'num': 5,
        'transitions': ['new'],
    }
    wont_fix = {
        'num': 4,
        'transitions': ['new'],
    }
    in_progress = {
        'num': 3,
        'transitions': ['new', 'fix_committed'],
    }
    fix_committed = {
        'num': 2,
        'transitions': ['in_progress', 'fix_released'],
    }
    fix_released = {
        'num': 1,
        'transitions': ['new'],
    }

    def __init__(self, vals):
        self.num = vals['num']
        self.transitions = vals['transitions']

    def can_transition(self, new_state):
        return new_state.name in self.transitions


print('Name:', BugStatus.in_progress)
print('Value:', BugStatus.in_progress.value)
print('Custom attribute:', BugStatus.in_progress.transitions)
print('Using attribute:', BugStatus.in_progress.can_transition(BugStatus.new))

# output
# Name: BugStatus.in_progress
# Value: (3, ['new', 'fix_committed'])
# Custom attribute: ['new', 'fix_committed']
# Using attribute: True
```

这个例子和上面用元组是等价的。

相关文档：

https://pymotw.com/3/enum/index.html

http://python.jobbole.com/84112/