# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-04T04:58:14+01:00).

- Učiteľ: `runs_v2/lofo/keylogger/hybrid/lightgbm/20261104-043557` (`lightgbm`, vstup `hybrid`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99981**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.977
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 86 s.
