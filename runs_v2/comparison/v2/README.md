# V2 – zero-day a kaskáda B: súhrn a vyhodnotenie téz

> Generované `src/evaluation/v2_report.py` (2026-11-04T20:47:50+01:00). Plán a kritériá (určené vopred): `docs/09_plan_v2.md`.
> Prahy z validácie (FPR ≤ 1 %), priemer cez seedy. Zero-day: v každom behu je jedna rodina vynechaná z tréningu aj
> validácie; hodnoty sú priemer (± sm. odchýlka) cez 7 rodín: backdoor, coinminer, dropper, keylogger, ransomware, rat, trojan.
> Hyperparametre z V1 (bez ladenia). Emulácia sa nemeria – „emulované súbory“ = podiel súborov, ktoré treba emulovať.

## 1. Časový test (rozdelenie V1, test apríl 2022)
Modely a kaskády A z `runs_final`, nové modely a kaskády B z `runs_v2/full`.

| prístup | TPR | FPR | F1 | emulované súbory | CPU ms/vz. |
|---|---|---|---|---|---|
| statický LightGBM | 0.9843 | 0.0048 | 0.9900 | 0.0000 | 0.6786 |
| dynamický LightGBM | 0.6572 | 0.0198 | 0.7852 | 1.0000 | 0.4269 |
| hybrid LightGBM | 0.9842 | 0.0047 | 0.9901 | 1.0000 | 0.0858 |
| hybrid dvojvetvová sieť (komplexný) | 0.9767 | 0.0058 | 0.9857 | 1.0000 | 32.4503 |
| študent statický (KD z hybridu) | 0.9581 | 0.0059 | 0.9761 | 0.0000 | 0.3037 |
| študent statický (bez KD) | 0.9613 | 0.0076 | 0.9771 | 0.0000 | 0.3039 |
| študent statický (KD, variant A) | 0.9667 | 0.0068 | 0.9802 | 0.0000 | 0.3060 |
| študent statický (KD z dvojvetvovej siete) | 0.9701 | 0.0083 | 0.9813 | 0.0000 | 0.3021 |
| študent dynamický (KD z hybridu) | 0.5214 | 0.0171 | 0.6790 | 1.0000 | 0.2956 |
| študent dynamický (bez KD) | 0.5391 | 0.0177 | 0.6938 | 1.0000 | 0.2957 |
| študent dynamický (KD, variant A) | 0.5050 | 0.0157 | 0.6652 | 1.0000 | 0.2965 |
| študent dynamický (KD z dvojvetvovej siete) | 0.5182 | 0.0135 | 0.6775 | 1.0000 | 0.2768 |
| kaskáda A-main | 0.9579 | 0.0026 | 0.9774 | 1.0000 | 0.6209 |
| kaskáda A-nokd | 0.9605 | 0.0027 | 0.9787 | 1.0000 | 0.6210 |
| kaskáda A-modal | 0.9635 | 0.0025 | 0.9804 | 1.0000 | 0.6250 |
| kaskáda A-heavy | 0.9534 | 0.0027 | 0.9750 | 1.0000 | 8.7934 |
| kaskáda A-baselines | 0.9831 | 0.0039 | 0.9898 | 1.0000 | 1.1218 |
| kaskáda A-twobranch | 0.9683 | 0.0025 | 0.9828 | 1.0000 | 0.6011 |
| kaskáda B-main | 0.9587 | 0.0034 | 0.9775 | 0.1065 | 0.3407 |
| kaskáda B-direct | 0.9674 | 0.0032 | 0.9821 | 0.1065 | 0.3128 |
| kaskáda B-heavy | 0.9528 | 0.0031 | 0.9745 | 0.1065 | 2.4469 |
| kaskáda B-baselines | 0.9241 | 0.0004 | 0.9604 | 0.0035 | 0.6801 |
| kaskáda B-nokd | 0.9601 | 0.0035 | 0.9782 | 0.0906 | 0.3355 |
| kaskáda B-twobranch | 0.9679 | 0.0038 | 0.9821 | 0.0853 | 0.3310 |

