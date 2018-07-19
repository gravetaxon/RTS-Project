# voter.py
# load all of the model, have them to compare


# use openModel from makeOutput as basis to open the models
import h5py
from keras.models import load_model
import pylab
import matplotlib
#matplotlib.use('Agg')
#Not needed since the setting has been migrated to the user arguments in the home directory
import matplotlib.pyplot as plt
import numpy as np
import os
import loader
import settings
import sys
import random
import pathlib
from pathlib import Path
from loader import getSetting
from loader import setSetting
from scipy.io import savemat

## Signal definitions
nrtsSig = 0 # Signal is not a rts frame
rtsSig  = 1 # Signal is a rts frame
mrtsSig = 2 # Signal is a possible rts frame
ertsSig = 3 # Signal is an erratic signal frame
resv1   = 4 # Reserved for future use.
resv2   = 5 # Reserved for future use.
# from 0.01 to 1 scales the dataset for debugging purposes
DebugPercent=0.50 # Release has DebugPercent = 1.00 (100% of data)
ReleaseModel= True # Which model to load? True -> big data, False -> Small dataset

def openModel(name):
    if type(name) == str:
        SavedModels = getSetting('./settings.txt','{}Saved='.format(name)).split(',')
    # Saved Models has the model numbers that are to be loaded
    NumModel = len(SavedModels)
    ModelsUsed =str(name)+":"
    for each in SavedModels:
        ModelsUsed+=str(each)+','
    ModelsUsed=ModelsUsed[:-1]
    print ("DEBUG: Using the following models: {}".format(ModelsUsed))
    models = []
    print("DEBUG: Loading models...")
    for each in SavedModels:
        model_name = './PiCam/CNNlin_model_{}_{}.h5'.format(str(name),str(each))
        print("Loading model {}".format(each))
        model = load_model(model_name)
        models.append(model)
    modelLoad = min(5,NumModel) # Load no more than five of the models
    modelOut = random.sample(models,modelLoad)
    return (modelOut, len(modelOut))


def askVoter(name, modelIn, numModel, dataIn):
    # Ask a group of models from modelIn to judge on a pixel
    # name     <- Name of the model/voter
    # modelIn  <- group of models to use
    # numModel <- How many models are in modelIn
    # dataIn   <- pixel data from runVotes loop
    # Output   -> float number between 0 and 1
    vote = 0
    votes =[]
    for voter in modelIn:
        mp = voter.predict(dataIn)
        votes.append(mp[0])
    #print("DEBUG: {} Votes: {}".format(name,votes))
    if len(votes)>0:
        vote = np.mean(votes)
    return float(vote)

def runVotes():
    # load RTS, ERTS, and MRTS models
    # then load dataset
    # next for each row and col ask the "voters" to vote on the respective model type
    # Since each vote is between 0 and 1, use expected value formula to determine the category
    #
    # Load models
    (modelRTS,numRts)    = openModel('RTS')
    (modelMRTS,numMrts)  = openModel('MRTS')
    (modelERTS,numErts)  = openModel('ERTS')
    (modelNRTS, numNrts) = openModel('NRTS')
    pixel = loader.load(ReleaseModel) # Load the big guy
    DataShape = pixel.shape
    maxRow = int(round(DataShape[1]*DebugPercent)) #1944
    maxCol = int(round(DataShape[2]*DebugPercent)) #2592
    votesArray = np.zeros((maxRow,maxCol)) # 1944 x 2592
    print("DEBUG: votesArray size: {}".format(votesArray.shape))
    for i in range(0,maxRow):
        print("Percent complete: {}".format(float(i*100.0/maxRow)))
        for j in range(0,maxCol):
            pix = pixel[0:DataShape[0],i,j]  # HOTFIX: Rotated the data set back to proper position had row and columns swapped
            ppix = pix[None,:,None]
            # Have RTS Vote
            rtsVote = askVoter('RTS',modelRTS,numRts,ppix)
            # Have MRTS Vote
            mrtsVote = askVoter('MRTS',modelMRTS,numMrts,ppix)
            # Have ERTS Vote
            ertsVote = askVoter('ERTS',modelERTS,numErts,ppix)
            # Have NRTS Vote
            nrtsVote = askVoter('NRTS',modelNRTS,numNrts,ppix)
            # Take expected value
            #print ("nrts, rts,mrts,erts")
            #print(round(nrtsVote ,2), round(rtsVote,2),round(mrtsVote,2),round(ertsVote,2))
            votesArray[i,j]=round(nrtsVote * nrtsSig,2)+ round(rtsVote*rtsSig,2)+round(mrtsVote*mrtsSig,2)+round(ertsVote*ertsSig,2)
    return votesArray
# Threading requires an even split of the dataset so find the intersection of the
# shape of the data's main parameters that we want to split across (row & column)
# pixel.split(N) should split the data into N even blocks


def makeOutput(voterDB=None):
    # each of the votes are to be compiled into an matrix with the cat as the data point
    # Store it into a textfile or numpy file at voterDB

    outarry = runVotes()
    if type(voterDB)==None:
        # Runs and print the array
        print(outarry)
    elif type(voterDB)==pathlib.PosixPath or type(voterDB)==pathlib.WindowsPath:
        # We have been given a path, might be good?
        #np.savetxt(voterDB,outarry,delimiter=',',fmt='%1.2f')	# Matlab compatible fmt
        savemat(voterDB,mdict={'votes':outarry})
        print("File outputted")
        # Pythonic loading of matlab file:
        # scipy.io.loadmat(filepath)['name of array']
    else:
        # check if the file exists and write to it
        print(outarry)
