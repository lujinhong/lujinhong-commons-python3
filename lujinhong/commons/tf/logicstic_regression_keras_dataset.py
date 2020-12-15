# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2020年08月28日 10:26
    PROJECT: lujinhong-commons-python3
DESCRIPTION: TODO
"""

import tensorflow as tf
import pandas as pd
print(tf.__version__)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


## 1、准备数据集
df_train = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/train.csv')
df_eval = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/eval.csv')
y_train = df_train.pop('survived')
y_eval = df_eval.pop('survived')

ds_train = tf.data.Dataset.from_tensor_slices((dict(df_train),y_train)).batch(2)
ds_eval = tf.data.Dataset.from_tensor_slices((dict(df_eval),y_eval)).batch(2)

## 2、构建feature_column
CATEGORICAL_COLUMNS = ['sex', 'n_siblings_spouses', 'parch', 'class', 'deck',
                       'embark_town', 'alone']
NUMERIC_COLUMNS = ['age', 'fare']

feature_columns = []
#对类别特征做one-hot，还可以用embeding_column做embedding。
for feature_name in CATEGORICAL_COLUMNS:
    vocabulary = df_train[feature_name].unique()
    feature_columns.append(tf.feature_column.indicator_column(tf.feature_column.categorical_column_with_vocabulary_list(feature_name,vocabulary)))

for feature_name in NUMERIC_COLUMNS:
    feature_columns.append(tf.feature_column.numeric_column(feature_name,dtype=tf.float32))

#除上述特征外，还可以做组合特征。

## 3、构建并运行模型
feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

model = tf.keras.Sequential([
    feature_layer,
    # tf.keras.layers.Dense(128, activation='relu'),
    # tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(loss = 'binary_crossentropy', optimizer='sgd',metrics=['accuracy'])

model.fit(ds_train)
model.evaluate(ds_eval)

