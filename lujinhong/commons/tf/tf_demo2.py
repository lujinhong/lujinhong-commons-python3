import tensorflow as tf
import numpy as np

a = np.float32(np.random.rand(1))
b = tf.ones([1])

c = a + b

tf.initialize_all_variables

with tf.Session() as sess:
    print(sess.run(c))
    print(a, sess.run(b), sess.run(c))
