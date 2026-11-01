# Spustenie na inom počítači (napr. pracovný notebook)

Claude ani prihlásenie do Claude **netreba** – všetko robia skripty. Potrebný je Python 3.11 a internet.

## 1. Získať projekt
Repozitár je súkromný, preto jedna z možností:
- `git clone https://github.com/DukeRino7/dizertacka_quovadis.git` (pýta prihlásenie na GitHub), alebo
- na GitHube *Code → Download ZIP* (v prehliadači prihlásený na GitHub) a rozbaliť, alebo
- skopírovať priečinok projektu z PC **bez** `data\`, `processed\static\` a `.venv\` (USB / OneDrive).

## 2. Príprava (raz)
V PowerShelli v koreni projektu:
```
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```
Vytvorí `.venv`, nainštaluje knižnice (PyTorch ~2,5 GB), overí grafickú kartu, stiahne EMBER (~0,9 GB, presne
revíziu z `configs/data/static.yaml`), pripraví statické dáta a **overí, že sú bitovo zhodné s PC** (vypíše „ZHODA“).
Ak skopíruješ `processed\static` z PC, nič sa nesťahuje – iba sa overí zhoda.

## 3. Statická časť (niekoľko hodín)
```
powershell -ExecutionPolicy Bypass -File scripts\run_static.ps1
```
Tréning lr, rf, lightgbm, mlp_small, mlp_large → meranie spotreby → analýza príznakov → kontrolné experimenty →
porovnanie. Počas behu počítač nezaťažovať (merania spotreby). Výpis: `runs\static\run_static_log.txt`.
Počet vlákien sa nastaví podľa počítača automaticky (`configs/protocol.yaml: auto_threads`).

## 4. Prenos výsledkov
Zabaliť `runs\static`, `runs\static_ablations`, `runs\comparison` a preniesť na PC (alebo `git push`).
Uložené modely (`runs\**\model\`) nie sú v gite, ale sú v týchto priečinkoch – prenášať aj s nimi.
**Merania spotreby porovnávať iba z jedného počítača** (každý beh má v `environment.json` názov počítača a hardvér).
