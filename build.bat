@echo off
setlocal
cd /d "%~dp0"

rem Paket yalnizca requirements.txt'teki bagimliliklari icersin diye derleme
rem kendi sanal ortamini kullanir; boylece gelistiricinin genel yorumlayicisinda
rem kurulu baska paketler (numpy, pandas, lxml ...) yanlislikla exe'ye toplanmaz.
rem Hazir bir yorumlayici PYTHON_BIN ortam degiskeniyle verilebilir.
rem A dedicated venv keeps the exe free of whatever else happens to be installed
rem in the developer's interpreter -- see THIRD_PARTY_NOTICES.md section 3.
if defined PYTHON_BIN goto have_python

set "BUILD_VENV=%TEMP%\GermanCourseAI-build-venv"
if exist "%BUILD_VENV%\Scripts\python.exe" goto venv_ready
echo Temiz sanal ortam olusturuluyor: %BUILD_VENV%
python -m venv "%BUILD_VENV%" || exit /b 1
:venv_ready
set "PYTHON_BIN=%BUILD_VENV%\Scripts\python.exe"
"%PYTHON_BIN%" -m pip install --upgrade pip || exit /b 1
"%PYTHON_BIN%" -m pip install -r requirements.txt || exit /b 1
"%PYTHON_BIN%" -m pip install pyinstaller || exit /b 1

:have_python
"%PYTHON_BIN%" -c "import sys" >nul 2>&1 || (echo HATA: PYTHON_BIN calistirilamadi: %PYTHON_BIN% & exit /b 1)
echo Yorumlayici: %PYTHON_BIN%

"%PYTHON_BIN%" -m PyInstaller --noconfirm --clean GermanCourseAI.spec
if errorlevel 1 exit /b %errorlevel%
echo Built: %CD%\dist\GermanCourseAI.exe

rem Dagitim arsivi: lisans bildirimleri exe'nin yaninda durmalidir.
rem The MIT/BSD/HPND components require their notices to travel with the binary.
set "STAGE=%CD%\build\win-zip"
if exist "%STAGE%" rmdir /s /q "%STAGE%"
mkdir "%STAGE%" || exit /b 1
copy /y "%CD%\dist\GermanCourseAI.exe" "%STAGE%" >nul || exit /b 1
copy /y "%CD%\LICENSE" "%STAGE%" >nul || exit /b 1
copy /y "%CD%\THIRD_PARTY_NOTICES.md" "%STAGE%" >nul || exit /b 1
if exist "%CD%\dist\GermanCourseAI-Windows.zip" del /q "%CD%\dist\GermanCourseAI-Windows.zip"
"%PYTHON_BIN%" -c "import pathlib,sys,zipfile; stage=pathlib.Path(sys.argv[1]); zf=zipfile.ZipFile(sys.argv[2],'w',zipfile.ZIP_DEFLATED); [zf.write(p,p.name) for p in sorted(stage.iterdir())]; zf.close()" "%STAGE%" "%CD%\dist\GermanCourseAI-Windows.zip"
if errorlevel 1 exit /b %errorlevel%
rmdir /s /q "%STAGE%"
echo Packaged: %CD%\dist\GermanCourseAI-Windows.zip (exe + LICENSE + THIRD_PARTY_NOTICES.md)
