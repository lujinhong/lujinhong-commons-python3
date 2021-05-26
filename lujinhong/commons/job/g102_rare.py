# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2021年04月23日 11:21 上午
    PROJECT: lujinhong-commons-python3
DESCRIPTION: g102 rare数据分析
"""
import os

#当前剩余碎片
LEFT_ORANGE = '135'
LEFT_RED = '136'
LEFT_GOLDEN = '137'
#上一次购买碎片的时间
BUY_ORANGE_TIME = '132'
BUY_RED_TIME = '133'
BUY_GOLDEN_TIME = '134'

LAST_FAIL = '131'
VIP_LEVEL = '128'
BB_RANG = '130'
LEFT_YUANBAO = '129'

DIR = '/Users/ljhn1829/Downloads/g102'

def construct_label_dict(labels_str):
    label_dict = {}
    for label in labels_str.split(','):
        l = label.split(':')
        label_dict[l[0]] = l[1]
    return label_dict

def check_satisfied(label_dict):
    label_keys = label_dict.keys()
    if (\
        LEFT_RED in label_keys and 10<=int(label_dict[LEFT_RED])<=14 \
        and VIP_LEVEL in label_keys  and 6 <= int(label_dict[VIP_LEVEL]) <= 14 \
        # and BB_RANG in label_keys and 31 <= int(label_dict[BB_RANG]) <=70 \
        and LEFT_YUANBAO in label_keys and 40000.0 <= float(label_dict[LEFT_YUANBAO]) <= 100000.0\
        and LAST_FAIL in label_keys and '2021-04-22' in label_dict[LAST_FAIL] \
        # and BUY_ORANGE_TIME in label_keys and '2021-04-22' in label_dict[BUY_ORANGE_TIME]\
            ) :
        print(label_dict)
        return True

count = 0
for dir_path, dir_names, file_names in os.walk(DIR):
    for file in file_names:
        with open(dir_path + '/' + file,encoding='utf-8') as f:
            for line in f:
                role,labels,change_date = line.split('\001\t\001')
                label_dict = construct_label_dict(labels)
                if(check_satisfied(label_dict)):
                    count +=1

print(count)





# print(type('109:1:20210419'.split(':')))
# print(construct_label_dict('109:1:20210419,127:103643:20210419,19:2021-04-19:20210419,22:365683:20210419,25:2020-09-16:20210419,21:236:20210419,24:308:20210419,14:10741:20210421,20:2020-08-22 13:47:38:20210419,23:8:20210419,8:23:20210421'))

