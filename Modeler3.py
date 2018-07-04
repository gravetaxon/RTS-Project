#!/usr/local/bin/python3
#  RTS_Project/PyFiles/Updated
from keras.models import Sequential
from keras.layers import Dense, Dropout,Activation
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalAveragePooling1D, MaxPooling1D, Flatten, LSTM
import numpy as np
import os
import sys
import random
import settings
from sklearn.preprocessing import scale
from timeit import default_timer as timer
from scipy import stats
import math

timeStart = timer()

if os.name == 'posix':
    os.nice(10)

def runModel(name=''):
    x_test = np.load('./PiCam/x_test_{}.npy'.format(name))
    x_train = np.load('./PiCam/x_train_{}.npy'.format(name))
    y_test = np.load('./PiCam/y_test_{}.npy'.format(name))
    y_train = np.load('./PiCam/y_train_{}.npy'.format(name))
    X_train = np.expand_dims(x_train, axis=2) # reshape (569, 30) to (569, 30, 1)
    #Y_train = np.expand_dims(y_train, axis=2) # reshape (569, 30) to (569, 30, 1)
    X_test = np.expand_dims(x_test, axis=2) # reshape (569, 30) to (569, 30, 1)
    #Y_test = np.expand_dims(y_test, axis=2) # reshape (569, 30) to (569, 30, 1)

    # Grab the settings from the settings.py file

    NumberHLayers=settings.HiddenLayers
    FilterSize=settings.FilterSize
    KernelSize=settings.KernelSizes

    #NumberHLayers = 4             # Number of hidden layers (excluding input and output layers
    #FilterSize=[62,62,62,62,62,62]      # Filter size for each of the layers
    #KernelSize=[11,7,5,5,11,3]          # The kernel size for each hidden layer plus
                                  # the input and output layers as the last two data points

    MinAccuracy = 0.75
    MaxLosses   = 1.05
    InitialSeed = 311967 # semi-random number to have stablity in the model

    # Control group - Ben's initial attempt.
    # Input  32  12
    # Layer  64  12
    # Output 128 12

    #NumberHLayers = 1
    #FilterSize=[64,32,128]
    #KernelSize=[12,12,12]

    DropPercent =0.5                    # Dropout rate is 50%
    AxisCount = 1
    BatchSize = 16
    Epochs    = 50

    score = []
    saved = []
    losses =[]
    accuracy=[]

    #DEBUG: NumberRoutines was 50
    NumberRoutines = settings.NumberRoutines
    for each in range(NumberRoutines):
        print (each)
        model = Sequential()
        random.seed() # each loop should have a different seed to generate slightly different models
        # Input Layer
        # input_shape means that we are expecting vectors of the form IxDxN where N is the number of data sets (i.e. each picture), I is the index length of the time/indep, and D is the index for the size of the data
        # in our case the data is a 1500x1x4235 shape
        model.add(Conv1D(filters= FilterSize[-2], kernel_size= KernelSize[-2], activation='relu', input_shape=(1500,1,)))
        model.add(MaxPooling1D(3))
        print ("adding input layer")
        if NumberHLayers == 0:
            print("No hidden layers")
        for layer in range(NumberHLayers):
            model.add(Conv1D(filters=FilterSize[layer],kernel_size=KernelSize[layer], activation='relu'))
            print("Adding Layer Conv1D("+str(FilterSize[layer])+",  "+str(KernelSize[layer])+")")
            if layer%2==0:
                   model.add(Dropout(DropPercent))
                   print("Adding dropout")
            model.add(MaxPooling1D(3))
            print("adding pooling")

        # Output Layer
        model.add(Conv1D(filters= FilterSize[-1], kernel_size= KernelSize[-1],activation='relu'))
        model.add(GlobalAveragePooling1D())
        model.add(Dense(units=AxisCount, activation='sigmoid'))
        print("adding output layer")
        model.compile(loss=settings.Loss,
                  optimizer='rmsprop',
                  metrics=['accuracy'])
        model.fit(X_train, y_train, batch_size=BatchSize, epochs=Epochs)
        scr = model.evaluate(X_test, y_test, batch_size=BatchSize)
        losses.append(scr[0])
        accuracy.append(scr[1])
        print ([each]+scr)
        score.append(scr)
        if ((scr[1]>MinAccuracy) and (scr[0]<= MaxLosses)):
            print("DEBUG: Saving model #{}".format(each))
            model.save('./PiCam/CNNlin_model_{}_{}.h5'.format(str(name),str(each)))
            saved.append(str(each))

    print (score)

    lossesMean = np.mean(losses)
    lossesVar = np.var(losses)
    accuracyMean = np.mean(accuracy)
    accuracyVar = np.var(accuracy)

    print ("Statistics of model:\n\tLosses:\n\t\tMean: {}\t\tVariance: {}\n\tAccuracy:\n\t\tMean: {}\t\tVariance:{}".format(lossesMean,lossesVar,accuracyMean,accuracyVar))
    df_=NumberRoutines-1
    cv=stats.t.ppf(q=0.950, df=df_)
    print ("Criticial Value: {}".format(cv))
    #cv=1.660 # T-stat with n=100, alpha =0.05 -> 95% CI
    ciLosses=[lossesMean-cv*(math.sqrt(lossesVar/NumberRoutines)) ,lossesMean+cv*(math.sqrt(lossesVar/NumberRoutines))]
    ciAccuracy=[accuracyMean-cv*(math.sqrt(accuracyVar/NumberRoutines)) ,accuracyMean+cv*(math.sqrt(accuracyVar/NumberRoutines))]

    print ("95% CI Losses: {}\nAccuracy: ".format(ciLosses,ciAccuracy))

    out = ''
    for each in saved:
        out +=str(each)+','
    out = out[:-1]


    settingsFile = open('./settings.py','r')
    settingsData = settingsFile.read()
    settingsFile.close()
    if  (settingsData.find('{}Saved='.format(name))<0):
        settingsData+='{}Saved=['.format(name)+out+']'
    elif (settingsData.find('{}Saved='.format(name))>=0):
        posbValue = settingsData.find("{}Saved=".format(name))
        poseValue = settingsData[posbValue:].find('\n')
        settingsData = settingsData[:posbValue]+'{}Saved=['.format(name)+str(out) +']\n'+settingsData[(posbValue+poseValue):]

    settingsFile = open('./settings.py','w')
    settingsFile.write(settingsData)
    settingsFile.close()
    timeEnd = timer()
    print("Total time elapsed: {}".format(timeEnd-timeStart))

    print("Run makeOutput.py next to generate output list")
