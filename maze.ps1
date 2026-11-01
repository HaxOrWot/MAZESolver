$venvPy = "Z:\VSCode\.venv\Scripts\python.exe"
if (Test-Path $venvPy) {
    & $venvPy "$PSScriptRoot\run.py" $args
} else {
    python "$PSScriptRoot\run.py" $args
}
