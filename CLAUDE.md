# Dizertačný výskum: hybridná detekcia malvéru

## Cieľ
Laboratórne porovnať statickú, dynamickú a hybridnú detekciu malvéru. Overiť, či kaskáda ľahkých modelov dosahuje porovnateľnú alebo lepšiu detekčnú kvalitu s nižším časom inferencie a výpočtovými nárokmi než samostatný komplexný hybridný model. Nejde o vývoj koncovej aplikácie.

## Navrhovaný prístup
- Pre každý súbor mať spárované statické a dynamické vstupy.
- Ľahký statický model a ľahký dynamický model vytvoriť destiláciou vedomostí.
- Ak sa oba modely zhodnú na malware/benign, prijať ich rozhodnutie.
- Pri nezhode poslať oba vstupy veľkému hybridnému modelu, ktorý rozhodne.
- Konkrétne architektúry, hyperparametre a spôsob destilácie zatiaľ nie sú určené.

## Dáta
Projekt je na počítači používateľa v `D:\dizertacka`.
- Statické dáta: `data/quovadis-ember`, zdroj https://huggingface.co/datasets/dtrizna/quovadis-ember
- Behaviorálne dáta: `data/quovadis-speakeasy`, zdroj https://huggingface.co/datasets/dtrizna/quovadis-speakeasy
- Behaviorálne reporty vznikli emuláciou Speakeasy. Neoznačovať ich za plnohodnotný beh vo Windows sandboxe.
- Párovať podľa SHA-256, nikdy podľa poradia riadkov. Jeden súbor je jedna vzorka; všetky jeho vlákna a vstupné body patria spolu.
- Skutočný formát, počty použiteľných párov a dostupné označenia najprv overiť v stiahnutých dátach.

## Postup a pravidlá
1. Overiť štruktúru dát, párovanie, označenia, duplicity a chýbajúce alebo poškodené záznamy. Pôvodné dáta nemeniť.
2. Vytvoriť spoločný index vzoriek a rovnaké train/validation/test rozdelenie pre všetky porovnávané modely. Zachovať pôvodný test a validáciu vyčleniť z tréningu.
3. Rozbehnúť statický, dynamický a hybridný baseline, potom destiláciu a kaskádu.
4. Všetky učené transformácie a destiláciu robiť iba na tréningu; prahy a hyperparametre vyberať na validácii. Test nepoužívať na ladenie.
5. Vyhodnotiť detekčnú kvalitu, podiel eskalácií, spoločné chyby pri zhode a prínos veľkého modelu pri nezhode. Samostatne merať inferenciu, tréning a prípravu priznakov.
6. Ukladať konfigurácie, seedy, modely, predikcie a metriky jednotlivých experimentov.

Kód organizovať do `src/data`, `src/models`, `src/training`, `src/evaluation`; konfigurácie do `configs`, výsledky do `runs`.
Neodhadovať neznáme vlastnosti dát ani nevymýšľať výsledky. Neurčené vedecké rozhodnutia prezentovať ako návrh, nie ako schválenú požiadavku.

## Dohodnuté rozhodnutia
- Výskumné otázky, pravidlá výberu modelov (TPR pri FPR 1 % na validácii) a vykazovania výsledkov: `docs/00_vyskumne_otazky.md`.
- Protokol tréningu a sada modelov: `docs/03_protokol_a_modely.md`; destilácia a kaskáda: `docs/05_destilacia_a_kaskada.md`.
- Pred každým výberom alebo vyhodnotením tieto dokumenty skontrolovať; pravidlá nemeniť podľa výsledkov.
- **Finálne výsledky V1:** `runs_final/` (pracovný notebook, 2026-11-02), súhrn `docs/07_vysledky_v1.md`. Finálne čísla brať iba odtiaľ.

## Štruktúra projektu
Každý priečinok má vlastný `CLAUDE.md` s popisom účelu, pravidiel a aktuálneho stavu. Pri zmene ho aktualizovať.
- `data/` – pôvodné dáta, iba na čítanie.
- `processed/` – predspracované dáta (cache), znovu vytvoriteľné zo `src/data`.
- `configs/<prístup>/` – konfigurácie experimentov.
- `src/common`, `src/data`, `src/models/<prístup>`, `src/training`, `src/evaluation`, `src/cascade` (finálna kaskáda).
- `runs/<prístup>/<model>/` – výsledky a grafy, napr. `runs/static/lr/`; `runs/comparison/` – porovnanie prístupov.
- `docs/` – súhrnné dokumenty pre dizertáciu (napr. `docs/01_audit_dat.md`).
- `scripts/` – spúšťacie skripty celého postupu (návod `SETUP.md`); finálny beh `scripts/run_all.ps1` do `runs_final/`.
- `resources/`, `runs/selection/`, `runs/teachers/` – pozri `CLAUDE.md` v príslušnom priečinku.

Prístupy: `static`, `dynamic`, `hybrid`, `students_static`, `students_dynamic`, `cascade`.

## Prostredie
- Python 3.11.9 vo `.venv` (spúšťať cez `.venv\Scripts\python.exe`). Knižnice: `requirements.txt`, presné verzie: `requirements-lock.txt`.
- GPU: NVIDIA GeForce RTX 2060, 6 GB; PyTorch s CUDA 13.0 (overené).
- Git: https://github.com/DukeRino7/dizertacka_quovadis (vetva `main`). Dáta, `processed/`, `.venv` a uložené modely sa necommitujú.
- Texty a dokumentáciu písať po slovensky s diakritikou.
