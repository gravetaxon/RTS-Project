
import h5py
import numpy as np
import os
import errno

Delta = 5

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
        mat = h5py.File('A5_p1_32C.mat') # testing dataset
        print ("Converting matlab dataset into numpy")
        matpixel = mat['p1']
    else:
        mat = h5py.File('A5_stack_32C.mat') # Full dataset
        print("Dataset is huge, caching on disk")

        print ("Converting matlab dataset into numpy")
        matpixel = mat["pixel"]
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
