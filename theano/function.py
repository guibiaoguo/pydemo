import numpy as np 
import theano.tensor as T 
import theano

x = T.dmatrix('x')
s = 1/(1 + T.exp(-x)) # logistic or soft step

logistic = theano.function([x], s)
print(logistic(np.arange(4).reshape((2,2))))

# multiply outputs for a function
a, b = T.dmatrices('a', 'b')
diff = a - b
abs_diff = abs(diff)

diff_squared = diff ** 2
f = theano.function([a, b], [diff, abs_diff, diff_squared])
x1,x2,x3= f(
    np.ones((2,2)), # a
    np.arange(4).reshape((2,2))  # b
)
print(x1, x2, x3)

# name for a function
x, y, w = T.dscalars('x', 'y', 'w')
z = (x + y) * w
f = theano.function([x,
                     theano.In(y, value=1),
                     theano.In(w,value=2)],
                    z)

print(f(23))    # 使用默认
print(f(23,1,4)) # 不使用默认
print(f(23,))

