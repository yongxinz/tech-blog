# 每周一个 Python 模块 | datetime

`datetime` 包含用于处理日期和时间的函数和类。

## Time

时间值用`time`类表示。 `time`实例有属性`hour`， `minute`，`second`，和`microsecond`，还可以包括时区信息。

```python
import datetime

t = datetime.time(1, 2, 3)
print(t)	# 01:02:03
print('hour       :', t.hour)	# hour       : 1
print('minute     :', t.minute)	# minute     : 2
print('second     :', t.second)	# second     : 3
print('microsecond:', t.microsecond)	# microsecond: 0
print('tzinfo     :', t.tzinfo)	# tzinfo     : None
```

`time`实例只保留时间值，而不是与时间相关联的日期。

```python
import datetime

print('Earliest  :', datetime.time.min)	# Earliest  : 00:00:00
print('Latest    :', datetime.time.max)	# Latest    : 23:59:59.999999
print('Resolution:', datetime.time.resolution)	# Resolution: 0:00:00.000001
```

`min`和`max`类属性反映了时间在一天的有效范围。

时间的分辨率限制在整个微秒。(也可以说是一个微秒，详见上面代码 Resolution)

```python
import datetime

for m in [1, 0, 0.1, 0.6]:
    try:
        print('{:02.1f} :'.format(m),
              datetime.time(0, 0, 0, microsecond=m))
    except TypeError as err:
        print('ERROR:', err)
  
# 输出
# 1.0 : 00:00:00.000001
# 0.0 : 00:00:00
# ERROR: integer argument expected, got float
# ERROR: integer argument expected, got float        
```

微秒的浮点值会导致`TypeError`。

## Date

日期值用`date` 类表示。实例具有属性`year`，`month`和 `day`。使用`today()`类方法可以轻松创建当前日期。

```python
import datetime

today = datetime.date.today()
print(today)	# 2018-03-18
print('ctime  :', today.ctime())	# ctime  : Sun Mar 18 00:00:00 2018
tt = today.timetuple()
print('tuple  : tm_year  =', tt.tm_year)	# tuple  : tm_year  = 2018
print('         tm_mon   =', tt.tm_mon)		# tm_mon   = 3
print('         tm_mday  =', tt.tm_mday)	# tm_mday  = 18
print('         tm_hour  =', tt.tm_hour)	# tm_hour  = 0
print('         tm_min   =', tt.tm_min)		# tm_min   = 0
print('         tm_sec   =', tt.tm_sec)		# tm_sec   = 0
print('         tm_wday  =', tt.tm_wday)	# tm_wday  = 6
print('         tm_yday  =', tt.tm_yday)	# tm_yday  = 77
print('         tm_isdst =', tt.tm_isdst)	# tm_isdst = -1
print('ordinal:', today.toordinal())	# ordinal: 736771
print('Year   :', today.year)	# Year   : 2018
print('Mon    :', today.month)	# Mon    : 3
print('Day    :', today.day)	# Day    : 18
```

还有一些类方法，用于从 POSIX 时间戳或整数表示公历中的日期值创建实例，其中 1 年 1 月 1 日为 1，每个后续日期将值递增 1。

```python
import datetime
import time

o = 733114
print(o)	# o               : 733114
print(datetime.date.fromordinal(o))	# fromordinal(o)  : 2008-03-13

t = time.time()
print(t)	# t               : 1521404434.262209
print(datetime.date.fromtimestamp(t))	# fromtimestamp(t): 2018-03-18
```

此示例说明了`fromordinal()`和 `fromtimestamp()` 使用的不同值类型。

与`time`一样，可以使用`min`和`max`属性确定支持的日期值范围。

```python
import datetime

print('Earliest  :', datetime.date.min)	# Earliest  : 0001-01-01
print('Latest    :', datetime.date.max)	# Latest    : 9999-12-31
print('Resolution:', datetime.date.resolution)	# Resolution: 1 day, 0:00:00
```

日期的精确度是整天。

创建新`date`实例的另一种方法是使用`replace()`。

```python
import datetime

d1 = datetime.date(2008, 3, 29)
print('d1:', d1.ctime())	# d1: Sat Mar 29 00:00:00 2008

d2 = d1.replace(year=2009)
print('d2:', d2.ctime())	# d2: Sun Mar 29 00:00:00 2009
```

此示例更改年份，日期和月份保持不变。

## timedeltas

可以使用两个`datetime`对象的做基本的计算，或通过将 `datetime`与 `timedelta` 组合来计算未来和过去的日期。减去日期会产生一个`timedelta`，也可以从日期中添加或减去`timedelta`以产生另一个日期。`timedelta`的内部值以天，秒和微秒存储。

```python
import datetime

print('microseconds:', datetime.timedelta(microseconds=1))	# 0:00:00.000001
print('milliseconds:', datetime.timedelta(milliseconds=1))	# 0:00:00.001000
print('seconds     :', datetime.timedelta(seconds=1))	# 0:00:01
print('minutes     :', datetime.timedelta(minutes=1))	# 0:01:00
print('hours       :', datetime.timedelta(hours=1))	# 1:00:00
print('days        :', datetime.timedelta(days=1))	# 1 day, 0:00:00
print('weeks       :', datetime.timedelta(weeks=1))	# 7 days, 0:00:00
```

