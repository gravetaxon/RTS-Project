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
import fnmatch

def buildLists():

    rtsList = []    # RTS files
    nonrtsList = [] # not RTS
    mrtsList=[]   # possible RTS
    ertsList=[]   # possible RTS

    if (loader.ensureFolder("./PiCam") and
    loader.ensureFolder("./PiCam/Plots") and
    loader.ensureFolder("./PiCam/Plots/RTS") and  # RTS
    loader.ensureFolder("./PiCam/Plots/NRTS") and # Not RTS
    loader.ensureFolder("./PiCam/Plots/MRTS") and # maybe RTS
    loader.ensureFolder("./PiCam/Plots/ERTS")): # Erratic RTS
        print ("DEBUG: We are good to go!")
        for each in os.listdir('./PiCam/Plots'):
            if each == "RTS":
                rtsList = os.listdir('./PiCam/Plots/RTS')
            elif each == 'NRTS':
                nonrtsList = os.listdir('./PiCam/Plots/NRTS')
            elif each == 'MRTS':
                mrtsList = os.listdir('./PiCam/Plots/MRTS')
            elif each == 'ERTS':
                ertsList = os.listdir('./PiCam/Plots/ERTS')
            else:
                print ('.') # debug tool to see if anything is happening at all
        # clean each list of 'weird' files #_#.png or #_# only
    # REGEX: [0-9]{1,4}_[0-9]{1,4}
    expression = re.compile('[0-9]{1,4}_[0-9]{1,4}')

    if len(rtsList) != 0:
        with  open('./PiCam/RTS_list.txt',"w+") as fname:
            for each in rtsList:
                    if expression.match(each) != None:
                        fname.write((each+"\n").replace('.png','').replace('_',' '))
    else:
        print("DEBUG: Nothing in the RTS folder")
    if len(nonrtsList)!=0:
        with open('./PiCam/NRTS_list.txt',"w+") as gname:
        for each in nonrtsList:
                if expression.match(each) != None:
                    gname.write((each+"\n").replace('.png','').replace('_', ' '))
    else:
        print("DEBUG: Nothing in the NRTS folder")
    if len(mrtsList)!=0:
        with open('./PiCam/MRTS_list.txt',"w+") as hname:
            for each in mrtsList:
                    if expression.match(each) != None:
                        hname.write((each+"\n").replace('.png','').replace('_',' '))
    else:
        print("DEBUG: Nothing in the MRTS folder")

    if len(mrtsList)!=0:
        with open('./PiCam/ERTS_list.txt',"w+") as hname:
            for each in ertsList:
                    if expression.match(each) != None:
                        hname.write((each+"\n").replace('.png','').replace('_',' '))
    else:
        print("DEBUG: Nothing in the ERTS folder")
