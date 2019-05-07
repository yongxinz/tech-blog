## 栈

栈（stack）又名堆栈，它是一种运算受限的线性表。其限制是仅允许在表的一端进行插入和删除运算。这一端被称为栈顶，相对地，把另一端称为栈底。向一个栈插入新元素又称作进栈、入栈或压栈，它是把新元素放到栈顶元素的上面，使之成为新的栈顶元素；从一个栈删除元素又称作出栈或退栈，它是把栈顶元素删除掉，使其相邻的元素成为新的栈顶元素。

栈可以用顺序表实现，也可以用链表实现，这里为了方便就用顺序表实现。

```python
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
```

## 队列

队列是一种特殊的线性表，特殊之处在于它只允许在表的前端（front）进行删除操作，而在表的后端（rear）进行插入操作，和栈一样，队列是一种操作受限制的线性表。进行插入操作的端称为队尾，进行删除操作的端称为队头。队列中没有元素时，称为空队列。

队列的数据元素又称为队列元素。在队列中插入一个队列元素称为入队，从队列中删除一个队列元素称为出队。因为队列只允许在一端插入，在另一端删除，所以只有最早进入队列的元素才能最先从队列中删除，故队列又称为先进先出（FIFO—first in first out）线性表

```python
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
```

## 双端队列

双端队列（deque，全名double-ended queue），是一种具有队列和栈的性质的数据结构。

双端队列中的元素可以从两端弹出，其限定插入和删除操作在表的两端进行。双端队列可以在队列任意一端入队和出队。

```python
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
```

原文链接：https://baagee.vip/index/article/id/102.html