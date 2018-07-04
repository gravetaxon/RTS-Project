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
import Modeler3
import voter
import makeOutput

buildLists()


DSfnHandler
