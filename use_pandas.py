import pandas
import numpy
import matplotlib.pyplot as plt

#Series 索引在左 值在右边
s = pandas.Series([1, 3, 6,numpy.nan, 44, 1])

print(s)
# DataFrame 表格型
dates = pandas.date_range('20210101', periods=6)
print(dates)
df = pandas.DataFrame(numpy.random.randn(6, 4), index=dates, columns=['a', 'b', 'c', 'd'])
print(df)

print(df['b'])

df1 = pandas.DataFrame(numpy.arange(12).reshape((3, 4)))
print(df1)

df2 = pandas.DataFrame({'A' : 1.,
                    'B' : pandas.Timestamp('20130102'),
                    'C' : pandas.Series(1,index=list(range(4)),dtype='float32'),
                    'D' : numpy.array([3] * 4,dtype='int32'),
                    'E' : pandas.Categorical(["test","train","test","train"]),
                    'F' : 'foo'})

print(df2)
print(df2.dtypes)
print(df2.index)
print(df2.columns)
print(df2.values)
print(df2.describe())
print(df2.T)

print(df2.sort_index(axis=1, ascending=False))
print(df2.sort_index(axis=0, ascending=False))

print(df2.sort_values(by= 'E'))

dates = pandas.date_range('20130101', periods=6)
df = pandas.DataFrame(numpy.arange(24).reshape((6,4)),index=dates, columns=['A','B','C','D'])
print(df)

#简单的筛选

print(df['A'])
print(df.A)
# 跨行和跨列
print(df[0:3])
print(df['20130102':'20130104'])

#根据标签选择
print(df.loc['20130102'])

print(df.loc[:, ['A', 'B']])

print(df.loc['20130102', ['A', 'B']])

#根据位置选择
print(df.iloc[3, 1])
print(df.iloc[3:5, 1:3])
print(df.iloc[[1, 3, 5],1:3])
#混合
#print(df.ix[:3,['A','C']])

#判断
print(df[df.A>8])

#设置值
df.iloc[2, 2] = 111
df.loc['20130101', 'B'] = 222
print(df)

df.B[df.A>4] = 0
print(df)
df['F'] = numpy.nan
print(df)
df['E'] = pandas.Series([1,2,3,4,5,6], index=pandas.date_range('20130101',periods=6))
print(df)

dates = pandas.date_range('20130101', periods=6)
df = pandas.DataFrame(numpy.arange(24).reshape((6,4)),index=dates, columns=['A','B','C','D'])
df.iloc[0,1] = numpy.nan
df.iloc[1,2] = numpy.nan
print(df)
# 0: 对行进行操作; 1: 对列进行操作
# 'any': 只要存在 NaN 就 drop 掉; 'all': 必须全部是 NaN 才 drop
print(df.dropna(axis= 0, how= 'any'))
print(df.fillna(value= 0))
print(df.isnull())
print(numpy.any(df.isnull()) == True)

data = pandas.read_csv('student.csv')
print(data)
data.to_pickle('student.pickle')

#定义资料集
df1 = pandas.DataFrame(numpy.ones((3,4))*0, columns=['a','b','c','d'])
df2 = pandas.DataFrame(numpy.ones((3,4))*1, columns=['a','b','c','d'])
df3 = pandas.DataFrame(numpy.ones((3,4))*2, columns=['a','b','c','d'])
print(df1)
print(df2)
print(df3)

#concat纵向合并
res = pandas.concat([df1, df2, df3], axis=0)

#打印结果
print(res)
res = pandas.concat([df1, df2, df3], axis=0, ignore_index=True)
print(res)

#定义资料集
df1 = pandas.DataFrame(numpy.ones((3,4))*0, columns=['a','b','c','d'], index=[1,2,3])
df2 = pandas.DataFrame(numpy.ones((3,4))*1, columns=['b','c','d','e'], index=[2,3,4])
print(df1)
print(df2)
#纵向"外"合并df1与df2
res = pandas.concat([df1, df2], axis=0, join='outer')

print(res)

res = pandas.concat([df1, df2], axis=0, join='inner')
print(res)
res = pandas.concat([df1, df2], axis=0, join='inner', ignore_index=True)
print(res)

#定义资料集
df1 = pandas.DataFrame(numpy.ones((3,4))*0, columns=['a','b','c','d'], index=[1,2,3])
df2 = pandas.DataFrame(numpy.ones((3,4))*1, columns=['b','c','d','e'], index=[2,3,4])
# join_axes 废弃了
#依照`df1.index`进行横向合并
#res = pandas.concat([df1, df2], axis=1, join_axes=[df1.index])

