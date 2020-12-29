def fact(n):
    if n == 1:
        return 1
    return n * fact(n -1)
print(fact(1))
print(fact(5))
print(fact(100))
#print(fact(1000))
#尾递归解决栈溢出
def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num - 1, num * product)
print(fact_iter(5, 1))
print(fact_iter(4, 5))
print(fact_iter(3, 20))
print(fact_iter(2, 60))
print(fact_iter(1, 120))

def move(n, a, b, c):
    if n == 1:
        print(a, '-->', c)
    else:
        move(n-1, a, c, b)
        print(a, '-->', c)
        move(n-1, b, a, c)
print(move(3, 'A', 'B', 'C'))
