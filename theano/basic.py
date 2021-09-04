import numpy as np 
import theano.tensor as T 
from theano import function

# basic
x = T.dscalar('x')  # 建立 x 的容器
y = T.dscalar('y')  # 建立 y 的容器
z = x+y     #  建立方程

# 使用 function 定义 theano 的方程, 
# 将输入值 x, y 放在 [] 里,  输出值 z 放在后面
f = function([x, y], z)  

print(f(2,3))  # 将确切的 x, y 值放入方程中
# 5.0

# to pretty-print the function
from theano import pp
print(pp(z)) 
# (x + y)

# how about martix

x = T.dmatrix('x')
y = T.dmatrix('y')

z = x + y
f = function([x, y], z)
print(f(
        np.arange(12).reshape((3,4)), 
        10*np.ones((3,4))
        )
      )