## 2. Zero-day – priemer cez rodiny (test apríl 2022 + januárové vzorky vynechanej rodiny)
| prístup | TPR vynech. rodiny (test) | sm. odch. cez rodiny | najhoršia rodina | TPR vynech. rodiny (január) | FPR | TPR všetok malvér | emulované súbory |
|---|---|---|---|---|---|---|---|
| statický LightGBM | 0.7922 | 0.2768 | 0.2408 | 0.8794 | 0.0047 | 0.9598 | 0.0000 |
| dynamický LightGBM | 0.5094 | 0.2430 | 0.1239 | 0.4708 | 0.0184 | 0.6492 | 1.0000 |
| hybrid LightGBM | 0.7870 | 0.3048 | 0.1684 | 0.8763 | 0.0045 | 0.9557 | 1.0000 |
| hybrid dvojvetvová sieť (komplexný) | 0.7614 | 0.2913 | 0.1864 | 0.8012 | 0.0068 | 0.9438 | 1.0000 |
| študent statický (KD z hybridu) | 0.7470 | 0.2731 | 0.1985 | 0.8140 | 0.0059 | 0.9337 | 0.0000 |
| študent statický (bez KD) | 0.7402 | 0.2752 | 0.1896 | 0.7818 | 0.0074 | 0.9308 | 0.0000 |
| študent statický (KD, variant A) | 0.7477 | 0.2786 | 0.1880 | 0.8060 | 0.0064 | 0.9343 | 0.0000 |
| študent statický (KD z dvojvetvovej siete) | 0.7620 | 0.2827 | 0.2020 | 0.8061 | 0.0074 | 0.9357 | 0.0000 |
| študent dynamický (KD z hybridu) | 0.4367 | 0.2688 | 0.1025 | 0.4592 | 0.0158 | 0.4989 | 1.0000 |
| študent dynamický (bez KD) | 0.4524 | 0.2397 | 0.1098 | 0.4740 | 0.0190 | 0.5166 | 1.0000 |
| študent dynamický (KD, variant A) | 0.4113 | 0.2923 | 0.0734 | 0.4581 | 0.0148 | 0.4612 | 1.0000 |
| študent dynamický (KD z dvojvetvovej siete) | 0.4045 | 0.2373 | 0.0932 | 0.4485 | 0.0151 | 0.4858 | 1.0000 |
| kaskáda A-main | 0.7392 | 0.2899 | 0.1441 | 0.8171 | 0.0023 | 0.9293 | 1.0000 |
| kaskáda A-nokd | 0.7348 | 0.2880 | 0.1483 | 0.7980 | 0.0024 | 0.9279 | 1.0000 |
| kaskáda A-modal | 0.7400 | 0.2915 | 0.1441 | 0.8076 | 0.0023 | 0.9303 | 1.0000 |
| kaskáda A-heavy | 0.7394 | 0.2740 | 0.1924 | 0.7780 | 0.0031 | 0.9270 | 1.0000 |
| kaskáda A-baselines | 0.7797 | 0.3004 | 0.1678 | 0.8753 | 0.0036 | 0.9536 | 1.0000 |
| kaskáda A-twobranch | 0.7468 | 0.2986 | 0.1447 | 0.8064 | 0.0021 | 0.9303 | 1.0000 |
| kaskáda B-main | 0.7309 | 0.3042 | 0.1031 | 0.8078 | 0.0030 | 0.9248 | 0.1216 |
| kaskáda B-direct | 0.7367 | 0.3085 | 0.1031 | 0.8271 | 0.0029 | 0.9321 | 0.1216 |
| kaskáda B-heavy | 0.7316 | 0.2848 | 0.1547 | 0.7720 | 0.0032 | 0.9203 | 0.1216 |
| kaskáda B-baselines | 0.6096 | 0.3188 | 0.0759 | 0.6791 | 0.0004 | 0.8758 | 0.0086 |
| kaskáda B-nokd | 0.7269 | 0.3031 | 0.1053 | 0.7738 | 0.0031 | 0.9213 | 0.1053 |
| kaskáda B-twobranch | 0.7461 | 0.3004 | 0.1460 | 0.7917 | 0.0032 | 0.9250 | 0.0884 |

