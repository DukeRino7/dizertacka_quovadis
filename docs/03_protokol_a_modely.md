# 03 – Trénovací protokol a modely

Stav k 2026-11-01. Dohodnuté s autorom práce: dve vrstvy modelov a neskorá fúzia ako hybridný baseline.
Parametre protokolu sú **NÁVRH** (`configs/protocol.yaml`) – zmena tam platí pre všetky modely.

## Dohodnutá sada modelov
**Vrstva A – spoločný rebríček** (rovnaké modely pre static, dynamic, hybrid; vstupom je vždy pevný vektor:
static = EMBER, dynamic = vektor z API volaní (reprezentácia sa určí po kontrole dát), hybrid = spojenie oboch):

| Názov | Model | Kód | Úloha |
|---|---|---|---|
| `lr` | logistická regresia (L2) | `src/models/tabular/logreg.py` | lineárny základ, najľahší |
| `rf` | Random Forest | `src/models/tabular/random_forest.py` | klasické strojové učenie |
| `lightgbm` | gradient boosting stromov | `src/models/tabular/lightgbm_model.py` | silný tabuľkový model |
| `mlp_small` | MLP, 1–2 skryté vrstvy | `src/models/tabular/mlp.py` | kandidát na ľahkého študenta |
| `mlp_large` | MLP, 3–5 vrstiev, 512–2048 neurónov | `src/models/tabular/mlp.py` | kandidát na učiteľa |

**Vrstva B – špecifické modely** (pripravené, čakajú na dáta; rovnaký protokol ako rebríček):
- `seq_cnn` (`src/models/dynamic/sequence_cnn.py`): embedding API + 1D konvolúcie nad postupnosťou volaní (prvých 1024),
- `two_branch` (`src/models/hybrid/two_branch.py`): statická MLP vetva + sekvenčná vetva, kandidát na veľký model v kaskáde,
- **neskorá fúzia** (`src/models/hybrid/late_fusion.py`): priemer / stacking skóre statického a dynamického modelu
  (kontrola, či sa eskalácia na veľký model oplatí).

## Spoločný protokol (platí pre každý model)
| Oblasť | Pravidlo | Dôvod |
|---|---|---|
| Použitie dát | train = učenie; validácia = ladenie, early stopping, prahy; test = iba finálne vyhodnotenie | test nesmie ovplyvniť žiadne rozhodnutie |
| Transformácia vstupu | LR a MLP: odstránenie konštantných príznakov, signed log1p, štandardizácia – fit iba na train (štatistiky vo float64), aplikácia vo float32 na mieste; stromy pôvodné hodnoty | ťažké chvosty EMBER príznakov; stromy sú invariantné voči monotónnym transformáciám |
| Nepomer tried | váhy vzoriek `n / (2 · n_trieda)` z tréningu | train 67 % malvéru, test 54 % |
| Ladenie hyperparametrov | Optuna TPE, **30 pokusov pre každý model**, seed 42, cieľ ROC-AUC na validácii | rovnaký rozpočet = férové porovnanie |
| Ochrana proti preučeniu | regularizácia v priestore hyperparametrov (C; hĺbka a min. listy stromov; L1/L2, bagging pri LightGBM; dropout, weight decay pri MLP); early stopping na validácii (LightGBM 100 kôl, MLP 8 epoch, obnova najlepšej epochy); sledovaný rozdiel ROC-AUC train − validácia | výber podľa validácie, nie podľa tréningu |
| Variabilita | finálne modely s 3 seedmi (0, 1, 2); uvádza sa priemer ± smerodajná odchýlka | náhodnosť inicializácie a vzorkovania |
| Prahy | pevný 0,5 a prah s FPR ≤ 1 % určený na validácii | typický pracovný bod detekcie malvéru |
| Nízka prevalencia | precision a falošné poplachy na 1 skutočný pri prevalencii 1 % a 0,1 % – prepočet z TPR/FPR pri prahu z validácie (`metrics.at_prevalence`) | téza 2; v teste je 54 % malvéru |
| Metriky | ROC-AUC, PR-AUC, TPR pri FPR 0,1 % a 1 %, log loss, Brier; pri prahoch accuracy, balanced accuracy, precision, recall, FPR, F1, MCC, matica zámen; detekcia podľa rodiny | ROC-AUC a TPR@FPR nezávisia od pomeru tried, ktorý sa medzi train a test mení |
| Výpočtové nároky | latencia 1 vzorky (CPU, 1 vlákno; GPU pri MLP), priepustnosť (CPU 12 vlákien; GPU), čas tréningu, čas ladenia, počet parametrov/uzlov, veľkosť na disku; transformácia vstupu meraná zvlášť | ľahký vs. ťažký sa meria, nepredpokladá |

