import numpy

array = numpy.array([[1,2,3],[4,5,6]])
print(array)
print('number of dim:',array.ndim)  # 维度
# number of dim: 2

print('shape :',array.shape)    # 行数和列数
# shape : (2, 3)

print('size:',array.size)   # 元素个数
# size: 6

# 创建数列
a = numpy.array([2,23,4])
print(a)
# 指定数据 dtype
a = numpy.array([2,23,4],dtype=int)
print(a.dtype)
print(a)

a = numpy.array([2,23,4],dtype=float)
print(a.dtype)
print(a)

# 创建全零数组
a = numpy.zeros((3,4))
print(a)
print(a.shape)
# 创建全1数组
a = numpy.ones((3,4),dtype= int)
print(a)
print(a.shape)
# 创建全空数组
a = numpy.empty((3,4))
print(a)
# 创建连续数组 
a = numpy.arange(10, 20, 2)
print(a)
print(a.shape)
# 使用reshape 改变数据的形状
a = numpy.arange(12).reshape((3,4))
print(a)
print(a.shape)
# 使用linspace 创建线段型数据
a = numpy.linspace(1, 10, 20)
print(a)
print(a.shape)
# 使用reshape
a = numpy.linspace(1, 10, 20).reshape((5, 4))
print(a)
print(a.shape)
# 矩阵运算
a = numpy.array([10,20,30,40])
b = numpy.arange(4)
print(a)
print(b)
c = a - b
print(c)
c = a + b
print(c)
c = a * b
print(c)
c = a ** b
print(c)
c = numpy.sin(a)
print(c)

a = numpy.array([[1, 1], [0, 1]])
b = numpy.arange(4).reshape((2, 2))

print(a)
print(b)
# 对应元素相乘
c = a * b
# 矩阵乘法 
# (1 1) (0 2) = 1 * 0 + 1 * 2 = 2
# (1 1) (1 3) = 1 * 1 + 1 * 3 = 4
# (0 1) (0 2) = 0 * 0 + 1 * 2 = 2
# (0 1) (1 3) = 0 * 1 + 1 * 3 = 3

c_dot = numpy.dot(a, b)
print(c)
print(c_dot)
c_dot2 = a.dot(b)
print(c_dot2)

a = numpy.random.random((2,4))
print(a)
print(a.shape)
print(numpy.sum(a))
print(numpy.min(a))
print(numpy.max(a))
#列查找
print(numpy.sum(a, axis=0))
print(numpy.min(a, axis=0))
print(numpy.max(a, axis=0))
#行查找
print(numpy.sum(a, axis=1))
print(numpy.min(a, axis=1))
print(numpy.max(a, axis=1))

a = numpy.arange(2,14).reshape((3,4))
print(a)
#求矩阵最小值索引
print(numpy.argmin(a))
#求矩阵最大值索引
print(numpy.argmax(a))
#求矩阵的均值
print(numpy.mean(a))
print(numpy.average(a))
print(a.mean())
#求矩阵的中位数
print(numpy.median(a))
#累加函数
c = numpy.cumsum(a)
print(c)
print(c.shape)
#累差函数
c = numpy.diff(a)
print(c)
print(c.shape)

#这个函数将所有非零元素的行与列坐标分割开，重构成两个分别关于行和列的矩阵
print(numpy.nonzero(a))
a = numpy.arange(-1, 14).reshape((3, 5))
print(a)
print(numpy.nonzero(a))

a = numpy.arange(14, 2, -1).reshape((3, 4))
print(a)
#排序
print(numpy.sort(a))
#矩阵转置
c = numpy.transpose(a)
print(c)
print(c.shape)
c = a.T
print(a.T)
#clip(Array,Array_min,Array_max)
print(numpy.clip(a,5,9))
#求平均值
print(numpy.mean(a, axis=0))
print(numpy.mean(b, axis=1))
# 索引
a = numpy.arange(3, 15)
print(a)
print(a[3])
a = numpy.arange(3, 15).reshape((3, 4))
print(a)
print(a[2])
print(a[2][1])
print(a[2, 1])
# 切片
print(a[1,:])
print(a[:, 2])
print(a[1, 1: 3])
for row in a:
    print(row)
# 迭代对称 ，翻转
for row in a.T:
    print(row)
#迭代
#展开为1列的数列
print(a.flatten())
#flat 迭代器
for item in a.flat:
    print(item)

#数列合并
a = numpy.array([1, 1, 1])
b = numpy.array([2, 2, 2])
#上下合并
print(numpy.vstack((a, b)))
c = numpy.vstack((a, b))
#属性 shape
print(a.shape, c.shape)
#左右合并
print(numpy.hstack((a, b)))
print(numpy.hstack((c, c)))
#数列转矩阵
print('数列转矩阵')
print(a)
print(a[numpy.newaxis,:])
print(a[numpy.newaxis,:].shape)
print(a[:, numpy.newaxis])
print(a[:, numpy.newaxis].shape)

a = numpy.array([1, 1, 1])[:,numpy.newaxis]
b = numpy.array([2, 2, 2])[:,numpy.newaxis]

c = numpy.vstack((a, b))
d = numpy.hstack((a, b))
print(a)
print(b)
print(c)
print(d)
print(a.shape, b.shape, c.shape, d.shape)

c = numpy.concatenate((a, b, b, a), axis=0)
print(c)
d = numpy.concatenate((a, b, b, a), axis=1)
print(d)

# 矩阵分割
a = numpy.arange(12).reshape((3, 4))
print(a)
# 纵向分割
print(numpy.split(a, 2, axis=1))
# 横向分割
print(numpy.split(a, 3, axis=0))
# 不等量分割
print(numpy.array_split(a, 3, axis=1))
print(numpy.vsplit(a, 3))
print(numpy.hsplit(a, 2))

# copy and deep copy
a = numpy.arange(4)
print(a)

b = a
c = a
d = b

a[0] = 11
print(a)
print(b is a)
print(c is a)
print(d is a)

d[1:3] = [22, 33]
print(a)
print(b)
print(c)

b = a.copy()
print(b)
a[3] = 44
print(a)
print(b)

x_data = numpy.random.rand(100)
x_data_1 = x_data.astype(numpy.float32)
print(x_data)
print(x_data_1)

numpy.random.seed(1)

# fake data
n_data = numpy.ones((100, 2))
x0 = numpy.random.normal(2*n_data, 1)      # class0 x shape=(100, 2)
y0 = numpy.zeros(100)                      # class0 y shape=(100, )
x1 = numpy.random.normal(-2*n_data, 1)     # class1 x shape=(100, 2)
y1 = numpy.ones(100)                       # class1 y shape=(100, )
x = numpy.vstack((x0, x1))  # shape (200, 2) + some noise
y = numpy.hstack((y0, y1))  # shape (200, )
print(x)
print(x.shape)
print(y)
a = numpy.arange(4).reshape(-1,2,2,1)
print(a)