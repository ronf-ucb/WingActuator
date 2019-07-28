# Keyboard control with hall effect sensing and telemetry
# updated for IP2.5 and AMS Hall angle sensor Jan. 2013
# treat encoder angle as 16 bits 0 ... 2pi (really 14 bits)
import msvcrt, sys
import numpy as np
from struct import *
import time
import pdb

import serial

offset_array = np.zeros((8,8))  # offset for unloaded sensor
sensor_array = np.zeros((8,8))



BS_COMPORT = 'COM3' # ron
# BS_COMPORT = 'COM4' # usually com3 or com4 depending on computer
# check Ports under device manager afetr plugging in K64F
BS_BAUDRATE = 115200


data_file_name = 'imudata.txt'
numSamples = 3000 # 1 kHz sampling in pid loop = 3 sec
alldata = [ [] ] * (numSamples+1)


ser = serial.Serial(BS_COMPORT, BS_BAUDRATE, timeout=10) 

def read_frame():
    ser.reset_input_buffer() # discard if current content in buffer
    ser.read_until('F',1)   # wait for first character of frame timing
    first_line = ser.readline()
    timestamp = float(first_line.split()[2]) # get time of sample
    print('Time stamp',timestamp)
    for i in range(0,7):
        line = ser.readline()
        line_array = np.array(list(map(float, line.split())))
 #       print(line,line_array)
        sensor_array[i] = line_array
 #       pdb.set_trace() 
 #   print(sensor_array)
    return sensor_array
    
def main():
    # 1 second timeout
    print('Sensor Interface to Cap sensor running on K64F')
    print('First read is offset')
    offset_array = read_frame()
    print('Offset array\n', offset_array)
    print('second read is array value')
    sensor_array = read_frame()
    print('Offset array\n', sensor_array)
#    print('Reading serial port')
#    s = ser.read(200)   
#    print(s)
    ser.close() # close port so won't conflict with next read 


#Provide a try-except over the whole main function
# for clean exit. The Xbee module should have better
# provisions for handling a clean exit, but it doesn't.
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
       ser.close()
    except IOError as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst) 
        print("IO Error.")
        ser.close()




