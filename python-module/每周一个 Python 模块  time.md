# 每周一个 Python 模块 | time

几乎所有的正式代码中，我们都需要与时间打交道。在Python中，与时间处理有关的模块包括`time`，`datetime`以及`calendar`，本节主要讲解time模块。

**在 Python 中，用三种方式来表示时间，分别是时间戳、格式化时间字符串和结构化时间**

1. 时间戳（`timestamp`）：也就是 1970 年 1 月 1 日之后的秒，例如 1506388236.216345，可以通过`time.time()`获得。时间戳是一个浮点数，可以进行加减运算，但请注意不要让结果超出取值范围。
2. 格式化的时间字符串（`string_time`）：也就是年月日时分秒这样的我们常见的时间字符串，例如`2017-09-26 09:12:48`，可以通过`time.strftime('%Y-%m-%d')`获得;
3. 结构化时间（`struct_time`）：一个包含了年月日时分秒的多元元组，例如`time.struct_time(tm_year=2017, tm_mon=9, tm_mday=26, tm_hour=9, tm_min=14, tm_sec=50, tm_wday=1, tm_yday=269, tm_isdst=0)`，可以通过`time.localtime()`获得。

由于 Python 的 time 模块实现主要调用 C 库，所以各个平台可能有所不同。time 模块目前只支持到 2038 年前。如果需要处理范围之外的日期，请使用 datetime 模块。

**UTC**（Coordinated Universal Time，世界协调时），亦即格林威治天文时间，世界标准时间。我们中国为东八区，比 UTC 早 8 个小时，也就是 UTC+8。关于 UTC 的缩写，有个故事，你可能已经注意到了，按英文的缩写，应该是 CUT，而不是 UTC。但是世界协调时在法文中的缩写是 TUC，两国互相不让，作为妥协，最后干脆简称 UTC。

**DST**（Daylight Saving Time）即夏令时。

## 结构化时间（`struct_time`）

使用`time.localtime()`等方法可以获得一个结构化时间元组。

```python
>>> time.localtime()
time.struct_time(tm_year=2017, tm_mon=9, tm_mday=26, tm_hour=10, tm_min=6, tm_sec=49, tm_wday=1, tm_yday=269, tm_isdst=0)
```

结构化时间元组共有 9 个元素，按顺序排列如下表：

| 索引 | 属性                      | 取值范围           |
| ---- | ------------------------- | ------------------ |
| 0    | tm_year（年）             | 比如2017           |
| 1    | tm_mon（月）              | 1 - 12             |
| 2    | tm_mday（日）             | 1 - 31             |
| 3    | tm_hour（时）             | 0 - 23             |
| 4    | tm_min（分）              | 0 - 59             |
| 5    | tm_sec（秒）              | 0 - 61             |
| 6    | tm_wday（weekday）        | 0 - 6（0表示周一） |
| 7    | tm_yday（一年中的第几天） | 1 - 366            |
| 8    | tm_isdst（是否是夏令时）  | 默认为-1           |

既然结构化时间是一个元组，那么就可以通过索引进行取值，也可以进行分片，或者通过属性名获取对应的值。

```python
>>>import time
>>> lt = time.localtime()
>>> lt
time.struct_time(tm_year=2017, tm_mon=9, tm_mday=26, tm_hour=9, tm_min=27, tm_sec=29, tm_wday=1, tm_yday=269, tm_isdst=0)
>>> lt[3]
9
>>> lt[2:5]
(26, 9, 27)
>>> lt.tm_wday
1
```

但是要记住，**Python 的 time 类型是不可变类型，所有的时间值都只读，不能改**！！

```python
>>> lt.tm_wday = 2
Traceback (most recent call last):
  File "<pyshell#12>", line 1, in <module>
    lt.tm_wday = 2
AttributeError: readonly attribute
```

## 格式化时间字符串

利用`time.strftime('%Y-%m-%d %H:%M:%S')`等方法可以获得一个格式化时间字符串。

```python
>>> time.strftime('%Y-%m-%d %H:%M:%S')
'2017-09-26 10:04:28'
```

注意其中的空格、短横线和冒号都是美观修饰符号，真正起控制作用的是百分符。对于格式化控制字符串`"%Y-%m-%d %H:%M:%S`，其中每一个字母所代表的意思如下表所示，注意大小写的区别：

