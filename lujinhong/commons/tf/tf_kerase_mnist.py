# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2021年03月11日 2:25 下午
    PROJECT: lujinhong-commons-python3
DESCRIPTION: 见jupyter notebook：tensorflow-keras的基本使用方式，用一个综合示例展示了tensorflow-kears的基础用法
"""

import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from tensorflow import keras

# 加载数据集，分割数据集
fashion_mnist = keras.datasets.fashion_mnist
(x_train_all,y_train_all),(x_test,y_test) = fashion_mnist.load_data()
x_valid, x_train = x_train_all[:5000], x_train_all[5000:]
y_valid, y_train = y_train_all[:5000], y_train_all[5000:]
print(x_train.shape, y_train.shape)
print(x_valid.shape, y_valid.shape)
print(x_test.shape, y_test.shape)


# 打印其中一个数据看看
def show_single_image(img_arr):
    plt.imshow(img_arr, cmap='binary')
    plt.show()

#print(x_train[0])
#show_single_image(x_train[0])


# 画出3*5个图片，以及其类别
def show_images(n_rows, n_columns, x_data, y_data, class_names):
    for row in range(n_rows):
        for col in range(n_columns):
            index = row*n_columns + col
            plt.subplot(n_rows, n_columns, index + 1)
            plt.imshow(x_data[index])
            plt.title(class_names[y_data[index]])
    plt.show()


class_names = ['T-shirt', 'Trouser', 'Pullover', 'Dress',
               'Coat', 'Sandal', 'Shirt', 'Sneaker',
               'Bag', 'Ankle boot']
# show_images(3, 5, x_train, y_train, class_names)


# 构建模型
model = keras.models.Sequential()
model.add(keras.layers.Flatten(input_shape=[28,28]))
model.add(keras.layers.Dense(300,activation='sigmoid'))
model.add(keras.layers.Dense(100,activation='sigmoid'))
model.add(keras.layers.Dense(10,activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='sgd',
              metrics='accuracy')

# 训练模型
history = model.fit(x_train, y_train, epochs=10, validation_data=(x_valid, y_valid))