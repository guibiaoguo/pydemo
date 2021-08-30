import tensorflow.compat.v1 as tf
import numpy as np
import os
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.disable_v2_behavior()

# Hyper parameters
N_SAMPLES = 20
N_HIDDEN = 100
LR = 0.01

digits = load_digits()
X = digits.data
y = digits.target
y = LabelBinarizer().fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)
print(X_train, X_test, y_train, y_test)
#添加神经层
# def add_layer(inputs, in_size, out_size, n_layer, activation_funtion = None):
#     layer_name = f"layer{n_layer}"
#     with tf.name_scope('layer'):
#         with tf.name_scope('Weights'):
#             Weights = tf.Variable(tf.random.normal([in_size, out_size]), name="W")
#             tf.summary.histogram(layer_name+'/Weights', Weights)
#         with tf.name_scope('biases'):
#             biases = tf.Variable(tf.zeros([1, out_size]) + 0.1, name='b')
#             tf.summary.histogram(layer_name+'/biases', biases)
#         with tf.name_scope('Wx_plus_b'):
#             Wx_plus_b = tf.matmul(inputs, Weights) + biases
#             Wx_plus_b = tf.nn.dropout(Wx_plus_b,rate= 1-keep_prob)
#         if activation_funtion is None:
#             outputs = Wx_plus_b
#         else:
#             outputs = activation_funtion(Wx_plus_b)
#             tf.summary.histogram(layer_name+'/outputs', outputs)
#         return outputs

with tf.name_scope('input'):
    keep_prob = tf.placeholder(tf.float32)
    xs = tf.placeholder(tf.float32,[None, 64], name='x_input') # 8*8
    ys = tf.placeholder(tf.float32,[None, 10], name='y_input')
    tf_is_training = tf.placeholder(tf.bool, None)  # to control dropout when training and testing
with tf.name_scope('overfitting_Net'):
#隐藏层
    o1 = tf.layers.dense(xs, N_HIDDEN, tf.nn.relu)
    #输出层
    o2 = tf.layers.dense(o1, N_HIDDEN, tf.nn.relu)
    o_out = tf.layers.dense(o2, 10)

    o_loss = tf.losses.mean_squared_error(ys, o_out)
with tf.name_scope('o_train'):
    o_train = tf.train.AdamOptimizer(LR).minimize(o_loss)
with tf.name_scope('dropout_Net'):
# dropout net
    d1 = tf.layers.dense(xs, N_HIDDEN, tf.nn.relu)
    d1 = tf.layers.dropout(d1, rate=0.5, training=tf_is_training)   # drop out 50% of inputs
    d2 = tf.layers.dense(d1, N_HIDDEN, tf.nn.relu)
    d2 = tf.layers.dropout(d2, rate=0.5, training=tf_is_training)   # drop out 50% of inputs
    d_out = tf.layers.dense(d2, 10)
    d_loss = tf.losses.mean_squared_error(ys, d_out)
with tf.name_scope('d_train'):
    d_train = tf.train.AdamOptimizer(LR).minimize(d_loss)
# the error between prediction and real data
tf.summary.histogram('o1', o1)
tf.summary.histogram('o2', o2)
tf.summary.histogram('o_out', o_out)
tf.summary.histogram('d1', o1)
tf.summary.histogram('d2', o2)
tf.summary.histogram('d_out', d_out)
tf.summary.scalar('O_loss', o_loss)     # add loss to scalar summary
tf.summary.scalar('D_loss', d_loss)     # add loss to scalar summary
init = tf.global_variables_initializer()

with tf.Session() as sess:
    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter("logs/train", sess.graph)
    test_writer = tf.summary.FileWriter("logs/test", sess.graph)
    sess.run(init)
     # train, set is_training=True

    for i in range(1000):
        if i % 50 == 0:
            sess.run([o_train, d_train], {xs: X_train, ys: y_train, tf_is_training: True}) 
            o_loss_, d_loss_, o_out_, d_out_ = sess.run(
            [o_loss, d_loss, o_out, d_out], {xs: X_test, ys: y_test, tf_is_training: False} # test, set is_training=False
            )
            print(o_loss_, d_loss_, o_out_, d_out_)
            #print(compute_accuracy(mnist.test.images, mnist.test.labels))
            train_result = sess.run(merged, feed_dict={xs: X_train, ys: y_train, tf_is_training: False})
            test_result = sess.run(merged, feed_dict={xs: X_test, ys: y_test, tf_is_training: False})
            train_writer.add_summary(train_result, i)
            test_writer.add_summary(test_result, i)