
del temp\*.tex

del temp\*.mef

..\tools\gconv\gconv.exe IGI2Models.qsc -all -InputPath=Export -OutputPath=Output\Output %1 %2 %3 %4 %5

pause

powershell -Command " python ..\tools\dconv mef decompile '..\Exports\temp' '..\Exports\Output' "

pause