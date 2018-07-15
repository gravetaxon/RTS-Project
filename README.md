# RTS-PROJECT

Version 2.0

Requirements:
  * Must have python 3.0+ (up to python 3.6)
  * Must have a data file, see loader.py for which file is needed
  * Able to run almost all operating systems, excluding FreeBSD and ArchLinux due to issues with versioning for the CUDA libraries

Usage:
  - install the environment with pip install -r requirements.txt or pip install -r requirements-gpu.txt
  - run python buildSets.py
  - then run python buildModels.py
  - then run python buildOutput.py
  - Signal Definitions (as of build  56bfdd5)

      Signal number of 0 indicates a signal is not a rts frame
      
      Signal number of 3 indicates a signal is a rts frame
      
      Signal number of 2 indicates a signal is a possible rts frame
      
      Signal number of 1 indicates a signal is an erratic signal frame
      
      
      ```python
      nrtsSig = 0 # Signal is not a rts frame
      rtsSig  = 3 # Signal is a rts frame
      mrtsSig = 2 # Signal is a possible rts frame
      ertsSig = 1 # Signal is an erratic signal frame
      resv1   = 4 # Reserved for future use.
      resv2   = 5 # Reserved for future use.
      ```
