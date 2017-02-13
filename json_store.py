##### modules used to test save_data

import RPi.GPIO as GPIO
from bottle import route, run, request, response
from bottle import static_file
import time
from time import sleep
from Adafruit_BME280 import *
from picamera import PiCamera
from sensor_functions import *
import base64

#######

import json

def save_data(data,filename='data.json'):
	"""
	A function that stores data in a 
	.json file
	"""
	with open(filename, "w") as f_obj:
		json.dump(data, f_obj)
	return

sensor_BME = BME280(mode=BME280_OSAMPLE_8)
camera = PiCamera()
data_array = []
for i in range(1):

        Humidity, Pascals, Temperature = read_BME(sensor_BME)
	if i>17:
        	im_str = take_pic(camera,filename='test.jpg')
	else:
		im_str = "NONE"
        dict = {
                "node": i,
                "pressure": Pascals,
                "humidity": Humidity,
                "temperature": Temperature,
                "location": "tbd",
                "pic": im_str
                }
	data_array.append(dict)

save_data(data_array)
