# buildOutput.py

from voter import makeOutput
from pathlib import Path
print ("Where would you like to put the voter database?")
vdb= input('Enter the filename of the voter database (ex. voter.txt, votes.db, etc...)\n')
vdbPath = Path(vdb).expanduser()
print(type(vdbPath))
print(vdbPath)
makeOutput(vdbPath)
