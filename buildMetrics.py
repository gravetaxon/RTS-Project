#!/usr/bin/env python3
#buildMetrics

#  Metrics
#   + How many of the RTS are of a certain amplitude range
#   + Dwell period of the RTS (given a RTS how long does it take between signal switching)
#
#  Method
#   + open mat file that has the array of results
#   + find all values that are within a margin of error of the RTS signal type
#        - RTS Signal type has a value of 1 and using a margin of error of 0.25
#   + For each of the RTS signals that are in the size, load each into a list (full data)
#   + find the min and max of each of the signals and update for each signal and divide by 2 to find the amplitude
#   +
#
#
#
#
#
#
#
#
import loader as ld
import scipy.io
import numpy as np
import glob
from scipy import stats

print ("Which grid file do you wish to open?")
fileList = glob.glob('*.mat')
selectionList = {i: fileList[i] for i in range(len(fileList))}
for key, value in selectionList.items():
    print ('\t'+str(key)+':')
    print ('\t'*2+str(value))
chosenFile = input('Please input the number of the file you wish to open: ')
if int(chosenFile) >0 and int(chosenFile)< len(selectionList):
    fileName = selectionList[int(chosenFile)]
else:
    print("Error: Incorrect file number, exiting program")
    exit(1)
dataIn = scipy.io.loadmat(str(fileName))
votes = dataIn['votes']
print("Was the grid formed from the big file or the small file? (stack vs pipe)?")
res = input('Please enter a choice: (Big/Small) ')
res =str(res).upper()
if res == 'BIG' or res =='B':
    dataFile =True
elif res == 'SMALL' or res =='S':
    dataFile =False
else:
    print("Incorrect response, exiting")
    exit(2)

pixel = ld.load(dataFile)
rtsValues = []
rtsAmps = []
mask = (votes>0.5)&(votes<1.5) # Create a mask for the signals that we want
for i in range(len(mask)):
    for j in range(len(mask[i])):
        if mask[i][j] ==True:
            data = pixel[:][i][j]
            minData = min(data)
            maxData = max(data)
            amplitude = (minData+maxData)*0.5
            rtsAmps.append([i,j,amplitude])
            rtsValues.append([i,j,data])
# RTS Values now has the dataset and amplitudes
# len rtsValues    -> 23405
# len rtsValues[0] -> 4
# rtsValues[i][0] -> row
# rtsValues[i][1] -> col
# rtsValues[i][2] -> data from pixel
meanAmp = np.mean(np.array(rtsAmps)[:,2])
maxAmp  = np.max(np.array(rtsAmps)[:,2])
minAmp  = np.min(np.array(rtsAmps)[:,2])
modeAmp = stats.mode(np.array(rtsAmps)[:,2])[0][0]
(histCount,histCats) =  np.histogram(np.array(rtsAmps)[:,2])
# histCount -> how many signals per category
# histCat -> what kind of categories are we dealing with
