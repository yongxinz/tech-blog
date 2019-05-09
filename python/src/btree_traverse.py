# -*- coding=utf-8 -*-


class Node(object):
    """节点类"""

    def __init__(self, element=-1, l_child=None, r_child=None):
        self.element = element
        self.l_child = l_child
        self.r_child = r_child


class Tree(object):
    """树类"""

    def __init__(self):
        self.root = Node()
        self.queue = []

    def add_node(self, element):
        """为树添加节点"""

        node = Node(element)
        # 如果树是空的，则对根节点赋值
        if self.root.element == -1:
            self.root = node
            self.queue.append(self.root)
        else:
            tree_node = self.queue[0]
            # 此结点没有左子树，则创建左子树节点
            if tree_node.l_child is None:
                tree_node.l_child = node
                self.queue.append(tree_node.l_child)
            else:
                tree_node.r_child = node
                self.queue.append(tree_node.r_child)
                # 如果该结点存在右子树，将此节点丢弃
                self.queue.pop(0)

    def front_recursion(self, root):
        """利用递归实现树的前序遍历"""

        if root is None:
            return

        print root.element,
        self.front_recursion(root.l_child)
        self.front_recursion(root.r_child)

    def middle_recursion(self, root):
        """利用递归实现树的中序遍历"""

        if root is None:
            return

        self.middle_recursion(root.l_child)
        print root.element,
        self.middle_recursion(root.r_child)

    def back_recursion(self, root):
        """利用递归实现树的后序遍历"""

        if root is None:
            return

        self.back_recursion(root.l_child)
        self.back_recursion(root.r_child)
        print root.element,

    @staticmethod
    def front_stack(root):
        """利用堆栈实现树的前序遍历"""

        if root is None:
            return

        stack = []
        node = root
        while node or stack:
            # 从根节点开始，一直找它的左子树
            while node:
                print node.element,
                stack.append(node)
                node = node.l_child
            # while结束表示当前节点node为空，即前一个节点没有左子树了
            node = stack.pop()
            # 开始查看它的右子树
            node = node.r_child

    @staticmethod
    def middle_stack(root):
        """利用堆栈实现树的中序遍历"""

        if root is None:
            return

        stack = []
        node = root
        while node or stack:
            # 从根节点开始，一直找它的左子树
            while node:
                stack.append(node)
                node = node.l_child
            # while结束表示当前节点node为空，即前一个节点没有左子树了
            node = stack.pop()
            print node.element,
            # 开始查看它的右子树
            node = node.r_child

    @staticmethod
    def back_stack(root):
        """利用堆栈实现树的后序遍历"""

        if root is None:
            return

        stack1 = []
        stack2 = []
        node = root
        stack1.append(node)
        # 这个while循环的功能是找出后序遍历的逆序，存在stack2里面
        while stack1:
            node = stack1.pop()
            if node.l_child:
                stack1.append(node.l_child)
            if node.r_child:
                stack1.append(node.r_child)
            stack2.append(node)
        # 将stack2中的元素出栈，即为后序遍历次序
        while stack2:
            print stack2.pop().element,

    @staticmethod
    def level_queue(root):
        """利用队列实现树的层次遍历"""

        if root is None:
            return

        queue = []
        node = root
        queue.append(node)
        while queue:
            node = queue.pop(0)
            print node.element,
            if node.l_child is not None:
                queue.append(node.l_child)
            if node.r_child is not None:
                queue.append(node.r_child)


if __name__ == '__main__':
    """主函数"""

    # 生成十个数据作为树节点
    elements = range(10)
    tree = Tree()
    for elem in elements:
        tree.add_node(elem)

    print '队列实现层次遍历:'
    tree.level_queue(tree.root)

    print '\n\n递归实现前序遍历:'
    tree.front_recursion(tree.root)
    print '\n递归实现中序遍历:'
    tree.middle_recursion(tree.root)
    print '\n递归实现后序遍历:'
    tree.back_recursion(tree.root)

    print '\n\n堆栈实现前序遍历:'
    tree.front_stack(tree.root)
    print '\n堆栈实现中序遍历:'
    tree.middle_stack(tree.root)
    print '\n堆栈实现后序遍历:'
    tree.back_stack(tree.root)
