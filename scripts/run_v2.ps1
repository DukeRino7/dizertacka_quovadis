# VERZIA V2 (docs\09_plan_v2.md): zero-day (vynechanie rodiny) + kaskáda B. Pokračuje po prerušení (značky _state).
# Predpoklady: priečinok projektu z V1 (data\, processed\, .venv\ a runs_final\ – stačí bez modelov), kód značky v2.
# Spustenie:
#   powershell -ExecutionPolicy Bypass -File scripts\run_v2.ps1                       (celý beh, 2–3 večery)
#   powershell -ExecutionPolicy Bypass -File scripts\run_v2.ps1 -Smoke -Families rat  (technická kontrola, ~1 h)
param([string]$RunsDir = "runs_v2",
      [string[]]$Families = @("backdoor", "coinminer", "dropper", "keylogger", "ransomware", "rat", "trojan"),
      [string]$V1 = "runs_final",
      [switch]$Smoke)
. "$PSScriptRoot\_common.ps1"
if ($Smoke -and $RunsDir -eq "runs_v2") { $RunsDir = "runs_v2_smoke" }
$ROOT = Join-Path (Get-Location) $RunsDir
if (-not (Test-Path "$V1\selection\hybrid.json")) { throw "Chýba $V1\selection – výsledky V1 musia byť v priečinku projektu." }
if (-not (Test-Path "processed\dynamic\cache")) { throw "Chýba processed\dynamic\cache – spusti V2 v priečinku projektu z V1 (alebo najprv run_dynamic.ps1)." }
$sm = if ($Smoke) { @("--smoke") } else { @() }
$lim = if ($Smoke) { @("--limit", "4000") } else { @() }

function Use-Root([string]$dir) {   # priečinok výsledkov pre nasledujúce kroky (RUNS_DIR + značky _state)
    $env:DIZERTACKA_RUNS_DIR = $dir
    $global:RUNS = $dir
    $global:STATE = Join-Path $dir "_state"
    New-Item -ItemType Directory -Force $global:STATE | Out-Null
}

New-Item -ItemType Directory -Force $ROOT | Out-Null
$ver = if (Test-Path "VERSION.txt") { (Get-Content "VERSION.txt" -Encoding utf8 -TotalCount 1) } else { "?" }
$commit = (& git rev-parse HEAD 2>$null); if (-not $commit) { $commit = "bez gitu (ZIP)" }
Add-Content (Join-Path $ROOT "RUN_INFO.txt") "V2: spustenie $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | počítač $env:COMPUTERNAME | commit $commit | verzia: $ver | rodiny: $($Families -join ',') | smoke: $Smoke" -Encoding utf8
Start-Transcript -Path (Join-Path $ROOT "run_v2_log.txt") -Append | Out-Null
$students = @("mlp_kd", "mlp_nokd", "mlp_kd_modal", "mlp_kd_twobranch")
$cascA = @("main", "nokd", "modal", "heavy", "baselines", "twobranch")
$cascB = @("b_main", "b_direct", "b_heavy", "b_baselines", "b_nokd", "b_twobranch")

# --- 1) časový test (rozdelenie V1): učiteľ dvojvetvová sieť, noví študenti, kaskády B na modeloch V1 ---------
Use-Root (Join-Path $ROOT "full")
$env:DIZERTACKA_HOLDOUT_FAMILY = ""; $env:DIZERTACKA_PARAMS_ROOTS = ""; $env:DIZERTACKA_RESULTS_FALLBACK = $V1
$r = @()
$r += Step "setup"        "Výber architektúr pevne z V1" @("-m", "src.training.v2_setup", "--from", $V1)
$r += Step "oof_twobranch" "Mäkké označenia – učiteľ dvojvetvová sieť" (@("-m", "src.training.teacher_oof", "--teacher", "hybrid/two_branch", "--runs-root", $global:RUNS) + $lim)
$r += Step "stud_static"  "Študent statický – učiteľ dvojvetvová sieť (ladenie)" (@("-m", "src.training.run_suite", "--approach", "students_static", "--skip-done", "--no-compare", "--models", "mlp_kd_twobranch") + $sm)
$r += Step "stud_dynamic" "Študent dynamický – učiteľ dvojvetvová sieť (ladenie)" (@("-m", "src.training.run_suite", "--approach", "students_dynamic", "--skip-done", "--no-compare", "--models", "mlp_kd_twobranch") + $sm)
$r += Step "bench_s"      "Meranie spotreby – nový statický študent"  @("-m", "src.evaluation.benchmark", "--approach", "students_static")
$r += Step "bench_d"      "Meranie spotreby – nový dynamický študent" @("-m", "src.evaluation.benchmark", "--approach", "students_dynamic")
Require $r "časový test V2"
foreach ($v in $cascB) { $r += Step "cascade_$v" "Kaskáda B: $v (časový test)" @("-m", "src.cascade.evaluate_b", "--config", "configs/cascade/$v.yaml") }
$r += Step "cascade_twobranch" "Kaskáda A: twobranch (časový test)" @("-m", "src.cascade.evaluate", "--config", "configs/cascade/twobranch.yaml")
Require $r "kaskády – časový test"

