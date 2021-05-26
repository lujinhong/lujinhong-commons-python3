# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2021年05月24日 3:45 下午
    PROJECT: lujinhong-commons-python3
DESCRIPTION:
        1、g102稀有道具数据文件预处理，生成最终的CSV文件
        2、使用CSV文件中的样本来训练模型。
"""

import numpy as np
import pandas as pd
import sklearn
import os
import json

POST_DIR = '/Users/ljhn1829/Downloads/g102-rare/post'
NEG_DIR = '/Users/ljhn1829/Downloads/g102-rare/neg'
SAMPLE_DIR = '/Users/ljhn1829/Downloads/g102-rare/sample'
ONLINE_KEYS = [148, 149, 150, 155, 156, 157]
OFFLINE_KEYS = [128, 129, 130, 135, 136, 137]
TITLES = ['vip_level', 'left_yuanbao', 'partner_rank', 'left_org', 'left_red', 'left_gold', 'label']
IDS = [11471, 11472, 11473]


# 将正样本整理成csv格式
def extract_positive_sample(dir):
    for filename in os.listdir(dir):
        csv_filename = filename + '.csv'
        with open(os.path.join(POST_DIR, csv_filename), 'a') as csv_file:
            with open(os.path.join(POST_DIR, filename)) as f:
                for line in f:
                    json_text = line[39:]
                    json_content = json.loads(json_text)['role_info']
                    csv_line = transform_json_to_csv(str(json_content).replace('\'', '"'), ONLINE_KEYS)
                    csv_file.write(csv_line + '\n')


def transform_json_to_csv(json_line, keys):
    json_content = json.loads(json_line)
    csv_line = ''
    for key in keys:
        if str(key) in json_content.keys():
            value = json_content[str(key)]
        else:
            value = ''
        csv_line = csv_line + str(value) + ','
    return csv_line[:-1]


# 将正样本整理成csv格式
def extract_negative_sample(file):
    with open(os.path.join(NEG_DIR, 'neg.txt'), 'w') as negative_sample_file:
        with open(os.path.join(NEG_DIR, file)) as f:
            for line in f:
                json_line = transform_to_json(line.split('\t')[1])
                csv_line = transform_json_to_csv(json_line, OFFLINE_KEYS)
                negative_sample_file.write((csv_line + '\n'))


def transform_to_json(ss):
    json_line = '{'
    ss_list = ss.split(',')
    for s in ss_list:
        key = s.split(':')[0]
        value = s.split(':')[1]
        json_line = json_line + '"' + key + '"' + ':"'  + value + '",';
    json_line = json_line[:-1] + '}'
    return json_line


# 生成最终样本
def generate_sample():
    for id in IDS:
        with open(os.path.join(SAMPLE_DIR, str(id)+'.csv'), 'w') as sf:
            sf.write(generate_first_line() + '\n')
            with open(os.path.join(POST_DIR, str(id)+'.txt.csv')) as pf:
                for line in pf:
                    sf.write(line.strip()+',1\n')
            with open(os.path.join(NEG_DIR, 'neg.txt')) as nf:
                for line in nf:
                    sf.write(line.strip()+',0\n')


def generate_first_line():
    csv_line = ''
    for title in TITLES:
        csv_line = csv_line + title + ','
    return csv_line[:-1]


def generate_sample_csv():
    #extract_positive_sample(POST_DIR)
    #extract_negative_sample('000000_0')
    generate_sample()
    pass


def train_model():
    for id in IDS:
        filename = os.path.join(SAMPLE_DIR, str(id)+'.csv')
        all_sample = pd.read_csv(filename)
        trains(all_sample)


def trains(sample_df):
    # shuffle
    all_sample = sample_df.sample(frac=1)
    # 拆分特征与标签
    lables = all_sample['label']
    features = all_sample.drop(['label'], axis=1)
    # 缺失值处理
    for feature in ['vip_level', 'left_yuanbao', 'left_org', 'left_red', 'left_gold']:
        features[feature].fillna(0, inplace=True)
    for feature in ['partner_rank']:
        features[feature].fillna(9999, inplace=True)
    # one-hot。先简单的分成5个数量相同的的类别：
    for feature in  ['vip_level', 'left_yuanbao', 'left_org', 'left_red', 'left_gold', 'partner_rank']:
        print(feature)
        # TODO:修改为具体的分箱值
        lst_bins = pd.cut(features[feature], 5, labels=[feature + '1',feature + '2',feature + '3',feature + '4',feature + '5'])
        onehot = pd.get_dummies(lst_bins)
        features = features.drop([feature], axis=1)
        features = features.join(onehot, lsuffix='l', rsuffix='r')
    print(features.head(), lables.head())


if __name__ == '__main__':
    #generate_sample_csv()
    train_model()






