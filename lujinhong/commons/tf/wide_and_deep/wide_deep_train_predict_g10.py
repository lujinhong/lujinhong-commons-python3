import tensorflow as tf
import numpy as np
import os
import sys
import logging
from itertools import islice
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

def _set_time_logging():
  handler = logging.StreamHandler(sys.stderr)
  handler.setFormatter(logging.Formatter("%(asctime)s:" + logging.BASIC_FORMAT, None))
  logger = logging.getLogger("tensorflow")
  # logger.removeHandler(tf.logging._handler)
  logger.addHandler(handler)


'''
读取文本数据，使用numpy数组构建dataset对象，然后训练模型。
基本思路：
1、创建Dataset对象：（1）创建一个[样本数，特征数]的二维数组，并初始化为0（2）根据样本数据，将二维数组相应的数据置位value（3）创建一个dict，key为列的名称，value为所有样本这列的值
                （4）根据样本数据，创建一个labels数组。（5）使用(dict,labels)创建Dataset对象。
2、创建Estimator对象（1）先创建列FeatureColumn对象。（2）创建Estimator对象
3、使用Estimator对象调用train(),evaluate()等方法。
'''
DIR_PREFIX = '/home/ljhn1829'
_BATCH_TRAIN_COUNT = 20000 #每次训练的样本数量
_TOTAL_TRAIN_COUNT = 200000 #样本的总量
_BATCH_EVALUATE_COUNT = 18000
_TOTAL_EVALUATE_COUNT = 18000
_BATCH_PREDICTION_COUNT = 200000
_TOTAL_PREDICT_COUNT = 40049062
_FEATURE_COUNT = 11318
# DIR_PREFIX = '/Users/ljhn1829/99_Project'
# _BATCH_TRAIN_COUNT = 100 #每次训练的样本数量
# _TOTAL_TRAIN_COUNT = 500 #样本的总量
# _BATCH_EVALUATE_COUNT = 200
# _TOTAL_EVALUATE_COUNT = 200
# _BATCH_PREDICTION_COUNT = 50
# _TOTAL_PREDICT_COUNT = 100
# _FEATURE_COUNT = 200
_HIDDEN_UNIT = [75, 50, 25]
_TRAINING_DATA_FILE = DIR_PREFIX + '/lujinhong-commons-python3/lujinhong/data/g10_train.txt'
_EVALUATE_DATA_FILE = DIR_PREFIX + '/lujinhong-commons-python3/lujinhong/data/g10_evaluate.txt'
_TO_PREDICT_DATA_FILE = DIR_PREFIX + '/lujinhong-commons-python3/lujinhong/data/g10_predict.txt'
_PREDICT_RESULT_DATA_FILE = DIR_PREFIX + '/lujinhong-commons-python3/lujinhong/data/g10_result.txt'
_MODEL_DIR = DIR_PREFIX + '/Downloads/wd_11318/'
ID_MAPPINT_FILE = DIR_PREFIX + '/lujinhong-commons-python3/lujinhong/data/id3.txt'
_DEVICE_ = '/job:localhost/replica:0/task:0/device:GPU:0'
id_dict = {}
id_dict_keys = []
begin_train = 0
begin_evaluate = 0
begin_prection = 0
udids = []

#若直接使用标签id，则最大的标签id可以到一百多万，也就是我们要构建一个一百多万维的数组。
#而每个标签都对应有一个从1开始自增的id，然后用这个id来替代标签id。
#如果计算还是慢的话，再做一个映射表，只取游戏了标签
def load_dict():
    id_file = open(ID_MAPPINT_FILE)
    for line in id_file:
        id = line.split(',')[0]
        label = line.split(',')[1].strip()
        id_dict[label] = id


def train_input_fn(data_file=_TRAINING_DATA_FILE, num_epochs=1,
                shuffle=1, batch_size=10):
    print("building dataset....")
    assert tf.gfile.Exists(data_file), (
        '%s not found. Please make sure you have run data_download.py and '
        'set the --data_dir argument to the correct path.' % data_file)

    f = open(data_file)
    line_count = 0
    labels = []
    features = np.zeros((_BATCH_TRAIN_COUNT, _FEATURE_COUNT))
    for line in islice(f, begin_train, None):
        if line_count < _BATCH_TRAIN_COUNT and ',' in line:
            feature_string = line.split(',')[0]
            label = line.split(',')[1]
            labels.append(int(label))
            feature_array = feature_string.split(' ')
            for f in feature_array:
                f = f.split(':')[0]
                if ('_' not in f  and len(f)>2  and not f.endswith('00') and f in id_dict_keys  and int(id_dict[f]) < _FEATURE_COUNT and not f == '801101'):
                    index = int(id_dict[f])
                    features[line_count, index] = 1
        line_count += 1
    features_dict = {}
    for i in range(_FEATURE_COUNT):
        features_dict[str(i)] = features[:, i]
    dataset = tf.data.Dataset.from_tensor_slices((features_dict, labels))
    print('Finish buiding dataset')

    if shuffle:
        dataset = dataset.shuffle(_BATCH_TRAIN_COUNT)
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.batch(batch_size)
    print('Dataset shuffle/repeat/batch')
    return dataset

