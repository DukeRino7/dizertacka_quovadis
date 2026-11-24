# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-22T22:42:05+01:00).

- Učiteľ: `runs_v4/real_full/lofo/Locker_SLocker_Ransomware/hybrid/mlp_large/20261122-223631` (`mlp`, vstup `hybrid`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99540**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.805
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 58 s.
