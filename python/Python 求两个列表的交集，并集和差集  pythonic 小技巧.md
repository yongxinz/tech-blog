# 求求你了，不要再写循环求两个列表的交集，并集和差集了 | pythonic 小技巧

在 Python 中，求两个列表的交集，并集和差集是经常会遇到的需求，而且也比较简单。

最容易想到的就是写循环，对两个列表分别进行循环，然后判断元素是否在另一个列表中，求得最终结果。

但这种方法比较 low，没啥技术含量。身为一名 Python 程序员，一定要写够 pythonic 的代码。

废话不多说，直接看代码。

```python
# list_operate.py

def main():
    list_a = [1, 2, 3, 4, 5]
    list_b = [4, 5, 6, 7, 8]

    # 求交集的两种方式
    res_a = [i for i in list_a if i in list_b]
    res_b = list(set(list_a).intersection(set(list_b)))

    print(f"res_a is: {res_a}")
    print(f"res_b is: {res_b}")

    # 求并集
    res_c = list(set(list_a).union(set(list_b)))
    print(f"res_c is: {res_c}")

    # 求差集的两种方式，在B中但不在A中
    res_d = [i for i in list_b if i not in list_a]
    res_e = list(set(list_b).difference(set(list_a)))

    print(f"res_d is: {res_d}")
    print(f"res_e is: {res_e}")


if __name__ == '__main__':
    main()

```

来看一下输出：

```python
# python3 list_operate.py
res_a is: [4, 5]
res_b is: [4, 5]
res_c is: [1, 2, 3, 4, 5, 6, 7, 8]
res_d is: [6, 7, 8]
res_e is: [8, 6, 7]
```

结果还是没问题的，别一顿操作猛如虎，结果是错的，那就尴尬了。

总结一下，基本上就是两种思路：

1. 使用列表表达式
2. 使用 set 的内置方法，再转换成 list

以上。

关注公众号 **AlwaysBeta**，学习更多 pythonic 小技巧。

**往期精彩：**