### TPR vynechanej rodiny podľa rodiny (test)
| prístup | backdoor | coinminer | dropper | keylogger | ransomware | rat | trojan |
|---|---|---|---|---|---|---|---|
| statický LightGBM | 0.9835 | 0.6006 | 0.9431 | 0.2408 | 0.9821 | 0.9234 | 0.8719 |
| dynamický LightGBM | 0.4223 | 0.4986 | 0.6799 | 0.1239 | 0.3132 | 0.7846 | 0.7432 |
| hybrid LightGBM | 0.9864 | 0.5966 | 0.9471 | 0.1684 | 0.9849 | 0.9473 | 0.8786 |
| hybrid dvojvetvová sieť (komplexný) | 0.9653 | 0.5588 | 0.9325 | 0.1864 | 0.9358 | 0.9462 | 0.8049 |
| študent statický (KD z hybridu) | 0.8859 | 0.5677 | 0.8902 | 0.1985 | 0.9370 | 0.9287 | 0.8212 |
| študent statický (bez KD) | 0.8883 | 0.5546 | 0.8968 | 0.1896 | 0.9383 | 0.9014 | 0.8123 |
| študent statický (KD, variant A) | 0.8967 | 0.5701 | 0.8995 | 0.1880 | 0.9215 | 0.9523 | 0.8058 |
| študent statický (KD z dvojvetvovej siete) | 0.9192 | 0.5525 | 0.9101 | 0.2020 | 0.9441 | 0.9377 | 0.8682 |
| študent dynamický (KD z hybridu) | 0.4692 | 0.2674 | 0.6971 | 0.1025 | 0.1407 | 0.7549 | 0.6252 |
| študent dynamický (bez KD) | 0.4821 | 0.2779 | 0.6759 | 0.1098 | 0.2694 | 0.7557 | 0.5960 |
| študent dynamický (KD, variant A) | 0.4644 | 0.0734 | 0.7288 | 0.0823 | 0.2040 | 0.7546 | 0.5714 |
| študent dynamický (KD z dvojvetvovej siete) | 0.4754 | 0.1855 | 0.6614 | 0.0932 | 0.2049 | 0.6306 | 0.5803 |
| static/lr | 0.8820 | 0.5582 | 0.8651 | 0.1787 | 0.8948 | 0.8943 | 0.8230 |
| static/rf | 0.8723 | 0.5730 | 0.9206 | 0.1816 | 0.9631 | 0.8617 | 0.8396 |
| static/mlp_small | 0.9622 | 0.5437 | 0.9021 | 0.2069 | 0.9182 | 0.9202 | 0.8424 |
| static/mlp_large | 0.9639 | 0.5740 | 0.9008 | 0.1956 | 0.9380 | 0.9425 | 0.8618 |
| dynamic/lr | 0.4582 | 0.2049 | 0.7222 | 0.1028 | 0.3745 | 0.6701 | 0.7217 |
| dynamic/rf | 0.1093 | 0.4535 | 0.6071 | 0.1172 | 0.0598 | 0.7607 | 0.3281 |
| dynamic/mlp_small | 0.4486 | 0.2563 | 0.6561 | 0.1069 | 0.1736 | 0.7549 | 0.6335 |
| dynamic/mlp_large | 0.4342 | 0.2654 | 0.6931 | 0.1066 | 0.3389 | 0.7576 | 0.6249 |
| hybrid/lr | 0.8820 | 0.5665 | 0.8532 | 0.2229 | 0.8443 | 0.9300 | 0.8267 |
| hybrid/rf | 0.9002 | 0.5938 | 0.9643 | 0.1713 | 0.9699 | 0.8503 | 0.8802 |
| hybrid/mlp_small | 0.8823 | 0.5633 | 0.8995 | 0.2033 | 0.8225 | 0.9120 | 0.8052 |
| hybrid/mlp_large | 0.8780 | 0.5574 | 0.8823 | 0.1819 | 0.8761 | 0.9242 | 0.8556 |
| dynamic/seq_cnn | 0.3572 | 0.4505 | 0.6323 | 0.0993 | 0.3226 | 0.7621 | 0.5189 |
| kaskáda A-main | 0.8904 | 0.5740 | 0.8955 | 0.1441 | 0.9433 | 0.9017 | 0.8255 |
| kaskáda A-nokd | 0.8912 | 0.5627 | 0.8995 | 0.1483 | 0.9425 | 0.8884 | 0.8111 |
| kaskáda A-modal | 0.8962 | 0.5719 | 0.9021 | 0.1441 | 0.9327 | 0.9245 | 0.8083 |
| kaskáda A-heavy | 0.8820 | 0.5544 | 0.9048 | 0.1924 | 0.9162 | 0.9245 | 0.8018 |
| kaskáda A-baselines | 0.9820 | 0.5986 | 0.9405 | 0.1678 | 0.9807 | 0.9152 | 0.8731 |
| kaskáda A-twobranch | 0.9206 | 0.5497 | 0.9101 | 0.1447 | 0.9469 | 0.9115 | 0.8442 |
| kaskáda B-main | 0.8844 | 0.5647 | 0.8929 | 0.1031 | 0.9416 | 0.9070 | 0.8224 |
| kaskáda B-direct | 0.8875 | 0.5624 | 0.8955 | 0.1031 | 0.9545 | 0.9245 | 0.8295 |
| kaskáda B-heavy | 0.8785 | 0.5558 | 0.8915 | 0.1547 | 0.9154 | 0.9240 | 0.8012 |
| kaskáda B-baselines | 0.8375 | 0.2835 | 0.8175 | 0.0759 | 0.9277 | 0.7538 | 0.5711 |
| kaskáda B-nokd | 0.8869 | 0.5544 | 0.8968 | 0.1053 | 0.9395 | 0.8959 | 0.8092 |
| kaskáda B-twobranch | 0.9187 | 0.5356 | 0.9101 | 0.1460 | 0.9450 | 0.9229 | 0.8445 |

