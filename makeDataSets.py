## @package makeDataSets.py
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

## Signal definitions
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

    # create the dataset from the text file that holds the listings
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
        elif sigType == nrtsSig and args.nrtsPath != None:
            # we have an argument passes that requests a rts analysis and have data
            szfilePath = Path(args.nrtsPath)
            if szfilePath.is_file():
                inputFile = open(str(args.nrtsPath),'r')
            else:
                inputFile = 0
            if type(inputFile) != int :
                # inputfile was succesful in opening the data!
                inputList = inputFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
                # The triple replace is to handle errors in the source file from lines with three newlines
                inputFile.close()
            else:
                inputList = ""
        elif sigType == mrtsSig and args.mrtsPath != None:
            # we have an argument passes that requests a rts analysis and have data
            szfilePath = Path(args.mrtsPath)
            if szfilePath.is_file():
                inputFile = open(str(args.mrtsPath),'r')
            else:
                inputFile = 0
            if type(inputFile) != int :
                # inputfile was succesful in opening the data!
                inputList = inputFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
                # The triple replace is to handle errors in the source file from lines with three newlines
                inputFile.close()
            else:
                inputList = ""
        elif sigType == ertsSig and args.ertsPath != None:
            # we have an argument passes that requests a rts analysis and have data
            szfilePath = Path(args.ertsPath)
            if szfilePath.is_file():
                inputFile = open(str(args.ertsPath),'r')
            else:
                inputFile = 0
            if type(inputFile) != int :
                # inputfile was succesful in opening the data!
                inputList = inputFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
                # The triple replace is to handle errors in the source file from lines with three newlines
                inputFile.close()
            else:
                inputList = ""
        else:
            print("DEBUG: signal file not found")
            return (False,0,0,-2)
        print("DEBUG: generating dataset from file {}".format(szfilePath))
        deadList = 0
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
                    deadList+=1

            if abs(tr_count-listLen)>delta:
                return (False, 0,0,-1)
            else:
                return (True, x_train,y_train, tr_count)
        else:
            print("DEBUG: Dataset is too small")
# ENDOF makeTrainingData

def makeTestingData (args, pixel, minSize, sigType):
    #inputs:
    # args     -> all commandline arguments
    # pixel    -> dataset
    # minSize  -> testingSizetest
    # sigType  -> signal type
    #outputs:
    # x_test  -> pixel data for testing
    # y_test  -> values for the data type
    # status   -> bool value of process success
    #

    (dataMax, supRow, supCol) = pixel.shape
    # create the dataset from the text file that holds the listings
    if sigType <= maxSig and sigType >= minSig:
        # Signal type is something that we understand
        if sigType == rtsSig and args.testrtsPath != None:
            # we have an argument passes that requests a rts analysis and have data
            szfilePath = Path(args.testrtsPath)
            if szfilePath.is_file():
                inputFile = open(str(args.testrtsPath),'r')
            else:
                inputFile = 0
            if type(inputFile) != int :
                # inputfile was succesful in opening the data!
                inputList = inputFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
                # The triple replace is to handle errors in the source file from lines with three newlines
                inputFile.close()
            else:
                inputList = ""
        elif sigType == nrtsSig and args.testnrtsPath != None:
            # we have an argument passes that requests a rts analysis and have data
            szfilePath = Path(args.testnrtsPath)
            if szfilePath.is_file():
                inputFile = open(str(args.testnrtsPath),'r')
            else:
                inputFile = 0
            if type(inputFile) != int :
                # inputfile was succesful in opening the data!
                inputList = inputFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
                # The triple replace is to handle errors in the source file from lines with three newlines
                inputFile.close()
            else:
                inputList = ""
        elif sigType == mrtsSig and args.testmrtsPath != None:
            # we have an argument passes that requests a rts analysis and have data
            szfilePath = Path(args.testmrtsPath)
            if szfilePath.is_file():
                inputFile = open(str(args.testmrtsPath),'r')
            else:
                inputFile = 0
            if type(inputFile) != int :
                # inputfile was succesful in opening the data!
                inputList = inputFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
                # The triple replace is to handle errors in the source file from lines with three newlines
                inputFile.close()
            else:
                inputList = ""
        elif sigType == ertsSig and args.testertsPath != None:
            # we have an argument passes that requests a rts analysis and have data
            szfilePath = Path(args.testertsPath)
            if szfilePath.is_file():
                inputFile = open(str(args.testertsPath),'r')
            else:
                inputFile = 0
            if type(inputFile) != int :
                # inputfile was succesful in opening the data!
                inputList = inputFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
                # The triple replace is to handle errors in the source file from lines with three newlines
                inputFile.close()
            else:
                inputList = ""
        else:
            print("DEBUG: signal file not found")
            return (False,0,0,-2)

        deadList = 0
        testLen  = len(inputList)
        if (testLen >= minSize):
            # we have enough data to do stuff
            x_test = np.zeros((testLen,dataMax))
            y_test = np.zeros(testLen)
            td_count = 0
            for each in inputList:
                if (each != ''):
                    (row,col)=each.split()
                    (row,col)=(int(row),int(col)) # convert the text strings into numbers
                    if (row<=supRow) and (col<=supCol):
                        x_test[td_count] = (pixel[0:dataMax,row,col])
                        y_test[td_count] = sigType
                        td_count +=1
                    else:
                        print("DEBUG: Error data out of range (testing rts bin)")
                        break
                else:
                    deadList +=1

            if abs(td_count - testLen) >=delta :
                print("DEBUG: We have lost data!!!! (testing bin)")
                print("DEBUG: Sizes:\n\t [dataWritten:dataExpected]\n{}:{}".format(td_count,testLen))
                return (False, 0,0,-1)
            else:
                print ("DEBUG: Dataset complete (testing bin)")
                return (True, x_test,y_test,td_count)

        else:
            # uhhh we need more data
            print("DEBUG: Too small of dataset, less than {} for all of the data types (testing bin)".format(testingTrainSize))
