print(dir('ABC'))
print(len('ABC'))
print('ABC'.__len__())

class MyObject(object):
    """docstring for MyObject"""
    def __init__(self):
        super(MyObject, self).__init__()
        self.x = 9

    def power(self):
        return self.x * self.x

obj = MyObject()

print(hasattr(obj, 'x'))
print(obj.x)
print(hasattr(obj, 'y'))
setattr(obj, 'y', 19)
print(hasattr(obj, 'y'))
print(getattr(obj, 'y'))
print(obj.y)

print(getattr(obj, 'z', 404))

print(hasattr(obj, 'power'))
print(getattr(obj, 'power'))

fn = getattr(obj, 'power')
print(fn())

