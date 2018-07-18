import tensorflow as tf
import numpy as np
from itertools import islice


_TOTAL_PREDICT_COUNT = 100
_BATCH_PREDICTION_COUNT = 10
_FEATURE_COUNT = 200
_HIDDEN_UNIT = [75, 50, 25]
DIR_PREFIX = '/Users/ljhn1829/99_Project'
# DIR_PREFIX = '/home/ljhn1829'
_TO_PREDICT_DATA_FILE = DIR_PREFIX + '/lujinhong-commons-python3/lujinhong/data/g10_predict.txt'
_PREDICT_RESULT_DATA_FILE = DIR_PREFIX + '/lujinhong-commons-python3/lujinhong/data/g10_result.txt'
_MODEL_DIR = DIR_PREFIX + '/Downloads/wd/'
ID_MAPPINT_FILE = DIR_PREFIX + '/lujinhong-commons-python3/lujinhong/data/id.txt'
_DEVICE_ = '/job:localhost/replica:0/task:0/device:GPU:0'
id_dict = {}
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

def to_predict_input_fn(data_file=_TO_PREDICT_DATA_FILE,  batch_size=1):
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
                if ('_' not in f  and len(f)>2  and not f.endswith('00') and int(id_dict[f]) < _FEATURE_COUNT and not f == '801101'):
                    index = int(id_dict[f])
                    features[line_count, index] = 1
        line_count += 1
    features_dict = {}
    for i in range(_FEATURE_COUNT):
        features_dict[str(i)] = features[:, i]
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

def predict_result(f, model):
    with tf.device(_DEVICE_):
        prection2 = model.predict(to_predict_input_fn)
        for p,u in zip(prection2,udids):
            # print(u, '\t', p['probabilities'][1])
            f.write(u + '\t' +  str(p['probabilities'][1]) + '\n')
            f.flush()

if __name__ == '__main__':
    load_dict()
    f = open(_PREDICT_RESULT_DATA_FILE, 'a')
    tf.logging.set_verbosity(tf.logging.INFO)
    model = build_estimator(_MODEL_DIR)
    for i in range(0, _TOTAL_PREDICT_COUNT-_BATCH_PREDICTION_COUNT+1, _BATCH_PREDICTION_COUNT):
        print(i)
        begin_prection = i
        predict_result(f, model)