| 格式 | 含义                                                         |
| ---- | ------------------------------------------------------------ |
| %a   | 本地星期名称的简写（如星期四为Thu）                          |
| %A   | 本地星期名称的全称（如星期四为Thursday）                     |
| %b   | 本地月份名称的简写（如八月份为agu）                          |
| %B   | 本地月份名称的全称（如八月份为august）                       |
| %c   | 本地相应的日期和时间的字符串表示（如：15/08/27 10:20:06）    |
| %d   | 一个月中的第几天（01 - 31）                                  |
| %f   | 微秒（范围0.999999）                                         |
| %H   | 一天中的第几个小时（24小时制，00 - 23）                      |
| %I   | 第几个小时（12小时制，0 - 11）                               |
| %j   | 一年中的第几天（001 - 366）                                  |
| %m   | 月份（01 - 12）                                              |
| %M   | 分钟数（00 - 59）                                            |
| %p   | 本地am或者pm的标识符                                         |
| %S   | 秒（00 - 61）                                                |
| %U   | 一年中的星期数。（00 - 53星期天是一个星期的开始。）第一个星期天之 前的所有天数都放在第0周。 |
| %w   | 一个星期中的第几天（0 - 6，0是星期天）                       |
| %W   | 和%U基本相同，不同的是%W以星期一为一个星期的开始。           |
| %x   | 本地相应日期字符串（如15/08/01）                             |
| %X   | 本地相应时间字符串（如08:08:10）                             |
| %y   | 去掉世纪的年份（00 - 99）两个数字表示的年份                  |
| %Y   | 完整的年份（4个数字表示年份）                                |
| %z   | 与UTC时间的间隔（如果是本地时间，返回空字符串）              |
| %Z   | 时区的名字（如果是本地时间，返回空字符串）                   |
| %%   | ‘%’字符                                                      |

## time 模块主要方法

### time.sleep(t)

time 模块最常用的方法之一，用来睡眠或者暂停程序 t 秒，t 可以是浮点数或整数。

### time.time()

返回当前系统时间戳。时间戳可以做算术运算。

```python
>>> time.time()
1506391907.020303
```

该方法经常用于计算程序运行时间：

```python
import time

def func():
    time.sleep(1.14)
    pass

t1 = time.time()
func()
t2 = time.time()
print(t2 - t1)
```

### time.gmtime([secs])

将一个时间戳转换为 UTC 时区的结构化时间。可选参数 secs 的默认值为`time.time()`。

```python
>>> time.gmtime()
time.struct_time(tm_year=2017, tm_mon=9, tm_mday=26, tm_hour=2, tm_min=14, tm_sec=17, tm_wday=1, tm_yday=269, tm_isdst=0)

>>> t = time.time() - 10000
>>> time.gmtime(t)
time.struct_time(tm_year=2017, tm_mon=9, tm_mday=25, tm_hour=23, tm_min=31, tm_sec=3, tm_wday=0, tm_yday=268, tm_isdst=0)
```

### time.localtime([secs])

将一个时间戳转换为当前时区的结构化时间。如果 secs 参数未提供，则以当前时间为准，即`time.time()`。

```python
>>> time.localtime()
time.struct_time(tm_year=2017, tm_mon=9, tm_mday=26, tm_hour=10, tm_min=20, tm_sec=42, tm_wday=1, tm_yday=269, tm_isdst=0)

>>> time.localtime(1406391907)
time.struct_time(tm_year=2014, tm_mon=7, tm_mday=27, tm_hour=0, tm_min=25, tm_sec=7, tm_wday=6, tm_yday=208, tm_isdst=0)

>>> time.localtime(time.time() + 10000)
time.struct_time(tm_year=2017, tm_mon=9, tm_mday=26, tm_hour=13, tm_min=7, tm_sec=54, tm_wday=1, tm_yday=269, tm_isdst=0)
```

### time.ctime([secs])

把一个时间戳转化为本地时间的格式化字符串。默认使用`time.time()`作为参数。

```python
>>> time.ctime()
'Tue Sep 26 10:22:31 2017'
>>> time.ctime(time.time())
'Tue Sep 26 10:23:51 2017'
>>> time.ctime(1406391907)
'Sun Jul 27 00:25:07 2014'
>>> time.ctime(time.time() + 10000)
'Tue Sep 26 13:11:55 2017'
```

### time.asctime([t])

把一个结构化时间转换为`Sun Aug 23 14:31:59 2017`这种形式的格式化时间字符串。默认将`time.localtime()`作为参数。

```python
>>> time.asctime()
'Tue Sep 26 10:27:23 2017'

>>> time.asctime(time.time())
Traceback (most recent call last):
  File "<pyshell#13>", line 1, in <module>
    time.asctime(time.time())
TypeError: Tuple or struct_time argument required
    
>>> time.asctime(time.localtime())
'Tue Sep 26 10:27:45 2017'
>>> time.asctime(time.gmtime())
'Tue Sep 26 02:27:57 2017'
```

### time.mktime(t)

将一个结构化时间转化为时间戳。`time.mktime()`执行与`gmtime()`,`localtime()`相反的操作，它接收`struct_time`对象作为参数,返回用秒数表示时间的浮点数。如果输入的值不是一个合法的时间，将触发`OverflowError`或`ValueError`。

```python
>>> time.mktime(1406391907)
Traceback (most recent call last):
  File "<pyshell#16>", line 1, in <module>
    time.mktime(1406391907)
TypeError: Tuple or struct_time argument required
    
>>> time.mktime(time.localtime())
1506393039.0
```

