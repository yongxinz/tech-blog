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
