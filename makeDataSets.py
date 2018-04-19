"""
There are 2,313 RTS candidates, so add 2,637 WN signals to create np.array(4950,1500)
"""
#!/usr/local/bin/python3
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

#import settings
if os.name == 'posix':
    os.nice(10)

#x_train = np.zeros((4982,1500))
#x_train = np.zeros((4235,1500)) #0.85*4982
#x_test = np.zeros((747,1500))

#y_train = np.zeros(4235)
#y_test  = np.zeros(747)

#y_train[1976:4235]=1
#y_test[347:747]=1
#                   data   row   col
# pixel dimensions 1500 x 972 x 1296
# pixel[0:1500,0:972,0:1296]
pixel = loader.load()
# Hard coded values (need to find way to get values programmatically)
#supRow = 972  # Cannot reach these values for either row or
#supCol = 1296 # col because it does *NOT* exist in the dataset.


if type(pixel)==np.ndarray:
    (dataMax, supRow, supCol) = pixel.shape
#else if type(pixel) = list:
#    ndims = np.ndim(pixel)
#    print("And magic needs to occur, not here yet")
#    break
else:
    print("we have a problem")

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
args = parser.parse_args()

if args.oldMethod :
    print("DEBUG: Activating old method!")

if args.rtsPath != None:
    print("DEBUG: rtsPath is {}".format(args.rtsPath) )
    #print("DEBUG: type of rtsPath is {}".format(type(args.rtsPath)))
    print("DEBUG: Checking if path is to a file!")
    rtsPath = Path(args.rtsPath)
    if rtsPath.is_file():
        print("DEBUG: it is a file! Opening rtsFile")
        rtsFile = open(str(args.rtsPath), 'r')
else:
    print("DEBUG: rts will be built from files IN directory")
    rtsFile = open('./PiCam/RTS_list.txt','r')

if args.mrtsPath != None:
    print("DEBUG: mrtsPath is {}".format(args.mrtsPath) )
    #print("DEBUG: type of mrtsPath is {}".format(type(args.mrtsPath)))
    print("DEBUG: Checking if path is to a file!")
    mrtsPath = Path(args.mrtsPath)
    if mrtsPath.is_file():
        print("DEBUG: it is a file! Opening rtsFile")
        mrtsFile = open(str(args.mrtsPath),'r')
else:
    print("DEBUG: mrts will be built from files IN directory")
    mrtsFile = open('./PiCam/MRTS_list.txt','r')


if args.nrtsPath != None:
    print("DEBUG: nrtsPath is {}".format(args.nrtsPath) )
    #print("DEBUG: type of nrtsPath is {}".format(type(args.nrtsPath)))
    print("DEBUG: Checking if path is to a file!")
    nrtsPath = Path(args.nrtsPath)
    if nrtsPath.is_file():
        print("DEBUG: it is a file! Opening rtsFile")
        nrtsFile = open(str(args.nrtsPath),'r')
else:
    print("DEBUG: mrts will be built from files IN directory")
    nrtsFile = open('./PiCam/NRTS_list.txt','r')

#rtsFile = open('./PiCam/RTS_list.txt','r')
#mrtsFile = open('./PiCam/MRTS_list.txt','r')
#nrtsFile = open('./PiCam/NRTS_list.txt','r')


# seek to the 0th bytes
rtsFile.seek(0)
mrtsFile.seek(0)
nrtsFile.seek(0)

# Let's read all of the files in and get the lengths to setup the initial arrays
rtsList = rtsFile.read().replace('\n\n','\n').split('\n') # each line in the file should be a single line and not split (yet...)
nrtsList = nrtsFile.read().replace('\n\n','\n').split('\n')
if args.oldMethod == False:
    mrtsList = mrtsFile.read().replace('\n\n','\n').split('\n')
else:
    mrtsList = ""
# close the files since we don't need them anymore
rtsFile.close()
mrtsFile.close()
nrtsFile.close()

# Let's get the lengths of each of the lists

rtsLen  = len(rtsList)
mrtsLen = len(mrtsList)
nrtsLen = len(nrtsList)

"""**************************************************"""
# Instead of using math to determine the testing dataset, should use the
# above method to load the testing dataset as well.
"""**************************************************"""

arrayLen = int(rtsLen + mrtsLen + nrtsLen)
print ('DEBUG: arrayLen {}'.format(arrayLen))
if (arrayLen>=100):
    x_train = np.zeros((arrayLen,1500))
    y_train = np.zeros(arrayLen)
else:
    print("DEBUG: Too small of dataset")

