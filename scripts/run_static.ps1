# CELÁ STATICKÁ ČASŤ: tréning 5 modelov, meranie spotreby, analýza príznakov, kontrolné experimenty, porovnanie.
# Spustenie z koreňa projektu:  powershell -ExecutionPolicy Bypass -File scripts\run_static.ps1
# Trvá niekoľko hodín. Počítač počas behu nezaťažovať (merania spotreby). Výpis: runs\static\run_static_log.txt
Set-Location (Split-Path $PSScriptRoot -Parent)
$vpy = ".venv\Scripts\python.exe"
$env:PYTHONIOENCODING = "utf-8"
New-Item -ItemType Directory -Force runs\static | Out-Null
Start-Transcript -Path "runs\static\run_static_log.txt" -Append | Out-Null

function Run([string]$title, [string[]]$cmdArgs) {
    Write-Host "`n=== $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $title ===" -ForegroundColor Cyan
    & $vpy @cmdArgs
    if ($LASTEXITCODE) { Write-Host "!!! Krok skončil s chybou (kód $LASTEXITCODE), pokračujem ďalej." -ForegroundColor Red }
}

Run "1/5 Tréning statických modelov (lr, rf, lightgbm, mlp_small, mlp_large)" @("-m", "src.training.run_suite", "--approach", "static")
Run "2/5 Meranie spotreby pri inferencii" @("-m", "src.evaluation.benchmark", "--approach", "static")
Run "3/5 Analýza využívania príznakov" @("-m", "src.evaluation.feature_importance", "--approach", "static")
Run "4/5 Kontrolné experimenty bez podpisu a času zostavenia" @("-m", "src.training.run_ablations", "--dir", "static_ablations")
Run "5/5 Porovnanie modelov" @("-m", "src.evaluation.compare", "--approach", "static")

Write-Host "`nHotovo. Výsledky: runs\comparison\static\README.md" -ForegroundColor Green
Write-Host "Prenos na PC: zabaliť priečinky runs\static, runs\static_ablations, runs\comparison (alebo git push)." -ForegroundColor Green
Stop-Transcript | Out-Null
