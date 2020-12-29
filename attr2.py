class Student(object):
    """docstring for Student"""
    def __init__(self, name):
        super(Student, self).__init__()
        self.name = name

s = Student('Bob')
s.score = 90

class Student2(object):
    name = 'Student'

s2 = Student2()
print(s2.name)
print(Student2.name)
s2.name = 'Michael'
print(s2.name)
print(Student2.name)
del s2.name
print(s2.name)

class Student3(object):
    """docstring for Student3"""
    count = 0
    def __init__(self, name):
        super(Student3, self).__init__()
        self.name = name
        Student3.count += 1

if Student3.count != 0:
    print('测试失败!')
else:
    bart = Student3('Bart')
    if Student3.count != 1:
        print('测试失败!')
    else:
        lisa = Student3('Bart')
        if Student3.count != 2:
            print('测试失败!')
        else:
            print('Students:', Student3.count)
            print('测试通过!')
