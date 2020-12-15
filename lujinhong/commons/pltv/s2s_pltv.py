# -*- coding: utf-8 -*-
import asyncio
from aiohttp import ClientSession
from time import time
import sys

os = 'ios'
in_file = '/Users/ljhn1829/Downloads/g83na/' + os + '.txt'

if os == 'ios':
    type_flag = 1
    link_id = '27F969CF085D78555060DE2216FC720A'
    id_type = 'idfa'
elif os == 'android':
    type_flag = 2
    link_id = '7440EC81E1C2ED7D2622A2D31394EC1F'
    id_type = 'advertisingid'
else:
    raise Exception('参数只能是ios或者android')


url = 'https://www.googleadservices.com/pagead/conversion/app/1.0'
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'AdMob/7.10.1 (Android 6.0; en_US; SM-G900F; Build/MMB29M; Proxy)',
}


start_time = time()


async def get_url(url, pay_load):
    async with ClientSession() as session:
        async with session.get(url, params=pay_load) as response:
            response = await response.read()
            print(response)

tasks = []
with open(in_file) as f:
    count = 1
    for rdid in f:
        rdid = rdid.strip()
        pay_load = {
            'dev_token': 'QKlG7YMEq7ne-qofbVa6fg',
            'link_id': link_id,
            'app_event_type': 'custom',
            'app_event_name': 'g83na_pltv_'+os,
            'rdid': rdid,
            'id_type': id_type,
            'lat': 0,
            'app_version': '1.2.4',
            'os_version': '6.0',
            'sdk_version': '1.9.5r6',
            'timestamp': str(time()),
        }
        task = asyncio.ensure_future(get_url(url, pay_load))
        tasks.append(task)
        count += 1
        if count % 100000 == 0 :
            print(count)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
print('total_time: %s' % (time() - start_time))
