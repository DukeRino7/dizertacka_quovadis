# V3 – B: kaskáda so špecialistom (súhrn)

> Generované `src/evaluation/v3_report.py`. Plán a kritériá (určené vopred): `docs/12_plan_v3.md`.
> Hlavný bod = rozpočet emulácie 10 % (hranica z validácie). Prahy z validácie, priemer cez seedy.
> Referencie sú z tých istých behov (rovnaké dáta). Zero-day = priemer cez vynechané rodiny.

## 1. Časový test (rozdelenie V1)

| prístup | tpr | fpr | f1 | emulation | cpu_ms |
|---|---|---|---|---|---|
| špecialista (hybrid) – HLAVNÝ | 0.9891 | 0.0052 | 0.9923 | 0.2150 | 0.6973 |
| statický LightGBM | 0.9843 | 0.0048 | 0.9900 | 0.0000 | – |
| dynamický LightGBM | 0.6572 | 0.0198 | 0.7852 | 1.0000 | – |
| hybrid LightGBM | 0.9842 | 0.0047 | 0.9901 | 1.0000 | – |
| kaskáda B-baselines (rovnaký rozpočet, V2) | 0.9831 | 0.0039 | 0.9898 | 0.2150 | – |
| špecialista (iba dynamika) | 0.9889 | 0.0048 | 0.9924 | 0.2150 | 0.6879 |
| špecialista, tréning 10 % (citlivosť) | 0.9908 | 0.0060 | 0.9928 | 0.2150 | 0.6960 |
| špecialista, tréning 40 % (citlivosť) | 0.9896 | 0.0058 | 0.9924 | 0.2150 | 0.6997 |

## 2. Zero-day – priemer cez 7 rodín (backdoor, coinminer, dropper, keylogger, ransomware, rat, trojan)

| prístup | TPR vynech. rodiny | sm. odch. | najhoršia | TPR január | fpr | TPR všetok malvér | emulované | rodín |
|---|---|---|---|---|---|---|---|---|
| špecialista (hybrid) – HLAVNÝ | 0.7903 | 0.2934 | 0.1960 | 0.8790 | 0.0055 | 0.9623 | 0.2281 | 7 |
| statický LightGBM | 0.7922 | 0.2768 | 0.2408 | 0.8794 | 0.0047 | 0.9598 | 0.0000 | 7 |
| dynamický LightGBM | 0.5094 | 0.2430 | 0.1239 | 0.4708 | 0.0184 | 0.6492 | 1.0000 | 7 |
| hybrid LightGBM | 0.7870 | 0.3048 | 0.1684 | 0.8763 | 0.0045 | 0.9557 | 1.0000 | 7 |
| kaskáda B-baselines (rovnaký rozpočet, V2) | 0.7797 | 0.3004 | 0.1678 | 0.8753 | 0.0036 | 0.9536 | 0.2281 | 7 |
| špecialista (iba dynamika) | 0.7799 | 0.2809 | 0.2113 | 0.8763 | 0.0049 | 0.9490 | 0.2281 | 7 |
| špecialista, tréning 10 % (citlivosť) | 0.8176 | 0.2747 | 0.2155 | 0.8831 | 0.0059 | 0.9669 | 0.2281 | 7 |
| špecialista, tréning 40 % (citlivosť) | 0.7922 | 0.2943 | 0.1928 | 0.8800 | 0.0055 | 0.9618 | 0.2281 | 7 |

### TPR vynechanej rodiny podľa rodiny (test)

