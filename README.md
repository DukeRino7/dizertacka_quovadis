# Hybridná detekcia malvéru – experimentálna časť dizertácie

Laboratórne porovnanie statickej, dynamickej a hybridnej detekcie malvéru (malware/benign) a overenie,
či kaskáda dvoch ľahkých modelov vytvorených destiláciou vedomostí (statický + dynamický), ktorá pri ich
nezhode eskaluje vzorku veľkému hybridnému modelu, dosiahne porovnateľnú alebo lepšiu detekčnú kvalitu
s nižšími výpočtovými nárokmi než hybridný model použitý na každú vzorku.

## Dáta
- Statické: [dtrizna/quovadis-ember](https://huggingface.co/datasets/dtrizna/quovadis-ember)
- Behaviorálne (emulácia Speakeasy): [dtrizna/quovadis-speakeasy](https://huggingface.co/datasets/dtrizna/quovadis-speakeasy)

Dáta nie sú súčasťou repozitára. Stiahnuť ich do `data/quovadis-ember` a `data/quovadis-speakeasy`.
Výsledky auditu dát: [docs/01_audit_dat.md](docs/01_audit_dat.md).

## Prostredie
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Štruktúra
Popis v [CLAUDE.md](CLAUDE.md); každý priečinok má vlastný `CLAUDE.md`.
