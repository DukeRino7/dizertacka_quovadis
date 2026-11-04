# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-04T18:05:25+01:00).

- Učiteľ: `runs_v2/lofo/rat/dynamic/lightgbm/20261104-081647` (`lightgbm`, vstup `dynamic`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99672**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.834
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 146 s.
