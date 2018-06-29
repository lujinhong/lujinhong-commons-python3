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
_BATCH_SAMPLE_COUNT = 100 #每次训练的样本数量
_TOTAL_SAMPLE_COUNT = 218000 #样本的总量
_FEATURE_COUNT = 200
# _HIDDEN_UNIT = [100, 75, 50, 25]
_HIDDEN_UNIT = [75, 50, 25]
DIR_PREFIX = '/Users/ljhn1829/99_Project'
# DIR_PREFIX = '/home/ljhn1829'
_TRAINING_DATA_FILE = DIR_PREFIX + '/lujinhong-commons-python3/lujinhong/data/g10.txt'
_MODEL_DIR = DIR_PREFIX + '/Downloads/wd/'
ID_MAPPINT_FILE = DIR_PREFIX + '/lujinhong-commons-python3/lujinhong/data/id.txt'
_DEVICE_ = '/job:localhost/replica:0/task:0/device:GPU:0'
id_dict = {}
begin = 0

#若直接使用标签id，则最大的标签id可以到一百多万，也就是我们要构建一个一百多万维的数组。
#而每个标签都对应有一个从1开始自增的id，然后用这个id来替代标签id。
#如果计算还是慢的话，再做一个映射表，只取游戏了标签
def load_dict():
    id_file = open(ID_MAPPINT_FILE)
    for line in id_file:
        id = line.split(',')[0]
        label = line.split(',')[1].strip()
        id_dict[label] = id


def my_input_fn(data_file=_TRAINING_DATA_FILE, num_epochs=1,
                shuffle=1, batch_size=10):
    print("building dataset....")
    assert tf.gfile.Exists(data_file), (
        '%s not found. Please make sure you have run data_download.py and '
        'set the --data_dir argument to the correct path.' % data_file)

    f = open(data_file)
    line_count = 0
    labels = []
    features = np.zeros((_BATCH_SAMPLE_COUNT, _FEATURE_COUNT))
    for line in islice(f, begin, None):
        if line_count < _BATCH_SAMPLE_COUNT and ',' in line:
            feature_string = line.split(',')[0]
            label = line.split(',')[1]
            labels.append(int(label))
            feature_array = feature_string.split(' ')
            for f in feature_array:
                f = f.split(':')[0]
                if ('_' not in f  and len(f)>2  and not f.endswith('00') and int(id_dict[f]) < _FEATURE_COUNT and not f == '801101'):
                    index = int(id_dict[f])
                    features[line_count, index] = 1
        line_count += 1
    features_dict = {}
    for i in range(_FEATURE_COUNT):
        features_dict[str(i)] = features[:, i]
    dataset = tf.data.Dataset.from_tensor_slices((features_dict, labels))
    print('Finish buiding dataset')

    if shuffle:
        dataset = dataset.shuffle(_BATCH_SAMPLE_COUNT)
    dataset = dataset.repeat(num_epochs)
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


def main():
    with tf.device(_DEVICE_):
        # dataset = my_input_fn('../../data/h50.txt', 40, 1, 1)
        model = build_estimator(_MODEL_DIR)
        # 或者用lambda传参数
        print("training......")
        model.train(my_input_fn)
        print("evaluating......")
        eval = model.evaluate(my_input_fn)
        print(eval)


if __name__ == '__main__':
    _set_time_logging()
    load_dict()
    tf.logging.set_verbosity(tf.logging.INFO)
    for i in range(0, _TOTAL_SAMPLE_COUNT-_BATCH_SAMPLE_COUNT, _BATCH_SAMPLE_COUNT):
        print('trainng sample: ', i, ' to ', i + _BATCH_SAMPLE_COUNT)
        begin = i
        main()