| prístup | backdoor | coinminer | dropper | keylogger | ransomware | rat | trojan |
|---|---|---|---|---|---|---|---|
| špecialista (hybrid) – HLAVNÝ | 0.9844 | 0.6035 | 0.9497 | 0.1960 | 0.9779 | 0.9359 | 0.8845 |
| statický LightGBM | 0.9835 | 0.6006 | 0.9431 | 0.2408 | 0.9821 | 0.9234 | 0.8719 |
| dynamický LightGBM | 0.4223 | 0.4986 | 0.6799 | 0.1239 | 0.3132 | 0.7846 | 0.7432 |
| hybrid LightGBM | 0.9864 | 0.5966 | 0.9471 | 0.1684 | 0.9849 | 0.9473 | 0.8786 |
| kaskáda B-baselines (rovnaký rozpočet, V2) | 0.9820 | 0.5986 | 0.9405 | 0.1678 | 0.9807 | 0.9152 | 0.8731 |
| špecialista (iba dynamika) | 0.9050 | 0.5960 | 0.9458 | 0.2113 | 0.9596 | 0.9436 | 0.8983 |
| špecialista, tréning 10 % (citlivosť) | 0.9832 | 0.7775 | 0.9458 | 0.2155 | 0.9785 | 0.9375 | 0.8854 |
| špecialista, tréning 40 % (citlivosť) | 0.9832 | 0.6118 | 0.9497 | 0.1928 | 0.9841 | 0.9348 | 0.8888 |

## 3. Kritériá (docs/12, bod 2)

### špecialista (hybrid) – HLAVNÝ
- **B1 (téza 1):** TPR vynech. rodiny 0.7903 vs. statický 0.7922 (potrebné +1%), FPR 0.0055 vs. 0.0047, lepší alebo rovný v 5 z 7 rodín → **nesplnené**
- **B2 (téza 2):** zero-day FPR 0.0055 (statický 0.0047, dynamický 0.0184), TPR 0.9623 vs. statický 0.9598 → **nesplnené**; časový test → **nesplnené**
- **B3 (prínos oproti V2):** TPR vynech. rodiny 0.7903 vs. B-baselines 0.7797, FPR 0.0055 vs. 0.0036 → **nesplnené**

### špecialista (iba dynamika)
- **B1 (téza 1):** TPR vynech. rodiny 0.7799 vs. statický 0.7922 (potrebné +1%), FPR 0.0049 vs. 0.0047, lepší alebo rovný v 3 z 7 rodín → **nesplnené**
- **B2 (téza 2):** zero-day FPR 0.0049 (statický 0.0047, dynamický 0.0184), TPR 0.9490 vs. statický 0.9598 → **nesplnené**; časový test → **splnené**
- **B3 (prínos oproti V2):** TPR vynech. rodiny 0.7799 vs. B-baselines 0.7797, FPR 0.0049 vs. 0.0036 → **nesplnené**

### špecialista, tréning 10 % (citlivosť) _(citlivosť, nie hlavný variant)_
- **B1 (téza 1):** TPR vynech. rodiny 0.8176 vs. statický 0.7922 (potrebné +1%), FPR 0.0059 vs. 0.0047, lepší alebo rovný v 4 z 7 rodín → **nesplnené**
- **B2 (téza 2):** zero-day FPR 0.0059 (statický 0.0047, dynamický 0.0184), TPR 0.9669 vs. statický 0.9598 → **nesplnené**; časový test → **nesplnené**
- **B3 (prínos oproti V2):** TPR vynech. rodiny 0.8176 vs. B-baselines 0.7797, FPR 0.0059 vs. 0.0036 → **nesplnené**

### špecialista, tréning 40 % (citlivosť) _(citlivosť, nie hlavný variant)_
- **B1 (téza 1):** TPR vynech. rodiny 0.7922 vs. statický 0.7922 (potrebné +1%), FPR 0.0055 vs. 0.0047, lepší alebo rovný v 5 z 7 rodín → **nesplnené**
- **B2 (téza 2):** zero-day FPR 0.0055 (statický 0.0047, dynamický 0.0184), TPR 0.9618 vs. statický 0.9598 → **nesplnené**; časový test → **nesplnené**
- **B3 (prínos oproti V2):** TPR vynech. rodiny 0.7922 vs. B-baselines 0.7797, FPR 0.0055 vs. 0.0036 → **nesplnené**

## 4. Krivka rozpočtu emulácie (doplnok)

