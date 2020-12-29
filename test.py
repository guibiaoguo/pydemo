print("Hello World!")
print(r'''hello,\n
world''')
s1=72

s2=85

r=(s2/s1-1)*100

print('%.1f%%' %r)

print(f'{r:.1f}%')
L = [
    ['Apple', 'Google', 'Microsoft'],
    ['Java', 'Python', 'Ruby', 'PHP'],
    ['Adam', 'Bart', 'Lisa']
]
# 打印Apple:
print(L[0][0])
# 打印Python:
print(L[1][1])
# 打印Lisa:
print(L[2][2])
birth = input('birth')
birth = int(birth)
if birth < 2000:
    print("00前")
else:
    print("00后")
height = 1.75
weight = 120.5
bmi = weight/height**2
if bmi < 18.5:
    print("小明的BMI=%.1f,体重过轻" %bmi)
elif bmi < 25:
    print(f"小明的BMI={bmi:1f},体重正常")
elif bmi < 28:
    print("小明的BMI={.1f},体重过重".format(bmi))
elif bmi < 32:
    print("小明的BMI=%.1f,体重肥胖" %bmi)
else:
    print("小明的BMI=%.1f,体重严重肥胖" %bmi)
names = ['Michael','Bob', 'Tracy']
for name in names:
    print(name)
listname = ['Bart', 'Lisa', 'Adam']
for name in listname:
    print(f"Hell,{name}")
while n <= 1000:
    print(n)
    n = n + 1
print('END')
