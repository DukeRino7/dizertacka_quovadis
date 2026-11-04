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
| `run_v2.ps1` | **V2** (docs/09): časový test s novými študentmi a kaskádami B (`runs_v2\full`), 7 zero-day behov (`runs_v2\lofo\<rodina>`), súhrn; `-Smoke -Families rat` = technická kontrola do `runs_v2_smoke\` |
| `run_v3.ps1` | **V3** (docs/12): špecialisti v časovom teste (`runs_v3\full`, s meraním CPU) a v 7 zero-day behoch (`runs_v3\lofo\<rodina>`, komponenty z `runs_v2`), súhrn B a scenár C; `-Smoke -Families rat` = technická kontrola do `runs_v3_smoke\` |
| `status.ps1` | prehľad stavu: hotové / rozpracované kroky, ďalší krok (`src/common/status.py`) |
| `_common.ps1` | spoločné funkcie: krok so značkou `runs\_state\<id>.done` (pokračovanie po prerušení) |

Výsledky idú do `runs\` alebo do priečinka z premennej `DIZERTACKA_RUNS_DIR` (nastavuje `run_all.ps1`).
