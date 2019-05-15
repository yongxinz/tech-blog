本文用 Python 实现了插入排序、希尔排序、冒泡排序、快速排序、直接选择排序、堆排序、归并排序。

先整体看一下各个算法之间的对比，然后再进行详细介绍：

排序算法 | 平均时间复杂度 | 最好情况 | 最坏情况 | 空间复杂度 | 排序方式 | 稳定性
---|---|---|---|---|---|---|---
插入排序 | O(n²) | O(n) | O(n²) | O(1) | In-place | 稳定
冒泡排序 | O(n²) | O(n) | O(n²) | O(1) | In-place | 稳定
选择排序 | O(n²) | O(n²) | O(n²) | O(1) | In-place | 不稳定
快速排序 | O(n log n) | O(n log n) | O(n²) | O(log n) | In-place | 不稳定
希尔排序 | O(n log n) | O(n log n) | O(n log n) | O(1) | In-place | 不稳定
堆排序   | O(n log n) | O(n log n) | O(n log n) | O(1) | In-place | 不稳定
归并排序 | O(n log n) | O(n log n) | O(n log n) | O(n) | Out-place | 稳定


n：数据规模

In-place：占用常数内存，不占用额外内存

Out-place：占用额外内存

稳定性：排序后 2 个相等键值的顺序和排序之前它们的顺序相同

## 插入排序
**描述**

时间复杂度为 O(n^2)，是稳定的排序方法。

插入排序的基本操作就是将一个数据插入到已经排好序的有序数据中，从而得到一个新的、个数加一的有序数据，算法适用于少量数据的排序。

插入算法把要排序的数组分成两部分：第一部分包含了这个数组的所有元素，但将最后一个元素除外（让数组多一个空间才有插入的位置），而第二部分就只包含这一个元素（即待插入元素）。在第一部分排序完成后，再将这个最后元素插入到已排好序的第一部分中。

**代码实现**
```python
# -*- coding: UTF-8 -*-


def insert_sort(lists):
    # 插入排序 时间复杂度为 O(n^2)
    count = len(lists)
    for i in range(1, count):
        key = lists[i]
        j = i - 1
        while j >= 0:
            if lists[j] > key:
                lists[j + 1] = lists[j]
                lists[j] = key
            j -= 1
    return lists


if __name__ == "__main__":
    test = [2, 5, 4, 6, 7, 3, 2]
    print(insert_sort(test))
```

## 希尔排序

**描述**

时间复杂度为 O(n log n)，是不稳定的排序方法。

希尔排序(Shell Sort)是插入排序的一种，也称缩小增量排序，是直接插入排序算法的一种更高效的改进版本。

该方法因 DL．Shell 于 1959 年提出而得名。 希尔排序是把记录按下标的一定增量分组，对每组使用直接插入排序算法排序；随着增量逐渐减少，每组包含的关键词越来越多，当增量减至 1 时，整个文件恰被分成一组，算法便终止。

**代码实现**

```python
# -*- coding: UTF-8 -*-


def shell_sort(lists):
    # 希尔排序 时间复杂度是 O(n log n)
    count = len(lists)
    step = 2
    group = int(count / step)
    while group > 0:
        for i in range(0, group):
            j = i + group
            while j < count:
                k = j - group
                key = lists[j]
                while k >= 0:
                    if lists[k] > key:
                        lists[k + group] = lists[k]
                        lists[k] = key
                    k -= group
                j += group
        group = int(group / step)
    return lists


if __name__ == "__main__":
    test = [2, 5, 4, 6, 7, 3, 2]
    print(shell_sort(test))
```

## 冒泡排序

**描述**

时间复杂度是 O(n²)， 是稳定排序算法。

它重复地走访过要排序的数列，一次比较两个元素，如果他们的顺序错误就把他们交换过来。走访数列的工作是重复地进行直到没有再需要交换，也就是说该数列已经排序完成。

**代码实现**
```python
# -*- coding: UTF-8 -*-


def bubble_sort(lists):
    # 冒泡排序 时间复杂度是 O(n²)
    count = len(lists)
    for i in range(0, count - 1):
        for j in range(0, count - i - 1):
            if lists[j] > lists[j + 1]:
                lists[j], lists[j + 1] = lists[j + 1], lists[j]
    return lists


if __name__ == "__main__":
    test = [2, 5, 4, 6, 7, 3, 2]
    print(bubble_sort(test))
```

## 快速排序
**描述**

快速排序的时间复杂度是 O(n log n)， 是不稳定排序算法。

通过一趟排序将要排序的数据分割成独立的两部分，其中一部分的所有数据都比另外一部分的所有数据都要小，然后再按此方法对这两部分数据分别进行快速排序，整个排序过程可以递归进行，以此达到整个数据变成有序序列。

**代码实现**

