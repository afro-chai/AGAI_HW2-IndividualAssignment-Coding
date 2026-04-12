@echo off
setlocal
cd /d "%~dp0.."
set PYTHONPATH=%CD%
set PYTHONUNBUFFERED=1
set STOCKTRADER_SKIP_LLM=
call "%CD%\.venv\Scripts\activate.bat"
python -u -m src.main --backtest --ticker-workers 2 1>>"%CD%\logs\live_pipeline.log" 2>&1
exit /b %ERRORLEVEL%
