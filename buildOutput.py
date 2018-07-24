#!/usr/bin/env python3

# buildOutput.py
import loader 
from pathlib import Path
from voter import makeOutput

response = input('Do you wish to save the output?\nYes/No: ')
if len(response) >0:
  response = str(response).upper()[0]
else:
  response ='N'


if response == 'Y':
  print ("Where would you like to put the voter database?")
  vdb= input('Enter the filename of the voter database (ex. voter.txt, votes.db, etc...)\nPlease be aware that any file/path will be totally rewritten as the voter db. Be careful!!\n')
  vdbPath = Path(vdb).expanduser()
  print(type(vdbPath))
  print(vdbPath)
  loader.move('./settings.txt', './settings.py')
  print("Do you wish to run the multithreaded version?")
  res = input("Yes/No: ")
  if len(res)>0:
    res = str(res).upper()[0] # Only need the first ascii char for a response
  else:
    res = 'E'

  if res =='Y':
    makeOutput(vdbPath,True)
  elif res =='E':
    exit(0)
  else:
    makeOutput(vdbPath,False)
elif response =='E':
  exit(0)
else:
  print("Do you wish to run the multithreaded version?")
  res = input("Yes/No: ")
  if len(res)>0:
    res = str(res).upper()[0] # Only need the first ascii char for a response
  else:
    res='N'
  if res =='Y':
    makeOutput(None,True)
  elif res =='E':
    exit(0)
  else:
    makeOutput(None,False)
