# DESTILÁCIA A KASKÁDA: výber modelov podľa pravidla (docs\00), mäkké označenia učiteľov, študenti (destilácia,
# kontrola bez destilácie, variant A), meranie spotreby študentov, 5 variantov kaskády, záverečné porovnanie.
# Predpoklad: run_static.ps1 a run_dynamic_hybrid.ps1. Spustenie:
#   powershell -ExecutionPolicy Bypass -File scripts\run_distillation_cascade.ps1      (pokračuje po prerušení)
. "$PSScriptRoot\_common.ps1"
Start-Transcript -Path (Join-Path $RUNS "run_distillation_cascade_log.txt") -Append | Out-Null
$students = @("mlp_kd", "mlp_nokd", "mlp_kd_modal")
$r = @()
$r += Step "select"       "Výber najlepších modelov podľa pravidla" @("-m", "src.training.select_best", "--groups", "hybrid", "static", "dynamic")
Require $r "výber modelov"
Write-Host "Vybraný učiteľ (hybrid): $RUNS\selection\hybrid.md" -ForegroundColor Yellow
$r += Step "oof_hybrid"   "Mäkké označenia – hybridný učiteľ"               @("-m", "src.training.teacher_oof", "--teacher", "auto:hybrid")
$r += Step "oof_static"   "Mäkké označenia – statický učiteľ (variant A)"   @("-m", "src.training.teacher_oof", "--teacher", "auto:static")
$r += Step "oof_dynamic"  "Mäkké označenia – dynamický učiteľ (variant A)"  @("-m", "src.training.teacher_oof", "--teacher", "auto:dynamic")
$r += Step "stud_static"  "Študenti – statickí"   (@("-m", "src.training.run_suite", "--approach", "students_static", "--skip-done", "--models") + $students)
$r += Step "stud_dynamic" "Študenti – dynamickí"  (@("-m", "src.training.run_suite", "--approach", "students_dynamic", "--skip-done", "--models") + $students)
$r += Step "stud_bench_s" "Meranie spotreby – statickí študenti"  @("-m", "src.evaluation.benchmark", "--approach", "students_static")
$r += Step "stud_bench_d" "Meranie spotreby – dynamickí študenti" @("-m", "src.evaluation.benchmark", "--approach", "students_dynamic")
Require $r "študenti"
foreach ($v in @("main", "nokd", "modal", "heavy", "baselines")) {
    $r += Step "cascade_$v" "Kaskáda: $v" @("-m", "src.cascade.evaluate", "--config", "configs/cascade/$v.yaml")
}
$r += Step "final_report" "Záverečné porovnanie (výskumné otázky)" @("-m", "src.evaluation.final_report")
Stop-Transcript | Out-Null
Require $r "destilácia a kaskáda"
Write-Host "`nHotovo: $RUNS\comparison\final\README.md" -ForegroundColor Green
