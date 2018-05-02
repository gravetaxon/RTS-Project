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
models = []
for each in SavedModels:
    model_name = './PiCam/CNNlin_model{}.h5'.format(str(each))
    model = load_model(model_name)
    models.append(model)

pixel = loader.load()
for i in range(1,DataShape[1]):
    print("status ",(i/DataShape[1])*100,"%" )
    for j in range(1,DataShape[2]):
        pix = pixel[0:DataShape[0], i, j]
        ppix = pix[None,:,None]
        votes = []
        for voter in random.sample(models,5):
            mp = model.predict(ppix) # how does this work with multiple categories?
            if (mp[0] ==0):
                # model voted yes
                votes.append(int(1))
            else:
                votes.append(int(0))
        # mean of votes
        VoterAve = np.mean(votes)
        if (VoterAve >=settings.DecisionStep):
            print(i,j)
            RTSRes.write("%d %d %d\r\n" %(i,j,VoterAve))
        else:
            print ("no vote")
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
