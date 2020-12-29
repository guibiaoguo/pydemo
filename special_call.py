class Student(object):
    """docstring for Student"""
    def __init__(self, name):
        super(Student, self).__init__()
        self.name = name
    
    def __call__(self):
        print('My name is %s.' %self.name)

s = Student('Michael')
print(s())
print(callable(Student('Michael')))
print(callable(max))
print(callable([1, 2, 3]))
print(callable(None))
print(callable('str'))

