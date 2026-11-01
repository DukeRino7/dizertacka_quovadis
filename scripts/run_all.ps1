# FINÁLNY BEH CELÉHO EXPERIMENTU (2–3 dni) na jednom počítači do samostatného priečinka výsledkov.
# Predpoklady: scripts\setup.ps1; rozhodnutia z predbežnej fázy zapísané v configs\ (najmä configs\data\dynamic.yaml).
# Spustenie:
#   powershell -ExecutionPolicy Bypass -File scripts\run_all.ps1 -RunsDir runs_final
# Po prerušení spustiť rovnako znova – pokračuje tam, kde skončil. Počas behu PC nezaťažovať (merania spotreby).
param([string]$RunsDir = "runs_final")
$root = Split-Path $PSScriptRoot -Parent
$env:DIZERTACKA_RUNS_DIR = (Join-Path $root $RunsDir)
New-Item -ItemType Directory -Force $env:DIZERTACKA_RUNS_DIR | Out-Null
$commit = (& git -C $root rev-parse HEAD 2>$null)
$ver = if (Test-Path (Join-Path $root "VERSION.txt")) { (Get-Content (Join-Path $root "VERSION.txt") -Encoding utf8 -TotalCount 1) } else { "?" }
if (-not $commit) { $commit = "bez gitu (ZIP)" }
$commit = "$commit | verzia: $ver"
$info = Join-Path $env:DIZERTACKA_RUNS_DIR "RUN_INFO.txt"
Add-Content $info "Finálny beh: spustenie $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | počítač $env:COMPUTERNAME | commit $commit" -Encoding utf8
Write-Host "Výsledky: $env:DIZERTACKA_RUNS_DIR (commit $commit)" -ForegroundColor Cyan
foreach ($s in @("run_static.ps1", "run_dynamic.ps1", "run_hybrid.ps1", "run_distillation_cascade.ps1")) {
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot $s)
    if ($LASTEXITCODE) { throw "$s skončil s chybou – oprav a spusti run_all.ps1 znova (hotové kroky sa preskočia)." }
}
Add-Content $info "Koniec: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -Encoding utf8
Write-Host "`nFINÁLNY BEH HOTOVÝ: $env:DIZERTACKA_RUNS_DIR\comparison\final\README.md" -ForegroundColor Green
