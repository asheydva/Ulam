# timing util

import time
import subprocess
import os

def runAndTimeCommand(cmd):
    print('runAndTimeCommand: ' + cmd + '\n')
    start_time = time.time()

    # this stopped working... TODO
    subprocess.check_output(cmd, shell=True, universal_newlines=True)
    elapsed_time = time.time() - start_time

    print('{}: {:10.2f}'.format(cmd, elapsed_time))
