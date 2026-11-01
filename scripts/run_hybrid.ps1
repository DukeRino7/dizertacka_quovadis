# HYBRIDNÁ ČASŤ: hybridné modely (rebríček nad spojeným vektorom + dvojvetvová sieť), meranie spotreby,
# analýza príznakov, porovnanie. Predpoklad: run_static.ps1 (statické dáta) a run_dynamic.ps1 (dynamické dáta).
# Spustenie:  powershell -ExecutionPolicy Bypass -File scripts\run_hybrid.ps1      (pokračuje po prerušení)
. "$PSScriptRoot\_common.ps1"
Start-Transcript -Path (Join-Path $RUNS "run_hybrid_log.txt") -Append | Out-Null
$models = @("lr", "rf", "lightgbm", "mlp_small", "mlp_large", "two_branch")
$r = @()
$r += Step "hyb_train"      "Tréning hybridných modelov"     (@("-m", "src.training.run_suite", "--approach", "hybrid", "--skip-done", "--models") + $models)
$r += Step "hyb_benchmark"  "Meranie spotreby – hybridné"    @("-m", "src.evaluation.benchmark", "--approach", "hybrid")
$r += Step "hyb_importance" "Analýza príznakov – hybridné"   @("-m", "src.evaluation.feature_importance", "--approach", "hybrid")
$r += Step "hyb_compare"    "Porovnanie hybridných modelov"  @("-m", "src.evaluation.compare", "--approach", "hybrid")
Stop-Transcript | Out-Null
Require $r "hybridná časť"
Write-Host "`nHybridná časť hotová: $RUNS\comparison\hybrid\README.md" -ForegroundColor Green
