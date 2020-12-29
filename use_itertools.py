import itertools

natuals = itertools.count(1)
for n in natuals:
    print(n)
    if (n == 100):
        break

cs = itertools.cycle('ABC')
for c in cs:
    print(c)
    break

ns = itertools.repeat('A', 3)
for n in ns:
    print(n)

natuals = itertools.count(1)
ns = itertools.takewhile(lambda x: x <= 10, natuals)
print(list(ns))

for c in itertools.chain('ABC', 'XYZ'):
    print(c)

for key,group in itertools.groupby('AAAABBBCCADD'):
    print(key,list(group))

def pi(N):
    natuals = itertools.count(1,2)
    ns = list(itertools.takewhile(lambda x: x <= 2*N - 1, natuals))
    num = [(2 - i%4)*4/i for i in ns]
    return sum(num)
# 测试:
print(pi(10))
print(pi(100))
print(pi(1000))
print(pi(10000))
assert 3.04 < pi(10) < 3.05
assert 3.13 < pi(100) < 3.14
assert 3.140 < pi(1000) < 3.141
assert 3.1414 < pi(10000) < 3.1415
print('ok')    