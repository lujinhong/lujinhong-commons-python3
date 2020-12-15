# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2019年10月08日 14:57
    PROJECT: lujinhong-commons-python3
DESCRIPTION: 新增计划，看看限制曝光对点击有多大影响
"""

IMP_FILE = '/Users/ljhn1829/Downloads/g10/imp.txt'
TMP_FILE = '/Users/ljhn1829/Downloads/g10/tmp.txt'

def filter_imp(MINS):
    remain_imp_dict = {}
    imp_file = open(IMP_FILE, 'r')
    tmp_file = open(TMP_FILE, 'w')
    for line in imp_file:
        udid,req_id,imp_id,price,imp_time,is_click = line.split('\t')
        ss = ''
        if udid in remain_imp_dict:
            ss = remain_imp_dict[udid] + ','
        ss = ss + (price + '::' + str.strip(imp_time) + "::" + str.strip(is_click))
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
        price,imp_time,is_click = imp.split('::')
        current_mins = int(imp_time[11:13])*60 + int(imp_time[14:16])
        if current_mins - last_mins >= mins:
            last_mins = current_mins
            ss += imp + ','
        # else:
        #     print(imps)
    return ss[:-1]


def sum_price_click(min):
    tmp_file = open(TMP_FILE,'r')
    all_price = 0.0
    all_click = 0
    uniq_click = 0
    for line in tmp_file:
        udid,imps = line.split('\t')
        if '::1' in line:
            uniq_click += 1
        # flag = 0
        for imp in imps.split(','):
            price = imp.split('::')[0]
            is_click = imp.split('::')[2]
            if price == '-2': price = '0.0'
            all_price += float(price)
            all_click += int(is_click)
            # if is_click == '1': flag = 1
        # uniq_click += flag
    print(str(min) + '\t' + str(all_price) + "\t" + str(all_click) + "\t" + str(uniq_click))




if __name__ == '__main__':
    # filter_imp(1)
    # sum_price_click(1)
    for min in [0,1,2,3,4,5,6,7,8,9,10,15,20,30,60]: #0,5,10,20,30,60,120,240,600,
        # print(str(min) + '=============')
        filter_imp(min)
        sum_price_click(min)
