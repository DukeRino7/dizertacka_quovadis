# Súhrn V4 – KronoDroid

> Generované `src/evaluation/v4_report.py` (2026-11-24T18:56:40+01:00) z `runs_v4`. Plán a kritériá: `docs/19_plan_v4.md`. Hlavná miera O1/O2: TPR pri FPR 1 % z ROC krivky testu.

## 1. Hlavné otázky (docs/19, oddiel 4)
Rozdiel v p. b., 95 % interval z párového bootstrapu (2000 opakovaní). Kritérium O1/O2: rozdiel ≥ +1 p. b. a dolná hranica > 0.

| | čo | rozdiel (IS) | splnené |
|---|---|---|---|
| O1 | real_full, hlavné: hybrid − statický (TPR pri FPR 1 %) | +1.78 (+1.15 až +2.38) | **áno** |
| O1-Z | real_full, zero-day (priemer rodín): hybrid − statický | +11.38 (+9.70 až +13.00) | **áno** |
| D-norm (real_full) | hybrid s podielmi volaní − statický | +1.74 (+1.14 až +2.36) | **áno** |
| Δ real_p | real_p: hybrid − statický | +2.76 (+2.01 až +3.46) | – |
| Δ emu_p | emu_p: hybrid − statický | +2.00 (+1.32 až +2.63) | – |
| O2 | Δ real_p − Δ emu_p | +0.76 (+0.30 až +1.28) | nie |
| O2-Z | zero-day: Δ real_p − Δ emu_p | +9.60 (+8.33 až +10.82) | **áno** |
| D-norm (real_p) | hybrid s podielmi volaní − statický | +2.33 (+1.56 až +3.06) | **áno** |
| D-norm (emu_p) | hybrid s podielmi volaní − statický | +1.57 (+0.88 až +2.20) | **áno** |

**Interpretácia podľa docs/19, 4.3:** O1 platí, O2 nie → dynamika pomáha aj z emulátora; rozdiel oproti Quo Vadis je skôr vo vlastnostiach datasetu.

### Kaskády oproti statickému modelu (prahy z validácie; p. b., 95 % IS)
Všetky varianty, bez výberu podľa testu.

