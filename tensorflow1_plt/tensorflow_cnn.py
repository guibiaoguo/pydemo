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

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    intial = tf.constant(0.1, shape=shape)
    return tf.Variable(intial)
def conv2d(x, W):
    # stride [1, x_movement,y_movement , 1]
    # Must have stribe[0] = 1 stribe[3] = 1
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs, keep_prob: 1})
    correct_prediction = tf.equal(tf.argmax(y_pre,1), tf.argmax(v_ys,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys, keep_prob: 1})
    return result

with tf.name_scope('input'):
    xs = tf.placeholder(tf.float32,[None, 784], name='x_input')
    ys = tf.placeholder(tf.float32,[None, 10], name='y_input')
    keep_prob = tf.placeholder(tf.float32)
    x_image = tf.reshape(xs, [-1, 28, 28, 1])
    #print(x_image.shape)
## conv1 layer ##
with tf.name_scope('conv1_layer'):
    W_conv1 = weight_variable([5, 5, 1, 32]) #patch 5*5, in size 1, out size 32
    b_conv1 = bias_variable([32])
    #h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1) # output size 28*28*32
    h_conv1 = tf.layers.conv2d(   # shape (28, 28, 1)
    inputs=x_image,
    filters=32,
    kernel_size=5,
    strides=1,
    padding='same',
    activation=tf.nn.relu
    )
    #h_pool1 = max_pool_2x2(h_conv1)                        # output size 14*14*32
    h_pool1 = tf.layers.max_pooling2d(
    h_conv1,
    pool_size=2,
    strides=2,
    )           # -> (14, 14, 16)
## conv2 layer2 ##
with tf.name_scope('conv2_layer'):
    W_conv2 = weight_variable([5, 5, 32, 64]) #patch 5*5, in size 32, out size 64
    b_conv2 = bias_variable([32])
    #h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2) # output size 28*28*64
    #h_pool2 = max_pool_2x2(h_conv2)                          # output size 7*7*64
    h_conv2 = tf.layers.conv2d(h_pool1, 64, 5, 1, 'same', activation=tf.nn.relu)    # -> (14, 14, 32)
    h_pool2 = tf.layers.max_pooling2d(h_conv2, 2, 2)    # -> (7, 7, 32)
## func1 layer ##
# with tf.name_scope('func1_layer'):
#     W_fc1 = weight_variable([7*7*64, 1024])
#     b_fc1 = bias_variable([1024])
#     #[n_samples, 7, 7, 64]->> [n_sample, 7*7*64]
#     h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
#     h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
#     h_fc1_drop = tf.nn.dropout(h_fc1, rate= 1 - keep_prob)
# ## func2 layer ##
# with tf.name_scope('func2_layer'):
#     W_fc2 = weight_variable([1024, 10])
#     b_fc2 = bias_variable([10])
#     #[n_samples, 7, 7, 64]->> [n_sample, 7*7*64]
#     prediction = tf.layers.dense(ys, 10, tf.nn.softmax)
flat = tf.reshape(h_pool2, [-1, 7*7*64])          # -> (7*7*32, )
prediction = tf.layers.dense(flat, 10)              # output layer
# the error between prediction and real data
with tf.name_scope('loss'):
    #cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),reduction_indices=[1])) # loss
    cross_entropy = tf.losses.softmax_cross_entropy(ys, prediction)
    tf.summary.scalar('loss', cross_entropy)
    
with tf.name_scope('train'):
    train_step=tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter("logs/", sess.graph)
    sess.run(init)

    for i in range(1000):
        batch_xs, batch_ys =  mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys, keep_prob: 0.5})
        if i % 50 == 0:
            print(compute_accuracy(test_x, test_y))
            result = sess.run(merged, feed_dict={xs: batch_xs, ys: batch_ys, keep_prob: 1})
            writer.add_summary(result,i)
    # print 10 predictions from test data
    test_output = sess.run(prediction, {xs: mnist.test.images[2000:4000][:30]})
    pred_y = np.argmax(test_output, 1)
    print(pred_y, 'prediction number')
    print(np.argmax(mnist.test.labels[2000:4000][:30], 1), 'real number')