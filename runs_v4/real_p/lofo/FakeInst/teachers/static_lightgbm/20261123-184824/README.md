# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-23T18:48:24+01:00).

- Učiteľ: `runs_v4/real_p/lofo/FakeInst/static/lightgbm/20261123-184203` (`lightgbm`, vstup `static`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99368**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.893
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 41 s.