**Pozn. k optimizmu validácie:** validácia sa používa na ladenie aj early stopping, preto jej výsledky sú mierne
optimistické. Nestranný odhad poskytuje iba test. Navyše test je z neskoršieho obdobia (časový posun).

**Hardvér meraní:** 6 jadier / 12 vlákien CPU, 17 GB RAM, NVIDIA GeForce RTX 2060 (6 GB).
Merania počas iných záťaží (napr. sťahovania dát) môžu byť ovplyvnené – finálne merania času zopakovať na nezaťaženom systéme.

## Meranie spotreby výpočtových zdrojov pri inferencii (benchmark)
Oficiálne čísla pre vety typu „kaskáda spotrebuje menej výpočtového výkonu než hybridný model“.
Meria sa **iba inferencia** (nasadenie modelu), nie tréning. Rovnaký postup pre všetky prístupy vrátane kaskády:
celá cesta pôvodný vstup → transformácia → model → skóre na testovacej množine, model zo seedu 0.

| Scenár | Čo sa meria |
|---|---|
| CPU dávka (12 vlákien, opakovane ≥ 5 s) | priepustnosť, **CPU čas na vzorku**, priemerné vyťaženie CPU, nárast RAM |
| CPU jedna vzorka (1 vlákno, ≥ 5 s) | latencia (medián, p95), CPU čas na vzorku |
| GPU dávka / jedna vzorka (iba MLP a neskôr sekvenčné modely) | priepustnosť, latencia, vyťaženie GPU, pamäť GPU, **energia GPU nad nečinnosťou na 1000 vzoriek** (hardvérové počítadlo karty) |

- Hlavná miera náročnosti: **CPU čas na vzorku** (nezávisí od počtu vlákien) a pri GPU energia na 1000 vzoriek.
- Spotrebu energie CPU na Windows nemožno spoľahlivo zmerať – neuvádza sa.
- Ukladajú sa iba súhrnné hodnoty (`benchmark.json`, ~1–2 kB na model), nie časové rady.
- Spúšťať na nezaťaženom počítači; zaťaženie pred meraním sa zapisuje a pri prekročení 15 % sa výsledok označí ⚠.

Spustenie: `.venv\Scripts\python.exe -m src.evaluation.benchmark --approach static`,
potom `python -m src.evaluation.compare --approach static` (tabuľka v `runs/comparison/static/README.md`).

## Analýza využívania príznakov a kontrolné experimenty (NÁVRH)
Cieľ: overiť, či sa modely neopierajú o artefakty zberu dát namiesto skutočných vlastností malvéru.
Pôvod podozrenia (`processed/static/STATISTICS.md`): najsilnejšie samostatné príznaky na tréningu sú počet URL
v reťazcoch (ROC-AUC 0,88), veľkosť tabuľky certifikátov (0,83), digitálny podpis (0,82) a čas zostavenia (0,77);
čas zostavenia má zároveň najväčší posun train → test. Žiadny príznak sám nedosahuje ROC-AUC 0,9.

1. **Dôležitosť príznakov** (`src/evaluation/feature_importance.py`, iba validácia): pokles ROC-AUC po
   premiešaní celej skupiny príznakov a sledovaných príznakov; SHAP (LightGBM), koeficienty (LR).
2. **Kontrolný experiment** (`configs/static_ablations/`): lr, lightgbm a mlp_large bez 4 príznakov
   (podpis, 2× tabuľka certifikátov, čas zostavenia) s hyperparametrami prevzatými z pôvodného modelu.
   Ak kvalita výrazne klesne, model sa o tieto artefakty opiera – dôležité zistenie pre interpretáciu.

Spustenie po dokončení statických modelov:
`python -m src.evaluation.feature_importance --approach static` a `python -m src.training.run_ablations --dir static_ablations`.

## Výstupy
- jeden beh: `runs/<prístup>/<model>/<dátum-čas>/README.md` (metriky, časy, grafy), `metrics.json`, `timing.json`,
  `predictions/`, `hpo_trials.csv`,
- prehľad behov modelu: `runs/<prístup>/<model>/CLAUDE.md`,
- porovnanie modelov: `runs/comparison/<prístup>/README.md`.

Spustenie celej sady: `.venv\Scripts\python.exe -m src.training.run_suite --approach static`.