### time.strftime(format [, t])

返回格式化字符串表示的当地时间。把一个`struct_time`（如`time.localtime()`和`time.gmtime()`的返回值）转化为格式化的时间字符串，显示的格式由参数`format`决定。如果未指定 t，默认传入`time.localtime()`。如果元组中任何一个元素越界，就会抛出`ValueError`的异常。

```python
>>> time.strftime("%Y-%m-%d %H:%M:%S")
'2017-09-26 10:34:50'
>>> time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())
'2017-09-26 02:34:53'
```

### time.strptime(string[,format])

将格式化时间字符串转化成结构化时间。该方法是`time.strftime()`方法的逆操作。`time.strptime()`方法根据指定的格式把一个时间字符串解析为时间元组。要注意的是，你提供的字符串要和 format 参数的格式一一对应，如果 string 中日期间使用“-”分隔，format 中也必须使用“-”分隔，时间中使用冒号“:”分隔，后面也必须使用冒号分隔，否则会报格式不匹配的错误。并且值也要在合法的区间范围内，千万不要整出 14 个月来。

```python
>>> import time
>>> stime = "2017-09-26 12:11:30"
>>> st = time.strptime(stime,"%Y-%m-%d %H:%M:%S")
>>> st
time.struct_time(tm_year=2017, tm_mon=9, tm_mday=26, tm_hour=12, tm_min=11, tm_sec=30, tm_wday=1, tm_yday=269, tm_isdst=-1)
>>> for item in st:
    print(item)


2017
9
26
12
11
30
1
269
-1
>>> wrong_time = "2017-14-26 12:11:30"
>>> st  = time.strptime(wrong_time,"%Y-%m-%d %H:%M:%S")
Traceback (most recent call last):
  File "<pyshell#8>", line 1, in <module>
    st  = time.strptime(wrong_time,"%Y-%m-%d %H:%M:%S")
  File "C:\Python36\lib\_strptime.py", line 559, in _strptime_time
    tt = _strptime(data_string, format)[0]
  File "C:\Python36\lib\_strptime.py", line 362, in _strptime
    (data_string, format))
ValueError: time data '2017-14-26 12:11:30' does not match format '%Y-%m-%d %H:%M:%S'
```

### time.clock()

返回执行当前程序的 CPU 时间。用来衡量不同程序的耗时。该方法在不同的系统上含义不同。在 Unix 系统上，它返回的是“进程时间”，用秒表示的浮点数（时间戳）。在 Windows 中，第一次调用，返回的是进程运行的实际时间，而第二次之后的调用是自第一次调用以后到现在的运行时间。

```python
import time

def procedure() :
  time.sleep(3)

time1 = time.clock()
procedure()
print(time.clock() - time1, "seconds process time!") 

# 2.999257758349577 seconds process time!
```

## 时间格式之间的转换

Python 的三种类型时间格式，可以互相进行转换，如下图和下表所示：

![image.png-23.5kB](http://static.zybuluo.com/feixuelove1009/puafhqjgxe3uc2e4jvf0f60h/image.png)

| 从             | 到             | 方法              |
| -------------- | -------------- | ----------------- |
| 时间戳         | UTC结构化时间  | gmtime()          |
| 时间戳         | 本地结构化时间 | localtime()       |
| UTC结构化时间  | 时间戳         | calendar.timegm() |
| 本地结构化时间 | 时间戳         | mktime()          |
| 结构化时间     | 格式化字符串   | strftime()        |
| 格式化字符串   | 结构化时间     | strptime()        |

```python
>>> t = time.time()         # t是一个时间戳

>>> time.gmtime(t - 10000)      # t减去1万秒，然后转换成UTC结构化时间
time.struct_time(tm_year=2017, tm_mon=9, tm_mday=25, tm_hour=22, tm_min=50, tm_sec=36, tm_wday=0, tm_yday=268, tm_isdst=0)

>>> lt = time.localtime(t - 10000)  # t减去1万秒，然后转换成中国本地结构化时间
time.struct_time(tm_year=2017, tm_mon=9, tm_mday=26, tm_hour=6, tm_min=50, tm_sec=36, tm_wday=1, tm_yday=269, tm_isdst=0)

>>> time.mktime(lt)     # 从本地结构化时间转换为时间戳
1506379836.0
>>> st = time.strftime("%Y-%m-%d %H:%M:%S",lt)  # 从本地结构化时间转换为时间字符串
>>> st
'2017-09-26 06:50:36'

>>> lt2 = time.strptime(st, "%Y-%m-%d %H:%M:%S") # 从时间字符串转换为结构化时间
>>> lt2
time.struct_time(tm_year=2017, tm_mon=9, tm_mday=26, tm_hour=6, tm_min=50, tm_sec=36, tm_wday=1, tm_yday=269, tm_isdst=-1)
```

相关文档：

https://pymotw.com/3/time/index.html

http://www.liujiangblog.com/course/python/68