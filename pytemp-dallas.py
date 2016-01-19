# From Jan 18 2016
# for the Dallas temp sensor DS18B20 and similar
# Requires the OneWire (W1) modules be installed on your Pi
#
import os
import glob
import time
import subprocess
import syslog

#time.sleep(30)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder1 = glob.glob(base_dir + '10*')[0]
device_file1 = device_folder1 + '/w1_slave'

syslog.syslog('Beginning Temperature Monitoring - Raspberry Pi Office Sensor')

def read_temp_raw():
        catdata = subprocess.Popen(['cat',device_file1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = catdata.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

while True:
        current_temp = read_temp()
        #print('Office1=' + str(current_temp))
        syslog.syslog('office1=' + str(current_temp))
        time.sleep(59)