if args.testrtsPath != None or args.testmrtsPath != None or args.testnrtsPath != None:
    # load the files if at lease rts and either mrts or nrts has been given
    if (args.testrtsPath != None and args.testmrtsPath!= None) or (args.testrtsPath != None and args.testnrtsPath!= None):
        if Path(args.testrtsPath).is_file():
            rtstestFile = open(str(args.testrtsPath),'r')
        else:
            print ("DEBUG: Could not open the testing data list. Opening known good list")
            rtstestFile = open("./PiCam/RTS_List_test.txt", 'r')
        if args.testmrtsPath != None or args.testnrtsPath != None:
            # check which if both are here
            if Path(args.testnrtsPath).is_file():
                nrtstestFile = open(str(args.testnrtsPath),'r')
            else:
                nrtstestFile = open("./PiCam/WN_ListSh_test.txt",'r')
            if Path(args.testmrtsPath).is_file():
                mrtstestFile = open(str(args.testmrtsPath),'r')
            else:
                mrtstestFile = open("./PiCam/WN_ListSh_test.txt",'r')
    else:
        # user provided only the maybe and non signal files, override users choice and use default files
        if Path('./PiCam/RTS_List_test.txt').is_file() and Path('./PiCam/WN_ListSh_test.txt').is_file():
            rtstestFile = open("./PiCam/RTS_List_test.txt", "r+")
            nrtstestFile = open("./PiCam/WN_ListSh_test.txt",'r')
            mrtstestFile = open("./PiCam/WN_ListSh_test.txt",'r')
    # at this point all of the files have been opened just read them if __name__ == '__main__':
    rtstestFile.seek(0)
    nrtstestFile.seek(0)
    mrtstestFile.seek(0)
    rtstestList = rtstestFile.read().replace('\n\n','\n').split('\n') # each line in the file should be a single line and not split (yet...)
    nrtstestList = nrtstestFile.read().replace('\n\n','\n').split('\n') # each line in the file should be a single line and not split (yet...)
    if args.oldMethod == False:
        mrtstestList = mrtstestFile.read().replace('\n\n','\n').split('\n') # each line in the file should be a single line and not split (yet...)
    else:
        mrtstestList = ""
    rtstestFile.close()
    mrtstestFile.close()
    nrtstestFile.close()
    rtstestLen = len(rtstestList)
    nrtstestLen = len(nrtstestList)
    mrtstestLen = len(mrtstestList)
    if rtstestLen >0 and rtstestLen <= rtsLen:
        rtsTestCount = rtstestLen
    else:
        print("DEBUG: Error has occured with rts test data")
        rtsTestCount = 0
    if nrtstestLen >0  and nrtstestLen <= nrtsLen:
        nrtsTestCount = nrtstestLen
    else:
        print("DEBUG: Error has occured with nrts test data")
        nrtsTestCount = 0
    if mrtstestLen >0  and mrtstestLen <= mrtsLen:
        mrtsTestCount = mrtstestLen
    else:
        print("DEBUG: Error has occured with mrts test data")
        mrtsTestCount = 0
    testLen = int(rtstestLen + nrtstestLen + mrtstestLen)
    if (testLen>=10):
        x_test = np.zeros((testLen,1500))
        y_test = np.zeros(testLen)
    else:
        print("DEBUG: Too small of dataset")

else:
    # use the computation method
    # add the lengths and make the zeros arrays
    arrayLen = int(rtsLen + mrtsLen + nrtsLen)
    testLen = int(0.15*arrayLen)

    if (arrayLen>=100):
        x_train = np.zeros((arrayLen,1500))
        y_train = np.zeros(arrayLen)
    else:
        print("DEBUG: Too small of dataset")
    # Change ME TOO!!!!!!!!!!
    if (testLen>=10):
        x_test = np.zeros((testLen,1500))
        y_test = np.zeros(testLen)
    else:
        print("DEBUG: Too small of dataset")

    # split the testLen into integer groups proportional to ratio of rts, mrts, nrts to the total lengths

    rtsRatio = float(rtsLen)/float(arrayLen)
    mrtsRatio = float(mrtsLen)/float(arrayLen)
    nrtsRatio = float(nrtsLen)/float(arrayLen)

    rtsTestCount = int(rtsRatio*testLen)
    mrtsTestCount = int(mrtsRatio*testLen)
    nrtsTestCount = int(testLen- (rtsTestCount+mrtsTestCount)) # nrts is usually the largest group so we can afford to lose a few the data point from the test group.

    if ( (rtsTestCount > rtsLen) and (rtsTestCount>0)):
        print ("DEBUG: Error has occured! Math error for array size for rts")


    if (mrtsTestCount > mrtsLen) and (mrtsTestCount>0):
        print ("DEBUG: Error has occured! Math error for array size for mrts")

    if (nrtsTestCount > nrtsLen) and (nrtsTestCount>0):
        print ("DEBUG: Error has occured! Math error for array size for nrts")

# y dataset completed after this
# 0 - rts
# 1 - nrts
# 2 - mrts
#

y_train[rtsLen:nrtsLen+rtsLen] =1
y_train[nrtsLen+rtsLen:]=2
y_test[rtsTestCount:(rtsTestCount+nrtsTestCount)]=1
y_test[(rtsTestCount+nrtsTestCount):]=2

