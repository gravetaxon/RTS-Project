#!/usr/local/bin/python3


##### This is a pre-run filter

import settings
import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import numpy as np
import loader
import math
winwid = 500

pixel = loader.load()

loader.ensureFolder("./Picam/")
loader.ensureFolder("./Picam/RTS_CNN2demo/")
loader.ensureFolder("./Picam/Plots/")
RTSList = open("./PiCam/samp_RTS_List_garbage.txt", "w+") #Random telegraph signals
WNList = open("./PiCam/samp_WN_List.txt", "w+") # white noise

RTSList.seek(0)
WNList.seek(0)

SigmaStep = settings.SigmaStep # 1.5

print ("Sigma: ",SigmaStep)
for i in range(0,6):
    for j in range(0,1296):
        p = pixel[0:1500, i, j]
        for k in range(1,3):
            # Window Mean is the difference between the current window and previous window means
            # Test with rolling std's
            winmean = abs(np.mean(p[(k*winwid):((k+1)*winwid)])-np.mean(p[(k-1)*winwid:(k*winwid)]))
            if (winmean) > SigmaStep*np.std(p):
                # If the window mean is larger than 1.5 sigma above population mean then it is a RTS signal
                RTSList.write("%d %d\r\n" % (i,j))
                print(i,j)
                print(winmean,np.std(p))
                break
            else:
                if k ==2:
                    # Otherwise, if the winmean is within window and index is 2x
                    WNList.write("%d %d\r\n" % (i,j))
                    # Add to the whitenoise list

RTSList.close()
WNList.close()
print ("If no output above other than the sigma, change your sigma to something lower")
print ("Run makeRTSGuess.py and edit RTS_train and RTS_test files to find great examples of RTS signals")
print ("If the files are not edited, results are garbage")


#x = np.arange(0,500)

#plt.plot(x,p)
