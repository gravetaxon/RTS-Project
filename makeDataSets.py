#!/usr/bin/env python3

"""
There are 2,313 RTS candidates, so add 2,637 WN signals to create np.array(4950,1500)
"""

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

def makeTrainingData(args, pixel, minSize):
    #inputs:
    # args     -> all commandline arguments
    # pixel    -> dataset
    # minSize  -> testingSizetrain
    #
    #outputs:
    # x_train  -> pixel data for training
    # y_train  -> values for the data type
    # status   -> bool value of process success
    #

    (dataMax, supRow, supCol) = pixel.shape
    if args.oldMethod:
        # Binary method only
        # rts and nrts only
        print("DEBUG: Activating old binary method!")
        if args.rtsPath != None:
            print("DEBUG: rtsPath is {}".format(args.rtsPath))
            szRtsPath = Path(args.rtsPath)
            if szRtsPath.is_file():
                print("DEBUG: It is a file! Opening rtsFile")
                rtsFile = open(str(args.rtsPath),'r')
            else:
                print ("File not found, opening backup")
                rtsFile = open(('./PiCam/RTS_list.txt'),'r')
        else:
            print("DEBUG: RtsList will be built from directory listing")
            rtsFile = open(('./PiCam/RTS_list.txt'),'r')
        if args.nrtsPath != None:
            print("DEBUG: nrtsPath is {}".format(args.nrtsPath))
            szNrtsPath = Path(args.nrtsPath)
            if szNrtsPath.is_file():
                print("DEBUG: It is a file! Opening nrtsFile")
                nrtsFile = open(str(args.nrtsPath),'r')
            else:
                print ("File not found, opening backup")
                nrtsFile = open('./PiCam/NRTS_list.txt','r')
        else:
            print("DEBUG: Nrts will be built from directory listing")
            nrtsFile = open('./PiCam/NRTS_list.txt','r')
        rtsList  =  rtsFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
        nrtsList = nrtsFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
        rtsFile.close()
        nrtsFile.close()
        deadList = 1
        rtsLen  = len(rtsList)
        nrtsLen = len(nrtsList)
        arrayLen = int(rtsLen + nrtsLen)

        if (arrayLen >= minSize):
            # we have enough data to do stuff
            x_train = np.zeros((arrayLen,dataMax))
            y_train = np.zeros(arrayLen)
            tr_count = 0
            for each in rtsList:
                if (each != '') and (each != '.DS Store'):
                    (row,col)=each.split()
                    if (int(row)<=supRow) and (int(col)<=supCol):
                        x_train[tr_count] = (pixel[0:dataMax,int(row),int(col)])
                        y_train[tr_count] = 0
                        tr_count +=1
                    else:
                        print("DEBUG: Error data out of range (training rts bin)")
                        break
                else:
                    deadList +=1
            for each in nrtsList:
                if (each != '') and (each != '.DS Store'):
                    (row,col)=each.split()
                    if (int(row)<=supRow) and (int(col)<=supCol):
                        x_train[tr_count] = (pixel[0:dataMax,int(row),int(col)])
                        y_train[tr_count] = 1
                        tr_count +=1
                    else:
                        print("DEBUG: Error data out of range (training nrts bin)")
                        break
                else:
                    deadList +=1
            if abs(tr_count - arrayLen) >= delta :
                print("DEBUG: We have lost data!!!! (bin)")
                print("DEBUG: Sizes:\n\t [dataWritten:dataExpected]\n{}:{}".format(tr_count,arrayLen))
                return (False, 0,0,0)
            else:
                print ("DEBUG: Dataset complete")
                return (True, x_train,y_train, tr_count)

        else:
            # uhhh we need more data
            print("DEBUG: Too small of dataset, less than {} for all of the data types (bin)".format(testingTrainSize))
            return(False,0,0,0)
    else:
        # Categorical method
        # rts, nrts, and mrts lists
        print("DEBUG: Categorical method active")
        if args.rtsPath != None:
            print("DEBUG: rtsPath is {}".format(args.rtsPath))
            szRtsPath = Path(args.rtsPath)
            if szRtsPath.is_file():
                print("DEBUG: It is a file! Opening rtsFile")
                rtsFile = open(str(args.rtsPath),'r')
            else:
                print ("File not found, opening backup")
                rtsFile = open(('./PiCam/RTS_list.txt'),'r')
        else:
            print("DEBUG: RtsList will be built from directory listing")
            rtsFile = open(('./PiCam/RTS_list.txt'),'r')
        if args.nrtsPath != None:
            print("DEBUG: nrtsPath is {}".format(args.nrtsPath))
            szNrtsPath = Path(args.nrtsPath)
            if szNrtsPath.is_file():
                print("DEBUG: It is a file! Opening nrtsFile")
                nrtsFile = open(str(args.nrtsPath),'r')
            else:
                print ("File not found, opening backup")
                nrtsFile = open('./PiCam/NRTS_list.txt','r')
        else:
            print("DEBUG: Nrts will be built from directory listing")
            nrtsFile = open('./PiCam/NRTS_list.txt','r')
        if args.mrtsPath != None:
            print("DEBUG: mrtsPath is {}".format(args.mrtsPath))
            szMrtsPath = Path(args.mrtsPath)
            if szMrtsPath.is_file():
                print("DEBUG: It is a file! Opening mrtsFile")
                mrtsFile = open(str(args.mrtsPath),'r')
            else:
                print ("File not found, opening backup")
                mrtsFile = open('./PiCam/MRTS_list.txt','r')
        else:
            print("DEBUG: Mrts will be built from directory listing")
            mrtsFile = open('./PiCam/MRTS_list.txt','r')

        rtsList  =  rtsFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
        nrtsList = nrtsFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
        mrtsList = mrtsFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
        rtsFile.close()
        nrtsFile.close()
        mrtsFile.close()
        deadList = 1
        rtsLen  = len(rtsList)
        nrtsLen = len(nrtsList)
        mrtsLen = len(mrtsList)
        arrayLen = int(rtsLen + nrtsLen + mrtsLen)
        if (arrayLen >= minSize):
            # we have enough data to do stuff
            x_train = np.zeros((arrayLen,dataMax))
            y_train = np.zeros(arrayLen)
            tr_count = 0
            for each in rtsList:
                if (each != '') and (each != '.DS Store'):
                    (row,col)=each.split()
                    if (int(row)<=supRow) and (int(col)<=supCol):
                        x_train[tr_count] = (pixel[0:dataMax,int(row),int(col)])
                        y_train[tr_count] = 0
                        tr_count +=1
                    else:
                        print("DEBUG: Error data out of range (training rts cat)")
                        break
                else:
                    deadList +=1
            for each in nrtsList:
                if (each != '') and (each != '.DS Store'):
                    (row,col)=each.split()
                    if (int(row)<=supRow) and (int(col)<=supCol):
                        x_train[tr_count] = (pixel[0:dataMax,int(row),int(col)])
                        y_train[tr_count] = 1
                        tr_count +=1
                    else:
                        print("DEBUG: Error data out of range (training nts cat)")
                        break
                else:
                    deadList +=1
            for each in mrtsList:
                if (each != '') and (each != '.DS Store'):
                    (row,col)=each.split()
                    if (int(row)<=supRow) and (int(col)<=supCol):
                        x_train[tr_count] = (pixel[0:dataMax,int(row),int(col)])
                        y_train[tr_count] = 2
                        tr_count +=1
                    else:
                        print("DEBUG: Error data out of range (training mrts cat)")
                        break
                else:
                    deadList +=1
            if abs(tr_count -arrayLen) >= delta :
                print("DEBUG: We have lost data!!!! (cat)")
                print("DEBUG: Sizes:\n\t [dataWritten:dataExpected]\n{}:{}".format(tr_count,arrayLen))

                return (False, 0,0,0)
            else:
                print ("DEBUG: Dataset complete")
                return (True, x_train,y_train, tr_count)

        else:
            # uhhh we need more data
            print("DEBUG: Too small of dataset, less than {} for all of the data types (cat)".format(testingTrainSize))
            return (False,0,0,0)


