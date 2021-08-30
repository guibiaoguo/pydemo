#什么是id？一个对象的id值在CPython解释器里就代表它在内存中的`地址
import copy
a=[1,2,3]
b=a
print(id(a))
print(id(b))
print(id(a)==id(b))

b[0]= 2222
print(a,b)
print(id(a),id(b))
#copy.copy()

c=copy.copy(a)
print(id(c))
print(id(a)==id(c))
c[1]= 222222
print(a,b,c)
print(id(a), id(b), id(c))

#copy.deepcopy()
d=[1,2,[3,4]]
e=copy.deepcopy(d)
d[2][0]=333
print(d)
print(id(d))
