#!/usr/local/bin/python3
import os
import h5py
import pylab
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import loader
import settings
if os.name == 'posix':
    os.nice(10)

pixel = loader.load()
x = np.arange(0,1500)
fname = open("./PiCam/samp_RTS_List_garbage.txt", "r+")
fname.seek(0)



for line in fname:
    fields = line.strip().split()
    if fields:              #only lines that aren't empty
        row = int(fields[0])
        column = int(fields[1])
        #print(row,column)
        p = pixel[0:1500, row, column]
        plt.plot(x,p)
        plt.savefig('./PiCam/Plots/RTSGuess/%d_%d' % (row,column))
        plt.plot(x,p)
        plt.close()
        print ("*")


fname.close()




#x = np.arange(0,500)

#plt.plot(x,p)
