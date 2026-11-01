# src/models/hybrid/ – špecifické hybridné modely (vrstva B)

| Súbor | Model | Stav |
|---|---|---|
| `late_fusion.py` | neskorá fúzia skóre statického a dynamického modelu (priemer; stacking učený na validácii krížovo) | hotové, používa `src/cascade/evaluate.py` |
| `two_branch.py` | `two_branch` – statická MLP vetva + sekvenčná CNN vetva, spoločná hlava (kandidát na veľký model v kaskáde) | pripravené, overené na umelých dátach |

Hybridné modely spoločného rebríčka (ranná fúzia = spojený vektor) sú v `src/models/tabular/`, konfigurácie `configs/hybrid/`.