传递给构造函数的中间级别值将转换为天，秒和微秒。

`timedelta`的完整持续时间可以使用`total_seconds()`以秒数来检索。

```python
import datetime

for delta in [datetime.timedelta(microseconds=1),
              datetime.timedelta(milliseconds=1),
              datetime.timedelta(seconds=1),
              datetime.timedelta(minutes=1),
              datetime.timedelta(hours=1),
              datetime.timedelta(days=1),
              datetime.timedelta(weeks=1),
              ]:
    print('{:15} = {:8} seconds'.format(
        str(delta), delta.total_seconds())
    )

# 输出    
# 0:00:00.000001  =    1e-06 seconds
# 0:00:00.001000  =    0.001 seconds
# 0:00:01         =      1.0 seconds
# 0:01:00         =     60.0 seconds
# 1:00:00         =   3600.0 seconds
# 1 day, 0:00:00  =  86400.0 seconds
# 7 days, 0:00:00 = 604800.0 seconds    
```

返回值是一个浮点数，以适应次秒持续时间。

## 日期计算

日期计算使用标准算术运算符。

```python
import datetime

today = datetime.date.today()
print('Today    :', today)	# Today    : 2018-03-18

one_day = datetime.timedelta(days=1)
print('One day  :', one_day)	# One day  : 1 day, 0:00:00

yesterday = today - one_day
print('Yesterday:', yesterday)	# Yesterday: 2018-03-17

tomorrow = today + one_day
print('Tomorrow :', tomorrow)	# Tomorrow : 2018-03-19

print('tomorrow - yesterday:', tomorrow - yesterday)	# 2 days, 0:00:00
print('yesterday - tomorrow:', yesterday - tomorrow)	# -2 days, 0:00:00
```

示例说明了使用`timedelta` 对象计算新日期，可以减去日期实例以生成 timedeltas（包括负 delta 值）。

`timedelta`对象还支持与整数，浮点数和其他`timedelta`对象进行算术运算。

```python
import datetime

one_day = datetime.timedelta(days=1)
print('1 day    :', one_day)	# 1 day    : 1 day, 0:00:00
print('5 days   :', one_day * 5)	# 5 days   : 5 days, 0:00:00
print('1.5 days :', one_day * 1.5)	# 1.5 days : 1 day, 12:00:00
print('1/4 day  :', one_day / 4)	# 1/4 day  : 6:00:00

# assume an hour for lunch
work_day = datetime.timedelta(hours=7)
meeting_length = datetime.timedelta(hours=1)
print('meetings per day :', work_day / meeting_length)	# meetings per day : 7.0
```

在此示例中，计算一天的几个倍数，结果`timedelta`保持天数或小时数。最后一个示例演示了如何通过组合两个`timedelta`对象来计算值。在这种情况下，结果是浮点数。

## 日期和时间比较

可以使用标准比较运算符比较日期和时间值，以确定哪个更早或更晚。

```python
import datetime
import time

print('Times:')	# Times:
t1 = datetime.time(12, 55, 0)
print('  t1:', t1)	# t1: 12:55:00
t2 = datetime.time(13, 5, 0)
print('  t2:', t2)	# t2: 13:05:00
print('  t1 < t2:', t1 < t2)	# t1 < t2: True

print('Dates:')	# Dates:
d1 = datetime.date.today()
print('  d1:', d1)	# d1: 2018-03-18
d2 = datetime.date.today() + datetime.timedelta(days=1)
print('  d2:', d2)	# d2: 2018-03-19
print('  d1 > d2:', d1 > d2)	# d1 > d2: False
```

支持所有比较运算符。

## 组合日期和时间

使用`datetime`类来保存由日期和时间组件组成的值。与`date`一样，有几个简单的类方法可以创建`datetime`实例。

```python
import datetime

print('Now    :', datetime.datetime.now())
print('Today  :', datetime.datetime.today())
print('UTC Now:', datetime.datetime.utcnow())
print()

FIELDS = [
    'year', 'month', 'day',
    'hour', 'minute', 'second',
    'microsecond',
]

d = datetime.datetime.now()
for attr in FIELDS:
    print('{:15}: {}'.format(attr, getattr(d, attr)))
    
# 输出
# Now    : 2018-03-18 16:20:34.811583
# Today  : 2018-03-18 16:20:34.811616
# UTC Now: 2018-03-18 20:20:34.811627

# year           : 2018
# month          : 3
# day            : 18
# hour           : 16
# minute         : 20
# second         : 34
# microsecond    : 811817
```

`datetime`实例具有`date`和`time`对象的所有属性。

与`date`一样，`datetime`为创建新实例提供了方便的类方法。它还包括 `fromordinal()`和`fromtimestamp()`。

