# -*- coding: utf-8 -*-
from multiprocessing.pool import ThreadPool
from threading import get_ident

from time import time
import sys

from requests import get

if sys.argv[1] == 'ios':
    type_flag = 1
    link_id = '27F969CF085D78555060DE2216FC720A'
    id_type = 'idfa'
elif sys.argv[1] == 'android':
    type_flag = 2
    link_id = '7440EC81E1C2ED7D2622A2D31394EC1F'
    id_type = 'advertisingid'
else:
    raise Exception('参数只能是ios或者android')

start_time = time()


def get_url(url, params, ind):
    response = get(url, params)
    print(response.json(), ind)

url = 'https://www.googleadservices.com/pagead/conversion/app/1.0'
thread_pool = ThreadPool(10)
with open(sys.argv[2]) as f:
    for ind, rdid in enumerate(f):
        rdid = rdid.strip()
        pay_load = {
            'dev_token': 'QKlG7YMEq7ne-qofbVa6fg',
            'link_id': link_id,
            'app_event_type': 'custom',
            'app_event_name': 'g83na_pltv',
            'rdid': rdid,
            'id_type': id_type,
            'lat': 0,
            'app_version': '1.2.4',
            'os_version': '6.0',
            'sdk_version': '1.9.5r6',
            'timestamp': str(time()),
        }
        thread_pool.apply_async(get_url, args=(url, pay_load, ind))
thread_pool.close()
thread_pool.join()

print('total_time: %s' % (time() - start_time))
