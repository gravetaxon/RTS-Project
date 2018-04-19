# 
#
#
#
import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import numpy as np
import loader
import math
import os

rtsList = []    # RTS files
nonrtsList = [] # not RTS
mrtsList=[]   # possible RTS

if (loader.ensureFolder("./PiCam") and
loader.ensureFolder("./PiCam/Plots") and
loader.ensureFolder("./PiCam/Plots/RTS") and  # RTS
loader.ensureFolder("./PiCam/Plots/NRTS") and# Not RTS
loader.ensureFolder("./PiCam/Plots/MRTS") ): # maybe RTS
    print ("DEBUG: We are good to go!")
    for each in os.listdir('./PiCam/Plots'):
        if each == "RTS":
            rtsList = os.listdir('./PiCam/Plots/RTS')
        elif each == 'NRTS':
            nonrtsList = os.listdir('./PiCam/Plots/NRTS')
        elif each == 'MRTS':
            mrtsList = os.listdir('./PiCam/Plots/MRTS')
        else:
            print ('.') # debug tool to see if anything is happening at all
    # clean each list of 'weird' files #_#.png or #_# only

if len(rtsList) != 0:
	with  open('./PiCam/RTS_list.txt',"w+") as fname:
		for each in rtsList:
			fname.write((each+"\n").replace('.png','').replace('_',' '))
else:
	print("DEBUG: Nothing in the RTS folder")
if len(nonrtsList)!=0:
	with open('./PiCam/NRTS_list.txt',"w+") as gname:
		for each in nonrtsList:
			gname.write((each+"\n").replace('.png','').replace('_', ' '))
else:
	print("DEBUG: Nothing in the NRTS folder")
if len(mrtsList)!=0:
	with open('./PiCam/MRTS_list.txt',"w+") as hname:
		for each in mrtsList:
			hname.write((each+"\n").replace('.png','').replace('_',' '))
else:
	print("DEBUG: Nothing in the MRTS folder")
