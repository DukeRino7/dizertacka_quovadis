# processed/static/ – predspracovaný statický dataset (EMBER)

> Generované skriptom `src/data/build_static.py` (2026-11-01T13:40:06+01:00), konfigurácia `configs/data/static.yaml`.
> Neupravovať ručne. Znovuvytvorenie: `.venv\Scripts\python.exe -m src.data.build_static`.
> Štatistiky datasetu: [STATISTICS.md](STATISTICS.md).

## Súbory
| Súbor | Obsah |
|---|---|
| `X_<časť>.npy` | float32 [n, 2381], pôvodné EMBER hodnoty, časti `train`, `validation`, `test` |
| `y_<časť>.npy` | int8, 0 = benign, 1 = malware |
| `meta_<časť>.parquet` | `sha256`, `family`, `label`, `feature_group` – riadok i patrí k riadku i v X |
| `feature_names.csv` | `column`, `group`, `name` pre všetkých 2381 príznakov |
| `train_feature_stats.parquet` | štatistiky každého príznaku na tréningu (min, max, priemer, smer. odchýlka, kvantily, podiel nenulových, počet unikátnych hodnôt) |
| `drift_ks.parquet` | KS štatistika train–validácia a train–test pre každý príznak (iba popisné) |
| `plots/` | grafy k STATISTICS.md |
| `manifest.json` | konfigurácia, commit, prostredie, kontrolné súčty, časy spracovania |

Načítanie v kóde: `from src.data.static_dataset import load_split` → `load_split("train")` vráti `X`, `y`, `meta`
(X ako memory-map, nenačíta sa celé do RAM).

## Použité techniky spracovania
1. **Spoločný index a rozdelenie** (`processed/index`): jedna vzorka = jeden SHA-256; validácia vyčlenená
   z pôvodného tréningu stratifikovane podľa rodiny a so skupinami identických vektorov držanými spolu
   (`StratifiedGroupKFold`, seed 42); pôvodný časový test bez zmeny; odstránený prekryv
   train/test podľa SHA-256 (detaily a NÁVRHY v `processed/index/README.md`).
2. **Správne mapovanie riadkov**: riadok v pôvodnom `features.npy` sa určuje indexom z `hashes.txt`;
   nulové riadky zlyhaných extrakcií sa vynechávajú. Integrita overená pri čítaní (pozri `src/data/ember_source.py`).
3. **Kontrola hodnôt**: NaN a ±Inf (žiadne neboli nájdené – pozri STATISTICS.md), zhoda s pôvodnými dátami na náhodnej vzorke.
4. **Materializácia po častiach**: samostatné súbory pre train/validáciu/test → modely nikdy omylom
   nevidia test pri tréningu; formát `.npy` umožňuje rýchle načítanie cez memory-map.
5. **Popis príznakov**: názvy a skupiny podľa rozloženia EMBER v2 (`src/data/ember_layout.py`).
6. **Štatistiky iba z tréningu**: konštantné a takmer konštantné príznaky, rozsahy, ťažké chvosty, riedkosť.
7. **Popisná analýza posunu** train → test (KS), referenčne train → validácia.
8. **Pôvod a reprodukovateľnosť**: `manifest.json` (konfigurácia, git commit, verzie knižníc,
   SHA-256 vstupov aj výstupov, čas spracovania).

## Čo sa zámerne NErobí na uloženom datasete
- **Žiadna škálovanie, log-transformácia ani výber príznakov.** Sú to učené transformácie; robia sa až
  v experimente, fitované iba na tréningu (`src/data/static_transforms.py: StaticPreprocessor`)
  a ukladajú sa s modelom v `runs/`. Stromové modely ich nepotrebujú. Uložené dáta tak zostávajú
  neutrálne pre všetky modely.
- **Žiadne odstránenie konštantných príznakov** – informácia je v `train_feature_stats.parquet`;
  rozhodnutie patrí modelu/experimentu, aby všetky modely mali rovnaký vstup 2381 príznakov.
- **Žiadne vyvažovanie tried** (oversampling/undersampling) – prípadné váhy tried sa nastavujú v experimente.
- **Žiadne úpravy testu** – test sa nepoužíva na ladenie.

## Obmedzenia
- EMBER príznaky boli extrahované autormi datasetu; pôvodné PE súbory nie sú k dispozícii, preto
  **čas extrakcie statických príznakov sa nedá v tomto projekte zmerať** priamo z dát.
- 366 súborov z pôvodného datasetu nemá EMBER príznaky (zlyhaná extrakcia) – nie sú v indexe.