#打印结果
#print(res)
print(df1)
print(df2)
res = pandas.concat([df1, df2], axis=1)
print(res)

#定义资料集
df1 = pandas.DataFrame(numpy.ones((3,4))*0, columns=['a','b','c','d'])
df2 = pandas.DataFrame(numpy.ones((3,4))*1, columns=['a','b','c','d'])
df3 = pandas.DataFrame(numpy.ones((3,4))*1, columns=['a','b','c','d'])
s1 = pandas.Series([1,2,3,4], index=['a','b','c','d'])
print(df1)
print(df2)
print(df3)
print(s1)
#将df2合并到df1的下面，以及重置index，并打印出结果
res = df1.append(df2, ignore_index=True)
print(res)
#     a    b    c    d
# 0  0.0  0.0  0.0  0.0
# 1  0.0  0.0  0.0  0.0
# 2  0.0  0.0  0.0  0.0
# 3  1.0  1.0  1.0  1.0
# 4  1.0  1.0  1.0  1.0
# 5  1.0  1.0  1.0  1.0

#合并多个df，将df2与df3合并至df1的下面，以及重置index，并打印出结果
res = df1.append([df2, df3], ignore_index=True)
print(res)
#     a    b    c    d
# 0  0.0  0.0  0.0  0.0
# 1  0.0  0.0  0.0  0.0
# 2  0.0  0.0  0.0  0.0
# 3  1.0  1.0  1.0  1.0
# 4  1.0  1.0  1.0  1.0
# 5  1.0  1.0  1.0  1.0
# 6  1.0  1.0  1.0  1.0
# 7  1.0  1.0  1.0  1.0
# 8  1.0  1.0  1.0  1.0

#合并series，将s1合并至df1，以及重置index，并打印出结果
res = df1.append(s1, ignore_index=True)
print(res)
#     a    b    c    d
# 0  0.0  0.0  0.0  0.0
# 1  0.0  0.0  0.0  0.0
# 2  0.0  0.0  0.0  0.0
# 3  1.0  2.0  3.0  4.0

#定义资料集并打印出
left = pandas.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                             'A': ['A0', 'A1', 'A2', 'A3'],
                             'B': ['B0', 'B1', 'B2', 'B3']})
right = pandas.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'],
                              'C': ['C0', 'C1', 'C2', 'C3'],
                              'D': ['D0', 'D1', 'D2', 'D3']})

print(left)
#    A   B key
# 0  A0  B0  K0
# 1  A1  B1  K1
# 2  A2  B2  K2
# 3  A3  B3  K3

print(right)
#    C   D key
# 0  C0  D0  K0
# 1  C1  D1  K1
# 2  C2  D2  K2
# 3  C3  D3  K3

#依据key column合并，并打印出
res = pandas.merge(left, right, on='key')

print(res)
# A   B key   C   D
# 0  A0  B0  K0  C0  D0
# 1  A1  B1  K1  C1  D1
# 2  A2  B2  K2  C2  D2
# 3  A3  B3  K3  C3  D3

#定义资料集并打印出
left = pandas.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                      'key2': ['K0', 'K1', 'K0', 'K1'],
                      'A': ['A0', 'A1', 'A2', 'A3'],
                      'B': ['B0', 'B1', 'B2', 'B3']})
right = pandas.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                       'key2': ['K0', 'K0', 'K0', 'K0'],
                       'C': ['C0', 'C1', 'C2', 'C3'],
                       'D': ['D0', 'D1', 'D2', 'D3']})

print(left)
#    A   B key1 key2
# 0  A0  B0   K0   K0
# 1  A1  B1   K0   K1
# 2  A2  B2   K1   K0
# 3  A3  B3   K2   K1

print(right)
#    C   D key1 key2
# 0  C0  D0   K0   K0
# 1  C1  D1   K1   K0
# 2  C2  D2   K1   K0
# 3  C3  D3   K2   K0

#依据key1与key2 columns进行合并，并打印出四种结果['left', 'right', 'outer', 'inner']
res = pandas.merge(left, right, on=['key1', 'key2'], how='inner')
print(res)
#    A   B key1 key2   C   D
# 0  A0  B0   K0   K0  C0  D0
# 1  A2  B2   K1   K0  C1  D1
# 2  A2  B2   K1   K0  C2  D2

res = pandas.merge(left, right, on=['key1', 'key2'], how='outer')
print(res)
#     A    B key1 key2    C    D
# 0   A0   B0   K0   K0   C0   D0
# 1   A1   B1   K0   K1  NaN  NaN
# 2   A2   B2   K1   K0   C1   D1
# 3   A2   B2   K1   K0   C2   D2
# 4   A3   B3   K2   K1  NaN  NaN
# 5  NaN  NaN   K2   K0   C3   D3