#ENDOF makeTestingData

def dataFactors ( arrayLen, dataMax,  supRow, supCol):
    # Here we do the prime magic on the training dataset!
    # take the length of the training dataset and use prime factorization on it
    if (arrayLen > 0):
        DataFactor = loader.prime_factors(int(round(arrayLen)))
        ArrayFactor = loader.prime_factors(int(round(dataMax)))
        factors = DataFactor+ArrayFactor
        factors = list(set(factors)) # remove all the duplicates and then get it
                         # back to a list to manipulate it
        factors.sort(reverse=True)

        if (len(factors)>2):
            l=factors.pop(0) # pop the head
            s=factors.pop()  # pop the tail
            ProdFactors =factors # factors without the largest and smallest values
            factors = factors+[l]+[s] # [hidden,head,tail]

        print ("DEBUG: Factors:{}".format(factors))
        # FilterSize is determined by the product of the hidden layers
        # KernelSize is determined by the prime factors themselves
        NumberHLayers_in = len(factors)-2
        print("DEBUG: Possible Hidden Layer count:"+str(NumberHLayers_in))
        print("DEBUG: Prod Factors: {}".format(ProdFactors))
    # Potential bug: What happens when there are no hidden layers?
        if (NumberHLayers_in >0):
            # hidden layers exist! Use all the numbers from 0 to largest
            HiddenLayers_out = NumberHLayers_in
            FilterSize_Prod = 1
            for each in ProdFactors:
                FilterSize_Prod = FilterSize_Prod*int(each)
            print("DEBUG: FilterSize raw: {}".format(FilterSize_Prod))
            FilterSize_out = int(loader.smallest_power(FilterSize_Prod,2))
        # Check the hidden layer math
        # InputLayerKernel - sum(HiddenLayers) > OutputLayerKernel+1
        # and
        # 1stHL - sum(HiddenLayers) > OutputLayerKernel
        KernelSizes='['
        for each in factors:
            KernelSizes+=str(each)+','
        KernelSizes=KernelSizes[:-1]
        KernelSizes+=']'
        print("DEBUG: Kernel Size: "+KernelSizes)
        print("DEBUG: Filter Size: "+str(FilterSize_out))
        settingsFile = open('./settings.py','r')
        settingsData = settingsFile.read()
        print("Current settings data:\n{}".format(settingsData))
        settingsFile.close()

        if (settingsData.find('KernelSizes=')<0):
            settingsData+="KernelSizes="+KernelSizes+'\n'
        elif (settingsData.find('KernelSizes=')>=0):
            posbValue=settingsData.find('KernelSizes=') # What position does the string start
            poseValue=settingsData[posbValue:].find('\n')        # and where does it end? On the first newline
            settingsData=settingsData[:posbValue]+"KernelSizes="+KernelSizes+'\n'+settingsData[(posbValue+poseValue):]

        if (settingsData.find('HiddenLayers=')<0):
            settingsData+="HiddenLayers="+str(HiddenLayers_out)+'\n'
        elif (settingsData.find('HiddenLayers=')>=0):
            posbValue = settingsData.find('HiddenLayers=')
            poseValue = settingsData[posbValue:].find('\n')
            settingsData = settingsData[:posbValue]+"HiddenLayers="+str(HiddenLayers_out)+'\n'+settingsData[(posbValue+poseValue):]

        if (settingsData.find('FilterSize=')<0):
            out = (str(FilterSize_out)+',')*(len(factors))
            out = '['+out[:-1]+']'
            settingsData+="FilterSize="+out+'\n'
        elif (settingsData.find('FilterSize=')>=0):
            out = (str(FilterSize_out)+',')*(len(factors))
            out = '['+out[:-1]+']'
            posbValue = settingsData.find('FilterSize=')
            poseValue = settingsData[posbValue:].find('\n')
            settingsData=settingsData[:posbValue]+'FilterSize='+out+'\n'+settingsData[(posbValue+poseValue):]

        if (settingsData.find('Loss=')<0):
            settingsData +="Loss='binary_crossentropy'\n"
        elif (settingsData.find('Loss=')>=0):
            posbValue = settingsData.find('Loss=')
            poseValue = settingsData[posbValue:].find('\n')
            out="Loss=out+='binary_crossentropy'\n"
            settingsData= settingsData[:posbValue]+out+settingsData[(posbValue+poseValue):]

        if (settingsData.find('dataShape=')<0):
            settingsData +="dataShape=({},{},{})".format(dataMax, supRow, supCol)+'\n'
        elif (settingsData.find('dataShape=')>=0):

            posbValue = settingsData.find('dataShape=')
            poseValue = settingsData[posbValue:].find('\n')
            out = "dataShape=({},{},{})".format(dataMax, supRow, supCol)+'\n'
            settingsData = settingsData[:posbValue]+out+settingsData[(posbValue+poseValue):]
        settingsFile = open('./settings.py','w')
        settingsData= settingsData.replace('\n\n','\n').replace('\n \n','\n')
        print ("Data to be written:\n{}".format(settingsData))
        bytesWritten = settingsFile.write(settingsData)
        settingsFile.close()
        if (len(settingsData)==bytesWritten):
            status = True
        return status
    else:
        print("DEBUG: we had a failure to communicate...")
        return False
