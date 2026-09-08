@echo off
setlocal
cd /d "%~dp0"
python -m PyInstaller --noconfirm --clean GermanCourseAI.spec
if errorlevel 1 exit /b %errorlevel%
echo Built: %CD%\dist\GermanCourseAI.exe

rem Dagitim arsivi: lisans bildirimleri exe'nin yaninda durmalidir.
rem The MIT/BSD/HPND components require their notices to travel with the binary.
set "STAGE=%CD%\build\win-zip"
if exist "%STAGE%" rmdir /s /q "%STAGE%"
mkdir "%STAGE%" || exit /b 1
copy /y "%CD%\dist\GermanCourseAI.exe" "%STAGE%\" >nul || exit /b 1
copy /y "%CD%\LICENSE" "%STAGE%\" >nul || exit /b 1
copy /y "%CD%\THIRD_PARTY_NOTICES.md" "%STAGE%\" >nul || exit /b 1
if exist "%CD%\dist\GermanCourseAI-Windows.zip" del /q "%CD%\dist\GermanCourseAI-Windows.zip"
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Compress-Archive -Path '%STAGE%\*' -DestinationPath '%CD%\dist\GermanCourseAI-Windows.zip' -CompressionLevel Optimal"
if errorlevel 1 exit /b %errorlevel%
rmdir /s /q "%STAGE%"
echo Packaged: %CD%\dist\GermanCourseAI-Windows.zip (exe + LICENSE + THIRD_PARTY_NOTICES.md)
