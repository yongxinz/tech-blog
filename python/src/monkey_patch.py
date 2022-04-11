# 定义一个Dog类
class Dog:
    def eat(self):
        print("A dog is eating ...")


# 在类的外部给 Dog 类添加猴子补丁
def walk(self):
    print("A dog is walking ...")


Dog.walk = walk

# 与类的内部定义的属性和方法无差异
dog = Dog()
dog.eat()
dog.walk()
