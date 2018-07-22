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
  print("Do you wish to run the multithreaded version?")
  res = input("Yes/No: ")
  res = str(res).upper()[0] # Only need the first ascii char for a response
  if res =='Y':
    makeOutput(vdbPath,True)
  else:
    makeOutput(vdbPath,False)
else:
  makeOutput(None,False)