def makeTestingData (args, pixel, minSize):
    #inputs:
    # args     -> all commandline arguments
    # pixel    -> dataset
    # minSize  -> testingSizetest
    #
    #outputs:
    # x_test  -> pixel data for testing
    # y_test  -> values for the data type
    # status   -> bool value of process success
    #

    (dataMax, supRow, supCol) = pixel.shape
    if args.oldMethod:
        # Binary method only
        # rts and nrts only
        print("DEBUG: Activating old binary method!")
        if args.testrtsPath != None:
            print("DEBUG: rtsTestPath is {}".format(args.testrtsPath))
            sztestRtsPath = Path(args.testrtsPath)
            if sztestRtsPath.is_file():
                print("DEBUG: It is a file! Opening rtstestFile")
                rtstestFile = open(str(args.testrtsPath),'r')
            else:
                print ("File not found, opening backup")
                rtstestFile = open(('./PiCam/RTS_list_test.txt'),'r')
        else:
            print("DEBUG: RtsList will be built from directory listing")
            rtstestFile = open(('./PiCam/RTS_list_t.txt'),'r')
        if args.testnrtsPath != None:
            print("DEBUG: nrtsPath is {}".format(args.testnrtsPath))
            sztestNrtsPath = Path(args.testnrtsPath)
            if sztestNrtsPath.is_file():
                print("DEBUG: It is a file! Opening nrtsFile")
                nrtstestFile = open(str(args.testnrtsPath),'r')
            else:
                print ("File not found, opening backup")
                nrtstestFile = open('./PiCam/WN_ListSh_test.txt','r')
        else:
            print("DEBUG: Nrts will be built from directory listing")
            nrtstestFile = open('./PiCam/NRTS_list_t.txt','r')
        rtstestList  =  rtstestFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
        nrtstestList = nrtstestFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
        rtstestFile.close()
        nrtstestFile.close()
        deadList =1
        rtstestLen  = len(rtstestList)
        nrtstestLen = len(nrtstestList)
        testLen = int(rtstestLen + nrtstestLen) - deadList
        if (testLen >= minSize):
            # we have enough data to do stuff
            x_test = np.zeros((testLen,dataMax))
            y_test = np.zeros(testLen)
            td_count = 0
            for each in rtstestList:
                if (each != '') and (each != '.DS Store'):
                    (row,col)=each.split()
                    if (int(row)<=supRow) and (int(col)<=supCol):
                        x_test[td_count] = (pixel[0:dataMax,int(row),int(col)])
                        y_test[td_count] = 0
                        td_count +=1
                    else:
                        print("DEBUG: Error data out of range (testing rts bin)")
                        break
                else:
                    deadList +=1

            for each in nrtstestList:
                if (each != '') and (each != '.DS Store'):
                    (row,col)=each.split()
                    if (int(row)<=supRow) and (int(col)<=supCol):
                        x_test[td_count] = (pixel[0:dataMax,int(row),int(col)])
                        y_test[td_count] = 1
                        td_count +=1
                    else:
                        print("DEBUG: Error data out of range (testing nrts bin)")
                        break
                else:
                    deadList +=1

            if abs(td_count - testLen) >=delta :
                print("DEBUG: We have lost data!!!! (testing bin)")
                print("DEBUG: Sizes:\n\t [dataWritten:dataExpected]\n{}:{}".format(td_count,testLen))
                return (False, 0,0)
            else:
                print ("DEBUG: Dataset complete (testing bin)")
                return (True, x_test,y_test)

        else:
            # uhhh we need more data
            print("DEBUG: Too small of dataset, less than {} for all of the data types (testing bin)".format(testingTrainSize))
    else:
        # Categorical method
        # rts, nrts, and mrts lists
        print("DEBUG: Categorical method active")
        if args.testrtsPath != None:
            print("DEBUG: testrtsPath is {}".format(args.testrtsPath))
            sztestRtsPath = Path(args.testrtsPath)
            if sztestRtsPath.is_file():
                print("DEBUG: It is a file! Opening rtsFile")
                testrtsFile = open(str(args.testrtsPath),'r')
            else:
                print ("File not found, opening backup")
                testrtsFile = open(('./PiCam/RTS_list_test.txt'),'r')
        else:
            print("DEBUG: RtsList will be built from directory listing")
            testrtsFile = open(('./PiCam/RTS_list_t.txt'),'r')
        if args.testnrtsPath != None:
            print("DEBUG: nrtsPath is {}".format(args.testnrtsPath))
            sztestNrtsPath = Path(args.testnrtsPath)
            if stestzNrtsPath.is_fle():
                print("DEBUG: It is a file! Opening nrtsFile")
                testnrtsFile = open(str(args.testnrtsPath),'r')
            else:
                print ("File not found, opening backup")
                testnrtsFile = open('./PiCam/WN_ListSh_test.txt','r')
        else:
            print("DEBUG: Nrts will be built from directory listing")
            testnrtsFile = open('./PiCam/NRTS_list_t.txt','r')
        if args.testmrtsPath != None:
            print("DEBUG: mrtsPath is {}".format(args.testmrtsPath))
            sztestMrtsPath = Path(args.testmrtsPath)
            if sztestMrtsPath.is_fle():
                print("DEBUG: It is a file! Opening mrtsFile")
                testmrtsFile = open(str(args.testmrtsPath),'r')
            else:
                print ("File not found, opening backup")
                testmrtsFile = open('./PiCam/WN_ListSh_test.txt','r')
        else:
            print("DEBUG: Mrts will be built from directory listing")
            testmrtsFile = open('./PiCam/MRTS_list_t.txt','r')

        rtstestList  =  testrtsFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
        nrtstestList = testnrtsFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
        mrtstestList = testmrtsFile.read().replace('\n\n','\n').replace('\n\n','\n').replace('\n\n','\n').split('\n')
        testrtsFile.close()
        testnrtsFile.close()
        testmrtsFile.close()
        deadList =1
        testrtsLen  = len(rtstestList)
        testnrtsLen = len(nrtstestList)
        testmrtsLen = len(mrtstestList)
        testLen = int(testrtsLen + testnrtsLen + testmrtsLen) - deadList
        if (testLen >= minSize):
            # we have enough data to do stuff
            x_test = np.zeros((testLen,dataMax))
            y_test= np.zeros(testLen)
            tr_count = 0
            for each in rtstestList:
                if (each != '') and (each !='.DS Store'):
                    (row,col)=each.split()
                    if (int(row)<=supRow) and (int(col)<=supCol):
                        x_test[tr_count] = (pixel[0:dataMax,int(row),int(col)])
                        y_test[tr_count] = 0
                        tr_count +=1
                    else:
                        print("DEBUG: Error data out of range (testing rts bin)")
                        break
                else:
                    deadList +=1
            for each in nrtstestList:
                if (each != '') and (each != '.DS Store'):
                    (row,col)=each.split()
                    if (int(row)<=supRow) and (int(col)<=supCol):
                        x_test[tr_count] = (pixel[0:dataMax,int(row),int(col)])
                        y_test[tr_count] = 1
                        tr_count +=1
                    else:
                        print("DEBUG: Error data out of range (testing nrts bin)")
                        break
                else:
                    deadList +=1
            for each in mrtstestList:
                if (each != '') and (each != '.DS Store'):
                    (row,col)=each.split()
                    if (int(row)<=supRow) and (int(col)<=supCol):
                        x_test[tr_count] = (pixel[0:dataMax,int(row),int(col)])
                        y_test[tr_count] = 2
                        tr_count +=1
                    else:
                        print("DEBUG: Error data out of range (testing mrts bin)")
                        break
                else:
                    deadList +=1

            if abs(tr_count - testLen) >= delta :
                print("DEBUG: We have lost data!!!! (testing bin)")
                print("DEBUG: Sizes:\n\t [dataWritten:dataExpected]\n{}:{}".format(td_count,testLen))
                return (False, 0,0)
            else:
                print ("DEBUG: Dataset complete (testing bin)")
                return (True, x_test,y_test)

        else:
            # uhhh we need more data
            print("DEBUG: Too small of dataset, less than {} for all of the data types".format(testingTestSize))


