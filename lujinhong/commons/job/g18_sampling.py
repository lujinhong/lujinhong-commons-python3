# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2019年10月16日 17:18
    PROJECT: lujinhong-commons-python3
DESCRIPTION: TODO
"""

import math
in_file = '/home/ljhn1829/g18/g18.txt'
out_file_all = '/home/ljhn1829/g18/g18out_all.txt'
out_file_69 = '/home/ljhn1829/g18/g18out_69.txt'
out_file_89 = '/home/ljhn1829/g18/g18out_89.txt'
out_file_115 = '/home/ljhn1829/g18/g18out_115.txt'

def sampling():
    print()
    inf = open(in_file,'r')
    outf_all = open(out_file_all,'a')
    outf_69 = open(out_file_69,'a')
    outf_89 = open(out_file_89,'a')
    outf_115 = open(out_file_115,'a')
    for line in inf:

        udid,ds,grade,is_positive,features, = line.split('\t')
        # udid = ss[0]
        # features = ss[1]
        # is_positive = ss[2]
        out_line = udid + '\t'
        for feature in features.split(' '):
            # #
            # if ":" not in feature:
            #     prefix = feature
            # else:
            #     prefix = ''
            key = feature.split(':')[0]
            value = feature.split(':')[1]
            if key != 'Activation_udid':
                bin_value = 0
                if '-127' in value:
                    bin_value = -1
                if float(value) > 0.1 :
                    bin_value = int(math.log2(int(value.split('.')[0]) + 2)) + 1
                out_line += (key + '_' + str(bin_value) + ':1:20190101 ')

        outf_all.write(out_line + '\t' + is_positive + '\n')
        if grade == '69':
            outf_69.write(out_line + '\t' + is_positive + '\n')
        if grade == '89':
            outf_89.write(out_line + '\t' + is_positive + '\n')
        if grade == '115':
            outf_115.write(out_line + '\t' + is_positive + '\n')

    inf.close()
    outf_all.close()
    outf_69.close()
    outf_89.close()
    outf_115.close()


if __name__ == '__main__':
    sampling()