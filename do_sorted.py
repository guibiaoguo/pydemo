import os,json

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

dict3 = {}
with open(os.path.join("book/大雄5","diff.json"),'r',encoding='utf-8', errors='ignore') as f:
    dict1 = json.load(f)
    print(dict1)
    print(len(dict1))
    for k,v in sorted(dict1.items()):
        dict3[k] = v
with open(f"book/大雄5/diff.json",'w',encoding='utf-8') as f:
    json.dump(dict3, f, ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
