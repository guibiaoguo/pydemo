class Animal(object):
    """docstring for Animal"""
    def __init__(self, *arg):
        super(Animal, self).__init__()
        self.arg = arg
    
    def run(self):
        print('Animal is running..')

class Dog(Animal):
    """docstring for Dog"""
    def run(self):
        print('Dog is running..')

    def eat(self):
        print('Eating meat..')

class Cat(Animal):
    """docstring for Cat"""
    def run(self):
        print('Cat is running..')

    def eat(self):
        print('Eating fish..')

dog = Dog()
dog.run()

cat = Cat()
cat.run()

a = list()
b = Animal()
c = Dog()

print(isinstance(a, list))
print(isinstance(b, Animal))
print(isinstance(c, Dog))
print(isinstance(c, Animal))
print(isinstance(b, Dog))

def run_twice(animal):
    animal.run()
    animal.run()

run_twice(Animal())
run_twice(Dog())
run_twice(Cat())

class Tortoise(Animal):
    """docstring for Tortoise"""
    def run(self):
        print('Tortoise is running slowly..')

run_twice(Tortoise())

class Timer(object):
    """docstring for Timer"""
    def __init__(self, *arg):
        super(Timer, self).__init__()
        self.arg = arg
    
    def run(self):
        print("Start..")
        