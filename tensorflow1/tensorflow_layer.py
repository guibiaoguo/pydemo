import tensorflow.compat.v1 as tf
import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.disable_v2_behavior()

#添加神经层
def add_layer(inputs, in_size, out_size, activation_funtion = None):
    
    Weights = tf.Variable(tf.random.normal([in_size, out_size]), name="W")
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1, name='b')
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_funtion is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_funtion(Wx_plus_b)

    return outputs

x_data = np.linspace(-1, 1, 300)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape)
y_data = np.square(x_data) - 0.5 + noise

xs = tf.placeholder(tf.float32,[None, 1])
ys = tf.placeholder(tf.float32,[None, 1])

#隐藏层
l1 = add_layer(xs, 1, 10, activation_funtion=tf.nn.relu)
#输出层
prediction = add_layer(l1, 10, 1, activation_funtion=None)

loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    for i in range(1000):
        sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
        if i % 50 == 0:
            print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))