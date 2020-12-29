d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)
for value in d.values():
    print(value)
for ch in 'ABC':
    print(ch)

from collections.abc import Iterable
 
print(isinstance("abc", Iterable))
print(isinstance([1,2,3],Iterable))
print(isinstance(123,Iterable))

for i, value in enumerate(['A','B','C']):
    print(i,value)
for x,y in [(1, 1), (2, 4), (3, 6)]:
    print(x, y)    

def findMinAndMax(L):
    if (len(L) == 0):
        return None,None
    min=L[0]
    max=L[0]
for n in L:
        if n < min:
            min = n
        if n> max:
            max = n    
    return min,max
 # 测试
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')   