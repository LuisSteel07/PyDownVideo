set path_build=%CD%

md "%path_build%\dist\tools"
xcopy "%path_build%\tools" "%path_build%\dist\tools" /s /e
copy "%path_build%\python.png" "%path_build%\dist\python.png"
ren "%path_build%\dist\main.exe" "PyDownVideo.exe"