### Celý rebríček modelov (doplnok)
| prístup | TPR vynech. rodiny (test) | sm. odch. cez rodiny | najhoršia rodina | TPR vynech. rodiny (január) | FPR | TPR všetok malvér | emulované súbory |
|---|---|---|---|---|---|---|---|
| statický LightGBM | 0.7922 | 0.2768 | 0.2408 | 0.8794 | 0.0047 | 0.9598 | 0.0000 |
| dynamický LightGBM | 0.5094 | 0.2430 | 0.1239 | 0.4708 | 0.0184 | 0.6492 | 1.0000 |
| hybrid LightGBM | 0.7870 | 0.3048 | 0.1684 | 0.8763 | 0.0045 | 0.9557 | 1.0000 |
| hybrid dvojvetvová sieť (komplexný) | 0.7614 | 0.2913 | 0.1864 | 0.8012 | 0.0068 | 0.9438 | 1.0000 |
| static/lr | 0.7280 | 0.2701 | 0.1787 | 0.7686 | 0.0079 | 0.9205 | 0.0000 |
| static/rf | 0.7446 | 0.2782 | 0.1816 | 0.8177 | 0.0067 | 0.9331 | 0.0000 |
| static/mlp_small | 0.7565 | 0.2802 | 0.2069 | 0.8066 | 0.0070 | 0.9387 | 0.0000 |
| static/mlp_large | 0.7681 | 0.2856 | 0.1956 | 0.8274 | 0.0065 | 0.9515 | 0.0000 |
| dynamic/lr | 0.4649 | 0.2521 | 0.1028 | 0.4755 | 0.0602 | 0.4951 | 1.0000 |
| dynamic/rf | 0.3480 | 0.2715 | 0.0598 | 0.4018 | 0.0160 | 0.5325 | 1.0000 |
| dynamic/mlp_small | 0.4329 | 0.2578 | 0.1069 | 0.4455 | 0.0129 | 0.5041 | 1.0000 |
| dynamic/mlp_large | 0.4601 | 0.2409 | 0.1066 | 0.4701 | 0.0162 | 0.5307 | 1.0000 |
| hybrid/lr | 0.7322 | 0.2532 | 0.2229 | 0.7977 | 0.0069 | 0.8980 | 1.0000 |
| hybrid/rf | 0.7614 | 0.2893 | 0.1713 | 0.8563 | 0.0081 | 0.9283 | 1.0000 |
| hybrid/mlp_small | 0.7269 | 0.2596 | 0.2033 | 0.7857 | 0.0072 | 0.8586 | 1.0000 |
| hybrid/mlp_large | 0.7365 | 0.2738 | 0.1819 | 0.7953 | 0.0063 | 0.9078 | 1.0000 |
| dynamic/seq_cnn | 0.4490 | 0.2173 | 0.0993 | 0.4798 | 0.0145 | 0.6004 | 1.0000 |

