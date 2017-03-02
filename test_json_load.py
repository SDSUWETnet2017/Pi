# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 10:13:58 2017
A funtion to test how long it takes to load a .json file from single time
instance and the full database
@author: Stephen West
"""

import time
import json

# below tests the load time of test database
s_time = time.time()
with open('test_data.json') as f:
    x = json.load(f)
end_time = time.time()
load_time = end_time - s_time
print('\n########################################################')
print('<-- .json database load time : ' + str(load_time) + ' s -->')
print('########################################################\n')

# below tests load time of single time instace 
s_time = time.time()
with open('2017-02-28_20-50.json') as f:
    x = json.load(f)
end_time = time.time()
load_time = end_time - s_time
print('\n########################################################')
print('<-- .json database load time : ' + str(load_time) + ' s -->')
print('########################################################\n')