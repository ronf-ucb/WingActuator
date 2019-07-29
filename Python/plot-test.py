# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 17:40:10 2019

@author: ronf
"""
# test gray scale plot
import matplotlib.pyplot as plt
import numpy as np
import sys


#import pdb
plt.close("all")   # try to close all open figs

fig, ax = plt.subplots(1, 1)


INTENSITY_MAX = 255
INTENSITY_MIN = 0

def plot_array():
    Z = np.random.rand(8, 8)
    c = ax.pcolor(Z, cmap='Greys')
    ax.set_title('inside plot_array')
    fig.tight_layout()
    plt.show(block=False)  # this blocks on user input
    plt.pause(0.1)          # The plot properly appears.
    
    
    
def main():
    for i in range(0,10):
        print('>',)
        keypress = input()
        print('keypress =', i,keypress)
        plot_array()
    print('Done')
    sys.exit(0)
    
    
    #Provide a try-except over the whole main function
# for clean exit. The Xbee module should have better
# provisions for handling a clean exit, but it doesn't.
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except IOError as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst) 
        print("IO Error.")
       
