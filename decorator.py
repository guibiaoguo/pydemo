import functools
import time
def now():
    print('2020-12-21')
f = now
print(f())
print(now.__name__)
print(f.__name__)

def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args,**kw)
    return wrapper

@log
def now1():
    print('2020-12-21')
print(now1())

def log1(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print("%s %s()" % (text,func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
@log1('execute')
def now2():
    print('2020-12-21')
print(now2())
print(now2.__name__)

def metric(func):
    def wrapper(*args, **kw):
        t1 = time.time()
        result = func(*args, **kw)
        t2 = time.time()
        print(f"{func.__name__} executed in {t2 - t1}")
        return result
    return wrapper
@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y;

@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z;

f = fast(11, 22)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')

def log2(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print("%s %s() begin call" % (text,func.__name__))
            result = func(*args, **kw)
            print("%s %s() end call" % (text,func.__name__) )
            return result
        return wrapper
    return decorator
@log2('executed')
def sum(x, y):
    return x + y
print(sum(1,2))