# --- 2) zero-day: jedna rodina vynechaná z tréningu aj validácie ---------------------------------------------
foreach ($fam in $Families) {
    Use-Root (Join-Path $ROOT "lofo\$fam")
    $env:DIZERTACKA_HOLDOUT_FAMILY = $fam
    $env:DIZERTACKA_PARAMS_ROOTS = "$RunsDir\full;$V1"   # hyperparametre z V1 (nový študent z časti 1), bez ladenia
    $env:DIZERTACKA_RESULTS_FALLBACK = ""                # nikdy nepoužiť modely trénované s touto rodinou
    Write-Host "`n########## Zero-day: vynechaná rodina $fam ##########" -ForegroundColor Magenta
    $r = @()
    $r += Step "data_tab"  "[$fam] n-gramy API bez rodiny" @("-m", "src.data.build_dynamic_tabular", "--exclude-family", $fam)
    $r += Step "data_seq"  "[$fam] sekvencie API bez rodiny" @("-m", "src.data.build_dynamic_sequence", "--exclude-family", $fam)
    $r += Step "setup"     "[$fam] výber architektúr z V1" @("-m", "src.training.v2_setup", "--from", $V1)
    Require $r "príprava $fam"
    $r += Step "static"    "[$fam] statické modely"  (@("-m", "src.training.run_suite", "--approach", "static", "--skip-done", "--models", "lr", "rf", "lightgbm", "mlp_small", "mlp_large") + $sm)
    $r += Step "dynamic"   "[$fam] dynamické modely" (@("-m", "src.training.run_suite", "--approach", "dynamic", "--skip-done", "--models", "lr", "rf", "lightgbm", "mlp_small", "mlp_large", "seq_cnn") + $sm)
    $r += Step "hybrid"    "[$fam] hybridné modely"  (@("-m", "src.training.run_suite", "--approach", "hybrid", "--skip-done", "--models", "lr", "rf", "lightgbm", "mlp_small", "mlp_large", "two_branch") + $sm)
    Require $r "modely $fam"
    foreach ($t in @("auto:hybrid", "auto:static", "auto:dynamic", "hybrid/two_branch")) {
        $id = "oof_" + ($t -replace "[:/]", "_")
        $r += Step $id "[$fam] mäkké označenia učiteľa $t" (@("-m", "src.training.teacher_oof", "--teacher", $t, "--runs-root", $global:RUNS) + $lim)
    }
    $r += Step "stud_static"  "[$fam] statickí študenti"  (@("-m", "src.training.run_suite", "--approach", "students_static", "--skip-done", "--models") + $students + $sm)
    $r += Step "stud_dynamic" "[$fam] dynamickí študenti" (@("-m", "src.training.run_suite", "--approach", "students_dynamic", "--skip-done", "--models") + $students + $sm)
    Require $r "študenti $fam"
    foreach ($v in $cascA) { $r += Step "cascade_$v" "[$fam] kaskáda A: $v" @("-m", "src.cascade.evaluate", "--config", "configs/cascade/$v.yaml") }
    foreach ($v in $cascB) { $r += Step "cascade_$v" "[$fam] kaskáda B: $v" @("-m", "src.cascade.evaluate_b", "--config", "configs/cascade/$v.yaml") }
    Require $r "kaskády $fam"
}

# --- 3) súhrn V2 a vyhodnotenie téz podľa kritérií z docs/09 ---------------------------------------------------
Use-Root $ROOT
$env:DIZERTACKA_HOLDOUT_FAMILY = ""; $env:DIZERTACKA_PARAMS_ROOTS = ""; $env:DIZERTACKA_RESULTS_FALLBACK = ""
$r = @(Step "v2_report" "Súhrn V2 (tézy)" @("-m", "src.evaluation.v2_report", "--root", $RunsDir, "--v1", $V1))
Add-Content (Join-Path $ROOT "RUN_INFO.txt") "Koniec: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -Encoding utf8
Stop-Transcript | Out-Null
Require $r "súhrn V2"
Write-Host "`nV2 HOTOVÁ: $ROOT\comparison\v2\README.md" -ForegroundColor Green
