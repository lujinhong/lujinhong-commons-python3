# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2020年09月25日 10:49
    PROJECT: lujinhong-commons-python3
DESCRIPTION: TODO
"""
import subprocess

cmd = ''

for i in range(4):
    cmd += 'sleep 5 &\n'
cmd += 'wait'
print(cmd)

if subprocess.run(cmd, shell=True).returncode != 0:
    print(1)


# ret1 = subprocess.run(cmd, shell=True)
# print(ret1)



#
# ret1 = subprocess.call('sleep 10 &', shell=True)
# print('1')
# ret2 = subprocess.run('sleep 10 &\nwait', shell=True)
# print('2')
# ret3 = subprocess.run('wait', shell=True)
# print('Finish')