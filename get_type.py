print(type(123))
print(type('str'))
print(type(None))
print(type(abs))

class Animal(object):
     """docstring for Animal"""
     def __init__(self, *arg):
         super(Animal, self).__init__()
         self.arg = arg

a = Animal()
print(type(a))
print(type(123) == type(456))
print(type(123) == int)
print(type('abc') == type('123'))
print(type('abbc') == str)
print(type('abc') == type(123))

import types

def fn():
    pass

print(type(fn) == types.FunctionType)
print(type(abs) == types.FunctionType)
print(type(lambda x: x) == types.LambdaType)
print(type((x for x in range(10)))==types.GeneratorType)

class Dog(Animal):
    """docstring for Dog"""
    def __init__(self, *arg):
        super(Dog, self).__init__()
        self.arg = arg        

class Huksy(Dog):
    """docstring for Huksy"""
    def __init__(self, *arg):
        super(Huksy, self).__init__()
        self.arg = arg

a = Animal()
d = Dog()
h = Huksy()

print(isinstance(h, Huksy))
print(isinstance(h, Dog))
print(isinstance(h, Animal))

print(isinstance(d, Dog) and isinstance(d, Animal))        
print(isinstance(d, Huksy))

print(isinstance('a', str))
print(isinstance(123, int))
print(isinstance(b'a', bytes))

print(isinstance([1, 2, 3], (list, tuple)))
print(isinstance((1, 2, 3), (list, tuple)))

