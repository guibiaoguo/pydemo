class Student(object):
    """docstring for Student"""
    def __init__(self):
        super(Student, self).__init__()
        self.name = 'Michael'

    def __getattr__(self, attr):
        if attr == 'score':
            return 99
        if attr == 'age':
            return lambda: 25
        raise AttributeError("Student object has no attribute %s" %attr)

s = Student()
print(s.name)
print(s.score)
print(s.age())
#print(s.abc)

class Chain1(object):
    """docstring for Chain"""
    def __init__(self, path=''):
        self._path = path
    
    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__

class Chain(object):

    def __init__(self, path=''):
        self._path = path

    def users(self,name):
        return Chain('%s%s' %(self._path, name))

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__

print(Chain().status.user.timeline.list)
print(Chain1().user.friends)
print(Chain().users('Michael').repos)
