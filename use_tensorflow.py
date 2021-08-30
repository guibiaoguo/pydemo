import tensorflow.compat.v1 as tf
import numpy as np
import os,matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.disable_v2_behavior()
# create data
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data*0.03 + 0.4
### create tensorflow structure start ###
# Weights 有可能是矩阵，因此大写首字母
Weights = tf.Variable(tf.random.uniform([1], -1.0, 1.0))
biases = tf.Variable(tf.zeros([1]))

y = Weights*x_data + biases
# 计算预测误差
loss = tf.reduce_mean(tf.square(y-y_data))
# 传播误差
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

init = tf.global_variables_initializer()  # 替换成这样就好
### create tensorflow structure end ###

sess = tf.Session()
sess.run(init)          # Very important

for step in range(201):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(Weights), sess.run(biases))

matrix1 = tf.constant([[3, 3]])
matrix2 = tf.constant([[2], [2]])

product = tf.matmul(matrix1, matrix2) # matrix multiply np.dot(matrix1, matrix2)

# method 1
sess = tf.Session()
result = sess.run(product)
print(result)
sess.close()
# [[12]]

# method 2
with tf.Session() as sess:
    result2 = sess.run(product)
    print(result2)
# [[12]]

state = tf.Variable(0, name='counter')
print(state.name)

one = tf.constant(1)

new_value = tf.add(state, one)
update = tf.assign(state, new_value)

init = tf.global_variables_initializer() # must have if define Variable

with tf.Session() as sess:
    sess.run(init)
    for _in in range(3):
        sess.run(update)
        print(sess.run(state))


input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)


output = tf.multiply(input1, input2)

with tf.Session() as sess:
    print(sess.run(output, feed_dict={input1:[7.],input2:[2.0]}))

