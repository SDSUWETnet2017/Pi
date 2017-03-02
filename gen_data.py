# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Weather Engineering Team
Created on Tue Feb 28 10:46:24 2017

A function to be run on RPI supernode to generate 
single time  instance .json files that mimic real
data comming in from nodes

@author: Stephen West
"""

import time
from node import Node
import json
from matplotlib import pyplot as plt

latitudes = [32.775660,32.776315,32.776075,32.775567,32.775881,32.776689,
                 32.776804,32.776898,32.775683,32.774507]
                 
longitudes = [-117.071543, -117.071475,-117.071910,-117.071914,
                  -117.071002,-117.071394,-117.071858,-117.072355,-117.072382,
                  -117.071407]

N_nodes = 10
data_dict = {}
nodes = []
''' Use this code to generate a single time instance'''
#for i in range(N_nodes):
#    if i % 5 == 0:
#        node = Node(i+1,node_type='super')
#    else:
#        node = Node(i+1,node_type='sub')
#
#    data_dict['node '+str(i+1)] = [node.return_dict(),
#                                  latitudes[i],longitudes[i]]
#    
#with open('test_data.json','w') as f_obj:
#    json.dump(data_dict,f_obj)
#    
#    
#
''' Use this code to generate a single time instance every 10 minutes'''
#refresh time in minutes
refresh_time = 9.4

start_time = 0

for i in range(N_nodes):
    if i % 5 == 0:
        node = Node(i+1,node_type='super')
    else:
        node = Node(i+1,node_type='sub')
    nodes.append(node)

while True:
    if time.time() >= start_time + refresh_time*60 or start_time == 0:
        start_time = time.time()
        for i in range(N_nodes):  
            data_dict['node '+str(i+1)] = [nodes[i].return_dict(),
                                          latitudes[i],longitudes[i]]

# an error may occur if the file is open when the program tries to 
# write to it, a try except block prevents that

        try:
# 		use below code to timestamp file
#            fmt = '%Y-%m-%d_%H-%M'
#           timestamp = time.strftime(fmt,time.localtime())
#            f_name = timestamp + '.json'
            f_name = 'test_data.json'
                with open(f_name,'w') as f_obj:
           	json.dump(data_dict,f_obj)
        except:
            print('oops file not saved')
            pass
# Sleep for 30 sec
    time.sleep(30)
    
    
    
    

    
