# test and time ulam_sequence routine

from runAndTime import runAndTime

# sample results
# ulam_sequence.py 2  1000:     0.17
# ulam_sequence.py 3  3000:     0.26
# ulam_sequence.py 4  4000:     0.32
# ulam_sequence.py 5  5000:     0.45
# ulam_sequence.py 2 10000:     0.52
# ulam_sequence.py 2 20000:     1.54
# ulam_sequence.py 2 40000:     4.95
# ulam_sequence.py 2 80000:    20.24

if 0:
    n = 4
    str1 = str(n).rjust(2, '0')
    str2 = str(n * 1000).rjust(8, '0')
    logFile = ' test-' + str1 + '-' + str2 + '.log'
    runAndTime("ulam_sequence.py " + str1 + ' ' + str2 + logFile)

if 0:
    for n in range(4, 17):
        str1 = str(n).rjust(2, '0')
        str2 = str(n * 1000000).rjust(8, '0')
        logFile = ' ulam_sequence-' + str1 + '-' + str2 + '.log'
        runAndTime("ulam_sequence.py " + str1 + ' ' + str2 + logFile)

if 1:
    for n in range(2, 10):
        C = 2**n
        str1 = str(C).rjust(4, '0')
        str2 = "" ### str(C * 100).rjust(8, '0')
        logFile = "" ###' Abstract_Ulam_Sequence-' + str1 + '-' + str2 + '.log'
        runAndTime("Abstract_Ulam_Sequence.py " + str1 + ' ' + str2 + logFile)

