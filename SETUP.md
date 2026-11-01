# Spustenie experimentu (napr. na pracovnom notebooku)

Claude ani prihlásenie do Claude **netreba** – všetko robia skripty v PowerShelli. Potrebný je Python 3.11 – 3.13,
internet a pre neurónové siete grafická karta NVIDIA s aktuálnym ovládačom.

## 1. Získať projekt
- **Odporúčané:** `git clone https://github.com/DukeRino7/dizertacka_quovadis.git` (prihlásenie na GitHub) – finálny beh
  si potom zapíše presnú verziu kódu (commit) do `RUN_INFO.txt`;
- alebo GitHub *Code → Download ZIP* (verziu kódu treba potom zapísať ručne).

## 2. Príprava (raz)
```
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```
`.venv` + knižnice, kontrola GPU, EMBER (zafixovaná revízia), statické dáta + overenie „ZHODA“ s gitom.

## 3. Postup po častiach (predbežná fáza)
| Skript | Čo robí | Trvanie (odhad, notebook) |
|---|---|---|
| `scripts\run_static.ps1` | statické modely, spotreba, analýza príznakov, kontrolné experimenty, porovnanie | 4–7 h |
| `scripts\prepare_dynamic.ps1` | stiahnutie Speakeasy + audit → **rozhodnutie** podľa `processed\dynamic\audit\AUDIT.md` | hodiny (sťahovanie) |
| `scripts\run_dynamic_hybrid.ps1` | dynamické dáta, dynamické + hybridné modely, spotreba, porovnania | ~0,5–1 deň |
| `scripts\run_distillation_cascade.ps1` | výber modelov podľa pravidla, učitelia, študenti, kaskády, záverečný report | ~0,5 dňa |

Každý skript po prerušení stačí spustiť znova – hotové kroky sa preskočia (značky v `runs\_state\`).
Krok zopakuješ zmazaním jeho značky. Výpisy: `runs\*_log.txt`.

## 4. Finálny beh (všetko naraz, 2–3 dni)
Po predbežnej fáze, keď sú rozhodnutia zapísané v `configs\` a kód je zmrazený (značka v gite, napr. `final-v1`):
```
powershell -ExecutionPolicy Bypass -File scripts\run_all.ps1 -RunsDir runs_final
```
Všetko sa uloží do `runs_final\` (oddelene od predbežných výsledkov), vrátane `RUN_INFO.txt` (počítač, commit, čas).
Pri finálnom behu by mal byť Speakeasy dataset už stiahnutý alebo skopírovaný do `data\quovadis-speakeasy`.

## 5. Prenos výsledkov
Zabaliť priečinok s výsledkami (`runs\` alebo `runs_final\`) a preniesť na PC, alebo `git push`.
Uložené modely (`model\` v behoch) nie sú v gite, ale sú v týchto priečinkoch.
**Merania spotreby porovnávať iba z jedného počítača** (`environment.json` v každom behu = názov počítača a hardvér).
