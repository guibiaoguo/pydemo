import tensorflow.compat.v1 as tf
import numpy as np
import os
import os,matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.disable_v2_behavior()

from tensorflow.core.example import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
test_x = mnist.test.images[:2000]
test_y = mnist.test.labels[:2000]

#添加神经层 tf.layers.dense
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

def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    correct_prediction = tf.equal(tf.argmax(y_pre,1), tf.argmax(v_ys,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys})
    return result

with tf.name_scope('input'):
    xs = tf.placeholder(tf.float32,[None, 28*28], name='x_input')
    ys = tf.placeholder(tf.float32,[None, 10], name='y_input')

#隐藏层
# l1 = add_layer(xs, 784, 10, n_layer=1, activation_funtion=tf.nn.tanh)
l1 = tf.layers.dense(xs, 10, tf.nn.tanh)
#输出层
#prediction = add_layer(l1, 10, 10, n_layer=2, activation_funtion=tf.nn.softmax)
prediction = tf.layers.dense(l1, 10, tf.nn.softmax)
# the error between prediction and real data
with tf.name_scope('loss'):
    # cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),reduction_indices=[1])) # loss
    cross_entropy = tf.losses.softmax_cross_entropy(ys, prediction)
    tf.summary.scalar('loss', cross_entropy)

with tf.name_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.7).minimize(cross_entropy)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter("logs/", sess.graph)
    sess.run(init)

    for i in range(1000):
        batch_xs, batch_ys =  mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys})
        if i % 50 == 0:
            print(compute_accuracy(mnist.test.images[:2000], mnist.test.labels[:2000]))
            result = sess.run(merged, feed_dict={xs: batch_xs, ys: batch_ys})
            writer.add_summary(result,i)
    test_output = sess.run(prediction, {xs: mnist.test.images[2000:4000][:30]})
    pred_y = np.argmax(test_output, 1)
    print(pred_y, 'prediction number')
    print(np.argmax(mnist.test.labels[2000:4000][:30], 1), 'real number')