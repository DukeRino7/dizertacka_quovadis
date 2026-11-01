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
| dynamická časť | cache Speakeasy reportov | čaká na stiahnutie dát |

Konfigurácie: `configs/data/index.yaml`, `configs/data/static.yaml`.

Overené úskalia (detaily v `docs/01_audit_dat.md`):
- V EMBER `features.npy` sa riadok vzorky určuje **indexom z prvého stĺpca `hashes.txt`**, nie poradím riadku.
  Riadky zlyhaných extrakcií sú v matici nulové.
- Speakeasy: SHA-256 je iba v názve súboru, v traine `sha.json`, v teste `sha.dat.json`;
  train `report_backdoor` a `report_clean` majú ďalšiu úroveň podpriečinkov.
- 446 SHA-256 je v traine aj teste (keylogger). Aktuálne vyradené z tréningu (NÁVRH, `configs/data/index.yaml`).
- Validácia: 10 % tréningu, stratifikovane podľa rodiny, identické vektory spolu (NÁVRH).