| vetva | kaskáda | ΔTPR vs. statický | ΔFPR vs. statický |
|---|---|---|---|
| real_full | kaskáda A-main | -0.63 (-1.13 až -0.15) | -0.32 (-0.48 až -0.15) |
| real_full | kaskáda A-nokd | -0.45 (-0.92 až +0.02) | -0.33 (-0.49 až -0.16) |
| real_full | kaskáda A-modal | -0.42 (-0.92 až +0.07) | -0.34 (-0.50 až -0.16) |
| real_full | kaskáda A-heavy | -0.99 (-1.48 až -0.50) | -0.32 (-0.49 až -0.15) |
| real_full | kaskáda A-baselines | +2.28 (+1.87 až +2.70) | -0.21 (-0.36 až -0.07) |
| real_full | kaskáda A-heavyteacher | -0.97 (-1.46 až -0.46) | -0.34 (-0.51 až -0.19) |
| real_full | kaskáda B-main | -0.90 (-1.39 až -0.44) | -0.33 (-0.49 až -0.16) |
| real_full | kaskáda B-direct | +2.32 (+1.90 až +2.74) | +0.06 (-0.13 až +0.25) |
| real_full | kaskáda B-heavy | -1.24 (-1.74 až -0.77) | -0.31 (-0.49 až -0.14) |
| real_full | kaskáda B-baselines | +1.97 (+1.60 až +2.37) | -0.20 (-0.35 až -0.05) |
| real_full | kaskáda B-nokd | -0.75 (-1.21 až -0.28) | -0.34 (-0.50 až -0.19) |
| real_full | kaskáda B-heavyteacher | -1.25 (-1.73 až -0.75) | -0.36 (-0.52 až -0.21) |
| real_full | kaskáda B-baselines (rozpočet 10 %) | +1.58 (+1.24 až +1.93) | -0.24 (-0.38 až -0.10) |
| real_full | špecialista V3 (B-spec, 10 %) | +2.80 (+2.46 až +3.17) | +0.33 (+0.17 až +0.49) |
| real_full | špecialista V3 (B-spec-dyn, 10 %) | +2.49 (+2.16 až +2.86) | +0.20 (+0.06 až +0.34) |
| real_p | kaskáda A-main | -2.38 (-3.10 až -1.72) | -0.62 (-0.81 až -0.43) |
| real_p | kaskáda A-nokd | -0.86 (-1.51 až -0.26) | -0.57 (-0.75 až -0.39) |
| real_p | kaskáda A-modal | -1.47 (-2.13 až -0.85) | -0.63 (-0.82 až -0.45) |
| real_p | kaskáda A-heavy | -2.97 (-3.70 až -2.30) | -0.57 (-0.76 až -0.39) |
| real_p | kaskáda A-baselines | +2.29 (+1.79 až +2.80) | -0.48 (-0.65 až -0.31) |
| real_p | kaskáda A-heavyteacher | -1.90 (-2.61 až -1.26) | -0.59 (-0.78 až -0.41) |
| real_p | kaskáda B-main | -2.57 (-3.27 až -1.92) | -0.61 (-0.80 až -0.42) |
| real_p | kaskáda B-direct | +2.39 (+1.85 až +2.92) | -0.21 (-0.42 až +0.02) |
| real_p | kaskáda B-heavy | -3.14 (-3.85 až -2.47) | -0.58 (-0.77 až -0.40) |
| real_p | kaskáda B-baselines | +2.22 (+1.75 až +2.68) | -0.47 (-0.65 až -0.30) |
| real_p | kaskáda B-nokd | -1.00 (-1.63 až -0.39) | -0.54 (-0.72 až -0.37) |
| real_p | kaskáda B-heavyteacher | -2.06 (-2.77 až -1.42) | -0.58 (-0.77 až -0.40) |
| real_p | kaskáda B-baselines (rozpočet 10 %) | +1.59 (+1.15 až +2.03) | -0.51 (-0.68 až -0.34) |
| real_p | špecialista V3 (B-spec, 10 %) | +2.56 (+2.17 až +2.97) | +0.02 (-0.12 až +0.19) |
| real_p | špecialista V3 (B-spec-dyn, 10 %) | +2.52 (+2.14 až +2.94) | +0.11 (-0.02 až +0.26) |
| emu_p | kaskáda A-main | -5.23 (-5.86 až -4.58) | -0.55 (-0.74 až -0.37) |
| emu_p | kaskáda A-nokd | -3.74 (-4.34 až -3.14) | -0.54 (-0.73 až -0.37) |
| emu_p | kaskáda A-modal | -4.12 (-4.74 až -3.49) | -0.57 (-0.76 až -0.39) |
| emu_p | kaskáda A-heavy | -5.75 (-6.43 až -5.06) | -0.54 (-0.73 až -0.35) |
| emu_p | kaskáda A-baselines | +1.23 (+0.85 až +1.63) | -0.44 (-0.61 až -0.29) |
| emu_p | kaskáda A-heavyteacher | -5.11 (-5.77 až -4.47) | -0.57 (-0.76 až -0.39) |
| emu_p | kaskáda B-main | -5.31 (-5.94 až -4.67) | -0.54 (-0.73 až -0.36) |
| emu_p | kaskáda B-direct | +1.72 (+1.26 až +2.18) | -0.20 (-0.39 až -0.01) |
| emu_p | kaskáda B-heavy | -5.79 (-6.46 až -5.12) | -0.54 (-0.74 až -0.36) |
| emu_p | kaskáda B-baselines | +1.15 (+0.76 až +1.54) | -0.44 (-0.61 až -0.29) |
| emu_p | kaskáda B-nokd | -3.75 (-4.35 až -3.16) | -0.52 (-0.70 až -0.34) |
| emu_p | kaskáda B-heavyteacher | -5.17 (-5.83 až -4.52) | -0.56 (-0.74 až -0.38) |
| emu_p | kaskáda B-baselines (rozpočet 10 %) | +0.78 (+0.43 až +1.15) | -0.46 (-0.63 až -0.31) |
| emu_p | špecialista V3 (B-spec, 10 %) | +1.72 (+1.38 až +2.05) | -0.04 (-0.16 až +0.09) |
| emu_p | špecialista V3 (B-spec-dyn, 10 %) | +1.23 (+0.93 až +1.54) | -0.01 (-0.13 až +0.12) |