| variant | prístup | rozpočet | test | emulované | TPR | FPR | TPR vynech. rodiny |
|---|---|---|---|---|---|---|---|
| v3_spec | v3_spec | 0.1000 | časový | 0.2150 | 0.9891 | 0.0052 | – |
| v3_spec | b_baselines | 0.1000 | časový | 0.2150 | 0.9831 | 0.0039 | – |
| v3_spec | v3_spec | 0.2000 | časový | 0.3977 | 0.9891 | 0.0052 | – |
| v3_spec | b_baselines | 0.2000 | časový | 0.3977 | 0.9831 | 0.0039 | – |
| v3_spec | v3_spec | 0.3000 | časový | 0.5522 | 0.9891 | 0.0052 | – |
| v3_spec | b_baselines | 0.3000 | časový | 0.5522 | 0.9831 | 0.0039 | – |
| v3_spec | v3_spec | 0.4000 | časový | 0.6938 | 0.9891 | 0.0052 | – |
| v3_spec | b_baselines | 0.4000 | časový | 0.6938 | 0.9831 | 0.0039 | – |
| v3_spec | v3_spec | 0.1000 | zero-day | 0.2281 | 0.9623 | 0.0055 | 0.7903 |
| v3_spec | b_baselines | 0.1000 | zero-day | 0.2281 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec | v3_spec | 0.2000 | zero-day | 0.4009 | 0.9623 | 0.0055 | 0.7903 |
| v3_spec | b_baselines | 0.2000 | zero-day | 0.4009 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec | v3_spec | 0.3000 | zero-day | 0.5922 | 0.9622 | 0.0055 | 0.7903 |
| v3_spec | b_baselines | 0.3000 | zero-day | 0.5922 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec | v3_spec | 0.4000 | zero-day | 0.7197 | 0.9622 | 0.0055 | 0.7903 |
| v3_spec | b_baselines | 0.4000 | zero-day | 0.7197 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_dyn | v3_spec_dyn | 0.1000 | časový | 0.2150 | 0.9889 | 0.0048 | – |
| v3_spec_dyn | b_baselines | 0.1000 | časový | 0.2150 | 0.9831 | 0.0039 | – |
| v3_spec_dyn | v3_spec_dyn | 0.2000 | časový | 0.3977 | 0.9889 | 0.0048 | – |
| v3_spec_dyn | b_baselines | 0.2000 | časový | 0.3977 | 0.9831 | 0.0039 | – |
| v3_spec_dyn | v3_spec_dyn | 0.3000 | časový | 0.5522 | 0.9889 | 0.0048 | – |
| v3_spec_dyn | b_baselines | 0.3000 | časový | 0.5522 | 0.9831 | 0.0039 | – |
| v3_spec_dyn | v3_spec_dyn | 0.4000 | časový | 0.6938 | 0.9889 | 0.0048 | – |
| v3_spec_dyn | b_baselines | 0.4000 | časový | 0.6938 | 0.9831 | 0.0039 | – |
| v3_spec_dyn | v3_spec_dyn | 0.1000 | zero-day | 0.2281 | 0.9490 | 0.0049 | 0.7799 |
| v3_spec_dyn | b_baselines | 0.1000 | zero-day | 0.2281 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_dyn | v3_spec_dyn | 0.2000 | zero-day | 0.4009 | 0.9490 | 0.0049 | 0.7799 |
| v3_spec_dyn | b_baselines | 0.2000 | zero-day | 0.4009 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_dyn | v3_spec_dyn | 0.3000 | zero-day | 0.5922 | 0.9490 | 0.0049 | 0.7799 |
| v3_spec_dyn | b_baselines | 0.3000 | zero-day | 0.5922 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_dyn | v3_spec_dyn | 0.4000 | zero-day | 0.7197 | 0.9490 | 0.0049 | 0.7799 |
| v3_spec_dyn | b_baselines | 0.4000 | zero-day | 0.7197 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_f10 | v3_spec_f10 | 0.1000 | časový | 0.2150 | 0.9908 | 0.0060 | – |
| v3_spec_f10 | b_baselines | 0.1000 | časový | 0.2150 | 0.9831 | 0.0039 | – |
| v3_spec_f10 | v3_spec_f10 | 0.2000 | časový | 0.3977 | 0.9908 | 0.0060 | – |
| v3_spec_f10 | b_baselines | 0.2000 | časový | 0.3977 | 0.9831 | 0.0039 | – |
| v3_spec_f10 | v3_spec_f10 | 0.3000 | časový | 0.5522 | 0.9908 | 0.0060 | – |
| v3_spec_f10 | b_baselines | 0.3000 | časový | 0.5522 | 0.9831 | 0.0039 | – |
| v3_spec_f10 | v3_spec_f10 | 0.4000 | časový | 0.6938 | 0.9908 | 0.0060 | – |
| v3_spec_f10 | b_baselines | 0.4000 | časový | 0.6938 | 0.9831 | 0.0039 | – |
| v3_spec_f10 | v3_spec_f10 | 0.1000 | zero-day | 0.2281 | 0.9669 | 0.0059 | 0.8176 |
| v3_spec_f10 | b_baselines | 0.1000 | zero-day | 0.2281 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_f10 | v3_spec_f10 | 0.2000 | zero-day | 0.4009 | 0.9663 | 0.0059 | 0.8176 |
| v3_spec_f10 | b_baselines | 0.2000 | zero-day | 0.4009 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_f10 | v3_spec_f10 | 0.3000 | zero-day | 0.5922 | 0.9660 | 0.0059 | 0.8176 |
| v3_spec_f10 | b_baselines | 0.3000 | zero-day | 0.5922 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_f10 | v3_spec_f10 | 0.4000 | zero-day | 0.7197 | 0.9657 | 0.0059 | 0.8176 |
| v3_spec_f10 | b_baselines | 0.4000 | zero-day | 0.7197 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_f40 | v3_spec_f40 | 0.1000 | časový | 0.2150 | 0.9896 | 0.0058 | – |
| v3_spec_f40 | b_baselines | 0.1000 | časový | 0.2150 | 0.9831 | 0.0039 | – |
| v3_spec_f40 | v3_spec_f40 | 0.2000 | časový | 0.3977 | 0.9896 | 0.0058 | – |
| v3_spec_f40 | b_baselines | 0.2000 | časový | 0.3977 | 0.9831 | 0.0039 | – |
| v3_spec_f40 | v3_spec_f40 | 0.3000 | časový | 0.5522 | 0.9896 | 0.0058 | – |
| v3_spec_f40 | b_baselines | 0.3000 | časový | 0.5522 | 0.9831 | 0.0039 | – |
| v3_spec_f40 | v3_spec_f40 | 0.4000 | časový | 0.6938 | 0.9896 | 0.0058 | – |
| v3_spec_f40 | b_baselines | 0.4000 | časový | 0.6938 | 0.9831 | 0.0039 | – |
| v3_spec_f40 | v3_spec_f40 | 0.1000 | zero-day | 0.2281 | 0.9618 | 0.0055 | 0.7922 |
| v3_spec_f40 | b_baselines | 0.1000 | zero-day | 0.2281 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_f40 | v3_spec_f40 | 0.2000 | zero-day | 0.4009 | 0.9618 | 0.0055 | 0.7922 |
| v3_spec_f40 | b_baselines | 0.2000 | zero-day | 0.4009 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_f40 | v3_spec_f40 | 0.3000 | zero-day | 0.5922 | 0.9618 | 0.0055 | 0.7922 |
| v3_spec_f40 | b_baselines | 0.3000 | zero-day | 0.5922 | 0.9536 | 0.0036 | 0.7797 |
| v3_spec_f40 | v3_spec_f40 | 0.4000 | zero-day | 0.7197 | 0.9618 | 0.0055 | 0.7922 |
| v3_spec_f40 | b_baselines | 0.4000 | zero-day | 0.7197 | 0.9536 | 0.0036 | 0.7797 |
