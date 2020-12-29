from contextlib import contextmanager, closing
from urllib.request import urlopen

try:
    f = open('fact.py', 'r')
    print(f.read())
except Exception as e:
    raise e
finally:
    if f:
        f.close()

with open('do_try.py', 'r') as f:
    line = f.read()
    print(line)

class Query(object):
    """docstring for Query"""
    def __init__(self, name):
        super(Query, self).__init__()
        self.name = name

    def __enter__(self):
        print('Begin')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print('Error')
        else:
            print('End')

    def Query(self):
        print('Query info about %s...' % self.name)

with Query('Bob') as q:
    q.Query()


class Query1(object):
    """docstring for Query1"""
    def __init__(self, name):
        super(Query1, self).__init__()
        self.name = name
    
    def query(self):
        print('Query info about %s...' % self.name)

@contextmanager
def create_query(name):
    print('Begin')
    q = Query1(name)
    yield q
    print('End')

with create_query('Bob') as q:
    q.query()

@contextmanager
def tag(name):
    print('<%s>' % name)
    yield
    print('</%s>' % name)

with tag("h1"):
    print('hello')
    print('world')


with closing(urlopen('https://www.baidu.com')) as page:
    for line in page:
        print(line)

