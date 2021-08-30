import tensorflow.compat.v1 as tf
import numpy as np
import os
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.disable_v2_behavior()

digits = load_digits()
X = digits.data
y = digits.target
y = LabelBinarizer().fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)
print(X_train, X_test, y_train, y_test)
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
            Wx_plus_b = tf.nn.dropout(Wx_plus_b,rate= 1-keep_prob)
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
    keep_prob = tf.placeholder(tf.float32)
    xs = tf.placeholder(tf.float32,[None, 64], name='x_input') # 8*8
    ys = tf.placeholder(tf.float32,[None, 10], name='y_input')

#隐藏层
l1 = add_layer(xs, 64, 100, n_layer='l1', activation_funtion=tf.nn.tanh)
#输出层
prediction = add_layer(l1, 100, 10, n_layer='l2', activation_funtion=tf.nn.softmax)
# the error between prediction and real data
with tf.name_scope('loss'):
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),
reduction_indices=[1])) # loss
    tf.summary.scalar('loss', cross_entropy)

with tf.name_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter("logs/train", sess.graph)
    test_writer = tf.summary.FileWriter("logs/test", sess.graph)
    sess.run(init)

    for i in range(1000):
        if i % 50 == 0:
            sess.run(train_step,feed_dict={xs: X_train, ys: y_train, keep_prob: 0.5})
            #print(compute_accuracy(mnist.test.images, mnist.test.labels))
            train_result = sess.run(merged, feed_dict={xs: X_train, ys: y_train, keep_prob: 1})
            test_result = sess.run(merged, feed_dict={xs: X_test, ys: y_test, keep_prob: 1})
            train_writer.add_summary(train_result, i)
            test_writer.add_summary(test_result, i)