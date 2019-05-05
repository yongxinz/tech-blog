元素域 data 用来存放具体的数据。

链接域 prev 用来存放上一个节点的位置。

链接域 next 用来存放下一个节点的位置。

变量 p 指向链表的头节点（首节点）的位置，从 p 出发能找到表中的任意节点。

## 单链表

```python
# -*- coding: utf-8 -*-

from __future__ import print_function


class SingleNode(object):
    """节点"""

    def __init__(self, data):
        # 标识数据域
        self.data = data
        # 标识链接域
        self.next = None


class SingleLinkList(object):
    """单链表"""

    def __init__(self, node=None):
        # 私有属性头结点
        self.__head = node

    # is_empty() 链表是否为空
    def is_empty(self):
        return self.__head is None

    # length() 链表长度
    def length(self):
        # 数目
        count = 0
        # 当前节点
        current = self.__head
        while current is not None:
            count += 1
            # 当前节点往后移
            current = current.next
        return count

    # travel() 遍历整个链表
    def travel(self):
        # 访问的当前节点
        current = self.__head
        print('[', end=' ')
        while current is not None:
            print(current.data, end=' ')
            current = current.next
        print(']')

    # add(item) 链表头部添加元素
    def add(self, item):
        node = SingleNode(item)
        # 新节点的下一个节点为旧链表的头结点
        node.next = self.__head
        # 新链表的头结点为新节点
        self.__head = node

    # append(item) 链表尾部添加元素
    def append(self, item):
        node = SingleNode(item)
        if self.is_empty():
            # 为空节点时
            self.__head = node
        else:
            # 让指针指向最后节点
            current = self.__head
            while current.next is not None:
                current = current.next
            # 最后节点的下一个为新添加的node
            current.next = node

    # insert(index, item) 指定位置（从0开始）添加元素
    def insert(self, index, item):
        if index <= 0:
            # 在前方插入
            self.add(item)
        elif index > (self.length() - 1):
            # 在最后添加
            self.append(item)
        else:
            # 创建新节点
            node = SingleNode(item)
            # 遍历次数
            count = 0
            # 插入节点位置的上一个节点
            prev = self.__head
            # 查找到插入节点的上一个节点
            while count < (index - 1):
                count += 1
                prev = prev.next
            # 新节点的下一个节点为上一个节点的下一个节点
            node.next = prev.next
            # 上一个节点的下一个节点为新的节点
            prev.next = node

    # remove(item) 删除节点
    def remove(self, item):
        current = self.__head
        prev = None
        while current is not None:
            if current.data == item:
                # 找到要删除的节点元素
                if not prev:
                    # 没有上一个元素，比如删除头结点
                    self.__head = current.next
                else:
                    # 上一个节点的下一个节点指向当前节点的下一个节点
                    prev.next = current.next
                return  # 返回当前节点
            else:
                # 没找到，往后移
                prev = current
                current = current.next

    # search(item) 查找节点是否存在
    def search(self, item):
        # 当前节点
        current = self.__head
        while current is not None:
            if current.data == item:
                # 找到了
                return True
            else:
                current = current.next
        return False


if __name__ == '__main__':
    print('test:')
    single_link_list = SingleLinkList()

    print('--------判断是否为空-------')
    print(single_link_list.is_empty())

    print('-----------长度------------')
    print(single_link_list.length())

    single_link_list.append(2)
    single_link_list.append(3)
    single_link_list.append(5)

    print('-----------遍历------------')
    single_link_list.travel()

    single_link_list.add(1)
    single_link_list.add(0)
    single_link_list.insert(4, 4)
    single_link_list.insert(-1, -1)

    print('-----------遍历------------')
    single_link_list.travel()

    print('-----------查找------------')
    print(single_link_list.search(49))

    print('-----------删除------------')
    single_link_list.remove(-1)

    print('-----------遍历------------')
    single_link_list.travel()

    print('-----------长度------------')
    print(single_link_list.length())
```

