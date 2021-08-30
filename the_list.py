# -*- coding: utf-8 -*-

import random

for x in range(10):
    print(x)
a = [1, 2, 3]
b = [2, 3, 4]
a.extend(b)
a.append(5)
print(a)
print(b)
print(a)

c = set(a)
print(c)
d = list(c)
print(d)

for i,x in enumerate(range(10)):
    print(f'{i}:{x}')
x1 = 'ABC'
y1 = 'XYZ'
e = [x + y for x in x1 for y in y1]
print(e)

bookSourceList = ['http://www.xssk.la', 'https://www.dizhu.org', 'http://www.nanrenshu1.com。', 'https://shuapi.jiaston.com#2', 'http://www.zhaishuyuan.com', 'https://www.lightnovel.cn', 'http://www.bllyxw.com', 'https://wap.26ksw.com', 'http://api.gdugm.cn', 'https://m.juyit.com', 'https://www.qingdou.net']
print('http://www.xssk.la' in bookSourceList)
print(not True)
print("222".find('') > -1)
print('' != '')
print(isinstance(None, str))
print(random.randint(0,1000))
list1=[]
list1.insert(0,[3])
list1.insert(0,4)
print(list)
list1=[]
for i in range(10):
    list1.append([])
    for j in range(5):
        list1[i].append(j)
print(list1)
list2=[[1],[1,2],[1,2,3],[1,2,3,4],[1,2,3,4,5],[1,2,3,4,5,6],[1,2,3,4,5,6,7],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8,9]]
print(list(zip(*list2)))
a = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

b = list(map(list, zip(*list2)))
print(b)
list4=[]
for x in list2:
    list5=[]
    for j,y in enumerate(x):
        list4.append([])
print(list4)
print([[] for x in range(4)])
print('失效'.find('失效') > -1)
list5=[1,2]
print(list5.pop())
print(list5.pop())
print(len(list5))
tmap = {}
print(tmap.get('$word'))
t="动"
print(t[:1])
print(t[1:])
tkey=''
if tkey:
    print('aa')
else:
    print('bb')