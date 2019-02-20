@ECHO OFF
ECHO Delete Folder: %CD%?
PAUSE
SET FOLDER=%CD%
CD ..
echo DEL /F/Q/S "%FOLDER%"
echo RMDIR /Q/S "%FOLDER%"
