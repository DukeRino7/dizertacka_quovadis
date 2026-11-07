# Overenie robustnosti (docs/16)

> Generované `src/evaluation/robustness.py`. Iba z uložených predikcií, prahy z validácie. Rozdiely v percentuálnych bodoch.
> R1: párový bootstrap testu (2000 opakovaní, stratifikovane), metrika = priemer cez seedy (v zero-day aj cez 7 rodín).
> Pravidlá: *nižšie/horšie* = interval celý pod 0; *nie horšie* = dolná hranica > −1 p. b.; *rovnocenné* = interval v ±1 p. b.

## R1 – štatistická významnosť

| č. | tvrdenie | test | súbory | rozdiel [p. b.] | 95 % IS | potvrdené |
|---|---|---|---|---|---|---|
| 1 | A-baselines má nižšie FPR ako statický | časový | všetky | -0.09 | -0.17 až -0.02 | áno |
| 1 | A-baselines má nižšie FPR ako statický | časový | emulácia ok | -0.08 | -0.21 až +0.02 | nie |
| 1 | A-baselines má nižšie FPR ako statický | zero-day | všetky | -0.11 | -0.16 až -0.06 | áno |
| 1 | A-baselines má nižšie FPR ako statický | zero-day | emulácia ok | -0.09 | -0.17 až -0.02 | áno |
| 1 | A-baselines: TPR všetkého malvéru nie horšie ako statický | časový | všetky | -0.12 | -0.20 až -0.05 | áno |
| 1 | A-baselines: TPR všetkého malvéru nie horšie ako statický | časový | emulácia ok | +0.08 | -0.04 až +0.20 | áno |
| 1 | A-baselines: TPR všetkého malvéru nie horšie ako statický | zero-day | všetky | -0.62 | -0.70 až -0.54 | áno |
| 1 | A-baselines: TPR všetkého malvéru nie horšie ako statický | zero-day | emulácia ok | -0.90 | -1.03 až -0.76 | nie |
| 2 | B-baselines (10 %) má nižšie FPR ako statický | časový | všetky | -0.09 | -0.17 až -0.02 | áno |
| 2 | B-baselines (10 %) má nižšie FPR ako statický | časový | emulácia ok | -0.08 | -0.21 až +0.02 | nie |
| 2 | B-baselines (10 %) má nižšie FPR ako statický | zero-day | všetky | -0.11 | -0.16 až -0.06 | áno |
| 2 | B-baselines (10 %) má nižšie FPR ako statický | zero-day | emulácia ok | -0.09 | -0.17 až -0.02 | áno |
| 2 | B-baselines (10 %): TPR nie horšie ako statický | časový | všetky | -0.12 | -0.20 až -0.05 | áno |
| 2 | B-baselines (10 %): TPR nie horšie ako statický | časový | emulácia ok | +0.08 | -0.04 až +0.20 | áno |
| 2 | B-baselines (10 %): TPR nie horšie ako statický | zero-day | všetky | -0.62 | -0.70 až -0.54 | áno |
| 2 | B-baselines (10 %): TPR nie horšie ako statický | zero-day | emulácia ok | -0.90 | -1.03 až -0.76 | nie |
| 3 | B-baselines (10 %): TPR nie horšie ako hybrid | časový | všetky | -0.11 | -0.18 až -0.05 | áno |
| 3 | B-baselines (10 %): TPR nie horšie ako hybrid | časový | emulácia ok | +0.07 | -0.01 až +0.14 | áno |
| 3 | B-baselines (10 %): TPR nie horšie ako hybrid | zero-day | všetky | -0.21 | -0.26 až -0.16 | áno |
| 3 | B-baselines (10 %): TPR nie horšie ako hybrid | zero-day | emulácia ok | -0.05 | -0.10 až +0.01 | áno |
| 3 | B-baselines (10 %) má nižšie FPR ako hybrid | časový | všetky | -0.08 | -0.14 až -0.03 | áno |
| 3 | B-baselines (10 %) má nižšie FPR ako hybrid | časový | emulácia ok | -0.12 | -0.22 až -0.03 | áno |
| 3 | B-baselines (10 %) má nižšie FPR ako hybrid | zero-day | všetky | -0.09 | -0.12 až -0.06 | áno |
| 3 | B-baselines (10 %) má nižšie FPR ako hybrid | zero-day | emulácia ok | -0.12 | -0.18 až -0.06 | áno |
| 4 | A-main: TPR vynechanej rodiny horšie ako statický | zero-day | všetky | -5.30 | -5.88 až -4.75 | áno |
| 4 | A-main: TPR vynechanej rodiny horšie ako statický | zero-day | emulácia ok | -8.16 | -9.17 až -7.14 | áno |
| 4 | B-main: TPR vynechanej rodiny horšie ako statický | zero-day | všetky | -6.13 | -6.72 až -5.56 | áno |
| 4 | B-main: TPR vynechanej rodiny horšie ako statický | zero-day | emulácia ok | -10.60 | -11.60 až -9.58 | áno |
| 5 | hybrid = statický (TPR všetkého malvéru) | časový | všetky | -0.01 | -0.11 až +0.09 | áno |
| 5 | hybrid = statický (TPR všetkého malvéru) | časový | emulácia ok | +0.01 | -0.11 až +0.12 | áno |
| 5 | hybrid = statický (TPR všetkého malvéru) | zero-day | všetky | -0.42 | -0.50 až -0.33 | áno |
| 5 | hybrid = statický (TPR všetkého malvéru) | zero-day | emulácia ok | -0.85 | -0.99 až -0.71 | áno |
| 5 | hybrid = statický (TPR vynechanej rodiny) | zero-day | všetky | -0.51 | -0.83 až -0.22 | áno |
| 5 | hybrid = statický (TPR vynechanej rodiny) | zero-day | emulácia ok | -4.21 | -5.10 až -3.28 | nie |
| 6 | študent z dvojvetvovej siete = učiteľ (TPR vynechanej rodiny) | zero-day | všetky | +0.06 | -0.34 až +0.45 | áno |
| 6 | študent z dvojvetvovej siete = učiteľ (TPR vynechanej rodiny) | zero-day | emulácia ok | -0.91 | -1.36 až -0.43 | nie |

