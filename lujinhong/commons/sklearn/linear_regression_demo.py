# coding=utf-8

import numpy as np
from sklearn import datasets
from sklearn import linear_model

'''
1、线性回归的基本用法
'''

class LinearRegressionDemo:
    lr = 0
    diabetes_X_train = 0
    diabetes_Y_train = 0
    diabetes_X_test = 0
    diabetes_Y_test = 0

    # 加载数据，并随机分成训练与测试集
    def load_data(self):
        diabetes = datasets.load_diabetes()
        diabetes_X = diabetes.data
        diabetes_Y = diabetes.target
        np.random.seed(0)
        indices = np.random.permutation(len(diabetes_Y))
        self.diabetes_X_train = diabetes_X[indices[:-20]]
        self.diabetes_Y_train = diabetes_Y[indices[:-20]]
        self.diabetes_X_test = diabetes_X[indices[-20:]]
        self.diabetes_Y_test = diabetes_Y[indices[-20:]]

    def train(self):
        self.lr = linear_model.LinearRegression()
        self.lr.fit(self.diabetes_X_train, self.diabetes_Y_train)
        print(self.lr.coef_)

    def predict(self):
        print(self.lr.predict(self.diabetes_X_test))
        print(self.diabetes_Y_test)
        #计算均方差
        print(np.mean((self.lr.predict(self.diabetes_X_test) - self.diabetes_Y_test) ** 2))


if __name__ == "__main__":
    demo = LinearRegressionDemo()
    demo.load_data()
    demo.train()
    demo.predict()
