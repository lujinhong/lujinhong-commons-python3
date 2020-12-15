# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2019年08月23日 09:48
    PROJECT: lujinhong-commons-python3
DESCRIPTION: TODO
"""

import math
in_file = '/home/ljhn1829/g69/3.txt'
out_file = '/home/ljhn1829/g69/3out.txt'

def sampling():
    print()
    inf = open(in_file,'r')
    outf = open(out_file,'a')
    for line in inf:

        ss = line.split('\t')
        udid = ss[0]
        features = ss[1]
        is_positive = ss[2]
        out_line = udid + '\t'
        for feature in features.split(' '):
            key = feature.split(':')[0]
            value = feature.split(':')[1]
            if key != 'Activation_udid':
                bin_value = 0
                if '-127' in value:
                    bin_value = -1
                if float(value) > 0.1 :
                    bin_value = int(math.log2(int(value.split('.')[0]) + 2)) + 1
                out_line += (key + '_' + str(bin_value) + ':1:20190101 ')

        outf.write(out_line + '\t' + is_positive + '\n')

    inf.close()
    outf.close()


if __name__ == '__main__':
    sampling()