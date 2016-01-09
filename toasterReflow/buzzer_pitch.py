#!/usr/bin/python
# Author: LearningEmbedded.com
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this code and associated documentation files , to use, copy, modify, merge,
# publish, distribute when you agree to the following conditions:
# Attribution : You must give appropriate credit, provide a link to the license, 
#               and indicate if changes were made. You may do so in any reasonable
#               manner, but not in any way that suggests the licensor endorses you 
#               or your use.
# No additional restrictions   You may not apply legal terms or technological 
#                              measures that legally restrict others from doing
#                              anything the license permits.

# http://learningembedded.com/

import Adafruit_BBIO.GPIO as GPIO 		# import gpio module
import time					# import time

class buzzer:
    def __init__(self,buz_pin):
        self.buzzer_pin = buz_pin 				# initialize variable
        GPIO.setup(buz_pin, GPIO.OUT) 		# set pin as output

    def buzz(self,pitch, duration): 			# define a function
        period = 1.0 / pitch  				# calculate period
        delay = period / 2				# calculate delay
        cycles = int(duration * pitch) 		# calculate cycles
        for i in range(cycles): 
            GPIO.output(self.buzzer_pin, True) 		# set pin as high
            time.sleep(delay)
            GPIO.output(self.buzzer_pin, False) 		# set pin as low
            time.sleep(delay)

if __name__=="__main__":
    rs_buzz = buzzer("P8_12")
    while True:
        pitch_s = raw_input("Enter Pitch (200 to 2000): ")  # input pitch values
        pitch = float(pitch_s) 				    # typecast it to float
        duration_s = raw_input("Enter Duration (seconds): ")# enter duration
        duration = float(duration_s) 			    # typecast it to float
        rs_buzz.buzz(pitch, duration)				    # call buzz function
