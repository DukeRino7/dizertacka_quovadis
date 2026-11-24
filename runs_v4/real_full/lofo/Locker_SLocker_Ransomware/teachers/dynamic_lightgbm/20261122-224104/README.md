# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-22T22:41:04+01:00).

- Učiteľ: `runs_v4/real_full/lofo/Locker_SLocker_Ransomware/dynamic/lightgbm/20261122-223201` (`lightgbm`, vstup `dynamic`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.98341**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.571
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 74 s.
