# test and time ulam_sequence routine

from runAndTimeCommand import runAndTimeCommand

# sample results
# ulam_sequence.py 2  1000:     0.17
# ulam_sequence.py 3  3000:     0.26
# ulam_sequence.py 4  4000:     0.32
# ulam_sequence.py 5  5000:     0.45
# ulam_sequence.py 2 10000:     0.52
# ulam_sequence.py 2 20000:     1.54
# ulam_sequence.py 2 40000:     4.95
# ulam_sequence.py 2 80000:    20.24

# simplified version on laptop:
# py ulam_sequence.py 02 00160000   test-02-00160000.log:       8.04
# py ulam_sequence.py 02 01600000   test-02-01600000.log:     739.94
# py ulam_sequence.py 02 01000000 addend-02-01000000.log:     296.48

# py ulam_sequence.py 02 00010000 addend-02-00010000.log:       0.13 -- brute force
# py ulam_sequence.py 02 00100000 addend-02-00100000.log:       3.03 -- brute force
# py ulam_sequence.py 02 01000000 addend-02-01000000.log:     293.75 -- brute force

# Gibbs:
# py ulam_sequence.py 02 1000000000 addend-02-1000000000.log:    5947.57 -- 1.65 hr, 73,976,840 Ulam numbers

if 1:
    n = 2
    X = 11 #500*1000*1000 
    str1 = str(n).rjust(2, '0')
    str2 = str(n * X).rjust(8, '0')
    logFile = ' addend-' + str1 + '-' + str2 + '.log'
    runAndTimeCommand("py ulam_sequence.py " + str1 + ' ' + str2 + logFile)

if 0:
    for n in range(4, 18):
        str1 = str(n).rjust(2, '0')
        str2 = str(n * 1000000).rjust(8, '0')
        logFile = ' UlamSequenceDataCPP/ulam_sequence-' + str1 + '-' + str2 + '.log'
        runAndTimeCommand("run-cpp.bat " + str1 + ' ' + str2 + logFile)

if 0:
    for n in range(4, 18):
        str1 = str(n).rjust(2, '0')
        str2 = str(n * 1000000).rjust(8, '0')
        logFile = ' UlamSequenceData/ulam_sequence-' + str1 + '-' + str2 + '.log'
        runAndTimeCommand("ulam_sequence.py " + str1 + ' ' + str2 + logFile)


if 0:
    for n in range(2, 10):
        C = 2**n
        str1 = str(C).rjust(4, '0')
        str2 = "" ### str(C * 100).rjust(8, '0')
        logFile = "" ###' Abstract_Ulam_Sequence-' + str1 + '-' + str2 + '.log'
        runAndTimeCommand("Abstract_Ulam_Sequence.py " + str1 + ' ' + str2 + logFile)

