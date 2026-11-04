# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-04T05:19:13+01:00).

- Učiteľ: `runs_v2/lofo/keylogger/dynamic/lightgbm/20261104-040254` (`lightgbm`, vstup `dynamic`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99766**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.838
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 126 s.
