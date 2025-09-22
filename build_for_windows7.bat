@echo off
echo ================================================
echo Gmail OAuth Generator - Windows 7 Compatible Build
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8.10 for best Windows 7 compatibility
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Check if PyInstaller is installed
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller==4.10
    if errorlevel 1 (
        echo Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"
echo.

echo Building Windows 7 compatible executable...
echo This may take a few minutes...
echo.

REM Windows 7 compatible PyInstaller command
pyinstaller ^
    --onefile ^
    --noconsole ^
    --noupx ^
    --target-architecture=x86_64 ^
    --exclude-module=_tkinter ^
    --exclude-module=tkinter.dnd ^
    --exclude-module=tkinter.test ^
    --exclude-module=test ^
    --exclude-module=unittest ^
    --hidden-import=selenium ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.messagebox ^
    --add-data="output;output" ^
    --name=Gmail_OAuth_Generator_Win7 ^
    --distpath=dist ^
    --workpath=build ^
    main.py

if errorlevel 1 (
    echo.
    echo Build failed! Please check the error messages above.
    echo.
    echo Common solutions:
    echo 1. Install Python 3.8.10 for better Windows 7 compatibility
    echo 2. Install Visual C++ Redistributable 2015-2019
    echo 3. Run as Administrator
    echo 4. Disable antivirus temporarily
    pause
    exit /b 1
)

echo.
echo ================================================
echo Build completed successfully!
echo ================================================
echo.
echo Executable location: dist\Gmail_OAuth_Generator_Win7.exe
echo.

REM Copy additional files
echo Copying additional files...
if exist "README.md" copy "README.md" "dist\"
if exist "accounts.txt" copy "accounts.txt" "dist\"
if exist "requirements.txt" copy "requirements.txt" "dist\"
if exist "Windows7_Compatibility_Guide.md" copy "Windows7_Compatibility_Guide.md" "dist\"

REM Create output directory in dist
if not exist "dist\output" mkdir "dist\output"

echo.
echo Files copied to dist folder:
dir /b "dist"
echo.

echo ================================================
echo Windows 7 Compatibility Notes:
echo ================================================
echo 1. This build is optimized for Windows 7
echo 2. UPX compression is disabled
echo 3. Problematic modules are excluded
echo 4. Make sure Visual C++ Redistributable is installed
echo 5. Run as Administrator if needed
echo.
echo For troubleshooting, see: Windows7_Compatibility_Guide.md
echo.
pause