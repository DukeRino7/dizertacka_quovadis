# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-22T22:02:40+01:00).

- Učiteľ: `runs_v4/real_full/lofo/Boxer/hybrid/mlp_large/20261122-215648` (`mlp`, vstup `hybrid`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99510**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.797
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 67 s.
