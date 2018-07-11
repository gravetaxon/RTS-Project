<<<<<<< current
""" Metrics.py
Input:

    Model output list of probable RTS with row[space]col as the formate

Output:

    categories of amplitude and counts
    categories of transistion times and counts

"""
import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import numpy as np
import loader as ld
import os, os.path
from pathlib import Path
import random

# Check if the model output file is in the PiCam folder
fname = "./PiCam/model_Out.txt"
InputFile = Path(fname)
if (InputFile.isfile()):
    # file exists!
    FileIn = open(fname,'r')
    DataIn = FileIn.read()
    # load dataset
=======
""" Metric.py
-- Inputs --
    directory listing of the confirmed RTS signals

or

    model output from the RTS modeler (or voters)

-- Outputs --





"""
>>>>>>> before discard
