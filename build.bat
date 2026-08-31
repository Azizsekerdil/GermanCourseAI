@echo off
setlocal
cd /d "%~dp0"
python -m PyInstaller --noconfirm --clean GermanCourseAI.spec
if errorlevel 1 exit /b %errorlevel%
echo Built: %CD%\dist\GermanCourseAI.exe
