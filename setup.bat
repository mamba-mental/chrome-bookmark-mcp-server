@echo off
echo Installing Chrome Bookmark MCP Server dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Python is not installed. Please install Python 3.8 or later.
        pause
        exit /b 1
    )
    set PYTHON_CMD=python3
) else (
    set PYTHON_CMD=python
)

echo Using %PYTHON_CMD%
echo.

REM Install dependencies
echo Installing required packages...
%PYTHON_CMD% -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo.
echo To run the server manually:
echo   %PYTHON_CMD% server\MCP_Chrome_Server_033025.py
echo.
echo The server is configured in .mcp.json as "chrome-bookmark-server"
echo.
pause