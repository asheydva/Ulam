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

def runAndTime(cmd):
   start_time = time.time()
   subprocess.check_output(cmd, shell=True, universal_newlines=True)
   elapsed_time = time.time() - start_time

   print('{}: {:10.2f}'.format(cmd, elapsed_time))

if 1:
   n = 4
   str1 = str(n).rjust(2, '0')
   str2 = str(n * 1000).rjust(8, '0')
   logFile = ' test-' + str1 + '-' + str2 + '.log'
   runAndTime("ulam_sequence_set.py " + str1 + ' ' + str2 + logFile)

if 1:
   for n in range(4, 17):
      str1 = str(n).rjust(2, '0')
      str2 = str(n * 1000000).rjust(8, '0')
      logFile = ' ulam_sequence-' + str1 + '-' + str2 + '.log'
      runAndTime("ulam_sequence_set.py " + str1 + ' ' + str2 + logFile)
