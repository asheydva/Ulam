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

# simplified version on laptop:
# py ulam_sequence.py 02 00160000   test-02-00160000.log:       8.04
# py ulam_sequence.py 02 01600000   test-02-01600000.log:     739.94
# py ulam_sequence.py 02 01000000 addend-02-01000000.log:     296.48

if 1:
    n = 2
    X = 5000
    str1 = str(n).rjust(2, '0')
    str2 = str(n * X).rjust(8, '0')
    logFile = ' addend-' + str1 + '-' + str2 + '.log'
    runAndTime("py ulam_sequence.py " + str1 + ' ' + str2 + logFile)

if 0:
    for n in range(4, 18):
        str1 = str(n).rjust(2, '0')
        str2 = str(n * 1000000).rjust(8, '0')
        logFile = ' UlamSequenceDataCPP/ulam_sequence-' + str1 + '-' + str2 + '.log'
        runAndTime("run-cpp.bat " + str1 + ' ' + str2 + logFile)

if 0:
    for n in range(4, 18):
        str1 = str(n).rjust(2, '0')
        str2 = str(n * 1000000).rjust(8, '0')
        logFile = ' UlamSequenceData/ulam_sequence-' + str1 + '-' + str2 + '.log'
        runAndTime("ulam_sequence.py " + str1 + ' ' + str2 + logFile)


if 0:
    for n in range(2, 10):
        C = 2**n
        str1 = str(C).rjust(4, '0')
        str2 = "" ### str(C * 100).rjust(8, '0')
        logFile = "" ###' Abstract_Ulam_Sequence-' + str1 + '-' + str2 + '.log'
        runAndTime("Abstract_Ulam_Sequence.py " + str1 + ' ' + str2 + logFile)

