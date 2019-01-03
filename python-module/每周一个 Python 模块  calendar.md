# 每周一个 Python 模块 | calendar

`calendar`模块定义了`Calendar`类，它封装了值的计算，比如计算给定月份或年份中周的日期。此外，`TextCalendar`和 `HTMLCalendar`类可以生成预格式化的输出。

## 格式化示例

`prmonth()`方法是很简单，可以生成一个月的格式化文本输出。

```python
import calendar

c = calendar.TextCalendar(calendar.SUNDAY)
c.prmonth(2017, 7)

# 输出
#      July 2017
# Su Mo Tu We Th Fr Sa
#                    1
#  2  3  4  5  6  7  8
#  9 10 11 12 13 14 15
# 16 17 18 19 20 21 22
# 23 24 25 26 27 28 29
# 30 31
```

根据`TextCalendar`美国惯例，该示例配置为在周日开始周。默认是使用星期一开始一周的欧洲惯例。

可以使用`HTMLCalendar`和`formatmonth()`生成类似 HTML 的表格。呈现的输出看起来与纯文本大致相同，但是用 HTML 标记包装。每个表格单元格都有一个与星期几相对应的类属性，因此 HTML 可以通过 CSS 设置样式。

要以不同于其中一个可用默认值的格式生成输出，请使用`calendar`计算日期并将值组织为周和月范围，然后迭代结果。`Calendar`模块的 `weekheader()`，`monthcalendar()`和 `yeardays2calendar()`方法对此特别有用。

调用`yeardays2calendar()`会生成一系列“月份行”列表。每个列表包括月份作为另一个周列表。这几周是由日期编号（1-31）和工作日编号（0-6）组成的元组列表。超出月份的天数为 0。

```python
import calendar
import pprint

cal = calendar.Calendar(calendar.SUNDAY)

cal_data = cal.yeardays2calendar(2017, 3)
print('len(cal_data)      :', len(cal_data))

top_months = cal_data[0]
print('len(top_months)    :', len(top_months))

first_month = top_months[0]
print('len(first_month)   :', len(first_month))

print('first_month:')
pprint.pprint(first_month, width=65)

# 输出
# len(cal_data)      : 4
# len(top_months)    : 3
# len(first_month)   : 5
# first_month:
# [[(1, 6), (2, 0), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5)],
#  [(8, 6), (9, 0), (10, 1), (11, 2), (12, 3), (13, 4), (14, 5)],
#  [(15, 6), (16, 0), (17, 1), (18, 2), (19, 3), (20, 4), (21, 5)],
#  [(22, 6), (23, 0), (24, 1), (25, 2), (26, 3), (27, 4), (28, 5)],
#  [(29, 6), (30, 0), (31, 1), (0, 2), (0, 3), (0, 4), (0, 5)]]
```

相当于使用`formatyear()`。

```python
import calendar

cal = calendar.TextCalendar(calendar.SUNDAY)
print(cal.formatyear(2017, 2, 1, 1, 3))

# 输出
#                               2017
# 
#       January               February               March
# Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
#  1  2  3  4  5  6  7            1  2  3  4            1  2  3  4
#  8  9 10 11 12 13 14   5  6  7  8  9 10 11   5  6  7  8  9 10 11
# 15 16 17 18 19 20 21  12 13 14 15 16 17 18  12 13 14 15 16 17 18
# 22 23 24 25 26 27 28  19 20 21 22 23 24 25  19 20 21 22 23 24 25
# 29 30 31              26 27 28              26 27 28 29 30 31
# 
#        April                  May                   June
# Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
#                    1      1  2  3  4  5  6               1  2  3
#  2  3  4  5  6  7  8   7  8  9 10 11 12 13   4  5  6  7  8  9 10
#  9 10 11 12 13 14 15  14 15 16 17 18 19 20  11 12 13 14 15 16 17
# 16 17 18 19 20 21 22  21 22 23 24 25 26 27  18 19 20 21 22 23 24
# 23 24 25 26 27 28 29  28 29 30 31           25 26 27 28 29 30
# 30
# 
#         July                 August              September
# Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
#                    1         1  2  3  4  5                  1  2
#  2  3  4  5  6  7  8   6  7  8  9 10 11 12   3  4  5  6  7  8  9
#  9 10 11 12 13 14 15  13 14 15 16 17 18 19  10 11 12 13 14 15 16
# 16 17 18 19 20 21 22  20 21 22 23 24 25 26  17 18 19 20 21 22 23
# 23 24 25 26 27 28 29  27 28 29 30 31        24 25 26 27 28 29 30
# 30 31
# 
#       October               November              December
# Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa
#  1  2  3  4  5  6  7            1  2  3  4                  1  2
#  8  9 10 11 12 13 14   5  6  7  8  9 10 11   3  4  5  6  7  8  9
# 15 16 17 18 19 20 21  12 13 14 15 16 17 18  10 11 12 13 14 15 16
# 22 23 24 25 26 27 28  19 20 21 22 23 24 25  17 18 19 20 21 22 23
# 29 30 31              26 27 28 29 30        24 25 26 27 28 29 30
#                                             31
```

`day_name`，`day_abbr`，`month_name`，和 `month_abbr`模块主要用于生产定制格式化输出（即，包括在 HTML 输出链接）。它们会针对当前区域自动化配置。

## 区域设置

如果想生成非默认区域的格式化日历，可以使用`LocaleTextCalendar`或 `LocaleHTMLCalendar`。

