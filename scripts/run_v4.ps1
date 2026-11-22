# VERZIA V4 (docs\19_plan_v4.md): KronoDroid – vetvy real_full (hlavná), real_p a emu_p (emulátor vs. zariadenie),
# doplnkový časový posun malvéru (real_time). Rovnaký postup ako Quo Vadis (V1 + V2 + špecialista V3).
# Predpoklady: data\kronodroid (CSV), processed\kronodroid (src.data.kronodroid.build_kronodroid), kód značky v4.
# Spustenie:
#   powershell -ExecutionPolicy Bypass -File scripts\run_v4.ps1                                  (celý beh)
#   powershell -ExecutionPolicy Bypass -File scripts\run_v4.ps1 -Smoke -Families Boxer          (technická kontrola)
# Po prerušení spustiť rovnako znova – pokračuje tam, kde skončil (značky _state).
param([string]$RunsDir = "runs_v4",
      [string[]]$Branches = @("real_full", "real_p", "emu_p"),
      [string[]]$Families = @("Airpush/StopSMS", "Boxer", "FakeInst", "Locker/SLocker Ransomware", "BankBot"),
      [switch]$NoTime,
      [switch]$Smoke)
. "$PSScriptRoot\_common.ps1"
if ($Smoke -and $RunsDir -eq "runs_v4") { $RunsDir = "runs_v4_smoke" }
$ROOT = Join-Path (Get-Location) $RunsDir
if (-not (Test-Path "processed\kronodroid\emu_p\dynamic\tabular_norm\X_test.npy")) {   # .npy sa necommitujú
    & $global:VPY -m src.data.kronodroid.build_kronodroid
    if ($LASTEXITCODE) { throw "Príprava dát KronoDroid zlyhala." }
}
if (($Branches -contains "emu_p") -and -not ($Branches -contains "real_p") -and -not (Test-Path "$RunsDir\real_p\full\static")) {
    throw "emu_p preberá statické modely z real_p – spusti aj vetvu real_p (docs/19 4.2)."
}
$sm = if ($Smoke) { @("--smoke") } else { @() }
$lim = if ($Smoke) { @("--limit", "4000") } else { @() }
$ladder = @("lr", "rf", "lightgbm", "mlp_small", "mlp_large")
$students = @("mlp_kd", "mlp_nokd", "mlp_kd_modal", "mlp_kd_heavy")
$cascA = @("main", "nokd", "modal", "heavy", "baselines", "heavyteacher")
$cascB = @("b_main", "b_direct", "b_heavy", "b_baselines", "b_nokd", "b_heavyteacher")
$teachers = @("auto:hybrid", "auto:static", "auto:dynamic", "hybrid/mlp_large")

function Use-Root([string]$dir) {   # priečinok výsledkov pre nasledujúce kroky (RUNS_DIR + značky _state)
    $env:DIZERTACKA_RUNS_DIR = $dir
    $global:RUNS = $dir
    $global:STATE = Join-Path $dir "_state"
    New-Item -ItemType Directory -Force $global:STATE | Out-Null
}
function Fam-Dir([string]$fam) { return ($fam -replace "[/ ]", "_") }

New-Item -ItemType Directory -Force $ROOT | Out-Null
$ver = if (Test-Path "VERSION.txt") { (Get-Content "VERSION.txt" -Encoding utf8 -TotalCount 1) } else { "?" }
$commit = (& git rev-parse HEAD 2>$null); if (-not $commit) { $commit = "bez gitu (ZIP)" }
Add-Content (Join-Path $ROOT "RUN_INFO.txt") "V4: spustenie $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | počítač $env:COMPUTERNAME | commit $commit | verzia: $ver | vetvy: $($Branches -join ',') | rodiny: $($Families -join ',') | smoke: $Smoke" -Encoding utf8
Start-Transcript -Path (Join-Path $ROOT "run_v4_log.txt") -Append | Out-Null

