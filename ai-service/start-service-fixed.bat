@echo off
echo === AI Service Startup (Fixed) ===
echo.

REM Load environment variables from .env file
echo Loading environment variables...
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if not "%%a"=="" if not "%%b"=="" (
        set "%%a=%%b"
    )
)

REM Display loaded variables (hiding API key)
echo.
echo Environment variables loaded:
if defined HTTP_PROXY echo   HTTP_PROXY: %HTTP_PROXY%
if defined HTTPS_PROXY echo   HTTPS_PROXY: %HTTPS_PROXY%
if defined MCP_AUTH_TOKEN echo   MCP_AUTH_TOKEN: %MCP_AUTH_TOKEN%
if defined GEMINI_API_KEY (
    echo   GEMINI_API_KEY: ***configured***
) else (
    echo   WARNING: GEMINI_API_KEY not set!
)

echo.
echo Starting AI service on port 8001...
echo.

REM Use Python to start service with environment properly loaded
python start_service.py

pause 