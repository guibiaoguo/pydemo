sum = 0
n = 90
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)
n =1
while n <= 100:
    if n > 10:
        break
    print(n)
    n = n + 1
print('END')
n = 0
while n < 10:
    n = n + 1
    if n % 2 == 0:
        continue
    print(n)