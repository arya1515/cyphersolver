@echo off
setlocal
cd /d "%~dp0"
for /f "delims=" %%P in ('where pythonw.exe 2^>nul') do if not defined PYTHONW set "PYTHONW=%%P"
if not defined PYTHONW set "PYTHONW=pythonw.exe"
start "" /b "%PYTHONW%" run_all.py main97 97 --sa 10