## 3. Tézy (kritériá z docs/09)
### Téza 1 – kaskáda presnejšia a stabilnejšia v zero-day
- kaskáda A-main vs. statický LightGBM: TPR vynechanej rodiny 0.7392 ± 0.2899 vs. 0.7922 ± 0.2768; FPR 0.0023 vs. 0.0047; kaskáda ≥ model v 0 z 7 rodín
- kaskáda A-main vs. dynamický LightGBM: TPR vynechanej rodiny 0.7392 ± 0.2899 vs. 0.5094 ± 0.2430; FPR 0.0023 vs. 0.0184; kaskáda ≥ model v 7 z 7 rodín
- kaskáda A-main vs. hybrid LightGBM: TPR vynechanej rodiny 0.7392 ± 0.2899 vs. 0.7870 ± 0.3048; FPR 0.0023 vs. 0.0045; kaskáda ≥ model v 0 z 7 rodín
- kaskáda A-main vs. hybrid dvojvetvová sieť (komplexný): TPR vynechanej rodiny 0.7392 ± 0.2899 vs. 0.7614 ± 0.2913; FPR 0.0023 vs. 0.0068; kaskáda ≥ model v 3 z 7 rodín
- kaskáda B-main vs. statický LightGBM: TPR vynechanej rodiny 0.7309 ± 0.3042 vs. 0.7922 ± 0.2768; FPR 0.0030 vs. 0.0047; kaskáda ≥ model v 0 z 7 rodín
- kaskáda B-main vs. dynamický LightGBM: TPR vynechanej rodiny 0.7309 ± 0.3042 vs. 0.5094 ± 0.2430; FPR 0.0030 vs. 0.0184; kaskáda ≥ model v 6 z 7 rodín
- kaskáda B-main vs. hybrid LightGBM: TPR vynechanej rodiny 0.7309 ± 0.3042 vs. 0.7870 ± 0.3048; FPR 0.0030 vs. 0.0045; kaskáda ≥ model v 0 z 7 rodín
- kaskáda B-main vs. hybrid dvojvetvová sieť (komplexný): TPR vynechanej rodiny 0.7309 ± 0.3042 vs. 0.7614 ± 0.2913; FPR 0.0030 vs. 0.0068; kaskáda ≥ model v 3 z 7 rodín

### Téza 2 – menej falošných poplachov pri zachovaní citlivosti (TPR ≥ statický − 1 p. b.)
Časový test:

| kaskáda | FPR | FPR statický | FPR dynamický | TPR | TPR statický | spĺňa kritérium |
|---|---|---|---|---|---|---|
| kaskáda A-main | 0.0026 | 0.0048 | 0.0198 | 0.9579 | 0.9843 | nie |
| kaskáda A-nokd | 0.0027 | 0.0048 | 0.0198 | 0.9605 | 0.9843 | nie |
| kaskáda A-modal | 0.0025 | 0.0048 | 0.0198 | 0.9635 | 0.9843 | nie |
| kaskáda A-heavy | 0.0027 | 0.0048 | 0.0198 | 0.9534 | 0.9843 | nie |
| kaskáda A-baselines | 0.0039 | 0.0048 | 0.0198 | 0.9831 | 0.9843 | áno |
| kaskáda A-twobranch | 0.0025 | 0.0048 | 0.0198 | 0.9683 | 0.9843 | nie |
| kaskáda B-main | 0.0034 | 0.0048 | 0.0198 | 0.9587 | 0.9843 | nie |
| kaskáda B-direct | 0.0032 | 0.0048 | 0.0198 | 0.9674 | 0.9843 | nie |
| kaskáda B-heavy | 0.0031 | 0.0048 | 0.0198 | 0.9528 | 0.9843 | nie |
| kaskáda B-baselines | 0.0004 | 0.0048 | 0.0198 | 0.9241 | 0.9843 | nie |
| kaskáda B-nokd | 0.0035 | 0.0048 | 0.0198 | 0.9601 | 0.9843 | nie |
| kaskáda B-twobranch | 0.0038 | 0.0048 | 0.0198 | 0.9679 | 0.9843 | nie |

Zero-day (priemer cez rodiny):

| kaskáda | FPR | FPR statický | FPR dynamický | TPR | TPR statický | spĺňa kritérium |
|---|---|---|---|---|---|---|
| kaskáda A-main | 0.0023 | 0.0047 | 0.0184 | 0.9293 | 0.9598 | nie |
| kaskáda A-nokd | 0.0024 | 0.0047 | 0.0184 | 0.9279 | 0.9598 | nie |
| kaskáda A-modal | 0.0023 | 0.0047 | 0.0184 | 0.9303 | 0.9598 | nie |
| kaskáda A-heavy | 0.0031 | 0.0047 | 0.0184 | 0.9270 | 0.9598 | nie |
| kaskáda A-baselines | 0.0036 | 0.0047 | 0.0184 | 0.9536 | 0.9598 | áno |
| kaskáda A-twobranch | 0.0021 | 0.0047 | 0.0184 | 0.9303 | 0.9598 | nie |
| kaskáda B-main | 0.0030 | 0.0047 | 0.0184 | 0.9248 | 0.9598 | nie |
| kaskáda B-direct | 0.0029 | 0.0047 | 0.0184 | 0.9321 | 0.9598 | nie |
| kaskáda B-heavy | 0.0032 | 0.0047 | 0.0184 | 0.9203 | 0.9598 | nie |
| kaskáda B-baselines | 0.0004 | 0.0047 | 0.0184 | 0.8758 | 0.9598 | nie |
| kaskáda B-nokd | 0.0031 | 0.0047 | 0.0184 | 0.9213 | 0.9598 | nie |
| kaskáda B-twobranch | 0.0032 | 0.0047 | 0.0184 | 0.9250 | 0.9598 | nie |

