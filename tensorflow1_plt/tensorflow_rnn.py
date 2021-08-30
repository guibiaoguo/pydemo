import tensorflow.compat.v1 as tf
import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.disable_v2_behavior()

from tensorflow.core.example import input_data

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
test_x = mnist.test.images[:2000]
test_y = mnist.test.labels[:2000]
#hyperparameters
lr = 0.001
training_iters = 100000
batch_size = 128

n_inputs = 28 #MNIST data input (img shape: 28*28)
n_steps = 28
n_hidden_units = 128
n_classes = 10 #MNIST classes (0-9 digits)
LR = 0.01               # learning rate
#tf Graph input
x = tf.placeholder(tf.float32,[None, n_steps * n_inputs])
y = tf.placeholder(tf.float32,[None, n_classes])
image = tf.reshape(x, [-1, n_steps, n_inputs])     
# Define weights
# weights = {
#     #shape (28,128)
#     'in':tf.Variable(tf.random.normal([n_inputs, n_hidden_units])),
#     #shape (128,10)
#     'out':tf.Variable(tf.random.normal([n_hidden_units, n_classes]))
# }

# biases = {
#     # shape (128, )
#     'in':tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),
#     # shape (10, )
#     'out':tf.Variable(tf.constant(0.1, shape=[n_classes, ]))
# }

# def RNN(X, weights, biases):
#     # hidden layer for inut to cell
#     ##############################
#     # X (128 batch, 28 steps, 28 input)
#     # ==> (128*28, 28 inputs)
#     X = tf.reshape(X, [-1, n_inputs])

#     X_in = tf.matmul(X, weights['in']) + biases['in']
#     #X_in ==>(128batch*28 steps,128 hidden)
#     X_in = tf.reshape(X_in, [-1, n_steps, n_hidden_units])

#     #cell
#     ###################################################
#     # 使用 basic LSTM Cell.
#     lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(n_hidden_units, forget_bias=1.0, state_is_tuple=True)
#     init_state = lstm_cell.zero_state(batch_size, dtype=tf.float32) # 初始化全零 state

#     outputs, final_state = tf.nn.dynamic_rnn(lstm_cell, X_in, initial_state=init_state, time_major=False)
#     # hidden layer for output as the final results
#     ##############################################
#     results = tf.matmul(final_state[1], weights['out']) + biases['out']
    
#     return results

# pred = RNN(x, weights, biases)
# cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
# train_op = tf.train.AdamOptimizer(lr).minimize(cost)

# correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
# accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# RNN
rnn_cell = tf.nn.rnn_cell.LSTMCell(num_units=64)
outputs, (h_c, h_n) = tf.nn.dynamic_rnn(
    rnn_cell,                   # cell you have chosen
    image,                      # input
    initial_state=None,         # the initial hidden state
    dtype=tf.float32,           # must given if set initial_state = None
    time_major=False,           # False: (batch, time step, input); True: (time step, batch, input)
)
output = tf.layers.dense(outputs[:, -1, :], 10)              # output based on the last output step

loss = tf.losses.softmax_cross_entropy(onehot_labels=y, logits=output)           # compute cost
train_op = tf.train.AdamOptimizer(LR).minimize(loss)

accuracy = tf.metrics.accuracy(          # return (acc, update_op), and create 2 local variables
    labels=tf.argmax(y, axis=1), predictions=tf.argmax(output, axis=1),)[1]

# init= tf.initialize_all_variables() # tf 马上就要废弃这种写法
# 替换成下面的写法:
init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())

with tf.Session() as sess:
    sess.run(init_op)
    step = 0
    while step * batch_size < training_iters:
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        #batch_xs = batch_xs.reshape([batch_size, n_steps, n_inputs])
        sess.run([train_op], feed_dict={
            x: batch_xs,
            y: batch_ys,
        })
        if step % 20 == 0:
            print(sess.run(accuracy, feed_dict={
            x: batch_xs,
            y: batch_ys,
        }))
        step += 1

    # print 10 predictions from test data
    test_output = sess.run(output, {x: mnist.test.images[2000:4000][30:60]})
    pred_y = np.argmax(test_output, 1)
    print(pred_y, 'prediction number')
    print(np.argmax(mnist.test.labels[2000:4000][30:60], 1), 'real number')