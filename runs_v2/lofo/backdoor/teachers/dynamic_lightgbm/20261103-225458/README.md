# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-03T22:54:58+01:00).

- Učiteľ: `runs_v2/lofo/backdoor/dynamic/lightgbm/20261103-212927` (`lightgbm`, vstup `dynamic`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99641**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.811
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 135 s.
