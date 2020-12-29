def my_abs(x):
    if not isinstance(x,(int,float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
print(my_abs(-99))
#print(my_abs('A'))
import math
def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx,ny
x,y = move(100, 100, 60, math.pi / 6)
print(x,y)
r = move(100, 100, 60, math.pi / 6)
print(r)
print(math.sqrt(2))

def quadratic(a, b, c):
    if not isinstance(a,(int,float)) and not isinstance(b,(int,float)) and not isinstance(c,(int,float)):
        raise TypeError('bad operand type')
    delt = b**2 - 4*a*c
    if delt >= 0:
        x = (-b + math.sqrt(delt)/(2*a))
        y = (-b - math.sqrt(delt)/(2*a))
        return x,y
    else:
        return('无实根')
print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))
if quadratic(2, 3, 1) != (-0.5, -1.0):
    print('测试失败')
elif quadratic(1, 3, -4) != (1.0, -4.0):
    print('测试失败')
else:
    print('测试成功')    
