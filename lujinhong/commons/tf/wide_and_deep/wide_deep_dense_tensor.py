import tensorflow as tf
import numpy as np

'''
读取文本数据，使用numpy数组构建dataset对象，然后训练模型。
基本思路：
1、创建Dataset对象：（1）创建一个[样本数，特征数]的二维数组，并初始化为0（2）根据样本数据，将二维数组相应的数据置位value（3）创建一个dict，key为列的名称，value为所有样本这列的值
                （4）根据样本数据，创建一个labels数组。（5）使用(dict,labels)创建Dataset对象。
2、创建Estimator对象（1）先创建列FeatureColumn对象。（2）创建Estimator对象
3、使用Estimator对象调用train(),evaluate()等方法。
'''

def my_input_fn(data_file='../../data/h50.txt', num_epochs=10, shuffle=1, batch_size=1):
    assert tf.gfile.Exists(data_file), (
        '%s not found. Please make sure you have run data_download.py and '
        'set the --data_dir argument to the correct path.' % data_file)

    f = open(data_file)
    line_count = 0
    labels = []
    features = np.zeros((10,1000))
    for line in f:
        if ',,' in line:
            feature_string = line.split(',,')[0]
            label = line.split(',,')[1]
            labels.append(int(label))
            feature_array = feature_string.split(' ')
            for f in feature_array:
                if (':' in f and '_' not in f):
                    index = int(f.split(':')[0])
                    features[line_count,index] = 1
        line_count += 1
    features_dict = {}
    for i in range(1000):
        features_dict[str(i)] = features[:,i]
    print(features_dict['678'])
    dataset = tf.data.Dataset.from_tensor_slices((features_dict, labels))

    if shuffle:
        dataset = dataset.shuffle(1000)
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.batch(batch_size)
    return dataset

def build_model_columns():
    wide_columns = []
    deep_columns = []
    for i in range(1000):
        c = tf.feature_column.numeric_column(str(i))
        wide_columns.append(c)
        deep_columns.append(c)
    return wide_columns,deep_columns

def build_estimator(model_dir):
    wide_columns, deep_columns = build_model_columns()
    return tf.estimator.DNNLinearCombinedClassifier(
        model_dir=model_dir,
        linear_feature_columns=wide_columns,
        dnn_feature_columns=deep_columns,
        dnn_hidden_units=[100, 75, 50, 25])


def main():
    # dataset = my_input_fn('../../data/h50.txt', 40, 1, 1)
    model = build_estimator('/Users/ljhn1829/Downloads/wd/')
    # 或者用lambda传参数
    print("training......")
    model.train(my_input_fn)
    print("evaluating......")
    eval = model.evaluate(my_input_fn)
    print(eval)

if __name__ == '__main__':
    main()



