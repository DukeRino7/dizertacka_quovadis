# src/common/ – spoločné pomôcky

Kód, ktorý používajú všetky ostatné časti. Nemá obsahovať nič špecifické pre konkrétny model.

| Modul | Obsah |
|---|---|
| `paths.py` | cesty projektu; `RUNS_DIR` presmerovateľný premennou `DIZERTACKA_RUNS_DIR` |
| `config.py` | načítanie YAML |
| `hardware.py` | `load_protocol()`: počet vlákien podľa počítača (`auto_threads`) |
| `seed.py` | seedy Python, NumPy, PyTorch |
| `run.py` | priečinok behu, uloženie konfigurácie, protokolu a prostredia |
| `provenance.py` | git commit, prostredie (počítač, CPU, RAM, GPU, verzie knižníc), kontrolné súčty, JSON |

Meranie výpočtových nárokov je v `src/evaluation/` (`timing.py`, `resources.py`, `benchmark.py`).
