# configs/cascade/

Varianty kaskády. Kľúče: `name` (= priečinok v `runs/cascade/`), `components.static|dynamic|hybrid`
(`'<prístup>/<model>'` = posledný dokončený beh v `runs/`, alebo cesta k behu).

| Súbor | Obsah | Stav |
|---|---|---|
| `example_baselines.yaml` | predbežná kaskáda z baseline modelov (kontrola postupu pred destiláciou) | čaká na dynamické a hybridné behy |

Spustenie: `.venv\Scripts\python.exe -m src.cascade.evaluate --config configs/cascade/<variant>.yaml`.
