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
offset_flag = False


BS_COMPORT = 'COM3' # ron
# BS_COMPORT = 'COM4' # usually com3 or com4 depending on computer
# check Ports under device manager afetr plugging in K64F
BS_BAUDRATE = 115200


data_file_name = 'imudata.txt'
numSamples = 3000 # 1 kHz sampling in pid loop = 3 sec
alldata = [ [] ] * (numSamples+1)


ser = serial.Serial(BS_COMPORT, BS_BAUDRATE, timeout=30) 

def read_frame():
    temp_array = np.zeros((8,8))
    ser.reset_input_buffer() # discard if current content in buffer
    ser.read_until('Fr',2)   # wait for first character of frame timing
    first_line = ser.readline()
#    print('First line',first_line)
    timestamp = float(first_line.split()[2]) # get time of sample
    print('Time stamp',timestamp)
    for i in range(0,8):
        line = ser.readline()
        line_array = np.array(list(map(float, line.split())))
  #     print(line,line_array)
        temp_array[i] = line_array
 #       pdb.set_trace() 
 #   print(sensor_array)
    ser.flush()  # clear out left over characters
    return temp_array
 
def menu():
    print("-----------------enter char + <cr> --------------------")
    print("s: read sensor        |o: calculate offset")
    print("q: quit        |")
    
     
def display_sensor():
    print('second read is array value')
    temp_array = read_frame()
    sensor_array = temp_array - offset_array
    if offset_flag:
        print('Raw - Offset array\n', sensor_array)
    else:
        print('need offset first')


def read_offset():
    global offset_flag
    print('First read is offset')
    offset_array = read_frame()
    print('Offset array\n', offset_array)
    offset_flag = True
   
def main():
    # 1 second timeout
    print('Sensor Interface to Cap sensor running on K64F')
   #blank out any keypresses leading in...
#    while msvcrt.kbhit():
#        ch = msvcrt.getch()
    menu()
    while True:
        print('>',)
       # keypress = msvcrt.getch()   
        keypress = input()
        if keypress == '?':
            menu()
        elif keypress == 'o':
            read_offset()
        elif keypress == 's':
            display_sensor()
        elif (keypress == 'q') or (ord(keypress) == 26):
            print("Exit.")
            ser.close()
            sys.exit(0)
        else:
            print("** unknown keyboard command** \n")
            menu()    
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




