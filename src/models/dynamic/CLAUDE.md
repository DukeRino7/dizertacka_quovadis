# src/models/dynamic/ – špecifické dynamické modely (vrstva B)

| Súbor | Model (`model:`) | Vstup | Stav |
|---|---|---|---|
| `sequence_cnn.py` | `seq_cnn` – embedding API + paralelné 1D konvolúcie + maximum cez postupnosť | `processed/dynamic/sequence` (ID tokenov, `approach: dynamic_seq`) | pripravené, overené na umelých dátach |

Dynamické modely spoločného rebríčka (n-gramy API) sú v `src/models/tabular/`, konfigurácie `configs/dynamic/`.
Neurónové modely vrstvy B dedia spoločný tréningový cyklus z `src/models/torch_base.py`.