## 2. Modely na hlavnom rozdelení (priemer cez seedy)
Vybrané modely: real_full: static=static/lightgbm, dynamic=dynamic/lightgbm, hybrid=hybrid/lightgbm; real_p: static=static/lightgbm, dynamic=dynamic/lightgbm, hybrid=hybrid/lightgbm; emu_p: static=static/lightgbm, dynamic=dynamic/lightgbm, hybrid=hybrid/lightgbm

| vetva | model | ROC-AUC | TPR pri FPR 1 % (test) | TPR (prah z val.) | FPR (prah z val.) |
|---|---|---|---|---|---|
| real_full | statický (vybraný) | 0.9958 | 0.9603 | 0.9459 | 0.0062 |
| real_full | dynamický (vybraný) | 0.9857 | 0.8730 | 0.8688 | 0.0090 |
| real_full | hybrid (vybraný) | 0.9983 | 0.9781 | 0.9724 | 0.0076 |
| real_full | hybrid mlp_large (komplexný) | 0.9962 | 0.9663 | 0.9603 | 0.0072 |
| real_full | dynamic_norm | 0.9838 | 0.8624 | 0.8490 | 0.0071 |
| real_full | hybrid_norm | 0.9980 | 0.9777 | 0.9701 | 0.0068 |
| real_full | statický ALEBO dynamický (horná hranica) | – | – | 0.9820 | 0.0149 |
| real_p | statický (vybraný) | 0.9951 | 0.9507 | 0.9444 | 0.0080 |
| real_p | dynamický (vybraný) | 0.9824 | 0.8586 | 0.8455 | 0.0074 |
| real_p | hybrid (vybraný) | 0.9982 | 0.9783 | 0.9709 | 0.0062 |
| real_p | hybrid mlp_large (komplexný) | 0.9959 | 0.9555 | 0.9490 | 0.0078 |
| real_p | dynamic_norm | 0.9799 | 0.8392 | 0.8250 | 0.0071 |
| real_p | hybrid_norm | 0.9978 | 0.9740 | 0.9668 | 0.0062 |
| real_p | statický ALEBO dynamický (horná hranica) | – | – | 0.9812 | 0.0149 |
| emu_p | statický (vybraný) | 0.9951 | 0.9507 | 0.9444 | 0.0080 |
| emu_p | dynamický (vybraný) | 0.9780 | 0.8488 | 0.8381 | 0.0080 |
| emu_p | hybrid (vybraný) | 0.9969 | 0.9707 | 0.9632 | 0.0060 |
| emu_p | hybrid mlp_large (komplexný) | 0.9942 | 0.9566 | 0.9445 | 0.0063 |
| emu_p | dynamic_norm | 0.9752 | 0.8227 | 0.8111 | 0.0082 |
| emu_p | hybrid_norm | 0.9967 | 0.9664 | 0.9586 | 0.0061 |
| emu_p | statický ALEBO dynamický (horná hranica) | – | – | 0.9685 | 0.0155 |

## 3. Zero-day: TPR vynechanej rodiny pri FPR 1 % (ROC testu; rodina = test + holdout)
| vetva | rodina | n | statický (vybraný) | dynamický (vybraný) | hybrid (vybraný) |
|---|---|---|---|---|---|
| real_full | Airpush/StopSMS | 7775 | 0.5570 | 0.8582 | 0.8974 |
| real_full | Boxer | 3597 | 0.8973 | 0.4950 | 0.9486 |
| real_full | FakeInst | 2384 | 0.8428 | 0.6018 | 0.9471 |
| real_full | Locker/SLocker Ransomware | 1846 | 0.3891 | 0.4996 | 0.4559 |
| real_full | BankBot | 1297 | 0.9884 | 0.8186 | 0.9946 |
| real_full | **priemer** |  | 0.7350 | 0.6546 | 0.8487 |
| real_p | Airpush/StopSMS | 6507 | 0.5510 | 0.8448 | 0.8841 |
| real_p | Boxer | 3538 | 0.9458 | 0.5793 | 0.9497 |
| real_p | FakeInst | 2121 | 0.8466 | 0.6142 | 0.9591 |
| real_p | Locker/SLocker Ransomware | 1697 | 0.3815 | 0.5070 | 0.6321 |
| real_p | BankBot | 1230 | 0.9854 | 0.8201 | 0.9938 |
| real_p | **priemer** |  | 0.7421 | 0.6731 | 0.8838 |
| emu_p | Airpush/StopSMS | 6507 | 0.5510 | 0.5795 | 0.6711 |
| emu_p | Boxer | 3538 | 0.9458 | 0.3857 | 0.9474 |
| emu_p | FakeInst | 2121 | 0.8466 | 0.3725 | 0.9173 |
| emu_p | Locker/SLocker Ransomware | 1697 | 0.3815 | 0.2108 | 0.4115 |
| emu_p | BankBot | 1230 | 0.9854 | 0.8550 | 0.9913 |
| emu_p | **priemer** |  | 0.7421 | 0.4807 | 0.7877 |

