def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
print(person('Michael', 30))
print(person('Bob', 25, city='Beijing'))
print(person('Adam', 45, gender='M', job='Engineer'))
extra = {'city': 'Beijing', 'job': 'Engineer'}
print(person('Jack', 24, city=extra['city'], job=extra['job']))
print(person('Jack', 24, **extra))
print("读取关键字参数")
def person1(name, age, **kw):
    if 'city' in kw:
        pass
    if 'job' in kw:
        pass
    print('name:', name, 'age:', age, 'other:', kw)
print(person1('Jack', 24, city='Beijing', addr='Chaoyang', zipcode=12345))
print("命名参数")
def person2(name, age, *, city, job):
    print(name, age, city, job)
print(person2('Jack', 24, city='Beijing', job='Engineer'))
#命名参数有一个可变参数
def person3(name, age, *args, city='Beijing', job):
    print(name, age, city, job)
#print(person3('Jack', 25, 'Beijing', 'Engineer'))
print(person3('Jack', 25, job='Engineer'))
#参数组合：必选参数、默认参数、可变参数、命名关键字参数、关键字参数
print("参数组合")
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b=', b, 'c =', c, 'args =', args, 'kw =', kw)
def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b=', b, 'c=', c, 'd=', d, 'kw=', kw)
print(f1(1, 2))
print(f1(1, 2, c=3))
print(f1(1, 2, 3, 'a', 'b'))
print(f1(1, 2, 3, 'a', 'b', x=99))
print(f2(1, 2, d=99, ext=None))
args = (1, 2, 3, 4)
kw = {'d': 99, 'x': '#'}
print(f1(*args, **kw))
args = (1,2,3)
kw = {'d': 88, 'x': '#'}
print(f2(*args, **kw))
def product(*numbers):
    if len(numbers) == 0:
        raise TypeError('None')
    sum = 1
    for i in numbers:
        if not isinstance(i, (int, float)):
            raise TypeError('bad operand type')
        sum = sum * i
    return sum;
print('product(5) =', product(5))
print('product(5, 6) =', product(5, 6))
print('product(5, 6, 7) =', product(5, 6, 7))
print('product(5, 6, 7, 9) =', product(5, 6, 7, 9))
if product(5) != 5:
    print('测试失败!')
elif product(5, 6) != 30:
    print('测试失败!')
elif product(5, 6, 7) != 210:
    print('测试失败!')
elif product(5, 6, 7, 9) != 1890:
    print('测试失败!')
else:
    try:
        product()
        print('测试失败!')
    except TypeError:
        print('测试成功!')