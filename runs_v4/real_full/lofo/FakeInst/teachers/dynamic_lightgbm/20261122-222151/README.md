# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-22T22:21:51+01:00).

- Učiteľ: `runs_v4/real_full/lofo/FakeInst/dynamic/lightgbm/20261122-221211` (`lightgbm`, vstup `dynamic`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.98391**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.623
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 84 s.
