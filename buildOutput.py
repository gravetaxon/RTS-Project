#!/usr/bin/env python3

# buildOutput.py
import loader 
from pathlib import Path
from voter import makeOutput

response = input('Do you wish to save the output?\n')
response = str(response).upper()[0]

if response == 'Y':
  print ("Where would you like to put the voter database?")
  vdb= input('Enter the filename of the voter database (ex. voter.txt, votes.db, etc...)\nPlease be aware that any file/path will be totally rewritten as the voter db. Be careful!!\n')
  vdbPath = Path(vdb).expanduser()
  print(type(vdbPath))
  print(vdbPath)
  loader.move('./settings.txt', './settings.py')
  makeOutput(vdbPath)
else:
  makeOutput()
