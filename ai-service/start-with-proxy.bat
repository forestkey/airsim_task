@echo off
echo === AI Service with Proxy ===
echo.

REM Check if proxy is set in environment
if "%HTTP_PROXY%"=="" (
    echo No HTTP_PROXY environment variable found.
    echo.
    echo Common proxy settings:
    echo   - Clash: http://127.0.0.1:7890
    echo   - V2Ray/Shadowsocks: http://127.0.0.1:1080
    echo.
    set /p proxy_url="Enter proxy URL (or press Enter to skip): "
    
    if not "!proxy_url!"=="" (
        set HTTP_PROXY=!proxy_url!
        set HTTPS_PROXY=!proxy_url!
        echo Proxy set to: !proxy_url!
    ) else (
        echo No proxy configured, using direct connection.
    )
) else (
    echo Using existing proxy: %HTTP_PROXY%
)

echo.
echo Starting AI Service on port 8001...
echo.

REM Activate Python 3.12 environment
echo Please ensure you have activated your Python 3.12 environment (drone_312)
echo.

REM Start the service
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

pause 