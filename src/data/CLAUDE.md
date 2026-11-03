# src/data/ – príprava dát

Jediné miesto, ktoré číta surové dáta z `data/`. Ostatný kód pracuje s výstupmi v `processed/`.
Spúšťať z koreňa projektu cez `.venv\Scripts\python.exe -m src.data.<modul>`.

| Modul | Úloha | Stav |
|---|---|---|
| `ember_layout.py` | názvy a skupiny 2381 EMBER príznakov (rozloženie EMBER v2) | hotové |
| `ember_source.py` | čítanie pôvodných EMBER súborov s kontrolou integrity | hotové |
| `speakeasy_listing.py` | zoznam Speakeasy reportov podľa SHA-256 (zo zoznamu súborov HF) | hotové |
| `build_index.py` | spoločný index a rozdelenie → `processed/index` | hotové |
| `build_static.py` | statický dataset, štatistiky, grafy → `processed/static` | hotové |
| `static_dataset.py` | načítanie `processed/static` pre modely (`load_split`) | hotové |
| `static_transforms.py` | učené transformácie pre modely (`StaticPreprocessor`: konštantné stĺpce, signed log1p, štandardizácia) | hotové |
| `speakeasy_source.py` | nájdenie a robustné čítanie Speakeasy reportov, súhrn reportu | hotové (overené na teste) |
| `audit_dynamic.py` | audit dynamických dát → `processed/dynamic/audit` | pripravené, čaká na dáta |
| `build_dynamic.py` | normalizovaná cache reportov → `processed/dynamic/cache` | pripravené, čaká na dáta |
| `dynamic_features.py` | vektor z n-gramov API, udalostí a súhrnu (slovník iba z tréningu) | pripravené |
| `build_dynamic_tabular.py` | dynamický dataset pre rebríček → `processed/dynamic/tabular`; `--exclude-family` (V2) → `processed/dynamic/lofo/<rodina>/tabular` | hotové |
| `build_dynamic_sequence.py` | postupnosti ID tokenov API pre sekvenčné modely → `processed/dynamic/sequence` (slovník iba z tréningu); `--exclude-family` (V2) | hotové |
| `providers.py` | jednotné načítanie static / dynamic / hybrid / dynamic_seq / hybrid_seq (zarovnanie podľa SHA-256); zero-day (`DIZERTACKA_HOLDOUT_FAMILY`): rodina mimo train/validation, časť `holdout`, slovníky z `processed/dynamic/lofo/<rodina>` | hotové |

Konfigurácie: `configs/data/index.yaml`, `configs/data/static.yaml`, `configs/data/dynamic.yaml`.
Dynamické dáta: `docs/04_dynamicke_data.md` (formát, postup, poradie spustenia).

Overené úskalia (detaily v `docs/01_audit_dat.md`):
- V EMBER `features.npy` sa riadok vzorky určuje **indexom z prvého stĺpca `hashes.txt`**, nie poradím riadku.
  Riadky zlyhaných extrakcií sú v matici nulové.
- Speakeasy: SHA-256 je iba v názve súboru, v traine `sha.json`, v teste `sha.dat.json`;
  train `report_backdoor` a `report_clean` majú ďalšiu úroveň podpriečinkov.
- 446 SHA-256 je v traine aj teste (keylogger). Aktuálne vyradené z tréningu (NÁVRH, `configs/data/index.yaml`).
- Validácia: 10 % tréningu, stratifikovane podľa rodiny, identické vektory spolu (NÁVRH).
