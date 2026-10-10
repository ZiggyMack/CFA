@echo off
setlocal
set "OBSERVATORY_ENGINE=%~dp0..\..\.cache\godot-4.7.2\Godot_v4.7.2-stable_win64.exe"
if not exist "%OBSERVATORY_ENGINE%" (
  echo The portable Godot engine is missing. See README.md for setup.
  pause
  exit /b 1
)
if not exist "%~dp0.local" mkdir "%~dp0.local"
set "APPDATA=%~dp0.local\osdata"
set "OBSERVATORY_DATA_DIR=%~dp0.local"
if not exist "%APPDATA%" mkdir "%APPDATA%"
start "The Observatory" "%OBSERVATORY_ENGINE%" --path "%~dp0." --rendering-method gl_compatibility --log-file "%~dp0.local\play.log"
