# Mäkké označenia učiteľa (out-of-fold)

> Generované `src/training/teacher_oof.py` (2026-11-23T21:21:52+01:00).

- Učiteľ: `runs_v4/emu_p/lofo/Airpush_StopSMS/hybrid/lightgbm/20261123-211909` (`lightgbm`, vstup `hybrid`), hyperparametre z jeho behu.
- 5 častí tréningu (StratifiedGroupKFold podľa rodiny, skupiny identických vektorov spolu, seed 0).
- ROC-AUC mäkkých označení voči skutočnosti (celý tréning, out-of-fold): **0.99619**
- Podiel istých predikcií (p < 0,01 alebo > 0,99): 0.913
- Súbor: `train_oof.parquet` (sha256, family, label, fold, p_teacher). Trvanie 66 s.
