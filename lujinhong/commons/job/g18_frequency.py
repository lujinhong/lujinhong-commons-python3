# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2019年10月08日 14:57
    PROJECT: lujinhong-commons-python3
DESCRIPTION: TODO
"""

IMP_FILE = '/Users/ljhn1829/Downloads/hs/imp.txt'
NEW_FILE = '/Users/ljhn1829/Downloads/hs/new.txt'
TMP_FILE = '/Users/ljhn1829/Downloads/hs/tmp.txt'

def filter_imp(MINS):
    remain_imp_dict = {}
    imp_file = open(IMP_FILE, 'r')
    tmp_file = open(TMP_FILE, 'w')
    for line in imp_file:
        udid,price,imp_time = line.split('\t')
        ss = ''
        if udid in remain_imp_dict:
            ss = remain_imp_dict[udid] + ','
        ss = ss + (price + '::' + str.strip(imp_time))
        # print(udid,ss)
        remain_imp_dict[udid] = ss

    for key in remain_imp_dict.keys():
        udid = key
        imps = remain_imp_dict[key]
        imps = filter_function(imps,MINS)
        tmp_file.write(udid + '\t' + imps + '\n')


def filter_function(imps,mins):
    imp_list = imps.split(',')
    last_mins = -9999
    ss = ''
    for imp in imp_list:
        price,imp_time = imp.split('::')
        current_mins = int(imp_time[11:13])*60 + int(imp_time[14:16])
        if current_mins - last_mins >= mins:
            last_mins = current_mins
            ss += imp + ','
    return ss[:-1]

def sum_price():
    tmp_file = open(TMP_FILE,'r')
    all_price = 0.0
    for line in tmp_file:
        udid,imps = line.split('\t')
        for imp in imps.split(','):
            price = imp.split('::')[0]
            all_price += float(price)
    print('sum cost:' + str(all_price))


def new_count():
    tmp_file = open(TMP_FILE,'r')
    new_file = open(NEW_FILE,'r')
    new_dict = {}
    new_count = 0
    for line in new_file:
        udid,new_time = line.split('\t')
        day_diff = 0
        # if '2019-10-02' in new_time:
        #     day_diff = 1440
        new_dict[udid] = int(new_time[11:13])*60 + int(new_time[14:16]) + day_diff
    # for key in new_dict.keys():
    #     print(new_dict[key])
    for line in tmp_file:
        udid,imps = line.split('\t')
        if udid in new_dict:
            new_mins = new_dict[udid]
            for imp in imps.split(','):
                imp_time = imp.split('::')[1]
                # print(imp_time)
                imp_mins = int(imp_time[11:13])*60 + int(imp_time[14:16])
                if 0 < new_mins - imp_mins < 240: #炉石1440，回流240
                    new_count += 1
                    break
    print('sun_new:' + str(new_count))


if __name__ == '__main__':
    for min in [0,5,10,20,30,60,120,240,600,800,1000,1200,1440]: #0,5,10,20,30,60,120,240,600,
        print(str(min) + '=============')
        filter_imp(min)
        sum_price()
        new_count()