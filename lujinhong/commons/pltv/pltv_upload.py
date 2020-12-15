# -*- coding: utf-8 -*-
import time
import sys

import requests
import os

from os.path import exists

os = 'ios'
in_file = '/home/ljhn1829/g83na_pltv/' + os + '.txt'
log_file = 'log.txt' + os

if os == 'ios':
    type_flag = 1
    link_id = '217D8E70D5D0ABE80F0AC9FF28F96ED1'
    id_type = 'idfa'
elif os == 'android':
    type_flag = 2
    link_id = '9FE044E9DF1E4A7ECD2631A892432175'
    id_type = 'advertisingid'
else:
    raise Exception('参数只能是ios或者android')

url = 'https://www.googleadservices.com/pagead/conversion/app/1.0'
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'AdMob/7.10.1 (Android 6.0; en_US; SM-G900F; Build/MMB29M; Proxy)',
}

already_upload_count = 0
if exists(log_file):
    with open(log_file) as log_f:
        already_upload_count = int(log_f.readline().strip())

count = 0
event_name = 'g83na_pltv_' + os
with open(in_file) as f:
    for rdid in f:
        count = count + 1
        if count <= already_upload_count:
            continue
        rdid = rdid.strip()
        if count %100 == 0 :
            with open(log_file, 'w') as log_f:
                log_f.write(str(count))
        pay_load = {
            'dev_token': 'QKlG7YMEq7ne-qofbVa6fg',
            'link_id': link_id,
            'app_event_type': 'custom',
            'app_event_name': event_name,
            'rdid': rdid,
            'id_type': id_type,
            'lat': 0,
            'app_version': '1.2.4',
            'os_version': '6.0',
            'sdk_version': '1.9.5r6',
            'timestamp': time.time(),
        }
        response = requests.get(url, headers=headers, params=pay_load)
        if count % 100 == 0:
            print(time.time(), in_file, count, response)
