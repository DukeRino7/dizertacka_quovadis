# PRÍPRAVA PROSTREDIA A STATICKÝCH DÁT (Windows PowerShell)
# Spustenie z koreňa projektu:  powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
# Predpoklad: nainštalovaný Python 3.11 a internet. Claude ani GitHub účet sa nepotrebujú.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
function Step($t) { Write-Host "`n=== $t ===" -ForegroundColor Cyan }

Step "1/5 Python 3.11"
$py = $null
foreach ($c in @("py -3.11", "python")) {
    try { $v = & cmd /c "$c --version" 2>$null; if ($v -match "3\.11") { $py = $c; break } } catch {}
}
if (-not $py) { throw "Nenašiel sa Python 3.11. Nainštaluj ho z python.org (zaškrtni 'Add to PATH') a spusti znova." }
Write-Host "Používam: $py ($v)"

Step "2/5 Virtuálne prostredie .venv a knižnice (PyTorch ~2,5 GB, chvíľu potrvá)"
if (-not (Test-Path ".venv\Scripts\python.exe")) { & cmd /c "$py -m venv .venv"; if ($LASTEXITCODE) { throw "venv zlyhal" } }
$vpy = ".venv\Scripts\python.exe"
& $vpy -m pip install --upgrade pip -q
& $vpy -m pip install -r requirements.txt
if ($LASTEXITCODE) { throw "Inštalácia knižníc zlyhala." }

Step "3/5 Grafická karta"
& $vpy -c "import torch; ok=torch.cuda.is_available(); print('CUDA dostupná:', ok, '|', torch.cuda.get_device_name(0) if ok else 'bez GPU - neurónové siete pobežia na CPU (pomaly)')"
Write-Host "Ak je 'CUDA dostupná: False' a notebook má kartu NVIDIA, aktualizuj ovládač grafiky a spusti setup znova."

Step "4/5 Statické dáta"
$have = (Test-Path "processed\static\X_train.npy") -and (Test-Path "processed\static\X_test.npy")
if ($have) {
    Write-Host "Nájdené skopírované processed\static - overujem kontrolné súčty voči gitu."
    & $vpy -m src.data.verify_static
} else {
    Write-Host "Sťahujem EMBER (~0,9 GB) a pripravujem statické dáta."
    & $vpy -m src.data.download --dataset ember
    if ($LASTEXITCODE) { throw "Sťahovanie zlyhalo." }
    & $vpy -m src.data.build_static
}
if ($LASTEXITCODE) { throw "Príprava/overenie dát zlyhalo." }

Step "5/5 Hotovo"
Write-Host "Ďalej: powershell -ExecutionPolicy Bypass -File scripts\run_static.ps1" -ForegroundColor Green
