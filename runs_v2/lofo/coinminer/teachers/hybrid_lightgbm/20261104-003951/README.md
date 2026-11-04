# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-04T00:39:51+01:00).

- Učiteľ: `runs_v2/lofo/coinminer/hybrid/lightgbm/20261104-001521` (`lightgbm`, vstup `hybrid`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99986**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.978
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 89 s.
