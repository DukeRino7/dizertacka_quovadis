# DYNAMICKÁ ČASŤ: Speakeasy dáta (overenie/stiahnutie), audit, príprava dát, dynamické modely (rebríček + sekvenčná CNN),
# kontrolné experimenty (s udalosťami a súhrnom), meranie spotreby, analýza príznakov, porovnanie.
# Spustenie:  powershell -ExecutionPolicy Bypass -File scripts\run_dynamic.ps1      (pokračuje po prerušení)
# Speakeasy: najrýchlejšie skopírovať celý priečinok data\quovadis-speakeasy (vrátane .cache) z PC –
# krok stiahnutia potom iba overí, že nič nechýba. Rozhodnutia o reprezentácii: configs\data\dynamic.yaml, docs\04.
. "$PSScriptRoot\_common.ps1"
Start-Transcript -Path (Join-Path $RUNS "run_dynamic_log.txt") -Append | Out-Null
$models = @("lr", "rf", "lightgbm", "mlp_small", "mlp_large", "seq_cnn")
$r = @()
$r += Step "dyn_download"   "Speakeasy dáta (overenie / doplnenie)"          @("-m", "src.data.download", "--dataset", "speakeasy")
$r += Step "dyn_audit"      "Audit dynamických dát"                          @("-m", "src.data.audit_dynamic")
$r += Step "dyn_cache"      "Normalizovaná cache reportov"                   @("-m", "src.data.build_dynamic")
$r += Step "dyn_tabular"    "Vektor z API volaní (hlavná reprezentácia)"     @("-m", "src.data.build_dynamic_tabular")
$r += Step "dyn_tabular_full" "Kontrolná reprezentácia (s udalosťami a súhrnom)" @("-m", "src.data.build_dynamic_tabular", "--variant", "full")
$r += Step "dyn_sequence"   "Postupnosti API pre sekvenčný model"            @("-m", "src.data.build_dynamic_sequence")
Require $r "príprava dynamických dát"
$r += Step "dyn_train"      "Tréning dynamických modelov"   (@("-m", "src.training.run_suite", "--approach", "dynamic", "--skip-done", "--models") + $models)
$r += Step "dyn_ablations"  "Kontrolné experimenty (artefakt emulátora)"     @("-m", "src.training.run_ablations", "--dir", "dynamic_ablations", "--skip-done")
$r += Step "dyn_benchmark"  "Meranie spotreby – dynamické"                   @("-m", "src.evaluation.benchmark", "--approach", "dynamic")
$r += Step "dyn_importance" "Analýza príznakov – dynamické"                  @("-m", "src.evaluation.feature_importance", "--approach", "dynamic")
$r += Step "dyn_compare"    "Porovnanie dynamických modelov"                 @("-m", "src.evaluation.compare", "--approach", "dynamic")
Stop-Transcript | Out-Null
Require $r "dynamická časť"
Write-Host "`nDynamická časť hotová: $RUNS\comparison\dynamic\README.md" -ForegroundColor Green
