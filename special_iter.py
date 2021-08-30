#迭代器
class Fib(object):
    """docstring for Fib"""
    def __init__(self):
        super(Fib, self).__init__()
        self.a, self.b = 0, 1
        
    def __iter__(self):
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 1000000:
            raise StopIteration()
        return self.a

for n in Fib():
    print(n)
