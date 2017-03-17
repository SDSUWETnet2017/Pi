'''
Weather Engineering Team
2017/03/17
Classes to model the Sub and Super nodes in the weather network
'''
from Adafruit_BME280 import *
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import time
import base64
import SI1145 as SI1145

class Subnode():
    '''
    A class to format data from the Subnode
    '''
    def __init__(self,number):
        
        self.number = number
        self.temperature = 0
        self.humidity = 0
        self.UV = 0
        self.read = 0

    def format_temperature(self,temp):
        '''
        a function that takes temperature i2c hex val and returns
        a float with temperature in degrees f
        '''
        self.temperature = ((175.72*temp) / 65536 ) - 46.85
        self.temperature = self.temperature *(9/5)+32
    
        return

    def format_humidity(self,humidity):
        '''
        a function that takes humidity i2c hex val and returns a
        float with humidity in %
        '''
        self.humidity = ((125*humidity)/65536)-6

        
        return

    def format_uv(self,uv):
        '''
        a function that takes UV i2c data and returns a float with
        the uv index
        '''
        self.UV = uv/100
        
        return

    def update(self, data_vect):
        '''
        A funtion that updates the temperature, humidity, and uv vals from
        the UART data. Will be called in main
        '''
        self.temperture = self.format_temperature(data_vect[1])
        self.humidity = self.format_humidity(data_vect[2])
        self.UV = self.format_uv(data_vect[3])
        
        self.read = 1
        return
    
    def return_dict(self):
        '''
        A function that returns the time stamped data dictionary
        and sets the read flag to 0. Function called from main
        '''
        
        data_dict = {}
        timestamp = time.strftime('%Y-%m-%d %H:%M',time.localtime())
        data_vect = [self.temperature, self.humidity, self.UV]
        data_dict[timestamp] = data_vect

        # reset flag
        self.read = 0
        return data_dict

    def check_read(self,filename='Error_Log.txt'):
        '''
        a fucntion to check to see if the node was loaded with new info and
        write and error log if it was not. functon called from main
        '''
        
        if not self.read:
            msg = '- ' + time.strftime('%Y-%m-%d %H:%M',time.localtime())
            msg += ' NODE ' + str(self.number) +' NOT READ\n'
            with open(filename,'a') as f:
                f.write(msg)
        
        return 


class Supernode():

    def __init__(self,number):

        # initialize variables to 0
        self.number = number
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.UV = 0
        self.pic = ''
        self.air_quality = 0
        self.wind_speed = 0
        self.wind_direction = 0
        self.wind_gust = 0
        
        # initialize sensors
        try:
            self.camera = PiCamera()
        except:
            print('\n-PI camera problem reconnect camera and restart pi\n')
        try:
            self.sensor_BME = BME280(mode=BME280_OSAMPLE_8)
        except:
            print('\n-BME280 not connected-\nTurn off PI and connect sensor')
        try:
            self.uv_sensor = SI1145.SI1145()
        except:
            print('\n-SI1145 not connected-\nTurn off PI and connect sensor')

    def get_BME(self):

        '''
        This is the function that is going to return temperature, humidity
        and pressure from the BME280 sensor
        '''

        self.temperature = self.sensor_BME.read_temperature()
        self.temperature = self.temperature *(9/5)+32
        self.humidity = self.sensor_BME.read_humidity()
        self.pressure = self.sensor_BME.read_pressure()
        
        return

    def format_airQuality(self,airQuality):
        '''
        This function conversts the I2C hexadecimal value to the air
        quality in floating point representation

        '''
        self.air_quality = (363.32*(airQuality-13/4))-0.75
        
        return

    def take_pic(self,filename='/home/pi/pic.jpg',
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

        self.camera.resolution = resolution
	
	# rotate image
	self.camera.rotation = rotation
	self.camera.start_preview()
	self.camera.brightness = brightness
        
	# save pic
	self.camera.capture(filename)
	self.camera.stop_preview()

	# encode .jpg file as string
	with open(filename,"rb") as imageFile:
	# converts to str
		self.pic = base64.b64encode(imageFile.read())
		
        return

    def get_UV(self):

        '''
        This function returns the UV value read from SI1145 sensor
        '''

        self.UV = self.uv_sensor.readUV()/100

        return
    
    def format_windSpeed(self,windSpeed):
        '''
        This function returns the windspeed
        '''
        self.wind_speed = 5.20
        return

    def format_windDirection(self,windDirection):
        '''
        Returns the wind duirection
        '''

        self.wind_direction = 30
        return

    def format_windGust(self,windGust):
        '''
        A function that reads the hex windgust val given by PIC
        and converts it to float
        '''

        self.wind_gust = 5.68
        return
        

    def update(self,data_vect):
        '''
        This function updates all the sensor values or pictures onto a
        data vector
        '''
        self.get_BME()
        self.get_UV()
        self.take_pic()
        self.wind_speed = self.format_windSpeed(data_vect[1])
        self.wind_direction = self.format_windDirection(data_vect[2])
        self.wind_gust = self.format_windGust(data_vect[3])
        self.air_quality = self.format_airQuality(data_vect[4])

        return

    def return_dict(self):
        '''
        A function that returns the time stamped data dictionary
        Function called from main
        '''
        data_dict = {}
        data_vect = [self.temperature,self.humidity,self.UV,self.pressure,
                     self.wind_speed,self.wind_direction, self.wind_gust,
                     self.pic, self.air_quality]
        timestamp = time.strftime('%Y-%m-%d %H:%M',time.localtime())
        data_dict[timestamp] = data_vect
        
        return data_dict


