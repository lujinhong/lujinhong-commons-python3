import tensorflow as tf
import numpy as np

SAMPLE_COUNT = 200
FEATURE_COUNT = 20000
HIDDEN_UNIT = [50, 25]
CSV_COLUMNS = []
CSV_COLUMN_DEFAULTS = []

TRAINING_DATA_FILE = '/Users/ljhn1829/99_Project/lujinhong-commons-python3/lujinhong/data/h50.csv'
MODEL_DIR = '/Users/ljhn1829/Downloads/wd/csv/'
# TRAINING_DATA_FILE = '/home/ljhn1829/lujinhong-commons-python3/lujinhong/data/h50.csv'
# MODEL_DIR = '/home/ljhn1829/model/csv/'


def build_model_columns():
    wide_columns = []
    deep_columns = []
    for i in range(FEATURE_COUNT-1):
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
        dnn_hidden_units=HIDDEN_UNIT)

def my_input_fn(data_file=TRAINING_DATA_FILE, num_epochs=1, shuffle=1, batch_size=1):
    dataset = tf.data.TextLineDataset(data_file)
    if shuffle:
        dataset = dataset.shuffle(SAMPLE_COUNT)
    dataset = dataset.map(parse_csv,num_parallel_calls=5)
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.batch(batch_size)
    return dataset

def parse_csv(value):
    columns = tf.decode_csv(value, record_defaults=CSV_COLUMN_DEFAULTS)
    features = dict(zip(CSV_COLUMNS, columns))
    labels = features.pop('19999')
    return features, labels

def main():
    for i in range(FEATURE_COUNT):
        CSV_COLUMNS.append(str(i))
        CSV_COLUMN_DEFAULTS.append([0])
    dataset = my_input_fn(TRAINING_DATA_FILE, 1, 1, 1)
    # print(type(dataset))
    # iterator = dataset.make_one_shot_iterator()
    # next_element = iterator.get_next()
    # with tf.Session() as sess:
    #     value = sess.run(next_element)
    #     print(value)

    # with tf.device(_DEVICE_):
    model = build_estimator(MODEL_DIR)
    print("training......")
    model.train(my_input_fn)
    print("evaluating......")
    eval = model.evaluate(my_input_fn)
    print(eval)

if __name__ == '__main__':
    main()
