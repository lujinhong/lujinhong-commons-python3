# -*- coding: utf-8 -*-
import os
import time


while True:
    with os.popen('ps aux | grep s2s_ios') as f:
        t = f.readlines()
        if len(t) <= 2:
            os.system('nohup python3 /home/ljhn1829/g83na_pltv/s2s_ios.py >> ios.log 2>&1 &')
            print(time.time(), 'restart ios')
        with os.popen('ps aux | grep s2s_android') as f:
            t = f.readlines()
            if len(t) <= 2:
                os.system('nohup python3 /home/ljhn1829/g83na_pltv/s2s_android.py >> android.log 2>&1 &')
                print(time.time(), 'restart ios')
        time.sleep(5 * 60)

