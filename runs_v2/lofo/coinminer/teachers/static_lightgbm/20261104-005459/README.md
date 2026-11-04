# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-04T00:54:59+01:00).

- Učiteľ: `runs_v2/lofo/coinminer/static/lightgbm/20261103-232852` (`lightgbm`, vstup `static`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99986**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.979
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 905 s.