## 4. Tézy 1, 2, 4 – vetva real_full (prahy z validácie, kritériá docs/09)
Referencie: statický TPR/FPR 0.9459 / 0.0062, dynamický 0.8688 / 0.0090. „dyn. analýza“ = podiel testovacích súborov s dynamickou analýzou (kaskády A = 100 %).

| kaskáda | TPR | FPR | téza 2 (hlavné) | dyn. analýza | TPR rodiny (zero-day) | téza 1 | téza 2 (zero-day) |
|---|---|---|---|---|---|---|---|
| kaskáda A-main | 0.9397 | 0.0030 | **áno** | – | 0.7619 | **áno** | **áno** |
| kaskáda A-nokd | 0.9415 | 0.0029 | **áno** | – | 0.7554 | **áno** | **áno** |
| kaskáda A-modal | 0.9417 | 0.0028 | **áno** | – | 0.7209 | **áno** | **áno** |
| kaskáda A-heavy | 0.9361 | 0.0030 | **áno** | – | 0.7871 | **áno** | **áno** |
| kaskáda A-baselines | 0.9687 | 0.0040 | **áno** | – | 0.7902 | **áno** | **áno** |
| kaskáda A-heavyteacher | 0.9362 | 0.0027 | **áno** | – | 0.7500 | **áno** | **áno** |
| kaskáda B-main | 0.9369 | 0.0029 | **áno** | 0.3831 | 0.7439 | **áno** | **áno** |
| kaskáda B-direct | 0.9692 | 0.0068 | nie | 0.3831 | 0.8174 | nie | nie |
| kaskáda B-heavy | 0.9335 | 0.0030 | nie | 0.3831 | 0.7571 | **áno** | **áno** |
| kaskáda B-baselines | 0.9656 | 0.0042 | **áno** | 0.1661 | 0.7723 | **áno** | **áno** |
| kaskáda B-nokd | 0.9385 | 0.0028 | **áno** | 0.4583 | 0.7379 | **áno** | **áno** |
| kaskáda B-heavyteacher | 0.9335 | 0.0025 | nie | 0.4750 | 0.7342 | **áno** | **áno** |
| kaskáda B-baselines (rozpočet 10 %) | 0.9617 | 0.0038 | **áno** | 0.1031 | 0.7574 | **áno** | **áno** |
| špecialista V3 (B-spec, 10 %) | 0.9740 | 0.0094 | nie | 0.1031 | 0.8132 | nie | nie |
| špecialista V3 (B-spec-dyn, 10 %) | 0.9709 | 0.0082 | nie | 0.1031 | 0.8065 | nie | nie |

## 4. Tézy 1, 2, 4 – vetva real_p (prahy z validácie, kritériá docs/09)
Referencie: statický TPR/FPR 0.9444 / 0.0080, dynamický 0.8455 / 0.0074. „dyn. analýza“ = podiel testovacích súborov s dynamickou analýzou (kaskády A = 100 %).

