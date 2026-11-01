# STATICKÁ ČASŤ: tréning 5 modelov, meranie spotreby, analýza príznakov, kontrolné experimenty, porovnanie.
# Spustenie z koreňa projektu:  powershell -ExecutionPolicy Bypass -File scripts\run_static.ps1
# Po prerušení stačí spustiť znova – hotové kroky aj hotové modely sa preskočia. Počas behu PC nezaťažovať.
. "$PSScriptRoot\_common.ps1"
Start-Transcript -Path (Join-Path $RUNS "run_static_log.txt") -Append | Out-Null
$r = @()
$r += Step "static_train"      "Tréning statických modelov"             @("-m", "src.training.run_suite", "--approach", "static", "--skip-done")
$r += Step "static_benchmark"  "Meranie spotreby pri inferencii"        @("-m", "src.evaluation.benchmark", "--approach", "static")
$r += Step "static_importance" "Analýza využívania príznakov"           @("-m", "src.evaluation.feature_importance", "--approach", "static")
$r += Step "static_ablations"  "Kontrolné experimenty (bez podpisu a času zostavenia)" @("-m", "src.training.run_ablations", "--dir", "static_ablations", "--skip-done")
$r += Step "static_compare"    "Porovnanie statických modelov"          @("-m", "src.evaluation.compare", "--approach", "static")
Stop-Transcript | Out-Null
Require $r "statická časť"
Write-Host "`nStatická časť hotová: $RUNS\comparison\static\README.md" -ForegroundColor Green