# Spoločné kroky jedného behu (hlavné rozdelenie, zero-day alebo časový posun). $full = s ladením, benchmarkom a analýzami.
function Run-Pipeline([string]$branch, [string]$label, [bool]$full, [string]$shareFrom) {
    $r = @()
    if ($branch -eq "emu_p") {
        $r += Step "share_static" "[$label] statické modely prevzaté z real_p" @("-m", "src.training.v4_share_static", "--src", $shareFrom, "--dst", $global:RUNS)
    } else {
        $r += Step "static" "[$label] statické modely" (@("-m", "src.training.run_suite", "--approach", "static", "--skip-done", "--models") + $ladder + $sm)
        if ($full) {
            $r += Step "static_bench" "[$label] meranie spotreby – statické" @("-m", "src.evaluation.benchmark", "--approach", "static")
            $r += Step "static_imp"   "[$label] analýza príznakov – statické" @("-m", "src.evaluation.feature_importance", "--approach", "static")
        }
    }
    $r += Step "dynamic" "[$label] dynamické modely" (@("-m", "src.training.run_suite", "--approach", "dynamic", "--skip-done", "--models") + $ladder + $sm)
    $r += Step "hybrid"  "[$label] hybridné modely"  (@("-m", "src.training.run_suite", "--approach", "hybrid", "--skip-done", "--models") + $ladder + $sm)
    if ($full) {
        $r += Step "dyn_norm"   "[$label] kontrolný experiment D-norm" @("-m", "src.training.run_ablations", "--dir", "kronodroid/dynamic_ablations", "--skip-done")
        $r += Step "dyn_bench"  "[$label] meranie spotreby – dynamické" @("-m", "src.evaluation.benchmark", "--approach", "dynamic")
        $r += Step "hyb_bench"  "[$label] meranie spotreby – hybridné"  @("-m", "src.evaluation.benchmark", "--approach", "hybrid")
        $r += Step "dyn_imp"    "[$label] analýza príznakov – dynamické" @("-m", "src.evaluation.feature_importance", "--approach", "dynamic")
        $r += Step "hyb_imp"    "[$label] analýza príznakov – hybridné"  @("-m", "src.evaluation.feature_importance", "--approach", "hybrid")
        $r += Step "select"     "[$label] výber modelov podľa pravidla (docs/00)" @("-m", "src.training.select_best", "--groups", "hybrid", "static", "dynamic")
    } else {
        $r += Step "setup" "[$label] výber architektúr z hlavného rozdelenia" @("-m", "src.training.v2_setup", "--from", "$RunsDir\$branch\full")
    }
    Require $r "modely $label"
    foreach ($t in $teachers) {
        $id = "oof_" + ($t -replace "[:/]", "_")
        $r += Step $id "[$label] mäkké označenia učiteľa $t" (@("-m", "src.training.teacher_oof", "--teacher", $t, "--runs-root", $global:RUNS) + $lim)
    }
    $r += Step "stud_static"  "[$label] statickí študenti"  (@("-m", "src.training.run_suite", "--approach", "students_static", "--skip-done", "--models") + $students + $sm)
    $r += Step "stud_dynamic" "[$label] dynamickí študenti" (@("-m", "src.training.run_suite", "--approach", "students_dynamic", "--skip-done", "--models") + $students + $sm)
    if ($full) {
        $r += Step "stud_bench_s" "[$label] meranie spotreby – statickí študenti"  @("-m", "src.evaluation.benchmark", "--approach", "students_static")
        $r += Step "stud_bench_d" "[$label] meranie spotreby – dynamickí študenti" @("-m", "src.evaluation.benchmark", "--approach", "students_dynamic")
    }
    Require $r "študenti $label"
    foreach ($v in $cascA) { $r += Step "cascade_$v" "[$label] kaskáda A: $v" @("-m", "src.cascade.evaluate", "--config", "configs/kronodroid/cascade/$v.yaml") }
    foreach ($v in $cascB) { $r += Step "cascade_$v" "[$label] kaskáda B: $v" @("-m", "src.cascade.evaluate_b", "--config", "configs/kronodroid/cascade/$v.yaml") }
    $specs = if ($full) { @("v4_spec", "v4_spec_dyn", "v4_spec_f10", "v4_spec_f40") } else { @("v4_spec", "v4_spec_dyn") }
    $bench = if ($full) { @("--benchmark") } else { @() }
    foreach ($v in $specs) { $r += Step "spec_$v" "[$label] špecialista $v" (@("-m", "src.cascade.specialist", "--config", "configs/kronodroid/cascade/$v.yaml") + $bench + $sm) }
    if ($full -and -not $Smoke) { $r += Step "complementarity" "[$label] komplementarita" @("-m", "src.evaluation.complementarity", "--runs-root", $global:RUNS) }
    Require $r "kaskády $label"
}

foreach ($b in $Branches) {
    $env:DIZERTACKA_DATASET = $b
    # --- 1) hlavné (náhodné) rozdelenie: ladenie, výber, benchmark ---------------------------------------------
    Write-Host "`n########## V4 – vetva $b, hlavné rozdelenie ##########" -ForegroundColor Magenta
    Use-Root (Join-Path $ROOT "$b\full")
    $env:DIZERTACKA_HOLDOUT_FAMILY = ""; $env:DIZERTACKA_PARAMS_ROOTS = ""; $env:DIZERTACKA_RESULTS_FALLBACK = ""
    Run-Pipeline $b "$b full" $true "$RunsDir\real_p\full"

    # --- 2) zero-day: rodina vynechaná z tréningu aj validácie, hyperparametre z hlavného rozdelenia -------------
    foreach ($fam in $Families) {
        $fd = Fam-Dir $fam
        Write-Host "`n########## V4 – vetva $b, zero-day: $fam ##########" -ForegroundColor Magenta
        Use-Root (Join-Path $ROOT "$b\lofo\$fd")
        $env:DIZERTACKA_HOLDOUT_FAMILY = $fam
        $env:DIZERTACKA_PARAMS_ROOTS = "$RunsDir\$b\full"
        $env:DIZERTACKA_RESULTS_FALLBACK = ""   # nikdy nepoužiť modely trénované s touto rodinou
        Run-Pipeline $b "$b $fam" $false "$RunsDir\real_p\lofo\$fd"
    }
}

# --- 3) doplnkový časový posun malvéru (iba real_full, hyperparametre z hlavného rozdelenia) ----------------------
if (-not $NoTime -and ($Branches -contains "real_full")) {
    Write-Host "`n########## V4 – časový posun malvéru (real_time) ##########" -ForegroundColor Magenta
    $env:DIZERTACKA_DATASET = "real_time"
    Use-Root (Join-Path $ROOT "real_full\time")
    $env:DIZERTACKA_HOLDOUT_FAMILY = ""; $env:DIZERTACKA_PARAMS_ROOTS = "$RunsDir\real_full\full"; $env:DIZERTACKA_RESULTS_FALLBACK = ""
    Run-Pipeline "real_full" "real_full time" $false ""   # výber a hyperparametre z real_full/full
}

Use-Root $ROOT
$env:DIZERTACKA_DATASET = ""; $env:DIZERTACKA_HOLDOUT_FAMILY = ""; $env:DIZERTACKA_PARAMS_ROOTS = ""; $env:DIZERTACKA_RESULTS_FALLBACK = ""
Add-Content (Join-Path $ROOT "RUN_INFO.txt") "Koniec: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -Encoding utf8
Stop-Transcript | Out-Null
Write-Host "`nV4 HOTOVÁ: $ROOT (súhrn: src.evaluation.v4_report)" -ForegroundColor Green
