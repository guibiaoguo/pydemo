s =set([1,2,3])
print(s)
s = set([1,1,2,2,3,3])
print(s)
s.add(4)
print(s)
s.add(4)
print(s)
s.remove(4)
print(s)
s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
print(f"s1和s2的交集{s1 & s2}")
print(f"s1和s2的并集{s1 | s2}")
a = ['c', 'b', 'a']
print("未执行a.sort() %s" %a)
a.sort()
print(f"执行a.sort()后 {a}")
a = "abc"
print(a)
print(a.replace('a','A'))
