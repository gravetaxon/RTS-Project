#!/usr/local/bin/python3


#matplotlib.use('Agg')
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
if os.name == 'posix':
    os.nice(10)

RTSRes = open("./Picam/model_Out.txt","w+")
SavedModels =settings.Saved
NumModels = len(SavedModels)
DataShape = settings.dataShape
# For testing purposes reducing col and rows by a handicap
TestPercent = 1
loopData = (int(DataShape[0]),int(DataShape[1]*TestPercent),int(DataShape[2]*TestPercent))
models = []

ModelsUsed =""
for each in SavedModels:
    ModelsUsed+=str(each)+','
ModelsUsed=ModelsUsed[:-1]
print ("DEBUG: Using the following models: {}".format(ModelsUsed))

print("DEBUG: Loading models...")
for each in SavedModels:
    model_name = './PiCam/CNNlin_model{}.h5'.format(str(each))
    model = load_model(model_name)
    models.append(model)

voterCount = min(3,len(models)) # either the size of the array or the number of appeallete judges reviewing a case


pixel = loader.load()
for i in range(1,loopData[1]):
    print("status ",(i/loopData[1])*100,"%" )
    for j in range(1,loopData[2]):
        pix = pixel[0:loopData[0], i, j]
        ppix = pix[None,:,None]
        votes = []
        for voter in random.sample(models,voterCount):
            mp = model.predict(ppix) # how does this work with multiple categories?
    #        print(mp)
            if (mp[0] ==0):
                # model voted yes
                votes.append(int(1))
            else:
                # model voted no
                votes.append(int(0))
        # mean of votes
        VoterAve = np.mean(votes)
        if (VoterAve >=0.1):
            print(i,j)
            RTSRes.write("%d %d\r\n" %(i,j))
        #else:
        #    print ("Vote: {}\nWith {} voters".format(VoterAve, len(votes)))
        #print(i,j,mp[0])
        #if mp[0] == 0:
        #    print(i,j,mp[0])
    #        RTSRes.write("%d %d %d\r\n" %(i,j,mp[0]))
            #x = np.arange(0,1500)
            #plt.plot(x,pix)
            #plt.savefig('./PiCam/RTS_CNN2demo/%d_%d' % (i,j))
#            plt.plot(x,pix)
            #plt.close()

RTSRes.close()


#x = np.arange(0,500)

#plt.plot(x,p)
"""
Code to smooth data set

'''
Created on Mar 16, 2013

@author: tiago
'''

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import wiener, filtfilt, butter, gaussian, freqz
from scipy.ndimage import filters
import scipy.optimize as op
import matplotlib.pyplot as plt

def ssqe(sm, s, npts):
	return np.sqrt(np.sum(np.power(s-sm,2)))/npts

def testGauss(x, y, s, npts):
	b = gaussian(39, 10)
	#ga = filtfilt(b/b.sum(), [1.0], y)
	ga = filters.convolve1d(y, b/b.sum())
	plt.plot(x, ga)
	print "gaerr", ssqe(ga, s, npts)
	return ga

def testButterworth(nyf, x, y, s, npts):
	b, a = butter(4, 1.5/nyf)
	fl = filtfilt(b, a, y)
	plt.plot(x,fl)
	print "flerr", ssqe(fl, s, npts)
	return fl

def testWiener(x, y, s, npts):
	wi = wiener(y, mysize=29, noise=0.5)
	plt.plot(x,wi)
	print "wieerr", ssqe(wi, s, npts)
	return wi

def testSpline(x, y, s, npts):
	sp = UnivariateSpline(x, y, s=240)
	plt.plot(x,sp(x))
	print "splerr", ssqe(sp(x), s, npts)
	return sp(x)

def plotPowerSpectrum(y, w):
	ft = np.fft.rfft(y)
	ps = np.real(ft*np.conj(ft))*np.square(dt)
	plt.plot(w, ps)

if __name__ == '__main__':
	npts = 1024
	end = 8
	dt = end/float(npts)
	nyf = 0.5/dt
	sigma = 0.5
	x = np.linspace(0,end,npts)
	r = np.random.normal(scale = sigma, size=(npts))
	s = np.sin(2*np.pi*x)#+np.sin(4*2*np.pi*x)
	y = s + r
	plt.plot(x,s)
	plt.plot(x,y,ls='none',marker='.')
	ga = testGauss(x, y, s, npts)
	fl = testButterworth(nyf, x, y, s, npts)
	wi = testWiener(x, y, s, npts)
	sp = testSpline(x, y, s, npts)
	plt.legend(['true','meas','gauss','iir','wie','spl'], loc='upper center')
	plt.savefig("signalvsnoise.png")
	plt.clf()
	w = np.fft.fftfreq(npts, d=dt)
	w = np.abs(w[:npts/2+1]) #only freqs for real fft
	plotPowerSpectrum(s, w)
	plotPowerSpectrum(y, w)
	plotPowerSpectrum(ga, w)
	plotPowerSpectrum(fl, w)
	plotPowerSpectrum(wi, w)
	plotPowerSpectrum(sp, w)
	plt.yscale('log')
	plt.xlim([0,10])
	plt.ylim([1E-8,None])
	plt.legend(['true','meas','gauss','iir','wie','spl'], loc='upper center')
	plt.savefig("spectra.png")

"""