```python
import datetime

t = datetime.time(1, 2, 3)
print('t :', t)		# t : 01:02:03

d = datetime.date.today()
print('d :', d)		# d : 2018-03-18

dt = datetime.datetime.combine(d, t)
print('dt:', dt)	# dt: 2018-03-18 01:02:03
```

`combine()`从一个 `date`和一个`time`实例创建`datetime`实例。

## 格式化和解析

datetime对象的默认字符串表示形式使用ISO-8601格式（`YYYY-MM-DDTHH:MM:SS.mmmmmm`）。可以使用生成替代格式`strftime()`。

```python
import datetime

format = "%a %b %d %H:%M:%S %Y"

today = datetime.datetime.today()
print('ISO     :', today)	# ISO     : 2018-03-18 16:20:34.941204

s = today.strftime(format)
print('strftime:', s)	# strftime: Sun Mar 18 16:20:34 2018

d = datetime.datetime.strptime(s, format)
print('strptime:', d.strftime(format))	# strptime: Sun Mar 18 16:20:34 2018
```

使用`datetime.strptime()`于格式化字符串转换为 `datetime`实例。

Python的[字符串格式化迷你语言](https://docs.python.org/3.5/library/string.html#formatspec)可以使用相同的格式代码，方法是`:`在格式字符串的字段规范中放置它们。

```python
import datetime

today = datetime.datetime.today()
print('ISO     :', today)	# ISO     : 2018-03-18 16:20:35.006116
print('format(): {:%a %b %d %H:%M:%S %Y}'.format(today))	# format(): Sun Mar 18 16:20:35 2018
```

每个日期时间格式代码仍必须以前缀为前缀`%`，后续冒号将作为文字字符处理，以包含在输出中。

下表显示了美国/东部时区2016年1月13日下午5:00的所有格式代码。

| 符号 | 含义                                  | 例                           |
| ---- | ------------------------------------- | ---------------------------- |
| `%a` | 缩写的工作日名称                      | `'Wed'`                      |
| `%A` | 完整的工作日名称                      | `'Wednesday'`                |
| `%w` | 工作日编号 - 0（星期日）至6（星期六） | `'3'`                        |
| `%d` | 每月的一天（零填充）                  | `'13'`                       |
| `%b` | 缩写的月份名称                        | `'Jan'`                      |
| `%B` | 全月名称                              | `'January'`                  |
| `%m` | 一年中的一个月                        | `'01'`                       |
| `%y` | 没有世纪的一年                        | `'16'`                       |
| `%Y` | 与世纪的一年                          | `'2016'`                     |
| `%H` | 24小时制的小时                        | `'17'`                       |
| `%I` | 12小时制的小时                        | `'05'`                       |
| `%p` | 上午下午                              | `'PM'`                       |
| `%M` | 分钟                                  | `'00'`                       |
| `%S` | 秒                                    | `'00'`                       |
| `%f` | 微秒                                  | `'000000'`                   |
| `%z` | 时区感知对象的UTC偏移量               | `'-0500'`                    |
| `%Z` | 时区名称                              | `'EST'`                      |
| `%j` | 一年中的某一天                        | `'013'`                      |
| `%W` | 一年中的一周                          | `'02'`                       |
| `%c` | 当前区域设置的日期和时间表示形式      | `'Wed Jan 13 17:00:00 2016'` |
| `%x` | 当前区域设置的日期表示形式            | `'01/13/16'`                 |
| `%X` | 当前区域设置的时间表示                | `'17:00:00'`                 |
| `%%` | 文字`%`字符                           | `'%'`                        |

## 时区

在其中`datetime`，时区由子类表示 `tzinfo`。由于`tzinfo`是一个抽象基类，应用程序需要定义一个子类并为一些方法提供适当的实现以使其有用。

`datetime`确实在类`timezone`中使用了一个有点天真的实现，它使用UTC的固定偏移量，并且不支持一年中不同日期的不同偏移值，例如夏令时适用的地方，或者UTC的偏移量随时间变化的情况。

```python
import datetime

min6 = datetime.timezone(datetime.timedelta(hours=-6))
plus6 = datetime.timezone(datetime.timedelta(hours=6))
d = datetime.datetime.now(min6)

print(min6, ':', d)	
print(datetime.timezone.utc, ':',
      d.astimezone(datetime.timezone.utc))
print(plus6, ':', d.astimezone(plus6))

# convert to the current system timezone
d_system = d.astimezone()
print(d_system.tzinfo, '      :', d_system)

# UTC-06:00 : 2018-03-18 14:20:35.123594-06:00
# UTC : 2018-03-18 20:20:35.123594+00:00
# UTC+06:00 : 2018-03-19 02:20:35.123594+06:00
# EDT       : 2018-03-18 16:20:35.123594-04:00
```

要将日期时间值从一个时区转换为另一个时区，请使用 `astimezone()`。在上面的示例中，显示了UTC两侧6小时的两个独立时区，并且`utc`实例from `datetime.timezone`也用于参考。最终输出行显示系统时区中的值，通过`astimezone()`不带参数调用获取 。



相关文档：

https://pymotw.com/3/datetime/index.html

https://zhuanlan.zhihu.com/p/28209870