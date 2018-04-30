# RTS-PROJECT

Usage:
   run the program in the following method:
   + preprocess.py   -> to create a list of possible rts signals and generate folder structure
         + (optional) makePlots.py -> to generate all whitenoise plots
         + (optional) makeRTSGuess.py -> to generate all rts plots from the guesses made from preprocess
   + makeLists.py    -> to make the dataset lists for the next stage from the directory structure
   + makeDataSets.py -> compiles the numpy datasets for training and testing along with generating
                        the modeler's settings file
   + Modeler3.py     -> compiles the model in a string of 50 instances and saves only the top ten models
   + makeOutput.py   -> generates a list of plots that matches each of the categories 
