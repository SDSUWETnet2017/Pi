# A python 2.7 module for use on W.E.T. weather system
# Module is used on Raspberry Pi Super Nodes to read sensor 
# data

import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import time
import base64
from Adafruit_BME280 import *


def take_pic(camera,filename='/home/pi/TEST.jpg',
	location='test location',resolution=(600,600),
	brightness=50,rotation=0):

	"""
	This function takes a camera object, filename, location string,
	and resolution and returns a base 64 jpg encoded string.
	
	camera needs to be initialized before call: camera = PiCamera()

	image can be decoded on reception with following code
	f = open('filename.jpg', 'wb')
	f.write(base64.b64decode(im_str)
	f.close()
	"""

	# Create timestamp
	timestruct = time.localtime()
	timestamp = str(timestruct[0]) + '-' + str(timestruct[1])
	timestamp += '-' + str(timestruct[2]) + ' ' +  str(timestruct[3])
	if timestruct[4] < 10:
	        timestamp += ':0' + str(timestruct[4])
	else:
		 timestamp += ':' + str(timestruct[4])	

	# set size of image
	camera.resolution = resolution
	# rotate image
	camera.rotation = rotation
	camera.start_preview()
	camera.brightness = brightness
	# Put timestamp on pic
	camera.annotate_text = location + ' ' + timestamp

	# Puts black box around timestamp
	#camera.annotate_background = 0x0000ff
	#camera.annotate_foreground = 0xffff00

	# Set size of stamp, font can be between 6 and 160
	camera.annotate_text_size = 6

	# let camera take in light
	sleep(1)

	# save pic
	camera.capture(filename)
	camera.stop_preview()

	# encode .jpg file as string
	with open(filename,"rb") as imageFile:
	# converts to str
		im_str = base64.b64encode(imageFile.read())

	return im_str

def read_BME(sensor_BME):
	"""
	A funtion that returns pressure, humidity, and 
	pressure as read by BME 280 sensor

	Temperature in degrees C
	Humidity as a percentage
	Pressure in Pascalls
	
	sensor must be initialized with following code 
	before call
	
	sensor_BME = BME280(mode=BME280_OSAMPLE_8)
	
	BME_280 uses I2C
	"""

	h = sensor_BME.read_temperature()
        p = sensor_BME.read_pressure()
        t = sensor_BME.read_temperature()
	
	return h,p,t
