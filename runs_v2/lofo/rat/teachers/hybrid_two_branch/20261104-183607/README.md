# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-04T18:36:07+01:00).

- Učiteľ: `runs_v2/lofo/rat/hybrid/two_branch/20261104-172337` (`two_branch`, vstup `hybrid_seq`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99902**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.958
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 1839 s.
