@echo off
setlocal
set VENV_PYTHON=Z:\VSCode\.venv\Scripts\python.exe
if exist "%VENV_PYTHON%" (
    "%VENV_PYTHON%" "%~dp0run.py" %*
) else (
    python "%~dp0run.py" %*
)
