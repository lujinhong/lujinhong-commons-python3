import tensorflow as tf
import numpy as np

#创建tensor的方式
with  tf.Session() as sess:
    # 1、从numpy数组创建
    x1 = np.array([[11, 21, 31],[41, 51, 61]])
    tx1 = tf.convert_to_tensor(x1)
    print(tx1)
    print(sess.run(tx1))

    # 2、从常量创建
    x2 = [[1,2,3],[4,5,6]]
    tx2 = tf.constant(x2)
    print(tx2)
    print(sess.run(tx2))

    # 3、使用一些函数
    tx3 = tf.zeros((2,4))
    print(tx3)
    print(sess.run(tx3))
    tx3 = tf.ones((2,4))
    print(tx3)
    print(sess.run(tx3))
    tx3 = tf.random_normal((2,4))
    print(tx3)
    print(sess.run(tx3))
    zeros = tf.zeros(tx2.shape) #创建tx2同样形状的张量
    print(zeros)
    print(sess.run(zeros))

    # 4、placeholder
    tx4 = tf.placeholder(tf.float32)
    print(tx4)
    print(sess.run(tx4,feed_dict={tx4:[[1.,2.],[2.,4.]]}))

    # 5、变量
    # 6、SparseTensor

    #张量的阶
    print(sess.run(tf.rank(tx3))) #2
    #张量的shape
    print(sess.run(tf.shape(tx3)))


