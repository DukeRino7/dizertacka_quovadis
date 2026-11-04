# configs/cascade/

Varianty kaskády. Kľúče: `name` (= priečinok v `runs/cascade/`), `components.static|dynamic|hybrid`:
`'<prístup>/<model>'` (posledný dokončený beh), `auto:<skupina>` (model vybraný pravidlom, `runs/selection/`) alebo cesta k behu.

| Súbor | Študenti / modely | Hybrid | Účel |
|---|---|---|---|
| `main.yaml` | `mlp_kd` (destilácia z hybridu) | `auto:hybrid` | **hlavný výsledok** (otázka 4) |
| `nokd.yaml` | `mlp_nokd` (bez destilácie) | `auto:hybrid` | prínos destilácie v kaskáde |
| `modal.yaml` | `mlp_kd_modal` (učiteľ rovnakej modality) | `auto:hybrid` | variant A |
| `heavy.yaml` | `mlp_kd` | `hybrid/two_branch` | kaskáda s najťažším hybridom (doplnková analýza) |
| `baselines.yaml` | `auto:static`, `auto:dynamic` | `auto:hybrid` | referencia bez študentov |

| `twobranch.yaml` | `mlp_kd_twobranch` (učiteľ dvojvetvová sieť, V2) | `auto:hybrid` | destilácia z komplexného učiteľa |

**Kaskády B (V2, docs/09)** – `type: B`, spúšťa `src.cascade.evaluate_b`; spoločné: pásmo neistoty `uncertainty`
(FPR ≤ 0,1 % / 1 % malvéru pod `lo`), rozpočty emulácie 10–40 %, predpoklad 60 s emulácie:
`b_main` (hlavný, téza 4), `b_direct` (neisté rovno na hybrid), `b_heavy` (dvojvetvová sieť), `b_baselines`
(LightGBM namiesto študentov), `b_nokd`, `b_twobranch`.

**V3 (docs/12)** – spúšťa `src.cascade.specialist`: statický LightGBM → rozpočet emulácie (hlavný 10 %) → „špecialista“
(LightGBM s hyperparametrami hybridného LightGBM, učený iba na `train_fraction` tréningu najbližšie prahu podľa OOF skóre):
`v3_spec` (hlavný: statické + dynamické + log-odds statického skóre), `v3_spec_dyn` (iba dynamické + skóre),
`v3_spec_f10`, `v3_spec_f40` (citlivosť na veľkosť tréningovej oblasti, nie výber).

Spustenie: `.venv\Scripts\python.exe -m src.cascade.evaluate --config configs/cascade/<variant>.yaml`.