#ENDOF dataFactors

def main ():
    #import settings
    if os.name == 'posix':
        os.nice(10)

    # Open the input files

    # Add commandline parsing
    # short codes are single char only!
    parser = argparse.ArgumentParser(prog='makeDataSets.py', description="Creates the numpy dataset for train, testing, and running keras models")
    parser.add_argument("-r", "--rtsPath",      type=str, help="rtslist file that contains rts signals in col_row format")
    parser.add_argument("-n", "--nrtsPath",     type=str, help="nrtslist file that contains whitenoise signals")
    parser.add_argument("-m", "--mrtsPath",     type=str, help="mrtsList file that has possible rts signals")
    parser.add_argument("-e", "--ertsPath",     type=str, help="ertsList file that contains erratic signals")
    parser.add_argument("-s", "--testrtsPath",  type=str, help="rtsTestlist file that contains rts signals in col_row format for the testing data")
    parser.add_argument("-t", "--testnrtsPath", type=str, help="nrtsTestlist file that contains whitenoise signals for the testing data")
    parser.add_argument("-u", "--testmrtsPath", type=str, help="mrtsTestList file that has possible rts signals for the testing data")
    parser.add_argument("-a", "--testertsPath", type=str, help="ertsTestList file contains the listings for the erratic signals as testing data")
    parser.add_argument("-o", "--oldMethod", action='store_true', help="Activates a special routine that uses binary mode rather than categorical")
    #parser.add_argument("-","--",action='store_true',help="")

    args = parser.parse_args()

    testingSizeTest  = 30
    testingSizeTrain = 200


    pixel = loader.load()
    (dataMax, supRow, supCol) = pixel.shape

    # RTS testing and training
    (trainStatus_1, x_train_1,y_train_1, dataCount_1)  = makeTrainingData(args,pixel,testingSizeTrain,rtsSig)
    (testStatus_1, x_test_1,y_test_1,testCount_1)     = makeTestingData(args,pixel,testingSizeTest,rtsSig)
    # mRTS testing and training
    (trainStatus_2, x_train_2,y_train_2, dataCount_2)  = makeTrainingData(args,pixel,testingSizeTrain,mrtsSig)
    (testStatus_2, x_test_2,y_test_2,testCount_2)     = makeTestingData(args,pixel,testingSizeTest,mrtsSig)
    # eRTS testing and training
    (trainStatus_3, x_train_3,y_train_3, dataCount_3)  = makeTrainingData(args,pixel,testingSizeTrain,ertsSig)
    (testStatus_3, x_test_3,y_test_3,testCount_3)     = makeTestingData(args,pixel,testingSizeTest,ertsSig)
    # nRTS testing and training
    (trainStatus_4, x_train_4,y_train_4, dataCount_4)  = makeTrainingData(args,pixel,testingSizeTrain,nrtsSig)
    (testStatus_4, x_test_4,y_test_4,testCount_4)     = makeTestingData(args,pixel,testingSizeTest,nrtsSig)

    trainStatus = trainStatus_1 and trainStatus_2 and trainStatus_3 and trainStatus_4
    testStatus = testStatus_1 and testStatus_2 and testStatus_3 and testStatus_4
    countStatus = False
    dataCountStatus = False
    testCountStatus = False
    dataCount =0
    testCount =0
    if dataCount_1 >=0 and dataCount_2 >=0 and dataCount_3 >=0 and dataCount_4 >=0:
        dataCountStatus = True
        dataCount = dataCount_1+dataCount_2+dataCount_3+dataCount_4
    if testCount_1 >=0 and testCount_2 >=0 and testCount_3 >=0 and testCount_4 >=0:
        testCountStatus = True
        testCount= testCount_1+testCount_2+testCount_3+testCount_4

    countStatus = dataCountStatus and testCountSatus
    if countStatus & trainStatus & testStatus:
        x_train = np.concatenate((x_train_1,x_train_2,x_train_3,x_train_4),axis=0)
        y_train = np.concatenate((y_train_1,y_train_2,y_train_3,y_train_4),axis=0)
        x_test  = np.concatenate((x_test_1,x_test_2,x_test_3,x_test_4),axis=0)
        y_test  = np.concatenate((y_test_1,y_test_2,y_test_3,y_test_4),axis=0)
    else:
        x_train=y_train=x_test=y_test=0

    print ("DEBUG: \n\tSize of training data:\n{} ".format(dataCount))

    if type(x_train) == np.ndarray:
        arrayLen = x_train.shape[0]
        statusFactor                    = dataFactors (dataCount, dataMax,  supRow, supCol)
    else:
        statusFactor = False
    if trainStatus :
        # save the training data
        statusTraining = True
    else:
        # complain
        statusTraining = False
        print("DEBUG: Training data failed!")
    if testStatus :
        # save the testing data
        statusTest = True
    else:
        # complain
        statusTest = False
        print("DEBUG: Testing data failed!")
    # catchall for all possible errors
    status = statusFactor & statusTest & statusTraining & countStatus

    if (status == True):
        print("DEBUG: Saving new numpy datasets")
        np.save('./PiCam/x_train.npy',x_train)
        np.save('./PiCam/x_test.npy',x_test)
        np.save('./PiCam/y_train.npy',y_train)
        np.save('./PiCam/y_test.npy',y_test)
        print("DEBUG: run modeler next")
    else:
        print("DEBUG: We had an error in writing settings data and have not written incompatible training and/or testing data")


main()
