import tensorflow as tf
import numpy as np


'''
数据预处理，将我们的数据转变为csv格式
'''
TRAINING_DATA_FILE = '/Users/ljhn1829/99_Project/lujinhong-commons-python3/lujinhong/data/h50.txt'
TRAINING_DATA_CSV = '/Users/ljhn1829/99_Project/lujinhong-commons-python3/lujinhong/data/h50.csv'
ID_MAPPINT_FILE = '/Users/ljhn1829/99_Project/lujinhong-commons-python3/lujinhong/data/id.txt'
id_dict = {}

def load_dict():
    id_file = open(ID_MAPPINT_FILE)
    for line in id_file:
        id = line.split(',')[0]
        label = line.split(',')[1].strip()
        id_dict[label] = id
        if('800001' in label):
            print(id)
        # print(label)
    # for i in id_dict.keys():
    #     print(i)
    print(id_dict['800001'])


def main():
    load_dict()
    src_file = open(TRAINING_DATA_FILE)
    target_file = open(TRAINING_DATA_CSV, 'w')
    for line in src_file:
        list = np.zeros(20000, dtype=int)
        label = line.split(',,')[1]
        features = line.split(',,')[0].split(' ')
        for feature in features:
            f = feature.split(':')[0]
            if('_' not in f and not f.endswith('00') and len(f) > 2):
                id = id_dict[f]
                list[int(id) - 1] = 1
        str2 = ''
        for i in list:
            # print(i)
            str2 += (str(i)+',')
        str2 += label
        target_file.write(str2)


if __name__ == '__main__':
    main()
