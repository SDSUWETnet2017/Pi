"""
Weather Engineering Team
3/17/2017
Supernode main function

This program collects and parces UART data from PIC and 
stores formatted data in .json file
"""

import json
import serial
import time
from main_functions import *
from Node import Supernode, Subnode
import RPi.GPIO as GPIO

'''
Initialization Code 
'''

# Node Latitudes and Longitudes in order
# need to take these out once .json config file on volta
latitudes = [32.775660,32.776315,32.776075,32.775567,32.775881]
                 
longitudes = [-117.071543, -117.071475,-117.071910,-117.071914,
                  -117.071002]

# Create subnode and supernode class instances here
# supernode is node 1
supernode = Supernode(1)
subnodes = []
# element 0 in subnode list contains node 2
for i in range(len(latitudes[1:])):
    subnodes.append(Subnode(i+2))

# Create LOG txt file for testing
with open('log.txt', 'w') as f_obj:
	msg = '---Supernode 1 Program Log---\n'
	msg += '---Program Started ' + time.strftime('%Y-%m-%d %H:%M')
	msg += ' ---\n'
	f_obj.write(msg)
	f_obj.close()
	
# Create Error Log to be read by server
with open('Error_Log.txt','w') as f_obj:
	msg = '---Supernode 1 Error Log---\n'
	msg += '---Program Started ' + time.strftime('%Y-%m-%d %H:%M')
	msg += ' ---\n'
	f_obj.write(msg)
	f_obj.close()

# create data dictionary
data = {}

# Initilaize serial port 
# RX in pin 10, GPIO 15
# TX on pin 8, GPIO 14 	
port = serial.Serial('/dev/serial0', baudrate=9600)

# initialize gpio
'''
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT) #GPIO 21 set as output

# see if PIC is ready to read
GPIO.output(21,GPIO.HIGH)

GPIO.output(21,GPIO.LOW)

'''

'''
Action Code 
'''
read_start_seq(port)

print('Program started press "ctrl+z" to stop')
t1 = time.time()
while True:
    
    node_data = read_data(port)
    print(node_data)
    print('time in period : ',((time.time()-t1)/60))
    if not node_data:
        pass
    elif not node_data[0] == 'END':
        # load data into corresponding subnode class
        
        try:
            #print('in update subonode data')
            subnodes[int(node_data[0])-2].update(node_data)
            subnodes[int(node_data[0])-2].read = 1
        except:
            
            pass
    else:
        #print('write to .json\n')
        # reset period timer and send sig to pic to update clk if needed
        sync_PIC(port,t1,10)
        t1 = time.time() # reset cycle 
        # load data into supernode class
        supernode.update(node_data)
        for subnode in subnodes:
            subnode.check_read()
        data['node 1'] = supernode.return_dict()
        for i in range(len(subnodes)):
            data['node '+str(subnodes[i].number)] = subnodes[i].return_dict()

        # check to see if any node was not read and write error in Error Log

        # save data dictionary in .json file
        try:
            with open('newdata1.json','w') as f:
                json.dump(data,f)
        except:
            with open('Error_Log.txt', 'a') as f:
                msg = '- ' + time.strftime('%Y-%m-%d %H:%M',time.localtime())
                msg += ' new data could not be loaded to json file'
                f.write(msg)
        
        
        
