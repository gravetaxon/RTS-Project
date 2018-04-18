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
fname = open("./PiCam/samp_WN_List.txt", "r+")
fname.seek(0)
print ("This will create plots assoicated with white noise, approx 300 mb, are you sure you wish to continue?")
response = input("[Y]es/[N]o? ")
if response =="Yes" or response == "yes" or response == "y" or response == "Y" :
 for line in fname:
     fields = line.strip().split()
     if fields:              #only lines that aren't empty
         row = int(fields[0])
         column = int(fields[1])
         #print(row,column)
         p = pixel[0:1500, row, column]
         plt.plot(x,p)
         plt.savefig('./PiCam/Plots/%d_%d' % (row,column))
         plt.plot(x,p)
         plt.close()
else:
 print ("exiting...")

fname.close()




#x = np.arange(0,500)

#plt.plot(x,p)