## 单向循环链表
```python
# -*- coding: utf-8 -*-

from __future__ import print_function


class SingleNode(object):
    """节点"""

    def __init__(self, data):
        # 标识数据域
        self.data = data
        # 标识链接域
        self.next = None


class SingleCircleLinkList(object):
    """单向循环链表"""

    def __init__(self, node=None):
        # 私有属性头结点
        self.__head = node
        if node:
            # 不是构造空的链表
            # 头结点的下一个节点指向头结点
            node.next = node

    # is_empty() 链表是否为空
    def is_empty(self):
        return self.__head is None

    # length() 链表长度
    def length(self):
        if self.is_empty():
            # 空链表
            return 0
        count = 1  # 数目
        # 当前节点
        current = self.__head
        # 当前节点的下一个节点不是头结点则继续增加
        while current.next != self.__head:
            count += 1
            # 当前节点往后移
            current = current.next
        return count

    # travel() 遍历整个链表
    def travel(self):
        # 访问的当前节点
        if self.is_empty():
            return False
        current = self.__head
        print('[ ', end='')
        while current.next != self.__head:
            print(current.data, end=' ')
            current = current.next
        # 打印最后一个元素
        print(current.data, end=' ')
        print(']')

    # add(item) 链表头部添加元素
    def add(self, item):
        node = SingleNode(item)
        if self.is_empty():
            # 空链表
            self.__head = node
            node.next = node
        else:
            # 非空链表添加
            current = self.__head
            # 查找最后一个节点
            while current.next != self.__head:
                current = current.next
            # 新节点的下一个节点为旧链表的头结点
            node.next = self.__head
            # 新链表的头结点为新节点
            self.__head = node
            # 最后节点的下一个节点指向新节点
            current.next = node

    # append(item) 链表尾部添加元素
    def append(self, item):
        node = SingleNode(item)
        if self.is_empty():
            # 为空节点时
            self.__head = node
            node.next = node
        else:
            # 让指针指向最后节点
            current = self.__head
            while current.next != self.__head:
                current = current.next
            # 最后节点的下一个为新添加的node
            current.next = node
            # 新节点下一个节点指向头结点
            node.next = self.__head

    # insert(index, item) 指定位置（从0开始）添加元素
    def insert(self, index, item):
        if index <= 0:
            # 在前方插入
            self.add(item)
        elif index > (self.length() - 1):
            # 在最后添加
            self.append(item)
        else:
            # 创建新节点
            node = SingleNode(item)
            # 遍历次数
            count = 0
            # 插入节点位置的上一个节点
            prev = self.__head
            # 查找到插入节点的上一个节点
            while count < (index - 1):
                count += 1
                prev = prev.next
            # 新节点的下一个节点为上一个节点的下一个节点
            node.next = prev.next
            # 上一个节点的下一个节点为新的节点
            prev.next = node

    # remove(item) 删除节点
    def remove(self, item):
        if self.is_empty():
            return False
        current = self.__head
        prev = None
        while current.next != self.__head:
            if current.data == item:
                # 找到要删除的节点元素
                if current == self.__head:
                    # 删除结点,先找尾节点
                    rear = self.__head
                    while rear.next != self.__head:
                        rear = rear.next
                    # 头结点指向当前节点的下一个节点
                    self.__head = current.next
                    # 尾节点的下一个节点指向头结点
                    rear.next = self.__head
                else:
                    # 中间节点，上一个节点的下一个节点指向当前节点的下一个节点
                    prev.next = current.next
                return  # 返回当前节点
            else:
                # 没找到，往后移
                prev = current
                current = current.next
        # 循环结束current指向尾节点
        if current.data == item:
            if prev:
                # 如果删除最后一个节点
                prev.next = current.next
            else:
                # 删除只含有一个头结点的链表的头结点
                self.__head = None

    # search(item) 查找节点是否存在
    def search(self, item):
        # 当前节点
        if self.is_empty():
            # 空链表直接返回False
            return False
        current = self.__head
        while current.next != self.__head:
            if current.data == item:
                # 找到了
                return True
            else:
                current = current.next
        # 判断最后一个元素
        if current.data == item:
            return True
        return False


if __name__ == '__main__':
    print('test:')
    single_circle_link_list = SingleCircleLinkList()

    print('--------判断是否为空-------')
    print(single_circle_link_list.is_empty())

    print('-----------长度------------')
    print(single_circle_link_list.length())

    single_circle_link_list.append(2)
    single_circle_link_list.append(3)
    single_circle_link_list.append(5)
    #
    print('-----------遍历------------')
    single_circle_link_list.travel()
    #
    single_circle_link_list.add(1)
    single_circle_link_list.add(0)
    single_circle_link_list.insert(4, 4)
    single_circle_link_list.insert(-1, -1)
    #
    print('-----------遍历------------')
    single_circle_link_list.travel()
    #
    print('-----------查找------------')
    print(single_circle_link_list.search(4))
    #
    print('-----------删除------------')
    single_circle_link_list.remove(4)

    print('-----------遍历------------')
    single_circle_link_list.travel()

    print('-----------长度------------')
    print(single_circle_link_list.length())
```

