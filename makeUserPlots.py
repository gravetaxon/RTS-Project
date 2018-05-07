# makeUserPlots.py
#  input:
#         text file of graphs to print
#         or user inputs
#
# output:
#        graph from pixel database at row,column

#!/usr/local/bin/python3
import os
import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import loader
import settings
from pathlib import Path
if os.name == 'posix':
    os.nice(10)

pixel = loader.load()
(dataMax,supRow,supCol)=pixel.shape
t = np.arange(0,dataMax)
status =True
while(status):
    print ("Please choose between opening a file of (1) (g)raph data, (2) (u)ser input, (e) exit")
    choice= input("Enter choice: ")
    if str(choice) =="1" or str(choice) =="graph" or str(choice) =="g" :
        fileName = input("Enter path and filename of the file to be opened, (ex. './PiCam/output.txt')")
        if Path(fileName).is_file():
            fname = open(str(fileName),'r')
            for line in fname:
             fields = line.strip().split()
             if fields:              #only lines that aren't empty
                 row = int(fields[0])
                 column = int(fields[1])
                 #print(row,column)
                 p = pixel[0:dataMax, row, column]
                 plt.plot(t,p)
                 plt.savefig('./PiCam/Plots/%d_%d' % (row,column))
                 plt.plot(t,p)
                 plt.close()
            status=False # program complete
	    fname.close()
        else:
            status=True
    elif str(choice) == "2" or str(choice) =="user" or str(choice) =="u":
        (row,col)=input("Enter the row and column of the pixel graph separated by _ (ex. '10_4'):  ").split('_')
        if (0<int( row) <supRow) and (0< int(col) <supCol):
            p = pixel[0:dataMax,int(row),int(col)]
            plt.plot(t,p)
            plt.savefig('./PiCam/Plots/%d_%d' % (int(row),int(column)))
            plt.plot(t,p)
            plt.close()
        response = input("Wish to print another plot?")
        if response =="Y" or response=='y':
            status=True
        else:
            status=False
    elif str(choice)=='e' or str(choice)=='exit':
            status=False


