REM run UlamSecCPP\Release\UlamSecCPP.exe
REM called "run-cpp.bat " + str1 + ' ' + str2 + logFile
UlamSecCPP\Release\UlamSecCPP.exe %1 %2
move /y tempFile.txt %3

