
import h5py
import numpy as np
import os
import errno

Delta = 5

## Signal definitions
nrtsSig = 0 # Signal is not a rts frame
rtsSig  = 3 # Signal is a rts frame
mrtsSig = 2 # Signal is a possible rts frame
ertsSig = 1 # Signal is an erratic signal frame
resv1   = 4 # Reserved for future use.
resv2   = 5 # Reserved for future use.

def ensureFolder(file_path):
    if file_path[len(file_path)-1]!='/':
        #print(dir)
        file_path+='/' # add the ending slash
    dir = os.path.dirname(file_path)
    print(dir)
    if not os.path.exists(dir):
        #print("DEBUG: Making directory: ",dir)
        os.makedirs(dir)
        if os.path.exists(dir) == True:
            return True
        else:
            return False
    else:
        return True

def load(type=False):
    print ("Loading dataset, please wait...")
    if type != True:
        mat = h5py.File('A5_pipe1_32C.mat') # testing dataset
        print ("Converting matlab dataset into numpy")
        matpixel = mat['p1']
    else:
        mat = h5py.File('A5_stack_32C.mat') # Full dataset
        print("Dataset is huge, caching on disk")

        print ("Converting matlab dataset into numpy")
        matpixel = mat["pixel"]
    print ("DEBUG: {}".format(list(mat)))
    pixel = np.array(matpixel)
    print("Done loading and coverting dataset")
    return (pixel)

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def smallest_power(x,m):
    i=1
    testCon = m**i
    while (testCon < x):
        i+=1
        testCon = m**i
    if (i-1) >0:
        return m**(i-1)
    else:
        return m
def mean(x):
    return float(sum(numbers)) / max(len(numbers), 1)

def setSetting(filename,settingsTag ,settingsData):
    # filename -> where to write setting
    # settingsTag -> what to look for
    # settingsData -> what to write (explicitly)
    fileSettings = open(str(filename),'r')
    fileData = fileSettings.read()
    fileSettings.close()
    if (fileData.find(settingsTag) < 0):
        fileData += settingsTag
        fileData += settingsData
    elif(fileData.find(settingsTag) >= 0 ):
        beginValue = fileData.find(settingsTag)
        offset = fileData[beginValue:].find('\n')
        fileData = fileData[:beginValue] + settingsTag + settingsData + fileData[(beginValue+offset):]
    print(settingsTag+settingsData)
    fileSettings = open(str(filename),'w')
    numBytes = fileSettings.write(fileData)
    fileSettings.close()
    if numBytes >0:
        return True
    else:
        return False

def getSetting(filename, settingsTag):
    fileSettings = open(str(filename),'r')
    fileData = fileSettings.read()
    fileSettings.close()

    if(fileData.find(settingsTag)>=0):
        beginValue = fileData.find(settingsTag)
        offset = fileData[beginValue:].find('\n')
        settingsData = fileData[(beginValue+len(settingsTag)):(beginValue+offset)]
        return settingsData
    else:
        settingsData = ''
        return None

def move(source,dest):
    sFile = open(source,'r')
    dFile = open(dest,'w')
    data=sFile.read()
    dFile.write(data)
    sFile.close()
    dFile.close()