res = pandas.merge(left, right, on=['key1', 'key2'], how='left')
print(res)
#    A   B key1 key2    C    D
# 0  A0  B0   K0   K0   C0   D0
# 1  A1  B1   K0   K1  NaN  NaN
# 2  A2  B2   K1   K0   C1   D1
# 3  A2  B2   K1   K0   C2   D2
# 4  A3  B3   K2   K1  NaN  NaN

res = pandas.merge(left, right, on=['key1', 'key2'], how='right')
print(res)
#     A    B key1 key2   C   D
# 0   A0   B0   K0   K0  C0  D0
# 1   A2   B2   K1   K0  C1  D1
# 2   A2   B2   K1   K0  C2  D2
# 3  NaN  NaN   K2   K0  C3  D3

#定义资料集并打印出
df1 = pandas.DataFrame({'col1':[0,1], 'col_left':['a','b']})
df2 = pandas.DataFrame({'col1':[1,2,2],'col_right':[2,2,2]})

print(df1)
#   col1 col_left
# 0     0        a
# 1     1        b

print(df2)
#   col1  col_right
# 0     1          2
# 1     2          2
# 2     2          2

# 依据col1进行合并，并启用indicator=True，最后打印出
res = pandas.merge(df1, df2, on='col1', how='outer', indicator=True)
print(res)
#   col1 col_left  col_right      _merge
# 0   0.0        a        NaN   left_only
# 1   1.0        b        2.0        both
# 2   2.0      NaN        2.0  right_only
# 3   2.0      NaN        2.0  right_only

# 自定indicator column的名称，并打印出
res = pandas.merge(df1, df2, on='col1', how='outer', indicator='indicator_column')
print(res)
#   col1 col_left  col_right indicator_column
# 0   0.0        a        NaN        left_only
# 1   1.0        b        2.0             both
# 2   2.0      NaN        2.0       right_only
# 3   2.0      NaN        2.0       right_only

#定义资料集并打印出
left = pandas.DataFrame({'A': ['A0', 'A1', 'A2'],
                     'B': ['B0', 'B1', 'B2']},
                     index=['K0', 'K1', 'K2'])
right = pandas.DataFrame({'C': ['C0', 'C2', 'C3'],
                      'D': ['D0', 'D2', 'D3']},
                     index=['K0', 'K2', 'K3'])

print(left)
#     A   B
# K0  A0  B0
# K1  A1  B1
# K2  A2  B2

print(right)
#     C   D
# K0  C0  D0
# K2  C2  D2
# K3  C3  D3

#依据左右资料集的index进行合并，how='outer',并打印出
res = pandas.merge(left, right, left_index=True, right_index=True, how='outer')
print(res)
#      A    B    C    D
# K0   A0   B0   C0   D0
# K1   A1   B1  NaN  NaN
# K2   A2   B2   C2   D2
# K3  NaN  NaN   C3   D3

#依据左右资料集的index进行合并，how='inner',并打印出
res = pandas.merge(left, right, left_index=True, right_index=True, how='inner')
print(res)
#     A   B   C   D
# K0  A0  B0  C0  D0
# K2  A2  B2  C2  D2

#定义资料集
boys = pandas.DataFrame({'k': ['K0', 'K1', 'K2'], 'age': [1, 2, 3]})
girls = pandas.DataFrame({'k': ['K0', 'K0', 'K3'], 'age': [4, 5, 6]})

#使用suffixes解决overlapping的问题
res = pandas.merge(boys, girls, on='k', suffixes=['_boy', '_girl'], how='inner')
print(res)
#    age_boy   k  age_girl
# 0        1  K0         4
# 1        1  K0         5

# 随机生成1000个数据
data = pandas.Series(numpy.random.randn(1000),index=numpy.arange(1000))
 
# 为了方便观看效果, 我们累加这个数据
data.cumsum()

# pandas 数据可以直接观看其可视化形式
data.plot()

plt.show()

data = pandas.DataFrame(
    numpy.random.randn(1000,4),
    index=numpy.arange(1000),
    columns=list("ABCD")
    )
data.cumsum()
data.plot()
plt.show()

ax = data.plot.scatter(x='A',y='B',color='DarkBlue',label='Class1')
# 将之下这个 data 画在上一个 ax 上面
data.plot.scatter(x='A',y='C',color='LightGreen',label='Class2',ax=ax)
plt.show()