# x dataset is compiled by going through each set in turn and loading the speific pixel into the training dataset
tr_count = 0 # training data counter
for each in rtsList:
    if (each != ''):
        (row,col)=each.split()
        if (int(row)< supRow and int(col)<supCol):
            x_train[tr_count]=(pixel[0:1500,int(row),int(col)] )
            tr_count+=1
        else:
            print("DEBUG: Double check to insure selections are in the range of the data that is going to be used")
for each in nrtsList:
    if (each != ''):
        (row,col)=each.split()
        if (int(row)< supRow and int(col)<supCol):
            x_train[tr_count]=(pixel[0:1500,int(row),int(col)] )
            tr_count+=1
        else:
            print("DEBUG: Double check to insure selections are in the range of the data that is going to be used")
for each in mrtsList:
    if (each != ''):
        (row,col)=each.split()
        if (int(row)< supRow and int(col)<supCol):
            x_train[tr_count]=(pixel[0:1500,int(row),int(col)] )
            tr_count+=1
        else:
            print("DEBUG: Double check to insure selections are in the range of the data that is going to be used")

if (tr_count > arrayLen ):
    print("DEBUG: A math error has occured! We have more data than array actually said that we had!!")
    tr_count =0
    arrayLen = -1
else:
    print("DEBUG: Looks fine so far...")

# loading the test set, which is the leading edge of the training datasets
td_count = 0 # testing data counter

# we know that data exists for this because of the fact that the testcounts are smaller than the array lengths for each of
# the arrays
if (rtsTestCount>0):
    for i in range(0,rtsTestCount):
        each = rtsList[i]
        if each != '':
            (row,col)= each.split()
            if int(row)< supRow and int(col)<supCol:
                x_test[td_count]=(pixel[0:1500,int(row),int(col)])
                td_count+=1
            else:
                print("DEBUG: Double check to insure selections are in the range of the data that is going to be used")
else:
    print("DEBUG: No rts signals in the test set!!")

if (nrtsTestCount>0):
    for i in range(0,nrtsTestCount):
        each = nrtsList[i]
        if each != '':
            (row,col)= each.split()
            if int(row)< supRow and int(col)<supCol:
                x_test[td_count]=(pixel[0:1500,int(row),int(col)])
                td_count+=1
            else:
                print("DEBUG: Double check to insure selections are in the range of the data that is going to be used")
else:
    print("DEBUG: No whitenoise signals in the test set!!")
status = False # If this is false program does *NOT* write the new npy
               # outputs at the end

if (mrtsTestCount>0):
    for i in range(0,mrtsTestCount):
        each = mrtsList[i]
        if each != '':
            (row,col)= each.split()
            if int(row)< supRow and int(col)<supCol:
                x_test[td_count]=(pixel[0:1500,int(row),int(col)])
                td_count+=1
            else:
                print("DEBUG: Double check to insure selections are in the range of the data that is going to be used")
else:
    print("DEBUG: No possible rts signals in the test set!!")

# Here we do the prime magic on the training dataset!
# take the length of the training dataset and use prime factorization on it
if (arrayLen > 0):
    DataFactor = loader.prime_factors(int(round(arrayLen*0.85)))
    ArrayFactor = loader.prime_factors(int(round(dataMax*0.85)))
    factors = DataFactor+ArrayFactor
    factors = list(set(factors)) # remove all the duplicates and then get it
                     # back to a list to manipulate it
    factors.sort(reverse=True)
    if (len(factors)>2):
        largest = factors.pop(0)
        smallest = factors.pop()
        factors.append(largest)
        factors.append(smallest)
    print ("DEBUG: Factors:")
    print (factors)
    # FilterSize is determined by the product of the hidden layers
    # KernelSize is determined by the prime factors themselves
    NumberHLayers_in = len(factors)-2
    print("DEBUG: Possible Hidden Layer count:"+str(NumberHLayers_in))
    if (NumberHLayers_in >0):
        # hidden layers exist! Use all the numbers from 0 to largest
        HiddenLayers_out = NumberHLayers_in
        FilterSize_Prod = 1
        for each in factors[0:HiddenLayers_out]:
            FilterSize_Prod = FilterSize_Prod*int(each)
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
    print(settingsData)
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

    settingsFile = open('./settings.py','w')
    settingsData= settingsData.replace('\n\n','\n')
    print (settingsData)
    bytesWritten = settingsFile.write(settingsData)
    settingsFile.close()
    if (len(settingsData)==bytesWritten):
        status = True

else:
    print("DEBUG: we had a failure to communicate...")
# only update the numpy arrays if and only if the above algorithm has
# succeeded!

if (status == True):
    print("DEBUG: Saving new numpy datasets")
    np.save('./PiCam/x_train.npy',x_train)
    np.save('./PiCam/x_test.npy',x_test)
    np.save('./PiCam/y_train.npy',y_train)
    np.save('./PiCam/y_test.npy',y_test)
else:
    print("DEBUG: We had an error in writing settings data and have not written incompatible training and/or testing data")
