class Student(object):
    """docstring for Student"""
    def __init__(self):
        super(Student, self).__init__()

s = Student()
s.name = 'Michael'
print(s.name)

def set_age(self, age):
    self.age = age
from types import MethodType
s.set_age = MethodType(set_age, s)
s.set_age(25)
print(s.age)

def set_score(self, score):
    self.score = score
Student.set_score = set_score

s.set_score(100)
print(s.score)
s2 = Student()
s2.set_score(99)
print(s2.score)

class Student1(object):
    """docstring for Student1"""
    __slots__ = ('name', 'age')
    def __init__(self):
        super(Student1, self).__init__()

s3 = Student1()
s3.name = 'Michael'
s3.age = 25
#s3.score = 99

class GraduateStudent(Student1):
    """docstring for GraduateStudent"""
    __slots__ = ('score')
    def __init__(self):
        super(GraduateStudent, self).__init__()

g = GraduateStudent()
g.score = 9999
g.name = 'mael'
print(g.score)

