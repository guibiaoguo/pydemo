from functools import reduce
from collections import ChainMap

d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d['Michael'])
d['Adam'] = 67
print(d['Adam'])
d['Jack'] = 90
print(d['Jack'])
d['Jack'] = 88
print(d['Jack'])
print(d.get('Thomas'))
print(d.get('Thomas',-2))
print(d.pop('Bob'))
print(d)

li = [{'a': '1','c':'2'}, {'a':'2','b': '2','c':'3'}, {'a': '1','c':'2'}, {'a': '1','c':'2','d':'3'}]

def deleteDuplicate(li):
    func = lambda x, y: x if y in x else x + [y]
    li = reduce(func, [[], ] + li)
    return li

print(deleteDuplicate(li))

def deleteDuplicateSet(li):
    temp_list = list(set([str(i) for i in li]))
    li=[eval(i) for i in temp_list]
    return li

print("过滤所有重复数据")
print(deleteDuplicateSet(li))

print([{'a':{}}, ] + li)
print({'y':1})
print([dict(t) for t in set([tuple(d.items()) for d in li])])
print("通过固定字段过滤数据")

def deleteDuplicateKey(li,key):
    def func(x,y):
        if(y.get(key) in x):
            return x
        else:
            x[y.get(key)] = y
        return x
    li = reduce(func, [{}, ] + li)
    return li

print(deleteDuplicateKey(li,'a'))