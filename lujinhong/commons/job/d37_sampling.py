# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2019年08月23日 09:48
    PROJECT: lujinhong-commons-python3
DESCRIPTION: TODO
"""

import math


def sampling(in_file, out_file):
    print()
    inf = open(in_file,'r')
    outf = open(out_file,'a')
    for line in inf:

        ss = line.split('\t')
        udid = ss[0]
        features = ss[3]
        is_positive = ss[2]
        out_line = udid + '\t'
        for feature in features.split(' '):
            key = feature.split(':')[0]
            value = feature.split(':')[1]
            if key != 'Activation_udid':
                bin_value = 0


                if '-127' in value:
                # if value == '-127':
                    bin_value = -1
                    if udid == '1053066726@qq.com' and 'zy_rename_character_log' in key:
                        print(1)
                if float(value) > 0 :
                    bin_value = int(math.log2(int(value.split('.')[0]) + 2)) + 1
                    # if 'zy_rename_character_log' in key:
                    #     print(value)
                out_line += (key + '_' + str(bin_value) + ':1:20190101 ')
            if udid == '1053066726@qq.com' and 'zy_rename_character_log' in key:
                print(key)
                print(value)
                print(bin_value)



        outf.write(out_line + '\t' + is_positive + '\n')

    inf.close()
    outf.close()


if __name__ == '__main__':

    # bin_value = int(math.log2(int('2') + 2)) + 1
    # print(bin_value)

    for i in range(1,3):
        in_file = '/home/ljhn1829/g69/' + str(i) + '.txt'
        out_file = '/home/ljhn1829/g69/' + str(i) + 'out.txt'
        sampling(in_file, out_file)