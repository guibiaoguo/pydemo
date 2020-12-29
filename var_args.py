def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
print(power(5,2))
print(power(5,3))
print(power(5))
print(power(15))

def enroll(name, gender, age=6, city='Guangdong'):
    print('name:', name)
    print('gender:', gender)
    print(f'age:{age}')
    print("city:{}".format(city))
print(enroll('Sarah', 'F'))
print(enroll('Bob', 'M', 7))
print(enroll('Adam', 'M', city='Tianjing'))
print("默认参数必须是不可变对象")
def add_end(L=[]):
    L.append('END')
    return L
print(add_end([1,2,3]))
print(add_end(['x','y','z']))
print(add_end())
print("再一次执行add_end()=",add_end())
def add_end1(L=None):
    if L is None:
        L = []
    L.append('END')
print(add_end1())
print("再一次执行add_end1=",add_end1())
print("多个参数的函数可以通过list,tuple实现")
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc([1,2,3]))
print(calc([1,3,5,7]))
print("多个参数的函数可以通过可变参数实现")
def calc1(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc1(1, 2))
print(calc1())
nums = [1,2,3]
nums1 = (4,5,6)
print(calc1(*nums))
print(calc1(*nums1))
