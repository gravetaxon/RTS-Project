import Modeler3 as m3
import os
from pathlib import Path

# buildModels


## Signal definitions
nrtsSig = 0 # Signal is not a rts frame
rtsSig  = 3 # Signal is a rts frame
mrtsSig = 2 # Signal is a possible rts frame
ertsSig = 1 # Signal is an erratic signal frame
resv1   = 4 # Reserved for future use.
resv2   = 5 # Reserved for future use.

    print("Running models!")
    m3.runModel('RTS')  # <- Nominal binary model of RTS vs NRTS
    m3.runModel('MRTS') # <- Modeling the possible signal type vs non signals
    m3.runModel('ERTS') # <- Erratic model
    m3.runModel('NRTS') # <- Control model
    print ("Rerun this script and say no to be asked to allow output (BUG 1102: python import does not refresh on update of script)")
else:
    response = ''
    print("Do you wish to create output?")
    response = input('Y/N\n')
    response = str(response[0]).upper()

    if response == 'Y':
        from voter import makeOutput
        print ("Where would you like to put the voter database?")
        vdb= input('Enter the filename of the voter database (ex. voter.txt, votes.db, etc...)\n')
        vdbPath = Path(vdb).expanduser()
        print(type(vdbPath))
        print(vdbPath)
        makeOutput(vdbPath)
    elif response == 'N':
        print("To generate the voter database, please run: \"python voter.py\" and then go home for the day. Process takes a very long time to complete.")
    else:
        print("To generate the voter database, please run: \"python voter.py\" and then go home for the day. Process takes a very long time to complete.")
