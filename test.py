# Command line test
import argparse
import os, os.path
from pathlib import Path

parser = argparse.ArgumentParser(prog='makeDataSets.py', description="Creates the numpy dataset for train, testing, and running keras models")
parser.add_argument("-r","--rtsPath",type=str, help="rtslist file that contains rts signals in col_row format")
parser.add_argument("-n", "--nrtsPath",type=str, help="nrtslist file that contains whitenoise signals")
parser.add_argument("-m", "--mrtsPath",type=str, help="mrtsList file that has possible rts signals")
parser.add_argument("-tr","--testrtsPath",type=str, help="rtsTestlist file that contains rts signals in col_row format for the testing data")
parser.add_argument("-tn", "--testnrtsPath",type=str, help="nrtsTestlist file that contains whitenoise signals for the testing data")
parser.add_argument("-tm", "--testmrtsPath",type=str, help="mrtsTestList file that has possible rts signals for the testing data")
args = parser.parse_args()
if args.rtsPath != None:
    print("rtsPath is {}".format(args.rtsPath) )
    #print("type of rtsPath is {}".format(type(args.rtsPath)))
    print("Checking if path is to a file!")
    rtsPath = Path(args.rtsPath)
    if rtsPath.is_file():
        # once here just parse the bloody file!
        print ("file exists!!")
else:
    print("rts will be built from files IN directory")
    # put makeDataSets routine Here

if args.nrtsPath != None:
    print("nrtsPath is {}".format(args.nrtsPath) )
else:
    print("nrts will be built from files IN directory")
if args.mrtsPath != None:
    print("mrtsPath is {}".format(args.mrtsPath) )
else:
    print("mrts will be built from files IN directory")
