# Cap sensor interface. K64F running 8x8 capacitive sensor
# R.Fearing July 2019
############# plot won't show until end #####
#import msvcrt, sys

import matplotlib.pyplot as plt
import numpy as np # after matplotlib???
import sys
#from struct import *
#import time
#import pdb
import serial

plt.close("all")   # try to close all open figs

fig, ax = plt.subplots(1, 1)  # create just one plot

offset_array = np.zeros((8,8))  # offset for unloaded sensor
sensor_array = np.zeros((8,8))
offset_flag = False


BS_COMPORT = 'COM4' # ron
# BS_COMPORT = 'COM4' # usually com3 or com4 depending on computer
# check Ports under device manager afetr plugging in K64F
BS_BAUDRATE = 115200


data_file_name = 'imudata.txt'
numSamples = 3000 # 1 kHz sampling in pid loop = 3 sec
alldata = [ [] ] * (numSamples+1)

ser = serial.Serial(BS_COMPORT, BS_BAUDRATE, timeout=30) 

INTENSITY_MAX = 255
INTENSITY_MIN = 0


def plot_array():
    #Z = np.random.rand(8, 8)
    global sensor_array
    Z = sensor_array
    c = ax.pcolor(Z, cmap='Greys', vmin = -250, vmax = 50)
    ax.set_title('Cap sensor')
    fig.tight_layout()
    # plt.show()
    plt.show(block=False)  # this blocks on user input
    plt.pause(0.1) 
    
    


def read_frame():
    temp_array = np.zeros((8,8))
    ser.reset_input_buffer() # discard if current content in buffer
    ser.write(b'r') # send command to read frame
    ser.flush()
    ser.read(3)  # throw out 'r\n*' from K64F
    #char = ser.read(1)
    #while (char != b'F'):
    #    char = ser.read(1)
    #ser.read_until('Fr',2)   # wait for first character of frame timing
    first_line = ser.readline()
#    print('First line',first_line)
    timestamp = float(first_line.split()[2]) # get time of sample
    
    for i in range(0,8):
        line = ser.readline()
        print(i,line)
        line_array = np.array(list(map(float, line.split())))
        temp_array[i] = line_array
 #       pdb.set_trace() 
 #   print(sensor_array)
    ser.flush()  # clear out left over characters
    print('Time stamp',timestamp)  # print at end so don't lose time
    return temp_array
 
def menu():
    print("-----------------enter char + <cr> --------------------")
    print("s: read sensor        |o: calculate offset")
    print("q: quit               |p: plot array")
    
     
def display_sensor():
    global sensor_array, offset_array 
    print('second read is array value')
    temp_array = read_frame()
    sensor_array = temp_array - offset_array
    if offset_flag:
        print('Raw - Offset array\n', sensor_array)
        plot_array()
    else:
        print('need offset first')


def read_offset():
    global offset_flag, offset_array
    print('First read is offset')
    offset_array = read_frame()
    print('Offset array\n', offset_array)
    offset_flag = True
   
def main():
    # 1 second timeout
    print('Sensor Interface to Cap sensor running on K64F')
    print("Note: Will not generate plot until exiting program. matplotlib bug")
   #blank out any keypresses leading in...
#    while msvcrt.kbhit():
#        ch = msvcrt.getch()
 #   pdb.set_trace()
    menu()
    while True:
        print('>',)
       # keypress = msvcrt.getch()   
        keypress = input() # raw_input for python 2.7
        if keypress == '?':
            menu()
        elif keypress == 'o':
            read_offset()
        elif keypress == 's':
            display_sensor()
        elif keypress == 'p':
            plot_array()
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