### Body 7 a 8 – zo scenára C (párovo cez 10 rozdelení × 3 seedy; interval = neistota výberu kalibračných súborov)

| tvrdenie | test | kalibrácia | rozdiel [p. b.] | interval (2,5 – 97,5 %) | n párov |
|---|---|---|---|---|---|
| 7: špecialista − statický pri prekalibrovanom prahu (TPR) | zero-day | 5% | -0.67 | -4.20 až +3.04 | 30 |
| 7: špecialista − statický pri prekalibrovanom prahu (FPR) | zero-day | 5% | +0.04 | -0.17 až +0.26 | 30 |
| 8: statický prekalibrovaný − pôvodný (TPR) | zero-day | 5% | +2.45 | -2.49 až +6.04 | 30 |
| 8: statický prekalibrovaný − pôvodný (FPR) | zero-day | 5% | +0.26 | -0.19 až +0.63 | 30 |
| 7: špecialista − statický pri prekalibrovanom prahu (TPR) | zero-day | 20% | +0.27 | -1.63 až +3.84 | 30 |
| 7: špecialista − statický pri prekalibrovanom prahu (FPR) | zero-day | 20% | +0.03 | -0.11 až +0.15 | 30 |
| 8: statický prekalibrovaný − pôvodný (TPR) | zero-day | 20% | +3.58 | +0.76 až +6.14 | 30 |
| 8: statický prekalibrovaný − pôvodný (FPR) | zero-day | 20% | +0.44 | +0.09 až +0.78 | 30 |
| 7: špecialista − statický pri prekalibrovanom prahu (TPR) | časový | 5% | +0.07 | -0.41 až +0.64 | 30 |
| 7: špecialista − statický pri prekalibrovanom prahu (FPR) | časový | 5% | +0.05 | -0.49 až +0.92 | 30 |
| 8: statický prekalibrovaný − pôvodný (TPR) | časový | 5% | +0.59 | -0.63 až +1.13 | 30 |
| 8: statický prekalibrovaný − pôvodný (FPR) | časový | 5% | +0.29 | -0.24 až +0.68 | 30 |
| 7: špecialista − statický pri prekalibrovanom prahu (TPR) | časový | 20% | +0.06 | -0.29 až +0.35 | 30 |
| 7: špecialista − statický pri prekalibrovanom prahu (FPR) | časový | 20% | +0.02 | -0.40 až +0.37 | 30 |
| 8: statický prekalibrovaný − pôvodný (TPR) | časový | 20% | +0.91 | +0.40 až +1.10 | 30 |
| 8: statický prekalibrovaný − pôvodný (FPR) | časový | 20% | +0.43 | +0.09 až +0.69 | 30 |

