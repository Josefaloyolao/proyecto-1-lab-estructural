@echo off
echo Activando entorno virtual Python 3.12 + OpenSeesPy...
call "%~dp0.venv\Scripts\activate.bat"
echo.
echo Python: %VIRTUAL_ENV%\Scripts\python.exe
echo OpenSeesPy: listo
echo.
cmd /k
