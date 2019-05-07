# -*- coding: utf-8 -*-


class Deque(object):
    """双端队列"""

    def __init__(self):
        self.__items = []

    # add_front(item) 从队头加入一个item元素
    def add_front(self, item):
        self.__items.insert(0, item)

    # add_rear(item) 从队尾加入一个item元素
    def add_rear(self, item):
        self.__items.append(item)

    # remove_front() 从队头删除一个item元素
    def remove_front(self):
        return self.__items.pop(0)

    # remove_rear() 从队尾删除一个item元素
    def remove_rear(self):
        return self.__items.pop()

    # is_empty() 判断双端队列是否为空
    def is_empty(self):
        return self.__items == []

    # size() 返回队列的大小
    def size(self):
        return len(self.__items)

    def print_items(self):
        print(self.__items)


if __name__ == '__main__':
    deque = Deque()
    deque.add_front(1)
    deque.add_front(3)
    deque.add_front(5)
    deque.print_items()
    deque.add_rear(9)
    deque.add_rear(8)
    deque.add_rear(7)
    deque.print_items()
    print(deque.is_empty())
    print(deque.remove_front())
    print(deque.remove_rear())
    deque.print_items()
