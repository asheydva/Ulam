# timing util

import time
import subprocess
import os

def runAndTimeCommand(cmd):
    start_time = time.time()

    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    elapsed_time = time.time() - start_time

    print('runAndTimeCommand: output', output)

    print('runAndTimeCommand: {}: {:10.2f}'.format(cmd, elapsed_time))
