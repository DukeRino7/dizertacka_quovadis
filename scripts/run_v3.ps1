# VERZIA V3 (docs\12_plan_v3.md): B = kaskáda so špecialistom pre neisté súbory, C = prekalibrovanie prahu.
# Predpoklady: priečinok projektu, v ktorom bežala V2 (data\, processed\ vrátane processed\dynamic\lofo\, .venv\,
# runs_final\ a runs_v2\ – modely netreba, stačia predikcie a teachers\), kód značky v3.
# Spustenie:
#   powershell -ExecutionPolicy Bypass -File scripts\run_v3.ps1                        (celý beh, odhad 30–60 min)
#   powershell -ExecutionPolicy Bypass -File scripts\run_v3.ps1 -Smoke -Families rat   (technická kontrola, ~10 min)
param([string]$RunsDir = "runs_v3",
      [string[]]$Families = @("backdoor", "coinminer", "dropper", "keylogger", "ransomware", "rat", "trojan"),
      [string]$V1 = "runs_final",
      [string]$V2 = "runs_v2",
      [switch]$Smoke)
. "$PSScriptRoot\_common.ps1"
if ($Smoke -and $RunsDir -eq "runs_v3") { $RunsDir = "runs_v3_smoke" }
$ROOT = Join-Path (Get-Location) $RunsDir
if (-not (Test-Path "$V1\teachers\static_lightgbm")) { throw "Chýba $V1\teachers\static_lightgbm – výsledky V1 musia byť v priečinku projektu." }
foreach ($fam in $Families) {
    if (-not (Test-Path "$V2\lofo\$fam\teachers\static_lightgbm")) { throw "Chýba $V2\lofo\$fam\teachers\static_lightgbm – výsledky V2 musia byť v priečinku projektu." }
}
if (-not (Test-Path "processed\dynamic\cache")) { throw "Chýba processed\dynamic\cache – spusti V3 v priečinku projektu, kde bežala V2." }
$sm = if ($Smoke) { @("--smoke") } else { @() }
$variants = @("v3_spec", "v3_spec_dyn", "v3_spec_f10", "v3_spec_f40")

function Use-Root([string]$dir) {
    $env:DIZERTACKA_RUNS_DIR = $dir
    $global:RUNS = $dir
    $global:STATE = Join-Path $dir "_state"
    New-Item -ItemType Directory -Force $global:STATE | Out-Null
}

New-Item -ItemType Directory -Force $ROOT | Out-Null
$ver = if (Test-Path "VERSION.txt") { (Get-Content "VERSION.txt" -Encoding utf8 -TotalCount 1) } else { "?" }
$commit = (& git rev-parse HEAD 2>$null); if (-not $commit) { $commit = "bez gitu (ZIP)" }
Add-Content (Join-Path $ROOT "RUN_INFO.txt") "V3: spustenie $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | počítač $env:COMPUTERNAME | commit $commit | verzia: $ver | rodiny: $($Families -join ',') | smoke: $Smoke" -Encoding utf8
Start-Transcript -Path (Join-Path $ROOT "run_v3_log.txt") -Append | Out-Null

# --- 1) časový test (rozdelenie V1): komponenty a OOF skóre z runs_final, meranie CPU času špecialistu ---------
Use-Root (Join-Path $ROOT "full")
$env:DIZERTACKA_HOLDOUT_FAMILY = ""; $env:DIZERTACKA_PARAMS_ROOTS = ""; $env:DIZERTACKA_RESULTS_FALLBACK = $V1
$r = @()
foreach ($v in $variants) {
    $r += Step "spec_$v" "Špecialista $v (časový test)" (@("-m", "src.cascade.specialist", "--config", "configs/cascade/$v.yaml", "--benchmark") + $sm)
}
Require $r "špecialisti – časový test"

# --- 2) zero-day: komponenty a OOF skóre z runs_v2\lofo\<rodina> (modely bez tejto rodiny) -----------------------
foreach ($fam in $Families) {
    Use-Root (Join-Path $ROOT "lofo\$fam")
    $env:DIZERTACKA_HOLDOUT_FAMILY = $fam
    $env:DIZERTACKA_RESULTS_FALLBACK = "$V2\lofo\$fam"   # nikdy nie modely trénované s touto rodinou
    Write-Host "`n########## V3 zero-day: vynechaná rodina $fam ##########" -ForegroundColor Magenta
    $r = @()
    if (-not (Test-Path "processed\dynamic\lofo\$fam\tabular\manifest.json")) {
        $r += Step "data_tab" "[$fam] n-gramy API bez rodiny" @("-m", "src.data.build_dynamic_tabular", "--exclude-family", $fam)
    }
    if (-not (Test-Path "processed\dynamic\lofo\$fam\sequence\manifest.json")) {
        $r += Step "data_seq" "[$fam] sekvencie API bez rodiny" @("-m", "src.data.build_dynamic_sequence", "--exclude-family", $fam)
    }
    foreach ($v in $variants) {
        $r += Step "spec_$v" "[$fam] špecialista $v" (@("-m", "src.cascade.specialist", "--config", "configs/cascade/$v.yaml") + $sm)
    }
    Require $r "špecialisti $fam"
}

# --- 3) súhrn B a scenár C (prekalibrovanie prahu, iba z uložených predikcií) -----------------------------------
Use-Root $ROOT
$env:DIZERTACKA_HOLDOUT_FAMILY = ""; $env:DIZERTACKA_RESULTS_FALLBACK = ""
$r = @()
$r += Step "v3_report" "Súhrn V3 – B (kritériá)" @("-m", "src.evaluation.v3_report", "--root", $RunsDir)
$r += Step "v3_recal"  "V3 – C: prekalibrovanie prahu" (@("-m", "src.evaluation.v3_recalibration", "--v1", $V1, "--v2", $V2, "--v3", $RunsDir, "--families") + $Families)
Add-Content (Join-Path $ROOT "RUN_INFO.txt") "Koniec: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -Encoding utf8
Stop-Transcript | Out-Null
Require $r "súhrn V3"
Write-Host "`nV3 HOTOVÁ: $ROOT\comparison\v3\README.md a RECALIBRATION.md" -ForegroundColor Green
