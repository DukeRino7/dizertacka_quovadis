# src/models/hybrid/ – špecifické hybridné modely (vrstva B)

| Súbor | Model | Stav |
|---|---|---|
| `late_fusion.py` | neskorá fúzia skóre statického a dynamického modelu (priemer; stacking učený na validácii krížovo) | hotové, používa `src/cascade/evaluate.py` |
| (plánované) | dvojvetvová sieť: EMBER vetva + sekvenčná vetva nad API volaniami | pripravuje sa |

Hybridné modely spoločného rebríčka (ranná fúzia = spojený vektor) sú v `src/models/tabular/`, konfigurácie `configs/hybrid/`.
