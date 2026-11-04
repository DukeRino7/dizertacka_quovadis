# V2 – analýza príčin (zero-day)

> Generované `src/evaluation/v2_analysis.py`. Modely LightGBM z `runs_v2/lofo`, prahy z validácie (FPR 1 %),
> priemer cez seedy 0–2. Stĺpce **orákulum** používajú test (prah na teste, dokonalý druhý stupeň) – sú to iba
> horné hranice na vysvetlenie, nie výsledky metódy. Test vynechanej rodiny = apríl 2022, „jan“ = jej januárové vzorky.

## 1. Koľko môže kombinácia statického a dynamického rozhodnutia pridať
S = statický, D = dynamický, H = hybrid; „S alebo D“ = malvér, ak ho označí aspoň jeden (horná hranica pre
každé pravidlo, ktoré kombinuje tieto dve rozhodnutia).

| rodina | n | tpr_S | tpr_D | tpr_H | tpr_S_alebo_D | D_opraví_z_minutých_S | fpr_S | fpr_S_alebo_D |
|---|---|---|---|---|---|---|---|---|
| backdoor | 1940.000 | 0.984 | 0.422 | 0.986 | 0.990 | 0.385 | 0.005 | 0.019 |
| coinminer | 1684.000 | 0.601 | 0.499 | 0.597 | 0.609 | 0.022 | 0.005 | 0.019 |
| dropper | 252.000 | 0.943 | 0.680 | 0.947 | 0.947 | 0.070 | 0.005 | 0.028 |
| keylogger | 1041.000 | 0.241 | 0.124 | 0.168 | 0.245 | 0.005 | 0.005 | 0.029 |
| ransomware | 2139.000 | 0.982 | 0.313 | 0.985 | 0.982 | 0.017 | 0.005 | 0.017 |
| rat | 1258.000 | 0.923 | 0.785 | 0.947 | 0.923 | 0.000 | 0.005 | 0.019 |
| trojan | 1085.000 | 0.872 | 0.743 | 0.879 | 0.888 | 0.125 | 0.003 | 0.027 |
| PRIEMER | 1342.714 | 0.792 | 0.509 | 0.787 | 0.798 | 0.089 | 0.005 | 0.022 |

| rodina | tpr_S_jan | tpr_D_jan | tpr_H_jan | tpr_S_alebo_D_jan |
|---|---|---|---|---|
| backdoor | 0.993 | 0.498 | 0.992 | 0.994 |
| coinminer | 0.865 | 0.256 | 0.871 | 0.867 |
| dropper | 0.979 | 0.646 | 0.980 | 0.984 |
| keylogger | 0.429 | 0.367 | 0.395 | 0.432 |
| ransomware | 0.995 | 0.083 | 0.997 | 0.995 |
| rat | 0.964 | 0.774 | 0.968 | 0.965 |
| trojan | 0.930 | 0.671 | 0.932 | 0.943 |
| PRIEMER | 0.879 | 0.471 | 0.876 | 0.883 |

## 2. Oddeliteľnosť vynechanej rodiny a posun prahu
ROC-AUC = vynechaná rodina vs. neškodné testu (nezávislé od prahu). Orákulum = TPR statického modelu, keby prah
dosiahol na teste FPR 1 % alebo 2 % (prah z validácie dáva na teste FPR iba ~0,5 %).

| rodina | auc_S | auc_D | tpr_S | fpr_S | orakulum_tpr_S_pri_FPR_testu_1% | orakulum_tpr_S_pri_FPR_testu_2% |
|---|---|---|---|---|---|---|
| backdoor | 1.000 | 0.918 | 0.984 | 0.005 | 0.988 | 0.999 |
| coinminer | 0.990 | 0.835 | 0.601 | 0.005 | 0.782 | 0.897 |
| dropper | 0.998 | 0.964 | 0.943 | 0.005 | 0.959 | 0.974 |
| keylogger | 0.840 | 0.877 | 0.241 | 0.005 | 0.260 | 0.274 |
| ransomware | 0.999 | 0.902 | 0.982 | 0.005 | 0.993 | 0.995 |
| rat | 0.998 | 0.983 | 0.923 | 0.005 | 0.969 | 0.986 |
| trojan | 0.994 | 0.946 | 0.872 | 0.003 | 0.917 | 0.931 |
| PRIEMER | 0.974 | 0.918 | 0.792 | 0.005 | 0.838 | 0.865 |

## 3. Eskalácia pri rozpočte 10% (hranica z validácie) a horná hranica kaskády B
ROC-AUC v eskalovanej oblasti = vynechaná rodina vs. neškodné medzi eskalovanými súbormi testu.

| rodina | eskalované | eskalované_z_minutých_S | auc_v_eskalovanej_S | auc_v_eskalovanej_D | auc_v_eskalovanej_H | tpr_S | orakulum_dokonalý_2_stupeň |
|---|---|---|---|---|---|---|---|
| backdoor | 0.218 | 1.000 | 0.995 | 0.769 | 0.994 | 0.984 | 1.000 |
| coinminer | 0.265 | 0.996 | 0.959 | 0.679 | 0.949 | 0.601 | 0.998 |
| dropper | 0.202 | 1.000 | 0.973 | 0.812 | 0.970 | 0.943 | 1.000 |
| keylogger | 0.233 | 0.666 | 0.539 | 0.727 | 0.467 | 0.241 | 0.745 |
| ransomware | 0.231 | 0.974 | 0.994 | 0.738 | 0.995 | 0.982 | 1.000 |
| rat | 0.227 | 0.990 | 0.983 | 0.918 | 0.986 | 0.923 | 0.999 |
| trojan | 0.221 | 1.000 | 0.953 | 0.848 | 0.954 | 0.872 | 1.000 |
| PRIEMER | 0.228 | 0.946 | 0.914 | 0.784 | 0.902 | 0.792 | 0.963 |

## 4. Vynechaná rodina podľa výsledku emulácie (test, seed 0)

| rodina | podskupina | n | tpr_S | tpr_D |
|---|---|---|---|---|
| backdoor | emulácia ok | 1613 | 0.990 | 0.468 |
| backdoor | unsupported_api | 267 | 0.981 | 0.131 |
| backdoor | malý report | 60 | 0.833 | 0.267 |
| coinminer | emulácia ok | 678 | 0.938 | 0.796 |
| coinminer | unsupported_api | 998 | 0.371 | 0.299 |
| coinminer | malý report | 8 | 0.750 | 0.000 |
| dropper | emulácia ok | 178 | 0.933 | 0.787 |
| dropper | unsupported_api | 73 | 0.973 | 0.438 |
| dropper | malý report | 1 | 0.000 | 0.000 |
| keylogger | emulácia ok | 225 | 0.658 | 0.284 |
| keylogger | unsupported_api | 804 | 0.106 | 0.081 |
| keylogger | malý report | 12 | 0.917 | 0.167 |
| ransomware | emulácia ok | 1007 | 0.975 | 0.541 |
| ransomware | unsupported_api | 1091 | 0.986 | 0.052 |
| ransomware | malý report | 41 | 1.000 | 0.171 |
| rat | emulácia ok | 320 | 0.934 | 0.794 |
| rat | unsupported_api | 929 | 0.916 | 0.789 |
| rat | malý report | 9 | 0.778 | 0.000 |
| trojan | emulácia ok | 386 | 0.979 | 0.798 |
| trojan | unsupported_api | 644 | 0.792 | 0.784 |
| trojan | malý report | 55 | 0.945 | 0.218 |
