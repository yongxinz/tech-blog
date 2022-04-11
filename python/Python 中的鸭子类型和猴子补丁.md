**原文链接：** [Python 中的鸭子类型和猴子补丁](https://mp.weixin.qq.com/s/3WGFkl9MRbYjojFK7-eEww)

大家好，我是老王。

Python 开发者可能都听说过**鸭子类型**和**猴子补丁**这两个词，即使没听过，也大概率写过相关的代码，只不过并不了解其背后的技术要点是这两个词而已。

我最近在面试候选人的时候，也会问这两个概念，很多人答的也并不是很好。但是当我向他们解释完之后，普遍都会恍然大悟：“哦，是这个啊，我用过”。

所以，我决定来写一篇文章，探讨一下这两个技术。

## 鸭子类型

引用维基百科中的一段解释：

> **鸭子类型**（**duck typing**）在程序设计中是动态类型的一种风格。在这种风格中，一个对象有效的语义，不是由继承自特定的类或实现特定的接口，而是由"当前方法和属性的集合"决定。

更通俗一点的说：

> 当看到一只鸟走起来像鸭子、游泳起来像鸭子、叫起来也像鸭子，那么这只鸟就可以被称为鸭子。

也就是说，在鸭子类型中，关注点在于对象的行为，能作什么；而不是关注对象所属的类型。

我们看一个例子，更形象地展示一下：

```python
# 这是一个鸭子（Duck）类
class Duck:
    def eat(self):
        print("A duck is eating...")

    def walk(self):
        print("A duck is walking...")


# 这是一个狗（Dog）类
class Dog:
    def eat(self):
        print("A dog is eating...")

    def walk(self):
        print("A dog is walking...")


def animal(obj):
    obj.eat()
    obj.walk()


if __name__ == '__main__':
    animal(Duck())
    animal(Dog())
```

程序输出：

```
A duck is eating...
A duck is walking...
A dog is eating...
A dog is walking...
```

Python 是一门动态语言，没有严格的类型检查。只要 `Duck` 和 `Dog` 分别实现了 `eat` 和 `walk` 方法就可以直接调用。

再比如 `list.extend()` 方法，除了 `list` 之外，`dict` 和 `tuple` 也可以调用，只要它是可迭代的就都可以调用。

看过上例之后，应该对「**对象的行为**」和「**对象所属的类型**」有更深的体会了吧。

再扩展一点，其实鸭子类型和接口挺像的，只不过没有显式定义任何接口。

比如用 Go 语言来实现鸭子类型，代码是这样的：

```go
package main

import "fmt"

// 定义接口，包含 Eat 方法
type Duck interface {
	Eat()
}

// 定义 Cat 结构体，并实现 Eat 方法
type Cat struct{}

func (c *Cat) Eat() {
	fmt.Println("cat eat")
}

// 定义 Dog 结构体，并实现 Eat 方法
type Dog struct{}

func (d *Dog) Eat() {
	fmt.Println("dog eat")
}

func main() {
	var c Duck = &Cat{}
	c.Eat()

	var d Duck = &Dog{}
	d.Eat()

	s := []Duck{
		&Cat{},
		&Dog{},
	}
	for _, n := range s {
		n.Eat()
	}
}
```

通过显式定义一个 `Duck` 接口，每个结构体实现接口中的方法来实现。

## 猴子补丁

**猴子补丁**（**Monkey Patch**）的名声不太好，因为它会在运行时动态修改模块、类或函数，通常是添加功能或修正缺陷。

猴子补丁在内存中发挥作用，不会修改源码，因此只对当前运行的程序实例有效。

但如果滥用的话，会导致系统难以理解和维护。

主要有两个问题：

1. 补丁会破坏封装，通常与目标紧密耦合，因此很脆弱
2. 打了补丁的两个库可能相互牵绊，因为第二个库可能会撤销第一个库的补丁

所以，它被视为临时的变通方案，不是集成代码的推荐方式。

按照惯例，还是举个例子来说明：

```python
# 定义一个Dog类
class Dog:
    def eat(self):
        print("A dog is eating ...")


# 在类的外部给 Dog 类添加猴子补丁
def walk(self):
    print("A dog is walking ...")


Dog.walk = walk

# 调用方式与类的内部定义的属性和方法一样
dog = Dog()
dog.eat()
dog.walk()
```

程序输出：

```
A dog is eating ...
A dog is walking ...
```

这里相当于在类的外部给 `Dog` 类增加了一个 `walk` 方法，而调用方式与类的内部定义的属性和方法一样。

再举一个比较实用的例子，比如我们常用的 `json` 标准库，如果说想用性能更高的 `ujson` 代替的话，那势必需要将每个文件的引入：

```python
import json
```

改成：

```python
import ujson as json
```

如果这样改起来成本就比较高了。这个时候就可以考虑使用猴子补丁，只需要在程序入口加上：

```python
import json  
import ujson  


def monkey_patch_json():  
    json.__name__ = 'ujson'  
    json.dumps = ujson.dumps  
    json.loads = ujson.loads  


monkey_patch_json()
```

这样在以后调用 `dumps` 和 `loads` 方法的时候就是调用的 `ujson` 包，还是很方便的。

但猴子补丁就是一把双刃剑，问题也在上文中提到了，看需，谨慎使用吧。

以上就是本文的全部内容，如果觉得还不错的话，欢迎**点赞**，**转发**和**关注**，感谢支持。

---

**推荐阅读：**

- [**Python 学习路线（2022）**](https://mp.weixin.qq.com/s/CyJ92-CD1xnihlp-Dqj8Yw)
- [我写的 Python 代码，同事都说好](https://mp.weixin.qq.com/s/shO7Vw8U3xEJelzXgCa_mQ)