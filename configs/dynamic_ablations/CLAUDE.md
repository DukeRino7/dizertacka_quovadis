# configs/dynamic_ablations/ – kontrolné experimenty dynamických modelov

Rovnaký model ako v `configs/dynamic/`, ale na kontrolnej reprezentácii `processed/dynamic/tabular_full`
(API n-gramy + udalosti + súhrnné počty). Hyperparametre sa preberajú z pôvodného behu (`params_from`).
Účel: zmerať vplyv artefaktu emulátora (test emulovaný inou verziou/nastavením Speakeasy – docs/04).
Hlavná reprezentácia (iba API volania) je rozhodnutie z princípu, nie podľa výsledkov tohto experimentu.

Spustenie: `.venv\Scripts\python.exe -m src.training.run_ablations --dir dynamic_ablations`
