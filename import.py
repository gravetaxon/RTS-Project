# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 16:13:36 2017
Import matlab arrays and convert them to python format
@author: Ben WORK ONLY
"""

import h5py
import numpy as np

mat = h5py.File('A5_pipe1_32C.mat')
pixel = mat["p1"]
pixel = np.array(pixel) 