### Téza 3 – študent rýchlejší a s porovnateľnou presnosťou ako komplexný hybrid (zero-day, ±1 p. b.)
| študent | referencia | TPR vynech. rodiny študent | TPR referencia | rozdiel | CPU ms študent | CPU ms referencia | rýchlejší | porovnateľná presnosť (≥ −1 p. b.) |
|---|---|---|---|---|---|---|---|---|
| študent statický (KD z hybridu) | hybrid dvojvetvová sieť (komplexný) | 0.7470 | 0.7614 | -0.0144 | 0.3037 | 32.4503 | áno | nie |
| študent statický (bez KD) | hybrid dvojvetvová sieť (komplexný) | 0.7402 | 0.7614 | -0.0212 | 0.3039 | 32.4503 | áno | nie |
| študent statický (KD, variant A) | hybrid dvojvetvová sieť (komplexný) | 0.7477 | 0.7614 | -0.0137 | 0.3060 | 32.4503 | áno | nie |
| študent statický (KD z dvojvetvovej siete) | hybrid dvojvetvová sieť (komplexný) | 0.7620 | 0.7614 | 0.0006 | 0.3021 | 32.4503 | áno | áno |
| študent dynamický (KD z hybridu) | hybrid dvojvetvová sieť (komplexný) | 0.4367 | 0.7614 | -0.3247 | 0.2956 | 32.4503 | áno | nie |
| študent dynamický (bez KD) | hybrid dvojvetvová sieť (komplexný) | 0.4524 | 0.7614 | -0.3090 | 0.2957 | 32.4503 | áno | nie |
| študent dynamický (KD, variant A) | hybrid dvojvetvová sieť (komplexný) | 0.4113 | 0.7614 | -0.3501 | 0.2965 | 32.4503 | áno | nie |
| študent dynamický (KD z dvojvetvovej siete) | hybrid dvojvetvová sieť (komplexný) | 0.4045 | 0.7614 | -0.3569 | 0.2768 | 32.4503 | áno | nie |
| študent statický (KD z hybridu) | hybrid LightGBM | 0.7470 | 0.7870 | -0.0400 | 0.3037 | 0.0858 | nie | nie |
| študent statický (bez KD) | hybrid LightGBM | 0.7402 | 0.7870 | -0.0469 | 0.3039 | 0.0858 | nie | nie |
| študent statický (KD, variant A) | hybrid LightGBM | 0.7477 | 0.7870 | -0.0394 | 0.3060 | 0.0858 | nie | nie |
| študent statický (KD z dvojvetvovej siete) | hybrid LightGBM | 0.7620 | 0.7870 | -0.0251 | 0.3021 | 0.0858 | nie | nie |
| študent dynamický (KD z hybridu) | hybrid LightGBM | 0.4367 | 0.7870 | -0.3503 | 0.2956 | 0.0858 | nie | nie |
| študent dynamický (bez KD) | hybrid LightGBM | 0.4524 | 0.7870 | -0.3346 | 0.2957 | 0.0858 | nie | nie |
| študent dynamický (KD, variant A) | hybrid LightGBM | 0.4113 | 0.7870 | -0.3758 | 0.2965 | 0.0858 | nie | nie |
| študent dynamický (KD z dvojvetvovej siete) | hybrid LightGBM | 0.4045 | 0.7870 | -0.3826 | 0.2768 | 0.0858 | nie | nie |

### Téza 4 – podiel súborov, ktoré treba emulovať
Kaskáda A, dynamický a hybridný model emulujú 100 % súborov; kaskády B iba neisté (stĺpec „emulované súbory“
v tabuľkách 1 a 2). Čas s predpokladom 60 s emulácie na súbor: kaskáda B ≈ podiel × 60 s.

Súbory: `temporal_test.csv`, `zero_day_per_family.csv`.
