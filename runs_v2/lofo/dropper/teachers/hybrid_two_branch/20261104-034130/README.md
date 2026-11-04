# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-04T03:41:31+01:00).

- Učiteľ: `runs_v2/lofo/dropper/hybrid/two_branch/20261104-022321` (`two_branch`, vstup `hybrid_seq`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99917**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.965
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 1888 s.
