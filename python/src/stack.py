# -*- coding: utf-8 -*-


class Stack(object):
    """栈的实现类"""

    def __init__(self):
        self.__items = []

    # push(item) 添加一个新的元素item到栈顶
    def push(self, item):
        self.__items.append(item)

    # pop() 弹出栈顶元素
    def pop(self):
        return self.__items.pop()

    # peek() 返回栈顶元素
    def peek(self):
        return self.__items[self.size() - 1]

    # is_empty() 判断栈是否为空
    def is_empty(self):
        return self.__items == []

    # size() 返回栈的元素个数
    def size(self):
        return len(self.__items)


if __name__ == '__main__':
    stack = Stack()
    stack.push(2)
    stack.push(3)
    stack.push(4)
    stack.push(5)
    tmp = stack.pop()
    print(tmp)
    print(stack.peek())
    print(stack.size())
    print(stack.is_empty())
