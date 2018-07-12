import Modeler3 as m3
# buildModels
m3.runModel('RTS')  # <- Nominal binary model of RTS vs NRTS
m3.runModel('MRTS') # <- Modeling the possible signal type vs non signals
m3.runModel('ERTS') # <- Erratic model
m3.runModel('NRTS') # <- Control model