def dataFactors (args, arrayLen, dataMax,  supRow, supCol):
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
            settingsData +='Loss='
            if (args.oldMethod):
                settingsData +="'binary_crossentropy'\n"
            else:
                settingsData +="'categorical_crossentropy'\n"
        elif (settingsData.find('Loss=')>=0):
            posbValue = settingsData.find('Loss=')
            poseValue = settingsData[posbValue:].find('\n')
            out='Loss='
            if (args.oldMethod):
                out+="'binary_crossentropy'\n"
            else:
                out +="'categorical_crossentropy'\n"
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

def main ():
    #import settings
    if os.name == 'posix':
        os.nice(10)


    # Open the input files

    # Add commandline parsing
    # short codes are single char only!
    parser = argparse.ArgumentParser(prog='makeDataSets.py', description="Creates the numpy dataset for train, testing, and running keras models")
    parser.add_argument("-r","--rtsPath",type=str, help="rtslist file that contains rts signals in col_row format")
    parser.add_argument("-n", "--nrtsPath",type=str, help="nrtslist file that contains whitenoise signals")
    parser.add_argument("-m", "--mrtsPath",type=str, help="mrtsList file that has possible rts signals")
    parser.add_argument("-s","--testrtsPath",type=str, help="rtsTestlist file that contains rts signals in col_row format for the testing data")
    parser.add_argument("-t", "--testnrtsPath",type=str, help="nrtsTestlist file that contains whitenoise signals for the testing data")
    parser.add_argument("-u", "--testmrtsPath",type=str, help="mrtsTestList file that has possible rts signals for the testing data")
    parser.add_argument("-o", "--oldMethod", action='store_true', help="Activates a special routine that uses binary mode rather than categorical")
    #parser.add_argument("-","--",action='store_true',help="")


    args = parser.parse_args()

    testingSizeTest  = 100
    testingSizeTrain = 500


    pixel = loader.load()
    (dataMax, supRow, supCol) = pixel.shape

    (trainStatus, x_train,y_train, dataCount)  = makeTrainingData(args,pixel,testingSizeTrain)
    (testStatus, x_test,y_test)     = makeTestingData(args,pixel,testingSizeTest)
    print ("DEBUG: \n\tSize of training data:\n{} ".format(dataCount))
    if type(x_train) == np.ndarray:
        arrayLen = x_train.shape[0]
        statusFactor                    = dataFactors (args,dataCount, dataMax,  supRow, supCol)
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

    status = statusFactor & statusTest & statusTraining

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