```python
# -*- coding: UTF-8 -*-


def quick_sort(lists, left, right):
    # 快速排序 时间复杂度是 O(n log n)
    if left >= right:
        return lists
    key = lists[left]
    low = left
    high = right
    while left < right:
        while left < right and lists[right] >= key:
            right -= 1
        lists[left] = lists[right]
        while left < right and lists[left] <= key:
            left += 1
        lists[right] = lists[left]
    lists[right] = key
    quick_sort(lists, low, left - 1)
    quick_sort(lists, left + 1, high)
    return lists


if __name__ == "__main__":
    test = [2, 5, 4, 6, 7, 3, 2]
    print(quick_sort(test, 0, len(test) - 1))
```

### 直接选择排序
**描述**

选择排序的时间复杂度是 O(n²)， 是不稳定排序算法。

基本思想：第 1 趟，在待排序记录 r1 ~ r[n] 中选出最小的记录，将它与 r1 交换；第 2 趟，在待排序记录 r2 ~ r[n] 中选出最小的记录，将它与 r2 交换；以此类推，第 i 趟在待排序记录 r[i] ~ r[n] 中选出最小的记录，将它与 r[i] 交换，使有序序列不断增长直到全部排序完毕。

**代码实现**

```python
# -*- coding: UTF-8 -*-


def select_sort(lists):
    # 选择排序 时间复杂度是 O(n²)
    count = len(lists)
    for i in range(0, count):
        min = i
        for j in range(i + 1, count):
            if lists[min] > lists[j]:
                min = j
        lists[min], lists[i] = lists[i], lists[min]
    return lists


if __name__ == "__main__":
    test = [2, 5, 4, 6, 7, 3, 2]
    print(select_sort(test))
```

### 堆排序
**描述**

堆排序的时间复杂度是 O(n log n)， 是不稳定排序算法。

堆排序(Heapsort)是指利用堆积树（堆）这种数据结构所设计的一种排序算法，它是选择排序的一种。可以利用数组的特点快速定位指定索引的元素。堆分为大根堆和小根堆，是完全二叉树。大根堆的要求是每个节点的值都不大于其父节点的值，即 `A[PARENT[i]] >= A[i]`。在数组的非降序排序中，需要使用的就是大根堆，因为根据大根堆的要求可知，最大的值一定在堆顶。

**代码实现**

```python
# -*- coding: UTF-8 -*-

from collections import deque


def swap_param(lists, i, j):
    lists[i], lists[j] = lists[j], lists[i]
    return lists


def heap_adjust(lists, start, end):
    temp = lists[start]

    i = start
    j = 2 * i

    while j <= end:
        if (j < end) and (lists[j] < lists[j + 1]):
            j += 1
        if temp < lists[j]:
            lists[i] = lists[j]
            i = j
            j = 2 * i
        else:
            break
    lists[i] = temp


def heap_sort(lists):
    length = len(lists) - 1

    first_sort_count = length / 2
    for i in range(first_sort_count):
        heap_adjust(lists, first_sort_count - i, length)

    for i in range(length - 1):
        lists = swap_param(lists, 1, length - i)
        heap_adjust(lists, 1, length - i - 1)

    return [lists[i] for i in range(1, len(lists))]


def main():
    lists = deque([50, 16, 30, 10, 60,  90,  2, 80, 70])
    lists.appendleft(0)
    print heap_sort(lists)


if __name__ == '__main__':
    main()
```

### 归并排序
**描述**

时间复杂度是 O(n log n)， 是稳定排序算法。

归并排序是建立在归并操作上的一种有效的排序算法,该算法是采用分治法（Divide and Conquer）的一个非常典型的应用。将已有序的子序列合并，得到完全有序的序列；即先使每个子序列有序，再使子序列段间有序。若将两个有序表合并成一个有序表，称为二路归并。

归并过程为：比较a[i]和a[j]的大小，若a[i]≤a[j]，则将第一个有序表中的元素a[i]复制到r[k]中，并令i和k分别加上1；否则将第二个有序表中的元素a[j]复制到r[k]中，并令j和k分别加上1，如此循环下去，直到其中一个有序表取完，然后再将另一个有序表中剩余的元素复制到r中从下标k到下标t的单元。归并排序的算法我们通常用递归实现，先把待排序区间[s,t]以中点二分，接着把左边子区间排序，再把右边子区间排序，最后把左区间和右区间用一次归并操作合并成有序的区间[s,t]。

**代码实现**

```python
# -*- coding: UTF-8 -*-


def merge_sort(lists):
    # 归并排序 时间复杂度是 O(n log n)
    if len(lists) <= 1:
        return lists

    num = int(len(lists) / 2)
    left_lists = merge_sort(lists[:num])
    right_lists = merge_sort(lists[num:])

    return merge(left_lists, right_lists)


def merge(left_lists, right_lists):
    left, right = 0, 0
    result = []

    while left < len(left_lists) and right < len(right_lists):
        if left_lists[left] < right_lists[right]:
            result.append(left_lists[left])
            left += 1
        else:
            result.append(right_lists[right])
            right += 1

    result += left_lists[left:]
    result += right_lists[right:]

    return result


if __name__ == "__main__":
    test = [2, 5, 4, 6, 7, 3, 2]
    print(merge_sort(test))
```

参考文档：

https://baagee.vip/index/article/id/101.html

https://www.jianshu.com/p/d174f1862601