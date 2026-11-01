# Spoločné funkcie skriptov (načítava sa cez: . "$PSScriptRoot\_common.ps1").
# Každý krok po úspechu zapíše značku <RunsDir>\_state\<id>.done -> pri opätovnom spustení sa preskočí
# (pokračovanie po prerušení). Krok zopakuješ zmazaním jeho značky.
Set-Location (Split-Path $PSScriptRoot -Parent)
$global:VPY = ".venv\Scripts\python.exe"
$env:PYTHONIOENCODING = "utf-8"
if (-not (Test-Path $global:VPY)) { throw "Chýba .venv – najprv spusti scripts\setup.ps1" }
$global:RUNS = if ($env:DIZERTACKA_RUNS_DIR) { $env:DIZERTACKA_RUNS_DIR } else { "runs" }
$global:STATE = Join-Path $global:RUNS "_state"
New-Item -ItemType Directory -Force $global:STATE | Out-Null

function Step([string]$id, [string]$title, [string[]]$cmdArgs) {
    $mark = Join-Path $global:STATE "$id.done"
    if (Test-Path $mark) { Write-Host "--- $title : hotové skôr, preskakujem ($id)" -ForegroundColor DarkGray; return $true }
    Write-Host "`n=== $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $title  [$id] ===" -ForegroundColor Cyan
    & $global:VPY @cmdArgs | Out-Host   # výstup na obrazovku (inak by sa stal návratovou hodnotou funkcie)
    if ($LASTEXITCODE) {
        Write-Host "!!! Krok $id skončil s chybou (kód $LASTEXITCODE)." -ForegroundColor Red
        return $false
    }
    Set-Content $mark (Get-Date -Format "yyyy-MM-dd HH:mm:ss") -Encoding utf8
    return $true
}

function Require([bool[]]$results, [string]$what) {
    if ($results -contains $false) { throw "Niektorý krok ($what) zlyhal – pozri výpis vyššie. Po oprave spusti skript znova (hotové kroky sa preskočia)." }
}
