# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-04T07:57:01+01:00).

- Učiteľ: `runs_v2/lofo/ransomware/hybrid/two_branch/20261104-063823` (`two_branch`, vstup `hybrid_seq`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99921**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.964
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 1820 s.
