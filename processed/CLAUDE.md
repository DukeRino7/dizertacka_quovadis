# processed/ – predspracované dáta (cache)

Odvodené dáta vytvorené kódom zo `src/data`, aby sa surové dáta nespracovávali pri každom behu.

Pravidlá:
- Všetko tu musí byť **znovu vytvoriteľné** spustením skriptu zo `src/data`. Veľké dátové súbory
  (`*.npy`, `*.parquet`) sa necommitujú; dokumentácia, štatistiky, grafy a manifesty áno.
- Každý výstup má `manifest.json`: skript, konfigurácia, git commit, prostredie, SHA-256 vstupov a výstupov, časy.
- Učené transformácie (napr. normalizácia, slovník API volaní) sa sem **neukladajú**. Fitujú sa iba na
  tréningu v rámci konkrétneho experimentu a ukladajú sa do jeho priečinka v `runs/`.
- `README.md` a `STATISTICS.md` v podpriečinkoch generujú skripty – neupravovať ručne.

| Priečinok | Obsah | Vytvára | Stav |
|---|---|---|---|
| `index/` | spoločný index vzoriek a rozdelenie train/validation/test pre všetky modely | `python -m src.data.build_index` | hotové |
| `static/` | EMBER príznaky po častiach + štatistiky a grafy | `python -m src.data.build_static` | hotové |
| `dynamic/` | Speakeasy reporty vo forme pre modely | – | čaká na stiahnutie dát |

Poradie: najprv `build_index`, potom `build_static` (a neskôr dynamická časť).
