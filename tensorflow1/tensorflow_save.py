import tensorflow.compat.v1 as tf
import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.disable_v2_behavior()

W = tf.Variable([[1,2,3],[3,4,5]], dtype= tf.float32, name= "weight")
b = tf.Variable([[1,2,3]], dtype= tf.float32, name= "biases")

init = tf.global_variables_initializer()

saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init)
    save_path = saver.save(sess, "my_net/save_net.ckpt")
    print("Save to path: ", save_path)