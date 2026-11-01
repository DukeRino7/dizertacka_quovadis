# processed/ – predspracované dáta (cache)

Odvodené dáta vytvorené kódom zo `src/data`, aby sa surové dáta nespracovávali pri každom behu.

Pravidlá:
- Všetko tu musí byť **znovu vytvoriteľné** spustením skriptu zo `src/data`. Veľké dátové súbory
  (`*.npy`, `*.parquet`) sa necommitujú; dokumentácia, štatistiky, grafy a manifesty áno.
- Každý výstup má `manifest.json`: skript, konfigurácia, git commit, prostredie, SHA-256 vstupov a výstupov, časy.
- Učené transformácie **konkrétneho modelu** (napr. škálovanie) sa sem neukladajú – patria do behu v `runs/`.
  Výnimka: **spoločná reprezentácia** pre všetky modely prístupu (slovník n-gramov API v `dynamic/tabular`),
  naučená iba na tréningu a uložená s manifestom.
- `README.md` a `STATISTICS.md` v podpriečinkoch generujú skripty – neupravovať ručne.

| Priečinok | Obsah | Vytvára | Stav |
|---|---|---|---|
| `index/` | spoločný index vzoriek a rozdelenie train/validation/test pre všetky modely | `python -m src.data.build_index` | hotové |
| `static/` | EMBER príznaky po častiach + štatistiky a grafy | `python -m src.data.build_static` | hotové |
| `dynamic/audit/` | audit Speakeasy reportov | `python -m src.data.audit_dynamic` | čaká na dáta |
| `dynamic/cache/` | normalizované reporty (všetky vstupné body vzorky spolu) | `python -m src.data.build_dynamic` | čaká na dáta |
| `dynamic/sequence/` | ID tokenov API pre sekvenčné modely (slovník iba z tréningu) | `python -m src.data.build_dynamic_sequence` | čaká na dáta |
| `dynamic/tabular/` | vektor pre rebríček (slovník n-gramov iba z tréningu) | `python -m src.data.build_dynamic_tabular` | čaká na dáta |

Poradie: najprv `build_index`, potom `build_static` (a neskôr dynamická časť).