## R2 – iba súbory s úspešnou emuláciou

Testovacie súbory s úspešnou emuláciou: malvér 4407 z 9399, neškodné 3174 z 7940.
Podľa rodiny (úspešné / všetky): backdoor 1613 / 1940, coinminer 678 / 1684, dropper 178 / 252, keylogger 225 / 1041, ransomware 1007 / 2139, rat 320 / 1258, trojan 386 / 1085.

### Úrovne (zero-day, priemer cez rodiny a seedy)

| súbory | prístup | TPR vynech. rodiny | FPR |
|---|---|---|---|
| všetky | statický LightGBM | 0.7922 | 0.0047 |
| všetky | dynamický LightGBM | 0.5094 | 0.0184 |
| všetky | hybrid LightGBM | 0.7870 | 0.0045 |
| všetky | statický ALEBO dynamický (horná hranica) | 0.7978 | 0.0225 |
| všetky | kaskáda A-baselines | 0.7797 | 0.0036 |
| všetky | kaskáda B-baselines (10 %) | 0.7797 | 0.0036 |
| všetky | špecialista V3 | 0.7903 | 0.0055 |
| všetky | ROC-AUC statický LightGBM | 0.9742 | – |
| všetky | ROC-AUC dynamický LightGBM | 0.9180 | – |
| emulácia ok | statický LightGBM | 0.9178 | 0.0052 |
| emulácia ok | dynamický LightGBM | 0.6349 | 0.0227 |
| emulácia ok | hybrid LightGBM | 0.8756 | 0.0054 |
| emulácia ok | statický ALEBO dynamický (horná hranica) | 0.9243 | 0.0273 |
| emulácia ok | kaskáda A-baselines | 0.8733 | 0.0043 |
| emulácia ok | kaskáda B-baselines (10 %) | 0.8733 | 0.0043 |
| emulácia ok | špecialista V3 | 0.8900 | 0.0062 |
| emulácia ok | ROC-AUC statický LightGBM | 0.9964 | – |
| emulácia ok | ROC-AUC dynamický LightGBM | 0.9170 | – |

### Rozdiely oproti statickému modelu (zero-day, bootstrap)

| porovnanie | súbory | rozdiel [p. b.] | 95 % IS |
|---|---|---|---|
| statický ALEBO dynamický − statický (horná hranica kombinácie) | všetky | +0.56 | +0.39 až +0.76 |
| statický ALEBO dynamický − statický (horná hranica kombinácie) | emulácia ok | +0.65 | +0.39 až +0.92 |
| hybrid − statický | všetky | -0.51 | -0.83 až -0.22 |
| hybrid − statický | emulácia ok | -4.21 | -5.10 až -3.28 |
| špecialista V3 − statický | všetky | -0.19 | -0.50 až +0.11 |
| špecialista V3 − statický | emulácia ok | -2.78 | -3.63 až -1.88 |
| špecialista V3 − statický (FPR) | všetky | +0.09 | +0.04 až +0.13 |
| špecialista V3 − statický (FPR) | emulácia ok | +0.10 | +0.02 až +0.18 |

**Kritérium R2 (docs/16):** horná hranica kombinácie +0.65 p. b., hybrid -4.21 p. b., špecialista -2.78 p. b. na súboroch s úspešnou emuláciou → zistenie D **platí aj pri úspešnej emulácii**.