## 双向链表
```python
# -*- coding: utf-8 -*-

from __future__ import print_function


class DoubleNode(object):
    """节点"""

    def __init__(self, data):
        # 标识数据域
        self.data = data
        # 标识前一个链接域
        self.prev = None
        # 标识后一个链接域
        self.next = None


class DoubleLinkList(object):
    """双链表"""

    def __init__(self, node=None):
        # 私有属性头结点
        self.__head = node

    # is_empty() 链表是否为空
    def is_empty(self):
        return self.__head is None

    # length() 链表长度
    def length(self):
        count = 0  # 数目
        # 当前节点
        current = self.__head
        while current is not None:
            count += 1
            # 当前节点往后移
            current = current.next
        return count

    # travel() 遍历整个链表
    def travel(self):
        # 访问的当前节点
        current = self.__head
        print('[ ', end='')
        while current is not None:
            print(current.data, end=' ')
            current = current.next
        print(']')

    # add(item) 链表头部添加元素
    def add(self, item):
        node = DoubleNode(item)
        # 新节点的下一个节点为旧链表的头结点
        node.next = self.__head
        # 新链表的头结点为新节点
        self.__head = node
        # 下一个节点的上一个节点指向新增的节点
        node.next.prev = node

    # append(item) 链表尾部添加元素
    def append(self, item):
        node = DoubleNode(item)
        if self.is_empty():
            # 为空节点时
            self.__head = node
        else:
            # 让指针指向最后节点
            current = self.__head
            while current.next is not None:
                current = current.next
            # 最后节点的下一个为新添加的node
            current.next = node
            # 新添加的结点上一个节点为当前节点
            node.prev = current

    # search(item) 查找节点是否存在
    def search(self, item):
        # 当前节点
        current = self.__head
        while current is not None:
            if current.data == item:
                # 找到了
                return True
            else:
                current = current.next
        return False

    # insert(index, item) 指定位置（从0开始）添加元素
    def insert(self, index, item):
        if index <= 0:
            # 在前方插入
            self.add(item)
        elif index > (self.length() - 1):
            # 在最后添加
            self.append(item)
        else:
            # 创建新节点
            node = DoubleNode(item)
            current = self.__head
            # 遍历次数
            count = 0
            # 查找到插入节点的上一个节点
            while count < index:
                count += 1
                current = current.next
            # 新节点的下一个节点指向当前节点
            node.next = current
            # 新节点的上一个节点指向当前节点的上一个节点
            node.prev = current.prev
            # 当前节点的上一个节点的下一个节点指向新节点
            current.prev.next = node
            # 当前节点的上一个节点指向新节点
            current.prev = node

    # remove(item) 删除节点
    def remove(self, item):
        current = self.__head
        while current is not None:
            if current.data == item:
                # 找到要删除的节点元素
                if current == self.__head:
                    # 头结点
                    self.__head = current.next
                    if current.next:
                        # 如果不是只剩下一个节点
                        current.next.prev = None
                else:
                    # 当前节点的上一个节点的下一个节点指向当前节点的下一个节点
                    current.prev.next = current.next
                    if current.next:
                        # 如果不是删除最后一个元素，当前节点的下一个节点的上一个节点指向当前节点的上一个节点
                        current.next.prev = current.prev
                return  # 返回当前节点
            else:
                # 没找到，往后移
                current = current.next


if __name__ == '__main__':
    print('test:')
    double_link_list = DoubleLinkList()

    print('--------判断是否为空-------')
    print(double_link_list.is_empty())

    print('-----------长度------------')
    print(double_link_list.length())

    double_link_list.append(2)
    double_link_list.append(3)
    double_link_list.append(5)

    print('-----------遍历------------')
    double_link_list.travel()

    double_link_list.add(1)
    print('-----------遍历------------')
    double_link_list.travel()
    double_link_list.add(0)
    print('-----------遍历------------')
    double_link_list.travel()
    double_link_list.insert(4, 4)
    print('-----------遍历------------')
    double_link_list.travel()
    double_link_list.insert(-1, -1)

    print('-----------遍历------------')
    double_link_list.travel()

    print('-----------查找------------')
    print(double_link_list.search(4))

    print('-----------删除------------')
    double_link_list.remove(5)
    double_link_list.remove(-1)

    print('-----------遍历------------')
    double_link_list.travel()

    print('-----------长度------------')
    print(double_link_list.length())
```

原文链接：
https://baagee.vip/index/article/id/100.html