# scripts/ – spúšťacie skripty (Windows PowerShell)

Návod: `SETUP.md`. Skripty sú uložené ako UTF-8 s BOM (kvôli diakritike vo Windows PowerShell 5.1).

| Skript | Obsah |
|---|---|
| `setup.ps1` | prostredie, knižnice, kontrola GPU, EMBER, statické dáta + overenie zhody s gitom |
| `run_static.ps1` | statická časť |
| `run_dynamic.ps1` | Speakeasy (overenie/stiahnutie), audit, príprava dát, dynamické modely, kontrolné experimenty |
| `run_hybrid.ps1` | hybridné modely (rebríček + dvojvetvová sieť) |
| `run_distillation_cascade.ps1` | výber modelov, destilácia, študenti, kaskády, záverečný report |
| `run_all.ps1` | finálny beh všetkého do `runs_final\` (`-RunsDir`) |
| `status.ps1` | prehľad stavu: hotové / rozpracované kroky, ďalší krok (`src/common/status.py`) |
| `_common.ps1` | spoločné funkcie: krok so značkou `runs\_state\<id>.done` (pokračovanie po prerušení) |

Výsledky idú do `runs\` alebo do priečinka z premennej `DIZERTACKA_RUNS_DIR` (nastavuje `run_all.ps1`).