| kaskáda | TPR | FPR | téza 2 (hlavné) | dyn. analýza | TPR rodiny (zero-day) | téza 1 | téza 2 (zero-day) |
|---|---|---|---|---|---|---|---|
| kaskáda A-main | 0.9206 | 0.0018 | nie | – | 0.7140 | nie | **áno** |
| kaskáda A-nokd | 0.9357 | 0.0023 | **áno** | – | 0.7807 | **áno** | **áno** |
| kaskáda A-modal | 0.9296 | 0.0017 | nie | – | 0.7811 | **áno** | **áno** |
| kaskáda A-heavy | 0.9146 | 0.0023 | nie | – | 0.7371 | **áno** | **áno** |
| kaskáda A-baselines | 0.9673 | 0.0032 | **áno** | – | 0.8330 | **áno** | **áno** |
| kaskáda A-heavyteacher | 0.9253 | 0.0021 | nie | – | 0.7927 | **áno** | **áno** |
| kaskáda B-main | 0.9186 | 0.0019 | nie | 0.3867 | 0.6875 | nie | nie |
| kaskáda B-direct | 0.9682 | 0.0060 | **áno** | 0.3867 | 0.8293 | **áno** | **áno** |
| kaskáda B-heavy | 0.9130 | 0.0022 | nie | 0.3867 | 0.6928 | nie | nie |
| kaskáda B-baselines | 0.9665 | 0.0033 | **áno** | 0.1462 | 0.8040 | **áno** | **áno** |
| kaskáda B-nokd | 0.9344 | 0.0026 | **áno** | 0.3369 | 0.7505 | **áno** | **áno** |
| kaskáda B-heavyteacher | 0.9237 | 0.0022 | nie | 0.4014 | 0.7623 | **áno** | **áno** |
| kaskáda B-baselines (rozpočet 10 %) | 0.9603 | 0.0030 | **áno** | 0.1064 | 0.7848 | **áno** | **áno** |
| špecialista V3 (B-spec, 10 %) | 0.9700 | 0.0083 | nie | 0.1064 | 0.8091 | nie | nie |
| špecialista V3 (B-spec-dyn, 10 %) | 0.9696 | 0.0092 | nie | 0.1064 | 0.8047 | nie | nie |

## 4. Tézy 1, 2, 4 – vetva emu_p (prahy z validácie, kritériá docs/09)
Referencie: statický TPR/FPR 0.9444 / 0.0080, dynamický 0.8381 / 0.0080. „dyn. analýza“ = podiel testovacích súborov s dynamickou analýzou (kaskády A = 100 %).

| kaskáda | TPR | FPR | téza 2 (hlavné) | dyn. analýza | TPR rodiny (zero-day) | téza 1 | téza 2 (zero-day) |
|---|---|---|---|---|---|---|---|
| kaskáda A-main | 0.8921 | 0.0025 | nie | – | 0.6673 | nie | nie |
| kaskáda A-nokd | 0.9070 | 0.0026 | nie | – | 0.6996 | nie | nie |
| kaskáda A-modal | 0.9031 | 0.0023 | nie | – | 0.6776 | nie | nie |
| kaskáda A-heavy | 0.8869 | 0.0026 | nie | – | 0.6615 | nie | nie |
| kaskáda A-baselines | 0.9567 | 0.0036 | **áno** | – | 0.7290 | **áno** | **áno** |
| kaskáda A-heavyteacher | 0.8932 | 0.0023 | nie | – | 0.6787 | nie | nie |
| kaskáda B-main | 0.8913 | 0.0026 | nie | 0.3653 | 0.6676 | nie | nie |
| kaskáda B-direct | 0.9616 | 0.0060 | **áno** | 0.3653 | 0.7643 | **áno** | **áno** |
| kaskáda B-heavy | 0.8864 | 0.0026 | nie | 0.3653 | 0.6624 | nie | nie |
| kaskáda B-baselines | 0.9559 | 0.0036 | **áno** | 0.1462 | 0.7288 | **áno** | **áno** |
| kaskáda B-nokd | 0.9068 | 0.0029 | nie | 0.3369 | 0.6998 | nie | nie |
| kaskáda B-heavyteacher | 0.8926 | 0.0024 | nie | 0.5301 | 0.6786 | nie | nie |
| kaskáda B-baselines (rozpočet 10 %) | 0.9522 | 0.0034 | **áno** | 0.1064 | 0.7265 | **áno** | **áno** |
| špecialista V3 (B-spec, 10 %) | 0.9615 | 0.0076 | **áno** | 0.1064 | 0.7525 | nie | nie |
| špecialista V3 (B-spec-dyn, 10 %) | 0.9567 | 0.0079 | **áno** | 0.1064 | 0.7332 | nie | nie |

