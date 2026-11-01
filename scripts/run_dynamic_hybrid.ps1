# DYNAMICKÁ A HYBRIDNÁ ČASŤ: príprava dát, rebríček + sekvenčná CNN (dynamic), rebríček + dvojvetvová sieť (hybrid),
# meranie spotreby, analýza príznakov, porovnania. Predpoklad: prepare_dynamic.ps1 a potvrdená reprezentácia.
# Spustenie:  powershell -ExecutionPolicy Bypass -File scripts\run_dynamic_hybrid.ps1   (pokračuje po prerušení)
. "$PSScriptRoot\_common.ps1"
Start-Transcript -Path (Join-Path $RUNS "run_dynamic_hybrid_log.txt") -Append | Out-Null
$models = @("lr", "rf", "lightgbm", "mlp_small", "mlp_large")
$r = @()
$r += Step "dyn_cache"      "Normalizovaná cache reportov"          @("-m", "src.data.build_dynamic")
$r += Step "dyn_tabular"    "Vektor z API volaní pre rebríček"      @("-m", "src.data.build_dynamic_tabular")
$r += Step "dyn_sequence"   "Postupnosti API pre sekvenčné modely"  @("-m", "src.data.build_dynamic_sequence")
Require $r "príprava dát"
$r += Step "dyn_train"      "Tréning dynamických modelov"           (@("-m", "src.training.run_suite", "--approach", "dynamic", "--skip-done", "--models") + $models + @("seq_cnn"))
$r += Step "hyb_train"      "Tréning hybridných modelov"            (@("-m", "src.training.run_suite", "--approach", "hybrid", "--skip-done", "--models") + $models + @("two_branch"))
$r += Step "dyn_benchmark"  "Meranie spotreby – dynamické"          @("-m", "src.evaluation.benchmark", "--approach", "dynamic")
$r += Step "hyb_benchmark"  "Meranie spotreby – hybridné"           @("-m", "src.evaluation.benchmark", "--approach", "hybrid")
$r += Step "dyn_importance" "Analýza príznakov – dynamické"         @("-m", "src.evaluation.feature_importance", "--approach", "dynamic")
$r += Step "hyb_importance" "Analýza príznakov – hybridné"          @("-m", "src.evaluation.feature_importance", "--approach", "hybrid")
$r += Step "dyn_compare"    "Porovnanie dynamických modelov"        @("-m", "src.evaluation.compare", "--approach", "dynamic")
$r += Step "hyb_compare"    "Porovnanie hybridných modelov"         @("-m", "src.evaluation.compare", "--approach", "hybrid")
Stop-Transcript | Out-Null
Require $r "dynamická a hybridná časť"
Write-Host "`nHotovo: $RUNS\comparison\dynamic\README.md, $RUNS\comparison\hybrid\README.md" -ForegroundColor Green
