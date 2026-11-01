# PREHĽAD STAVU EXPERIMENTU: čo je hotové, čo rozpracované, aký je ďalší krok.
# Spustenie:  powershell -ExecutionPolicy Bypass -File scripts\status.ps1   (pri finálnom behu: -RunsDir runs_final)
param([string]$RunsDir = "")
Set-Location (Split-Path $PSScriptRoot -Parent)
if ($RunsDir) { $env:DIZERTACKA_RUNS_DIR = (Join-Path (Get-Location) $RunsDir) }
$env:PYTHONIOENCODING = "utf-8"
& ".venv\Scripts\python.exe" -m src.common.status