```python
import calendar

c = calendar.LocaleTextCalendar(locale='en_US')
c.prmonth(2017, 7)

print()

c = calendar.LocaleTextCalendar(locale='fr_FR')
c.prmonth(2017, 7)

# 输出
#      July 2017
# Mo Tu We Th Fr Sa Su
#                 1  2
#  3  4  5  6  7  8  9
# 10 11 12 13 14 15 16
# 17 18 19 20 21 22 23
# 24 25 26 27 28 29 30
# 31
#
#     juillet 2017
# Lu Ma Me Je Ve Sa Di
#                 1  2
#  3  4  5  6  7  8  9
# 10 11 12 13 14 15 16
# 17 18 19 20 21 22 23
# 24 25 26 27 28 29 30
# 31
```

一周的第一天不是语言环境设置的一部分，而且这个值就是该类的一个参数，就像`TextCalendar`一样。

## 计算日期

虽然日历模块主要侧重于以各种格式打印完整日历，但它还提供了以其他方式处理日期的有用功能，例如计算重复事件的日期。

例如，Python 亚特兰大用户组在每个月的第二个星期四开会。要计算一年的会议日期，请使用`monthcalendar()`。

```python
import calendar
import pprint

pprint.pprint(calendar.monthcalendar(2017, 7))

# 输出
# [[0, 0, 0, 0, 0, 1, 2],
#  [3, 4, 5, 6, 7, 8, 9],
#  [10, 11, 12, 13, 14, 15, 16],
#  [17, 18, 19, 20, 21, 22, 23],
#  [24, 25, 26, 27, 28, 29, 30],
#  [31, 0, 0, 0, 0, 0, 0]]
```

0 值是与给定月份重叠的一周中的时间，是另一个月的一部分。

一周的第一天默认为星期一。可以通过调用`setfirstweekday()`来更改，但由于日历模块包含用于索引返回的日期范围的常量 `monthcalendar()`，因此在这种情况下跳过该步骤更方便。

要计算一年的小组会议日期，假设它们总是在每个月的第二个星期四，查看 `monthcalendar()`输出来查找星期四。本月的第一周和最后一周填充 0 值作为前一个月或后一个月天数的占位符。例如，如果一个月在星期五开始，则星期四位置第一周的值将为 0。

```python
import calendar
import sys

year = int(sys.argv[1])

# Show every month
for month in range(1, 13):

    # Compute the dates for each week that overlaps the month
    c = calendar.monthcalendar(year, month)
    first_week = c[0]
    second_week = c[1]
    third_week = c[2]

    # If there is a Thursday in the first week,
    # the second Thursday is # in the second week.
    # Otherwise, the second Thursday must be in
    # the third week.
    if first_week[calendar.THURSDAY]:
        meeting_date = second_week[calendar.THURSDAY]
    else:
        meeting_date = third_week[calendar.THURSDAY]

    print('{:>3}: {:>2}'.format(calendar.month_abbr[month], meeting_date))

# 输出    
# Jan: 12
# Feb:  9
# Mar:  9
# Apr: 13
# May: 11
# Jun:  8
# Jul: 13
# Aug: 10
# Sep: 14
# Oct: 12
# Nov:  9
# Dec: 14
```

## 其他可能有用的函数列表

| 序号 | 函数及描述                                                   |
| ---- | ------------------------------------------------------------ |
| 1    | **calendar.calendar(year,w=2,l=1,c=6)** 返回一个多行字符串格式的year年年历，3个月一行，间隔距离为c。 每日宽度间隔为w字符。每行长度为21* W+18+2* C。l是每星期行数。 |
| 2    | **calendar.firstweekday( )** 返回当前每周起始日期的设置。默认情况下，首次载入calendar模块时返回0，即星期一。 |
| 3    | **calendar.isleap(year)** 是闰年返回True，否则为false。      |
| 4    | **calendar.leapdays(y1,y2)** 返回在Y1，Y2两年之间的闰年总数。 |
| 5    | **calendar.month(year,month,w=2,l=1)** 返回一个多行字符串格式的year年month月日历，两行标题，一周一行。每日宽度间隔为w字符。每行的长度为7* w+6。l是每星期的行数。 |
| 6    | **calendar.monthcalendar(year,month)** 返回一个整数的单层嵌套列表。每个子列表装载代表一个星期的整数。Year年month月外的日期都设为0;范围内的日子都由该月第几日表示，从1开始。 |
| 7    | **calendar.monthrange(year,month)** 返回两个整数。第一个是该月的星期几的日期码，第二个是该月的日期码。日从0（星期一）到6（星期日）;月从1到12。 |
| 8    | **calendar.prcal(year,w=2,l=1,c=6)** 相当于 print calendar.calendar(year,w,l,c). |
| 9    | **calendar.prmonth(year,month,w=2,l=1)** 相当于 print calendar.calendar（year，w，l，c）。 |
| 10   | **calendar.setfirstweekday(weekday)** 设置每周的起始日期码。0（星期一）到6（星期日）。 |
| 11   | **calendar.timegm(tupletime)** 和time.gmtime相反：接受一个时间元组形式，返回该时刻的时间辍（1970纪元后经过的浮点秒数）。 |
| 12   | **calendar.weekday(year,month,day)** 返回给定日期的日期码。0（星期一）到6（星期日）。月份为 1（一月） 到 12（12月）。 |



相关文档：

https://pymotw.com/3/calendar/index.html

https://www.imooc.com/wiki/detail/id/1911