def evaluate_input_fn(data_file=_EVALUATE_DATA_FILE, num_epochs=1,
                shuffle=0, batch_size=10):
    print("building dataset....")
    assert tf.gfile.Exists(data_file), (
        '%s not found. Please make sure you have run data_download.py and '
        'set the --data_dir argument to the correct path.' % data_file)

    f = open(data_file)
    line_count = 0
    labels = []
    features = np.zeros((_BATCH_EVALUATE_COUNT, _FEATURE_COUNT))
    for line in islice(f, begin_evaluate, None):
        if line_count < _BATCH_EVALUATE_COUNT and ',' in line:
            feature_string = line.split(',')[0]
            label = line.split(',')[1]
            labels.append(int(label))
            feature_array = feature_string.split(' ')
            for f in feature_array:
                f = f.split(':')[0]
                if ('_' not in f  and len(f)>2  and not f.endswith('00') and f in id_dict_keys  and int(id_dict[f]) < _FEATURE_COUNT and not f == '801101'):
                    index = int(id_dict[f])
                    features[line_count, index] = 1
        line_count += 1
    features_dict = {}
    for i in range(_FEATURE_COUNT):
        features_dict[str(i)] = features[:, i]
    dataset = tf.data.Dataset.from_tensor_slices((features_dict, labels))
    print('Finish buiding dataset')

    if shuffle:
        dataset = dataset.shuffle(_BATCH_EVALUATE_COUNT)
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.batch(batch_size)
    print('Dataset shuffle/repeat/batch')
    return dataset

def to_predict_input_fn(data_file=_TO_PREDICT_DATA_FILE,  batch_size=10):
    print("building predict dataset....")
    assert tf.gfile.Exists(data_file), (
        '%s not found. Please make sure you have run data_download.py and '
        'set the --data_dir argument to the correct path.' % data_file)
    udids.clear()
    f = open(data_file)
    line_count = 0
    features = np.zeros((_BATCH_PREDICTION_COUNT, _FEATURE_COUNT))
    for line in islice(f, begin_prection, None):
        if line_count < _BATCH_PREDICTION_COUNT:
            feature_string = line.split(',')[1]
            u = line.split(',')[0]
            udids.append(u)
            feature_array = feature_string.split(' ')
            for f in feature_array:
                f = f.split(':')[0]
                if ('_' not in f  and len(f)>2  and not f.endswith('00') and f in id_dict_keys and int(id_dict[f]) < _FEATURE_COUNT and not f == '801101'):
                    index = int(id_dict[f])
                    features[line_count, index] = 1
        line_count += 1
    features_dict = {}
    for i in range(_FEATURE_COUNT):
        features_dict[str(i)] = features[:, i]
    print(len(features_dict),len(udids))
    dataset = tf.data.Dataset.from_tensor_slices((features_dict, udids))
    print('Finish buiding dataset')

    dataset = dataset.batch(batch_size)
    print('Dataset shuffle/repeat/batch')
    return dataset


def build_model_columns():
    wide_columns = []
    deep_columns = []
    for i in range(_FEATURE_COUNT):
        c = tf.feature_column.numeric_column(str(i))
        wide_columns.append(c)
        deep_columns.append(c)
    return wide_columns, deep_columns


def build_estimator(model_dir):
    wide_columns, deep_columns = build_model_columns()
    return tf.estimator.DNNLinearCombinedClassifier(
        model_dir=model_dir,
        linear_feature_columns=wide_columns,
        dnn_feature_columns=deep_columns,
        dnn_hidden_units=_HIDDEN_UNIT)


def train():
    with tf.device(_DEVICE_):
        # dataset = my_input_fn('../../data/h50.txt', 40, 1, 1)
        model = build_estimator(_MODEL_DIR)
        # 或者用lambda传参数
        print("training......")
        model.train(train_input_fn)
        return model

def evaluate():
    with tf.device(_DEVICE_):
        model = build_estimator(_MODEL_DIR)
        print("evaluating......")
        eval = model.evaluate(evaluate_input_fn)
        print(eval)
        return model


def predict_result():
    model = build_estimator(_MODEL_DIR)
    f = open(_PREDICT_RESULT_DATA_FILE, 'a')
    with tf.device(_DEVICE_):
        prection2 = model.predict(to_predict_input_fn)
        for p,u in zip(prection2,udids):
            f.write(u + '\t' +  str(p['probabilities'][1]) + '\n')
            # print(u, '\t', p['probabilities'][1]
    f.close()


if __name__ == '__main__':
    _set_time_logging()
    load_dict()
    id_dict_keys = id_dict.keys()
    tf.logging.set_verbosity(tf.logging.INFO)
    for i in range(0, _TOTAL_TRAIN_COUNT, _BATCH_TRAIN_COUNT):
        logging.error('trainng sample: '+ str(i) )
        begin_train = i
        train()
    for i in range(0, _TOTAL_EVALUATE_COUNT, _BATCH_EVALUATE_COUNT):
        logging.error('evaluate sample: '+ str(i) )
        begin_evaluate = i
        evaluate()
    for i in range(0, _TOTAL_PREDICT_COUNT, _BATCH_PREDICTION_COUNT):
        print(i)
        begin_prection = i
        predict_result()