## 5. Téza 3 – študent vs. komplexný hybrid (mlp_large)
Kritérium: TPR nie horšie o viac ako 1 p. b. (hlavné aj zero-day) pri nižšom CPU čase na vzorku.

| vetva | študent | ΔTPR vs. mlp_large hybrid (hlavné) | ΔTPR rodiny (zero-day) | CPU ms/vz. študent | CPU ms/vz. mlp_large | téza 3 |
|---|---|---|---|---|---|---|
| real_full | statický študent mlp_kd | -0.0769 | -0.2546 | 0.0476 | 0.1148 | nie |
| real_full | dynamický študent mlp_kd | -0.2111 | -0.3133 | 0.0353 | 0.1148 | nie |
| real_full | statický študent mlp_kd_heavy | -0.0882 | -0.2607 | 0.0481 | 0.1148 | nie |
| real_full | dynamický študent mlp_kd_heavy | -0.2096 | -0.3422 | 0.0354 | 0.1148 | nie |
| real_p | statický študent mlp_kd | -0.1118 | -0.3180 | 0.0352 | 0.2411 | nie |
| real_p | dynamický študent mlp_kd | -0.2247 | -0.3254 | 0.0323 | 0.2411 | nie |
| real_p | statický študent mlp_kd_heavy | -0.0992 | -0.2055 | 0.0352 | 0.2411 | nie |
| real_p | dynamický študent mlp_kd_heavy | -0.2137 | -0.3182 | 0.0316 | 0.2411 | nie |
| emu_p | statický študent mlp_kd | -0.0901 | -0.1952 | 0.0313 | 0.1076 | nie |
| emu_p | dynamický študent mlp_kd | -0.3424 | -0.2960 | 0.0332 | 0.1076 | nie |
| emu_p | statický študent mlp_kd_heavy | -0.0998 | -0.1481 | 0.0324 | 0.1076 | nie |
| emu_p | dynamický študent mlp_kd_heavy | -0.3382 | -0.2980 | 0.0331 | 0.1076 | nie |

## 6. Špecialista V3 – kritériá B1–B3 (docs/19, 3.4)
| vetva | TPR rodiny špecialista | TPR rodiny statický | rodiny spec ≥ stat | B1 | B2 (hlavné) | B3 |
|---|---|---|---|---|---|---|
| real_full | 0.8132 | 0.6781 | 5 z 5 | nie | nie | nie |
| real_p | 0.8091 | 0.7110 | 5 z 5 | nie | nie | nie |
| emu_p | 0.7525 | 0.7110 | 5 z 5 | nie | **áno** | nie |

## 8. Výpočtové nároky – vetva real_full (benchmark, model zo seedu 0; čas dynamickej analýzy dataset neuvádza)
| model | CPU ms/vz. dávka | CPU ms/vz. 1 vz. | latencia ms (medián) | GPU J/1000 vz. | parametre/uzly | disk MB | tréning s (seed) | ladenie s |
|---|---|---|---|---|---|---|---|---|
| statický (static/lightgbm) | 0.2054 | 0.1454 | 0.1441 | – | 498553 | 27.6185 | 13.4053 | 725.0905 |
| dynamický (dynamic/lightgbm) | 0.2410 | 0.1497 | 0.1595 | – | 434868 | 23.8853 | 17.2084 | 713.0060 |
| hybrid (hybrid/lightgbm) | 0.1787 | 0.1223 | 0.1271 | – | 357120 | 19.8839 | 19.0675 | 949.4200 |
| hybrid komplexný (hybrid/mlp_large) | 0.1148 | 0.2782 | 0.1574 | 0.0000 | 317697 | 1.2931 | 13.6639 | 278.8118 |
| statický študent mlp_kd (students_static/mlp_kd) | 0.0476 | 0.1442 | 0.0799 | 0.0024 | 10753 | 0.0522 | 5.2045 | 243.4654 |
| dynamický študent mlp_kd (students_dynamic/mlp_kd) | 0.0353 | 0.1408 | 0.0790 | 0.0018 | 8641 | 0.0430 | 13.1504 | 333.7458 |
| statický študent mlp_kd_heavy (students_static/mlp_kd_heavy) | 0.0481 | 0.1470 | 0.0793 | 0.0038 | 10753 | 0.0522 | 4.8183 | 226.3350 |
| dynamický študent mlp_kd_heavy (students_dynamic/mlp_kd_heavy) | 0.0354 | 0.1439 | 0.0779 | 0.0028 | 8641 | 0.0430 | 24.3845 | 448.6045 |

