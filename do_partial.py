import functools
print(int('12345'))
print(int('12345', base=8))
print(int('12345', 16))
print(int('10000000',2))

def int2(x, base=2):
    return int(x, base)
print(int2('100000'))
print(int2('10101010'))
print(int2('1000',8))
_int2 = functools.partial(int, base=2)
print(_int2('100000'))
print(_int2('1001010'))
max2 = functools.partial(max, 10)
print(max2(5, 6, 7))

