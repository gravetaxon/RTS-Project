# voter.py
# load all of the model, have them to compare


# use openModel from makeOutput as basis to open the models
import h5py
from keras.models import load_model
import pylab
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import loader
import settings
import sys
import random


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

    print("DEBUG: Loading models...")
    for each in SavedModels:
        model_name = './PiCam/CNNlin_model_{}_{}.h5'.format(str(name),str(each))
        model = load_model(model_name)
        models.append(model)
    return (model, len(model))

def askVoter(name, modelIn, dataIn):
    # Ask a group of models from modelIn to judge on a pixel
    # name    <- Name of the model/voter
    # modelIn <- group of models to use
    # dataIn  <- pixel data from runVotes loop
    # Output  -> float number


def runVotes():
    # load RTS, ERTS, and MRTS models
    # then load dataset
    # next for each row and col ask the "voters" to vote on the respective model type
    # Since each vote is between 0 and 1, use expected value formula to determine the category
    #
    dataShap = settings.dataShape
    votesArray = np.array()

def makeOutput(voterDB):
    # each of the votes are to be compiled into an matrix with the cat as the data point
