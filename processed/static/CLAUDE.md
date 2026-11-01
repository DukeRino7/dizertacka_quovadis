# processed/static/ – predspracovaný statický dataset (EMBER)

- Súbory, použité techniky a obmedzenia: `README.md` (generovaný).
- Štatistiky datasetu a grafy: `STATISTICS.md`, `plots/`.
- Vytvára `src/data/build_static.py`, konfigurácia `configs/data/static.yaml`; vstup `processed/index`.
- Načítanie v kóde: `src.data.static_dataset.load_split("train" | "validation" | "test")`.
- Uložené sú pôvodné hodnoty príznakov; učené transformácie (`src/data/static_transforms.py`) sa robia až v experimente.