Odhad CPU času kaskád (dávka) zo súčtu komponentov a podielov na teste:

| kaskáda | podiel dyn. analýzy | podiel na hybrid | CPU ms/vz. (odhad) | hybrid na každej vzorke | statický samostatne |
|---|---|---|---|---|---|
| kaskáda A-main | 1.0000 | 0.1456 | 0.1089 | 0.1787 | 0.2054 |
| kaskáda A-baselines | 1.0000 | 0.0860 | 0.4617 | 0.1787 | 0.2054 |
| kaskáda A-heavy | 1.0000 | 0.1456 | 0.0996 | 0.1148 | 0.2054 |
| kaskáda B-main | 0.3831 | 0.0988 | 0.0788 | 0.1787 | 0.2054 |
| kaskáda B-baselines | 0.1661 | 0.0408 | 0.2527 | 0.1787 | 0.2054 |
| kaskáda B-baselines (rozpočet 10 %) | 0.1031 | 0.0335 | 0.2362 | 0.1787 | 0.2054 |
| kaskáda B-heavy | 0.3831 | 0.0988 | 0.0725 | 0.1148 | 0.2054 |

## 8. Výpočtové nároky – vetva real_p (benchmark, model zo seedu 0; čas dynamickej analýzy dataset neuvádza)
| model | CPU ms/vz. dávka | CPU ms/vz. 1 vz. | latencia ms (medián) | GPU J/1000 vz. | parametre/uzly | disk MB | tréning s (seed) | ladenie s |
|---|---|---|---|---|---|---|---|---|
| statický (static/lightgbm) | 0.2006 | 0.1489 | 0.1485 | – | 397091 | 22.3268 | 9.1547 | 481.0856 |
| dynamický (dynamic/lightgbm) | 0.1169 | 0.0932 | 0.0974 | – | 183222 | 10.0430 | 10.6493 | 477.0593 |
| hybrid (hybrid/lightgbm) | 0.0575 | 0.0496 | 0.0496 | – | 71318 | 4.0633 | 5.5146 | 339.9581 |
| hybrid komplexný (hybrid/mlp_large) | 0.2411 | 0.5125 | 0.2809 | 0.0000 | 2400257 | 9.6405 | 6.8366 | 186.2519 |
| statický študent mlp_kd (students_static/mlp_kd) | 0.0352 | 0.1375 | 0.0764 | 0.0017 | 10689 | 0.0519 | 4.7361 | 201.6353 |
| dynamický študent mlp_kd (students_dynamic/mlp_kd) | 0.0323 | 0.1310 | 0.0762 | 0.0021 | 8129 | 0.0408 | 6.9665 | 246.7174 |
| statický študent mlp_kd_heavy (students_static/mlp_kd_heavy) | 0.0352 | 0.1401 | 0.0754 | 0.0045 | 10689 | 0.0519 | 4.0328 | 177.1106 |
| dynamický študent mlp_kd_heavy (students_dynamic/mlp_kd_heavy) | 0.0316 | 0.1400 | 0.0754 | 0.0028 | 8129 | 0.0408 | 7.2596 | 261.5918 |

Odhad CPU času kaskád (dávka) zo súčtu komponentov a podielov na teste:

