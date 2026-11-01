# src/models/tabular/ – spoločný rebríček modelov (vrstva A)

Modely nad pevným vektorom príznakov. Ten istý kód sa používa pre static, dynamic aj hybrid – líši sa iba vstup.
Opis sady a protokolu: `docs/03_protokol_a_modely.md`.

| Súbor | Trieda (`model:` v konfigurácii) | Transformácia vstupu | GPU |
|---|---|---|---|
| `logreg.py` | `LogReg` (`logreg`) | áno | nie |
| `random_forest.py` | `RandomForest` (`random_forest`) | nie | nie |
| `lightgbm_model.py` | `LightGBM` (`lightgbm`) | nie | nie |
| `mlp.py` | `MLP` (`mlp`) – malé aj veľké MLP, líšia sa priestorom hyperparametrov; s `soft_targets` + `kd_alpha`, `kd_temperature` aj študent destilácie | áno | áno |

Rozhranie (`base.py: TabularModel`): `fit(X, y, w, X_val, y_val)` (validácia iba na early stopping),
`predict_proba(X)` = P(malware), `n_parameters()`, `set_threads(n)`, `save(dir)` / `load(dir)`.
Nový model = nový súbor s triedou + zápis do `REGISTRY` v `__init__.py` + konfigurácia v `configs/<prístup>/`.
