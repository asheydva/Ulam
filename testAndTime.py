# test and time ulam_sequence routine

import time
import subprocess
import os

# sample results
# ulam_sequence.py 2 1000	0.19148826599121094
# ulam_sequence.py 3 3000	0.3500633239746094
# ulam_sequence.py 4 4000	0.34407997131347656
# ulam_sequence.py 5 5000	0.4527900218963623
# ulam_sequence.py 2 10000	0.5585072040557861
# ulam_sequence.py 2 20000	1.494004249572754
# ulam_sequence.py 2 40000	5.431474208831787
# ulam_sequence.py 2 80000	21.91439437866211


fileName = 'ulam_sequence.log'

if os.path.exists(fileName):
    os.remove(fileName)

file = open(fileName, 'w+')

def runAndTime(cmd):
   file.write(cmd)

   start_time = time.time()
   output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
   elapsed_time = time.time() - start_time

   file.write(output)
   file.write('\n')

   print(cmd, elapsed_time, sep='\t')

# quick testing
runAndTime("ulam_sequence.py 2 1000")
runAndTime("ulam_sequence.py 3 3000")
runAndTime("ulam_sequence.py 4 4000")
runAndTime("ulam_sequence.py 5 5000")

# time consuming
runAndTime("ulam_sequence.py 2 10000")
runAndTime("ulam_sequence.py 2 20000")
runAndTime("ulam_sequence.py 2 40000")
runAndTime("ulam_sequence.py 2 80000")

file.close()
