# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-04T03:07:49+01:00).

- Učiteľ: `runs_v2/lofo/dropper/static/lightgbm/20261104-012654` (`lightgbm`, vstup `static`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99976**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.977
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 967 s.
