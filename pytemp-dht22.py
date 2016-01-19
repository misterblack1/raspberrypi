# From Jan 18 2016
# Reads temp and humidity for the DHT22 sensor and logs to Syslog
#
import os
import glob
import time
import subprocess
import syslog
import sys
import Adafruit_DHT

#time.sleep(30)

print('Beginning Temperature Monitoring - Raspberry Pi Display Living Room')
syslog.syslog('Beginning Temperature Monitoring - Raspberry Pi Display Living Room')

def read_temp():
        # read from GPIO pin 23 using a DHT22 sensor
        try:
                humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)
                temperature = temperature * 9/5.0 + 32
                return temperature, humidity
        except:
                syslog.syslog('Error: Failed to read from sensor. Will try again.')
                #print('Error: Failed to read from sensor. Will try again.')
                return -99.0,-99.0

while True:
        current_temp, current_humidity = read_temp()
        current_temp = format(current_temp, '.1f')
        current_humidity = format(float(current_humidity), '.1f')
        #print('lr_tempF=' + str(current_temp) +', lr_humidity='+ str(current_humidity))
        syslog.syslog('lr_tempF=' + str(current_temp) +', lr_humidity='+ str(current_humidity))
        time.sleep(59)
