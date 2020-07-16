import os
import time
import glob
import flask


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
sensor_dir = '/sys/bus/w1/devices/'
sensor_folder = glob.glob(sensor_dir + '28*')[0]
sensor_file = sensor_folder + '/w1_slave'

def read_raw_temp():
    f=open(sensor_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    
    lines = read_raw_temp()
    while lines[0].strip()[-3:]!= 'YES':
        time.sleep(0.2)
        lines = read_raw_temp()
    
    equals_pos = lines[1].find( 't=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) /1000.0
        return temp_c
        