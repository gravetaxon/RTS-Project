# Modular makeDataSets.py
# makeTrainingData will output a numpy array of (arrayLen x dataMax) that will
#   concatenated at the end to compile into the training data to be used
# likewise with makeTestingData
# both of the functions input will also have the definition of the signal (which number)
#  to indicate the signal type.

import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import numpy as np
import os
import loader
import argparse
import os, os.path
from pathlib import Path
import random

delta = loader.Delta
maxSig = 5
minSig = 0

# Signal definitions
nrtsSig = 0 # Signal is not a rts frame
rtsSig  = 1 # Signal is a rts frame
mrtsSig = 2 # Signal is a possible rts frame
ertsSig = 3 # Signal is an erratic signal frame
resv1   = 4 # Reserved for future use.
resv2   = 5 # Reserved for future use.


def makeTrainingData(args, pixel, minSize, sigType):
    #inputs:
    # args     -> all commandline arguments
    # pixel    -> dataset
    # minSize  -> minimum size needed to process (floor of 30 with normally distributed populations)
    # sigType  -> signal indicator (number from 0 to 5)
    #
    #outputs:
    # x_train  -> pixel data for training for sigType
    # y_train  -> values for the data type (sigType)
    # count    -> how many values for this sigType
    # status   -> bool value of process success
    #
    (dataMax, supRow, supCol) = pixel.shape
    if args.oldMethod:
        # create the dataset from the text file that holds the listins
        if sigType <= maxSig and sigType >= minSig:
            # Signal type is something that we understand
            if sigType == rtsSig and args.rtsPath != None:
                # we have an argument passes that requests a rts analysis and have data
                szfilePath = Path(args.rtsPath)
                if szfilePath.is_file():
                    inputFile = open(str(args.rtsPath),'r')
                else:
                    inputFile = 0
                if type(inputFile) != int :
                    # inputfile was succesful in opening the data!
                    inputList = inputFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
                    # The triple replace is to handle errors in the source file from lines with three newlines
                    inputFile.close()
                else:
                    inputList = ""
                deadList =1
                listLen = len(inputList)
                if listLen >= minSize:
                    # Start analysis
                    x_train = np.zeros((listLen,dataMax))
                    y_train = np.zeros(listLen) # output is a "binary value" i.e it either is or is not the signal
                                            # if it is the signal then the model pushes out a one else a zero
                    tr_count =0 # index of where we are in the training set
                    for each in inputLine:
                        if (each != ''):
                            (row,col)=each.split() # we have row col pair, split and test
                            (row,col)=(int(row),int(col)) # convert the text strings into numbers
                            if (row <= supRow) and (col <= supCol) and (row >= 0) and (col >= 0):
                                x_train[tr_count]=(pixel[0:dataMax,row,col])
                                y_train[tr_count]= int(sigType)
                                tr_count +=1
















    else:
        # create the dataset from the directory listing of the correct folder
