# coding=utf-8

import numpy as np
from sklearn import datasets
from sklearn import linear_model
from sklearn.model_selection import KFold, cross_val_score


class LogisticRegressionDemo:
    iris_X_train = 0
    iris_Y_train = 0
    iris_X_test = 0
    iris_Y_test = 0
    lr = 0

    # 加载数据，并随机分成训练与测试集
    def load_data(self):
        iris = datasets.load_iris()
        iris_X = iris.data
        iris_Y = iris.target
        np.random.seed(0)
        indices = np.random.permutation(len(iris_Y))
        self.iris_X_train = iris_X[indices[:-10]]
        self.iris_Y_train = iris_Y[indices[:-10]]
        self.iris_X_test = iris_X[indices[-10:]]
        self.iris_Y_test = iris_Y[indices[-10:]]

    def train(self):
        self.lr = linear_model.LogisticRegression()
        self.lr.fit(self.iris_X_train, self.iris_Y_train)

    def predict(self):
        predict_result = self.lr.predict(self.iris_X_test)
        print(predict_result)
        print(self.iris_Y_test)
        #测试集上的score
        print(self.lr.score(self.iris_X_test, self.iris_Y_test))
        #训练集上的score
        print(self.lr.score(self.iris_X_train, self.iris_Y_train))


    #交叉验证法
    def cross_validation(self):
        iris = datasets.load_iris()
        iris_X = iris.data
        iris_Y = iris.target
        k_fold = KFold(n_splits=20)
        for train,test in k_fold.split(iris_X):
            self.lr.fit(iris_X[train],iris_Y[train])
            print(self.lr.predict(iris_X[test]))
            print(self.lr.score(iris_X[test],iris_Y[test]))


if __name__ == "__main__":
    demo = LogisticRegressionDemo()
    demo.load_data()
    demo.train()
    demo.predict()
    demo.cross_validation()
