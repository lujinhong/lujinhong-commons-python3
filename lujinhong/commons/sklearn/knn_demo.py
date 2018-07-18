# coding=utf-8

import numpy as np
from sklearn import datasets
from sklearn import neighbors


class KNNDemo:
    iris_X_train = 0
    iris_Y_train = 0
    iris_X_test = 0
    iris_Y_test = 0
    knn = 0

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
        self.knn = neighbors.KNeighborsClassifier()
        self.knn.fit(self.iris_X_train, self.iris_Y_train)

    def predict(self):
        predict_result = self.knn.predict(self.iris_X_test)
        print(predict_result)
        print(self.iris_Y_test)
        #测试集上的score
        print(self.knn.score(self.iris_X_test,self.iris_Y_test))
        #训练集上的score
        print(self.knn.score(self.iris_X_train,self.iris_Y_train))


if __name__ == "__main__":
    demo = KNNDemo()
    demo.load_data()
    demo.train()
    demo.predict()
