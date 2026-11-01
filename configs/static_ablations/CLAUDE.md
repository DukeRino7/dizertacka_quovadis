# configs/static_ablations/ – kontrolné experimenty statických modelov

Rovnaký model ako v `configs/static/`, ale bez vybraných príznakov. Hyperparametre sa **preberajú**
z posledného behu pôvodného modelu (`params_from`) – nič sa znovu neladí, takže rozdiel vo výsledku
spôsobujú iba chýbajúce príznaky. Výsledky: `runs/static_ablations/<názov>/`, porovnanie
`runs/comparison/static_ablations/README.md`.

| Súbor | Vynechané príznaky | Účel |
|---|---|---|
| `lr_no_sig_ts.yaml`, `lightgbm_no_sig_ts.yaml`, `mlp_large_no_sig_ts.yaml` | podpis (3) + čas zostavenia (1) | spolieha sa model na artefakty zberu dát? |

Spustiť až po dokončení `runs/static/<model>`:
`.venv\Scripts\python.exe -m src.training.run_ablations --dir static_ablations`
