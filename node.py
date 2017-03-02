# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:17:33 2017

A class to be used on gen_data_2017-02-15.py
to generate test data for WETnet site

Data vectors hold a week of test data

To change duration of data change duration of data
edit temperature_sig.make_wave(duration=#days,framerate=144)


@author: Stephen West
"""

import thinkdsp as td
import random
import numpy as np
import math
import base64
import time

        
class Node():
    
    def __init__(self, number,node_type='sub'):
        
        self.number = number
        
        self.node_type = node_type
        
        self.start_time =  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        self.temp_vect = self.get_temp()
      
        self.humidity = self.get_humidity()
        
        self.UV = self.get_UV()
        self.n = 0
        self.get_n_initial()
        
        if self.node_type == 'sub':
            pass
        elif self.node_type == 'super':
            self.winddirect = random.random()*360
            self.windspeed = self.get_windspeed()   
            self.windgust = self.windspeed[self.n] + random.randint(0,10)+random.random()
            self.pressure = random.randint(96400000,96500000)/1000
            
            with open('test_api_decode.jpg',"rb") as imageFile:
                im_str = base64.b64encode(imageFile.read())
            self.pic = str(im_str)[1:] #to display actual picture
    
    def get_temp(self):
        '''
        A function that returns an array with data points that model
        Temperature
        '''
        temperature_sig = td.SinSignal(freq=1,amp=6,offset=(math.pi))
        # add noise
        temperature_sig += td.UncorrelatedUniformNoise()
        # evaluate function for a week(duration=7) ever 10 min (framerate=144)
        temp_wave = temperature_sig.make_wave(duration=8,framerate=144)
        # set ave temp of a node to be between 60 and 75 degrees
        temp_wave.ys += random.randint(60,75)
        return temp_wave.ys

    def get_humidity(self):
        # Model humidity as inverted hamming window with a dc offset 
        # between 50 and 60, for one day
        humidity = np.hamming(len(self.temp_vect)/8) + random.randint(50,60)
        # periodically repeat humidity function for entire week
        humidity = np.tile(humidity,8)
        return humidity
        
    def get_UV(self):
        '''
        A function that returns a week of UV index data as a vector
        '''
        n_points = len(self.temp_vect)//8
        # mean occurs at noon or in the middle of vector
        mean = 144/2
        # model UV index as normal distrobution with mean at 12:00 and var of 3.5 hrs
        sigma = math.sqrt(35*6)
        PI = math.pi
        UV = np.zeros(144)
        #time_vect = []
        for n in range(n_points):
            UV[n]= (1/(sigma*math.sqrt(2*PI)))*math.exp(-((n-mean)**2)/(2*(sigma**2)))


        # normalize UV function to have a peak of 1
        UV /= max(UV)
        # Guive vector a peak on UV index
        UV *= random.uniform(4,7)
        # Gen data for a week
        return np.tile(UV,8)
        
    def get_windspeed(self):
        '''
        A function that returns a week of windspeed data as a vector
        '''
        wind_sig = td.SinSignal(freq=1,amp=6,offset=(math.pi))
        # add noise
        wind_sig += td.UncorrelatedUniformNoise()
        # evaluate function for a week(duration=7) ever 10 min (framerate=144)
        wind_wave = wind_sig.make_wave(duration=8,framerate=144)
        # set ave temp of a node to be between 60 and 75 degrees
        wind_wave.ys += random.randint(1,10)
 
        return wind_wave.ys
        
    def get_wind_direction(self):
        # randomly change wind direction 
        rand = random.randint(1,11)
        if self.n % rand == 0:
            self.winddirect = random.random()*360
        return
    
    def get_wind_gust(self):
        self.windgust = self.windspeed[self.n] + random.randint(0,10)
        self.windgust += random.random()
        return
        
        
    def get_n_initial(self,Ts=10):
        '''data vectors will have phse shift depending on start time'''
        #get phase shift between start of wave and start time
        s_time = time.localtime()
        start_time = int(s_time[3]*60+s_time[4])
        self.n = start_time//10

        return
    
    def get_time_stamp(self):
        fmt = '%Y-%m-%d %H:%M'
        timestamp = time.strftime(fmt,time.localtime())
        return timestamp
        
    def return_dict(self,Ts=10):
        sensor_data_dict = {}
        # data vectors will have phase shift depending on start time

        if self.node_type == 'sub':
            data_vect=[self.temp_vect[self.n],self.humidity[self.n],self.UV[self.n]]
        else:
            self.get_wind_gust()
            self.get_wind_direction()
            data_vect=[self.temp_vect[self.n],self.humidity[self.n],self.UV[self.n],
                       self.pressure, self.windspeed[self.n],self.winddirect,
                        self.windgust, self.pic]
            

        sensor_data_dict[self.get_time_stamp()] = data_vect
        
        self.n += 1
        return sensor_data_dict

