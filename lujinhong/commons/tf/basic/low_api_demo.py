import tensorflow as tf
import numpy as np
from sklearn.metrics import roc_auc_score

#一、基础
# 1、构建feature/label数据
#使用每个样本一行更符合直观，但要注意y-x*w+b，应为x与y的行数是相等的。如果使用y=w*x+b的数据格式见后面。
x_data = np.float32(np.random.rand(100, 2)) # 随机输入
y_data = np.dot(x_data, [[0.100], [0.200]]) + 0.300

# 2、构造模型
b = tf.Variable(tf.zeros([1]))
W = tf.Variable(tf.random_uniform([2, 1], -1.0, 1.0))
y = tf.matmul(x_data, W) + b

# 3、定义损失函数及优化器
loss = tf.losses.mean_squared_error(labels=y_data,predictions=y)
# 定义损失函数的另一种方式
# loss = tf.reduce_mean(tf.square(y - y_data))
optimizer = tf.train.GradientDescentOptimizer(0.5)

# 4、训练
train = optimizer.minimize(loss)
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)
for step in range(0,501):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(W), sess.run(b),sess.run(loss))
# 得到最佳拟合结果 W: [[0.100  0.200]], b: [0.300]

# 5、预测
x_to_predict = np.float32([[1,2],[2,3],[4,5]])
y_predict = tf.matmul(x_to_predict,W) + b
print(sess.run(y_predict))


#二、使用y=w*x+b的格式
# 1、构建feature/label数据
x_data = np.float32(np.random.rand(2, 100)) # 随机输入
y_data = np.dot([0.100, 0.200], x_data) + 0.300

# 2、构造模型
b = tf.Variable(tf.zeros([1]))
W = tf.Variable(tf.random_uniform([1, 2], -1.0, 1.0))
y = tf.matmul(W, x_data) + b

# 3、定义损失函数及优化器
loss = tf.losses.mean_squared_error(labels=y_data.reshape(1,-1),predictions=y)
# 定义损失函数的另一种方式
# loss = tf.reduce_mean(tf.square(y - y_data))
optimizer = tf.train.GradientDescentOptimizer(0.5)

# 4、训练
train = optimizer.minimize(loss)
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)
for step in range(0,501):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(W), sess.run(b),sess.run(loss))
# 得到最佳拟合结果 W: [[0.100  0.200]], b: [0.300]

# 5、预测
x_to_predict = np.float32([[1,2,3],[3,4,5]])
y_predict = tf.matmul(W,x_to_predict) + b
print(sess.run(y_predict))

#三、使用张量
#上面的例子都是使用numpy的数组作为输入，以下例子使用tf的Tensor作为输入
x = tf.constant([[1], [2], [3], [4]], dtype=tf.float32)
y_true = tf.constant([[0], [-1], [-2], [-3]], dtype=tf.float32)

linear_model = tf.layers.Dense(units=1)
y_pred = linear_model(x)
loss = tf.losses.mean_squared_error(labels=y_true, predictions=y_pred)
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)

init = tf.global_variables_initializer()

sess = tf.Session()
sess.run(init)
for i in range(100):
    _, loss_value = sess.run((train, loss))
    print(loss_value)

print(sess.run(y_pred))