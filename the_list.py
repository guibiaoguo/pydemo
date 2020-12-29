for x in range(10):
    print(x)
a = [1, 2, 3]
b = [2, 3, 4]
a.extend(b)

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