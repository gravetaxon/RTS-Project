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

## Signal definitions
nrtsSig = 0 # Signal is not a rts frame
rtsSig  = 3 # Signal is a rts frame
mrtsSig = 2 # Signal is a possible rts frame
ertsSig = 1 # Signal is an erratic signal frame
resv1   = 4 # Reserved for future use.
resv2   = 5 # Reserved for future use.


def openModel(name):
    if type(name) == str:
        if name == 'RTS':
            SavedModels =settings.RTSSaved
        elif name == 'MRTS':
            SavedModels =settings.MRTSSaved
        elif name == 'ERTS':
            SavedModels =settings.ERTSSaved
        elif name == 'NRTS':
            SavedModels =settings.NRTSSaved
        else:
            # default behavior
            SavedModels = settings.Saved
    # Saved Models has the model numbers that are to be loaded
    NumModel = len(SavedModels)
    DataShape = settings.dataShape
    TestPercent = 0.01 # set this to the percentage of the data you want to use
    loopData = (int(DataShape[0]),int(DataShape[1]*TestPercent),int(DataShape[2]*TestPercent))
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
    return (models, len(models))


def askVoter(name, modelIn, numModel, dataIn):
    # Ask a group of models from modelIn to judge on a pixel
    # name     <- Name of the model/voter
    # modelIn  <- group of models to use
    # numModel <- How many models are in modelIn
    # dataIn   <- pixel data from runVotes loop
    # Output   -> float number between 0 and 1
    vote = 0
    votes =[]
    voterCount = min(5,numModel) # Max voters is 2 per model
    for voter in random.sample(modelIn,voterCount):
        mp = voter.predict(dataIn)
        votes.append(mp[0])
    print("DEBUG: {} Votes: {}".format(name,votes))
    if len(votes)>0:
        vote = np.mean(votes)
    return float(vote)

def runVotes():
    # load RTS, ERTS, and MRTS models
    # then load dataset
    # next for each row and col ask the "voters" to vote on the respective model type
    # Since each vote is between 0 and 1, use expected value formula to determine the category
    #
    dataShape = settings.dataShape
    # Load models
    (modelRTS,numRts)    = openModel('RTS')
    (modelMRTS,numMrts)  = openModel('MRTS')
    (modelERTS,numErts)  = openModel('ERTS')
    (modelNRTS, numNrts) = openModel('NRTS')
    #pixel = loader.load(True) # Load the big guy
    #maxRow = dataShape[1]
    #maxCol = dataShape[2]
    # TESTING SETUP
    pixel = loader.load(False) # Load the small guy
    maxRow = 10
    maxCol = 10
    # END OF TESTING SETUP
    votesArray = np.zeros((maxRow,maxCol))
    print("DEBUG: votesArray size: {}".format(votesArray.shape))
    for i in range(0,maxRow):
        for j in range(0,maxCol):
            pix = pixel[0:dataShape[0],i,j]
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
            print ("nrts, rts,mrts,erts")
            print(round(nrtsVote ,2), round(rtsVote,2),round(mrtsVote,2),round(ertsVote,2))
            votesArray[i,j]=round(nrtsVote * nrtsSig,2)+ round(rtsVote*rtsSig,2)+round(mrtsVote*mrtsSig,2)+round(ertsVote*ertsSig,2)
    return votesArray

def makeOutput(voterDB=None):
    # each of the votes are to be compiled into an matrix with the cat as the data point
    # Store it into a textfile or numpy file at voterDB
    dataShape = settings.dataShape
    outarry = runVotes()
    if type(voterDB)==None:
        # Runs and print the array
        print(outarry)
    else:
        # check if the file exists and write to it
        print(outarry)
