import tensorflow.compat.v1 as tf
import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.disable_v2_behavior()

#添加神经层
def add_layer(inputs, in_size, out_size, n_layer, activation_funtion = None):
    layer_name = f"layer{n_layer}"
    with tf.name_scope('layer'):
        with tf.name_scope('Weights'):
            Weights = tf.Variable(tf.random.normal([in_size, out_size]), name="W")
            tf.summary.histogram(layer_name+'/Weights', Weights)
        with tf.name_scope('biases'):
            biases = tf.Variable(tf.zeros([1, out_size]) + 0.1, name='b')
            tf.summary.histogram(layer_name+'/biases', biases)
        with tf.name_scope('Wx_plus_b'):
            Wx_plus_b = tf.matmul(inputs, Weights) + biases
        if activation_funtion is None:
            outputs = Wx_plus_b
        else:
            outputs = activation_funtion(Wx_plus_b)
            tf.summary.histogram(layer_name+'/outputs', outputs)
        return outputs
# Make up some data
x_data = np.linspace(-1, 1, 300)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape)
y_data = np.square(x_data) - 0.5 + noise

with tf.name_scope('input'):
    xs = tf.placeholder(tf.float32,[None, 1], name='x_input')
    ys = tf.placeholder(tf.float32,[None, 1], name='y_input')

#隐藏层
l1 = add_layer(xs, 1, 10, n_layer=1, activation_funtion=tf.nn.relu)
#输出层
prediction = add_layer(l1, 10, 1, n_layer=2, activation_funtion=None)
with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]))
    tf.summary.scalar('loss', loss)
with tf.name_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter("logs/", sess.graph)
    sess.run(init)

    for i in range(1000):
        sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
        if i % 50 == 0:
            result = sess.run(merged, feed_dict={xs: x_data, ys: y_data})
            writer.add_summary(result,i)