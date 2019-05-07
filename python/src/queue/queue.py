# -*- coding: utf-8 -*-


class Queue(object):
    """队列的实现"""

    def __init__(self):
        self.__items = []

    # push(item) 往队列中添加一个item元素
    def push(self, item):
        self.__items.insert(0, item)

    # pop() 从队列头部删除一个元素
    def pop(self):
        return self.__items.pop()

    # is_empty() 判断一个队列是否为空
    def is_empty(self):
        return self.__items == []

    # size() 返回队列的大小
    def size(self):
        return len(self.__items)


if __name__ == '__main__':
    queue = Queue()
    queue.push(1)
    queue.push(2)
    queue.push(3)
    queue.push(4)
    print(queue.pop())
    print(queue.pop())
    print(queue.pop())
    print(queue.size())
    print(queue.is_empty())