| kaskáda | podiel dyn. analýzy | podiel na hybrid | CPU ms/vz. (odhad) | hybrid na každej vzorke | statický samostatne |
|---|---|---|---|---|---|
| kaskáda A-main | 1.0000 | 0.1392 | 0.0754 | 0.0575 | 0.2006 |
| kaskáda A-baselines | 1.0000 | 0.0853 | 0.3224 | 0.0575 | 0.2006 |
| kaskáda A-heavy | 1.0000 | 0.1392 | 0.1010 | 0.2411 | 0.2006 |
| kaskáda B-main | 0.3867 | 0.0899 | 0.0528 | 0.0575 | 0.2006 |
| kaskáda B-baselines | 0.1462 | 0.0331 | 0.2196 | 0.0575 | 0.2006 |
| kaskáda B-baselines (rozpočet 10 %) | 0.1064 | 0.0347 | 0.2150 | 0.0575 | 0.2006 |
| kaskáda B-heavy | 0.3867 | 0.0899 | 0.0693 | 0.2411 | 0.2006 |

## 8. Výpočtové nároky – vetva emu_p (benchmark, model zo seedu 0; čas dynamickej analýzy dataset neuvádza)
| model | CPU ms/vz. dávka | CPU ms/vz. 1 vz. | latencia ms (medián) | GPU J/1000 vz. | parametre/uzly | disk MB | tréning s (seed) | ladenie s |
|---|---|---|---|---|---|---|---|---|
| statický (static/lightgbm) | 0.2006 | 0.1489 | 0.1485 | – | 397091 | 22.3268 | 9.1547 | 481.0856 |
| dynamický (dynamic/lightgbm) | 0.6350 | 0.3773 | 0.3764 | – | 972512 | 54.1034 | 27.7181 | 1081.3775 |
| hybrid (hybrid/lightgbm) | 0.2267 | 0.1510 | 0.1519 | – | 396683 | 22.2914 | 18.3220 | 660.7839 |
| hybrid komplexný (hybrid/mlp_large) | 0.1076 | 0.3154 | 0.1790 | 0.0444 | 323521 | 1.3203 | 9.6666 | 219.3261 |
| statický študent mlp_kd (students_static/mlp_kd) | 0.0313 | 0.1131 | 0.0624 | 0.0135 | 10689 | 0.0519 | 4.2700 | 208.5373 |
| dynamický študent mlp_kd (students_dynamic/mlp_kd) | 0.0332 | 0.1138 | 0.0632 | 0.0122 | 8129 | 0.0408 | 7.5808 | 322.7940 |
| statický študent mlp_kd_heavy (students_static/mlp_kd_heavy) | 0.0324 | 0.1083 | 0.0615 | 0.0032 | 10689 | 0.0519 | 4.0938 | 176.4629 |
| dynamický študent mlp_kd_heavy (students_dynamic/mlp_kd_heavy) | 0.0331 | 0.1134 | 0.0618 | 0.0033 | 8129 | 0.0408 | 6.3591 | 262.2813 |

Odhad CPU času kaskád (dávka) zo súčtu komponentov a podielov na teste:

| kaskáda | podiel dyn. analýzy | podiel na hybrid | CPU ms/vz. (odhad) | hybrid na každej vzorke | statický samostatne |
|---|---|---|---|---|---|
| kaskáda A-main | 1.0000 | 0.1596 | 0.1006 | 0.2267 | 0.2006 |
| kaskáda A-baselines | 1.0000 | 0.0775 | 0.8532 | 0.2267 | 0.2006 |
| kaskáda A-heavy | 1.0000 | 0.1596 | 0.0816 | 0.1076 | 0.2006 |
| kaskáda B-main | 0.3653 | 0.0933 | 0.0646 | 0.2267 | 0.2006 |
| kaskáda B-baselines | 0.1462 | 0.0304 | 0.3004 | 0.2267 | 0.2006 |
| kaskáda B-baselines (rozpočet 10 %) | 0.1064 | 0.0322 | 0.2755 | 0.2267 | 0.2006 |
| kaskáda B-heavy | 0.3653 | 0.0933 | 0.0535 | 0.1076 | 0.2006 |

## 7. Doplnkovo: časový posun malvéru (real_time, test = malvér 2015–2020)
| model | TPR pri FPR 1 % (test) | ROC-AUC |
|---|---|---|
| statický (vybraný) | 0.8456 | 0.9788 |
| dynamický (vybraný) | 0.6467 | 0.9637 |
| hybrid (vybraný) | 0.8996 | 0.9861 |

hybrid − statický: +5.40 (+3.98 až +7.20)
