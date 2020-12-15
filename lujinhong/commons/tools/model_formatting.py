# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2019年03月20日 17:42
    PROJECT: lujinhong-commons-python3
DESCRIPTION: FTRL模型的格式化
"""

import os

file_dir = '/Users/ljhn1829/Downloads/model/'
out_dir = '/Users/ljhn1829/Downloads/'
#模型中标签对应的weigh
label_weigh_dict = {}
#标签id对应的标签名称
label_name_dict = {}
all_file = os.listdir(file_dir)


def sort_dict(mydict):
    sorted_list = sorted(mydict.items(), key=lambda item: item[1], reverse=True)
    return sorted_list


def load_label_name():
    f = open('label.txt')
    for line in f.readlines():
        label_name_dict[line.split('\t')[0]] = line.split('\t')[1].strip()


# load_label_name()
for file in all_file:
    f = open(file_dir + file)
    outf= open(out_dir + 'formatting' + file, 'w')
    print('source file:{} to file:{}'.format(file_dir + file, out_dir + 'formatting' + file))
    # #只取第一行的第三个字段，然后放到字典中
    # .split('\t')[2]
    ss = f.readline()
    for s in ss.split(' '):
        # print(s)
        if ':' in s:
            label = s.split(':')[0]
            weigh = s.split(':')[1]
            if label != 'null':
                label_weigh_dict[label] = float(weigh)
    #根据weigh值排序
    sort_label_dict = sort_dict(label_weigh_dict)
    #输出到文件
    for item in sort_label_dict:
        label_name = label_name_dict[item[0]] if item[0] in label_name_dict.keys() else 'null'
        if item[0].startswith("724_3_"):
            label_name = '[实时标签]' + label_name_dict[item[0][6:]] if item[0][6:] in label_name_dict.keys() else 'null'
        # outf.write(item[0] + '\t' + str(item[1]) + '\t' + label_name + '\n')
        #输出成RTB格式
        outf.write(item[0] + '\01' + str(item[1]) + '\n')
    label_weigh_dict.clear()
    sort_label_dict.clear()
    outf.close()
    f.close()