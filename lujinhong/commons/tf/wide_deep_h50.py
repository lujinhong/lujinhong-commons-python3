import tensorflow as tf


def my_input_fn(data_file, num_epochs, shuffle, batch_size):
    assert tf.gfile.Exists(data_file), (
        '%s not found. Please make sure you have run data_download.py and '
        'set the --data_dir argument to the correct path.' % data_file)

    f = open(data_file)
    line_count = 0
    indices = []
    values = []
    labels = []
    max_feature_index = 0
    for line in f:
        if ',,' in line:
            feature_string = line.split(',,')[0]
            label = line.split(',,')[1]
            labels.append(int(label))
            feature_array = feature_string.split(' ')
            for f in feature_array:
                if (':' in f and '_' not in f):
                    feature = int(f.split(':')[0])
                    if (feature > max_feature_index):
                        max_feature_index = feature
                    indices.append([line_count, feature])
                    values.append(1)
        line_count += 1
    # sparse_tensor = tf.SparseTensor(indices,values,dense_shape=[10,1200000])
    sparse_tensor = tf.SparseTensor(indices, values, dense_shape=[line_count, max_feature_index + 1])
    print(type(sparse_tensor))

    dataset = tf.data.Dataset.from_tensor_slices((sparse_tensor, labels))

    if shuffle:
        dataset = dataset.shuffle(1000)
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.batch(batch_size)
    return dataset


def main():
    dataset = my_input_fn('../../data/h50.txt', 40, 1, 1)
    iterator = dataset.make_one_shot_iterator()
    next_element = iterator.get_next()
    with tf.Session() as sess:
        for i in range(400):
            value = sess.run(next_element)
            print(value)


if __name__ == '__main__':
    main()
