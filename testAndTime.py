# test and time ulam_sequence routine

import time
import subprocess
import os

# sample results
# ulam_sequence.py 2  1000:     0.17
# ulam_sequence.py 3  3000:     0.26
# ulam_sequence.py 4  4000:     0.32
# ulam_sequence.py 5  5000:     0.45
# ulam_sequence.py 2 10000:     0.52
# ulam_sequence.py 2 20000:     1.54
# ulam_sequence.py 2 40000:     4.95
# ulam_sequence.py 2 80000:    20.24


fileName = 'ulam_sequence.log'

if os.path.exists(fileName):
    os.remove(fileName)

file = open(fileName, 'w+')

def runAndTime(cmd, logResult=None):
   file.write(cmd)
   file.write('\n')

   start_time = time.time()
   output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
   elapsed_time = time.time() - start_time

   if logResult:
      file.write(output)
      file.write('\n')

   print('{}: {:8.2f}'.format(cmd, elapsed_time))

# quick testing
if 1:
   runAndTime("ulam_sequence.py 2  1000", True)
   runAndTime("ulam_sequence.py 3  3000", True)
   runAndTime("ulam_sequence.py 4  4000", True)
   # don't log results - lines are too long
   runAndTime("ulam_sequence.py 5  5000", False)

# time consuming
if 1:
   runAndTime("ulam_sequence.py 2 10000", False)
   runAndTime("ulam_sequence.py 2 20000", False)
   runAndTime("ulam_sequence.py 2 40000", False)
   runAndTime("ulam_sequence.py 2 80000", False)

# longest
if 0:
   runAndTime("ulam_sequence.py 2 100000", False)
   runAndTime("ulam_sequence.py 2 200000", False)
   runAndTime("ulam_sequence.py 2 400000", False)
   runAndTime("ulam_sequence.py 2 800000", False)

file.close()
