



ECHO PRESS ANY KEY TO CONTINUE TO START CONVERSION OF MODELS USING GCONV
del temp\*.tex
del temp\*.mef
..\tools\gconv\gconv.exe IGI1Models.qsc -all -InputPath=Export -OutputPath=Output\Output %1 %2 %3 %4 %5



ECHO PRESS ANY KEY TO CONTINUE TO CONVERT MODEL VERSION FOR IGI 1
pause
copy temp\*.mef Output\*.mef
powershell -Command " python ..\tools\dconv mef Version '..\Exports\Output' '..\Exports\temp' "


ECHO PRESS ANY KEY TO CONTINUE TO RECREATE RESOURECE FILE
pause
del Output\*.mef
..\tools\gconv\gconv.exe temp\level1.asc

ECHO DONE!!
pause