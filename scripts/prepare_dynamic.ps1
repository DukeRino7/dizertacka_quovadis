# PRÍPRAVA DYNAMICKÝCH DÁT, ČASŤ 1: stiahnutie Speakeasy (~5,5 GB) a audit.
# Spustenie:  powershell -ExecutionPolicy Bypass -File scripts\prepare_dynamic.ps1
# ROZHODOVACÍ BOD: po audite skontrolovať processed\dynamic\audit\AUDIT.md a potvrdiť reprezentáciu
# v configs\data\dynamic.yaml (docs\04_dynamicke_data.md). Až potom scripts\run_dynamic_hybrid.ps1.
# Ak sú dáta skopírované z iného PC do data\quovadis-speakeasy, sťahovanie iba doplní chýbajúce súbory.
. "$PSScriptRoot\_common.ps1"
Start-Transcript -Path (Join-Path $RUNS "prepare_dynamic_log.txt") -Append | Out-Null
$r = @()
$r += Step "dyn_download" "Stiahnutie Speakeasy reportov" @("-m", "src.data.download", "--dataset", "speakeasy")
$r += Step "dyn_audit"    "Audit dynamických dát"         @("-m", "src.data.audit_dynamic")
Stop-Transcript | Out-Null
Require $r "príprava dynamických dát"
Write-Host "`nAudit: processed\dynamic\audit\AUDIT.md – skontrolovať a rozhodnúť (docs\04), potom run_dynamic_hybrid.ps1" -ForegroundColor Yellow
