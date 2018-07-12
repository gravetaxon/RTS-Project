"""Run everything in the following order:

+ Run preprocess.py to ident possible signals
    - makePlots.py to find out which plots you want to use for possible rts, and nonrts signal sets
    - makeRTSGuess.py to see which are good estimates for the whole gamuet of rts signal sets (rts, maybe, and not rts),
    - move the image files in the correct locations ./PiCam/RTS for rts signals, ./PiCam/MRTS for possible RTS signals,
      and ./PiCam/NRTS for non rts signals only(i.e known whitenoise signals)
+ run makeLists.py to generate the dataset files that makeDataSets.py needs
+ run makeDataSets.py to generate the numpy datasets needed for the modeler subsystem
+ run Modeler.py which will generate about 50 instances of the models to test for highest accuracy and least losses,
only the top 5 models will be saved for possible usage.
+ run makeOutput.py with the argument of which model number you wish to use for output
+ makeOutput will output a csv file to show which column, row, and type each of the pixels are according to the model.





"""
import loader
import makeLists
import makeDataSets
import Modeler3 as m3
#import voter        #The following imports were migrated to their own script to separate the output from the modeling systems.
#import makeOutput

## Signal definitions
nrtsSig = 0 # Signal is not a rts frame
rtsSig  = 3 # Signal is a rts frame
mrtsSig = 2 # Signal is a possible rts frame
ertsSig = 1 # Signal is an erratic signal frame
resv1   = 4 # Reserved for future use.
resv2   = 5 # Reserved for future use.


listStatus = makeLists.buildLists()
if listStatus:
    makeDataSets.DSfnHandler(inrtsPath="./PiCam/RTS_list.txt",innrtsPath="./PiCam/NRTS_list.txt",inmrtsPath="./PiCam/MRTS_list.txt",inertsPath="./PiCam/ERTS_list.txt",intestrtsPath=None,intestnrtsPath=None,intestmrtsPath=None,intestertsPath=None,inoldMethod=False)
    # All dataset created: RTS vs NRTS, MRTS vs NRTS, ERTS vs NRTS, NRTS vs NRTS
    # Run each of the modelers and then load all of the saved models in the output module
    #m3.runModel('RTS')  # <- Nominal binary model of RTS vs NRTS
    #m3.runModel('MRTS') # <- Modeling the possible signal type vs non signals
    #m3.runModel('ERTS') # <- Erratic model
    #m3.runModel('NRTS') # <- Control model
    # Since all of the models have been run and saved in the settings let's load up the models in a voting framework
    print("DEBUG: Run buildModels")
