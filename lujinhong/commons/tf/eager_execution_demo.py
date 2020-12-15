# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2019年03月21日 15:49
    PROJECT: lujinhong-commons-python3
DESCRIPTION: 一个使用eager_execution做线性拟合的完整例子。
"""

import tensorflow as tf

# 1、样本数据
# A toy dataset of points around 3 * x + 2
NUM_EXAMPLES = 2000
training_inputs = tf.random.normal([NUM_EXAMPLES])
noise = tf.random.normal([NUM_EXAMPLES])
training_outputs = training_inputs * 3 + 2 + noise


# 2.1 定义模型结构
class Model(tf.keras.Model):
    def __init__(self):
        super(Model, self).__init__()
        self.W = tf.Variable(5., name='weight')
        self.B = tf.Variable(10., name='bias')

    def call(self, inputs):
        return inputs * self.W + self.B


# 2.2 定义损失函数
# The loss function to be optimized
def loss(model, inputs, targets):
    error = model(inputs) - targets
    return tf.reduce_mean(tf.square(error))


# 2.3 优化器（即训练过程）：计算loss、梯度、根据梯度更新参数
def grad(model, inputs, targets):
    with tf.GradientTape() as tape:
        loss_value = loss(model, inputs, targets)
    return tape.gradient(loss_value, [model.W, model.B])

optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)


# 3、循环训练模型
model = Model()
print("Initial loss: {:.3f}".format(loss(model, training_inputs, training_outputs)))
# Training loop
for i in range(300):
    grads = grad(model, training_inputs, training_outputs)
    optimizer.apply_gradients(zip(grads, [model.W, model.B]))
    if i % 20 == 0:
        print("Loss at step {:03d}: {:.3f}".format(i, loss(model, training_inputs, training_outputs)))

print("Final loss: {:.3f}".format(loss(model, training_inputs, training_outputs)))
print("W = {}, B = {}".format(model.W.numpy(), model.B.numpy()))