class Animal(object):
    """docstring for Animal"""
    def __init__(self):
        super(Animal, self).__init__()

class Mammal(Animal):
    """docstring for Mammal"""
    def __init__(self):
        super(Mammal, self).__init__()

class Bird(object):
    """docstring for Bird"""
    def __init__(self):
        super(Bird, self).__init__()

class Dog(Mammal):
    """docstring for Dog"""
    def __init__(self):
        super(Dog, self).__init__()

class Bat(Mammal):
    """docstring for Bat"""
    def __init__(self):
        super(Bat, self).__init__()

class Parrot(Bird):
    """docstring for Parrot"""
    def __init__(self):
        super(Parrot, self).__init__()

class Ostrich(Bird):
    """docstring for Ostrich"""
    def __init__(self):
        super(Ostrich, self).__init__()
        
class Runnable(object):
    """docstring for Runnable"""
    def __init__(self):
        super(Runnable, self).__init__()
    
    def run(self):
        print("Running...")

class Flyable(object):
    """docstring for Flyable"""
    def __init__(self):
        super(Flyable, self).__init__()
    
    def fly(self):
        print("Flying...")

class Dog1(Mammal, Runnable):
    """docstring for Dog1"""
    def __init__(self):
        super(Dog1, self).__init__()

class Bat1(Mammal, Flyable):
    """docstring for Bat"""
    def __init__(self):
        super(Bat, self).__init__()


        
                        