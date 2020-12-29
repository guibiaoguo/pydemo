print(sorted([36, 5, -12, 9, -21]))
print(sorted([36, 5, -12, 9, -21], key=abs))
print(sorted(['bob', 'about', 'Zoo', 'Credit']))
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower))
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True))
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
print(L[0][1])
def by_name(t):
    return t[0]
def by_score(t):
    return -t[1]

L1 = sorted(L, key=by_name)  
L2 = sorted(L, key=by_score)
print(L1)
print(L2)
