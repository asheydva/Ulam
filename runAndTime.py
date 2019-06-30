# timing util

import time
import subprocess
import os

def runAndTime(cmd):
    start_time = time.time()
    subprocess.check_output(cmd, shell=True, universal_newlines=True)
    elapsed_time = time.time() - start_time

    print('{}: {:10.2f}'.format(cmd, elapsed_time))
