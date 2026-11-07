# V3 – C: prekalibrovanie prahu na nových neškodných súboroch (samostatný scenár)

> Generované `src/evaluation/v3_recalibration.py`. Plán: `docs/12_plan_v3.md`, bod 3. Kalibrácia používa iba
> neškodné súbory aprílového testu (kalibračná časť), hodnotí sa na zvyšku testu; malvér kalibrácia nevidí.
> 10 náhodných rozdelení × seedy, hodnota = priemer ± sm. odchýlka cez rozdelenia a seedy.
> „pôvodný“ = prahy z validácie na tej istej hodnotiacej časti. Hlavné výsledky V1–V3 sa týmto nemenia.

## 1. Časový test – TPR všetkého malvéru

| kalibrácia (podiel neškodných) | prístup | TPR pôvodný | TPR prekalibrovaný | FPR pôvodný | FPR prekalibrovaný |
|---|---|---|---|---|---|
| 1% | statický LightGBM | 0.9843 ± 0.0004 | 0.9761 ± 0.0429 | 0.0048 ± 0.0002 | 0.0152 ± 0.0153 |
| 1% | dynamický LightGBM | 0.6572 ± 0.0057 | 0.5699 ± 0.1522 | 0.0198 ± 0.0039 | 0.0158 ± 0.0151 |
| 1% | hybrid LightGBM | 0.9842 ± 0.0030 | 0.9644 ± 0.0690 | 0.0047 ± 0.0002 | 0.0161 ± 0.0169 |
| 1% | hybrid dvojvetvová sieť | 0.9767 ± 0.0043 | 0.8996 ± 0.2191 | 0.0058 ± 0.0007 | 0.0144 ± 0.0158 |
| 1% | kaskáda A-main | 0.9579 ± 0.0039 | 0.9094 ± 0.1913 | 0.0026 ± 0.0001 | 0.0069 ± 0.0065 |
| 1% | kaskáda A-baselines | 0.9831 ± 0.0015 | 0.9636 ± 0.0694 | 0.0039 ± 0.0001 | 0.0125 ± 0.0134 |
| 1% | kaskáda B-main | 0.9587 ± 0.0050 | 0.9441 ± 0.0506 | 0.0034 ± 0.0001 | 0.0040 ± 0.0017 |
| 1% | kaskáda B-baselines (rozpočet 10 %) | 0.9831 ± 0.0015 | 0.9713 ± 0.0469 | 0.0039 ± 0.0001 | 0.0125 ± 0.0134 |
| 1% | kaskáda V3 špecialista (hybrid) | 0.9891 ± 0.0033 | 0.9785 ± 0.0382 | 0.0052 ± 0.0005 | 0.0119 ± 0.0130 |
| 1% | kaskáda V3 špecialista (dynamika) | 0.9889 ± 0.0028 | 0.9754 ± 0.0261 | 0.0048 ± 0.0009 | 0.0071 ± 0.0083 |
| 5% | statický LightGBM | 0.9843 ± 0.0004 | 0.9902 ± 0.0061 | 0.0047 ± 0.0003 | 0.0076 ± 0.0031 |
| 5% | dynamický LightGBM | 0.6572 ± 0.0057 | 0.5567 ± 0.0779 | 0.0197 ± 0.0038 | 0.0089 ± 0.0049 |
| 5% | hybrid LightGBM | 0.9842 ± 0.0030 | 0.9876 ± 0.0079 | 0.0047 ± 0.0002 | 0.0085 ± 0.0038 |
| 5% | hybrid dvojvetvová sieť | 0.9767 ± 0.0043 | 0.9836 ± 0.0094 | 0.0058 ± 0.0007 | 0.0086 ± 0.0037 |
| 5% | kaskáda A-main | 0.9579 ± 0.0039 | 0.9586 ± 0.0245 | 0.0026 ± 0.0001 | 0.0031 ± 0.0013 |
| 5% | kaskáda A-baselines | 0.9831 ± 0.0015 | 0.9864 ± 0.0074 | 0.0038 ± 0.0002 | 0.0058 ± 0.0022 |
| 5% | kaskáda B-main | 0.9587 ± 0.0050 | 0.9550 ± 0.0204 | 0.0034 ± 0.0002 | 0.0038 ± 0.0010 |
| 5% | kaskáda B-baselines (rozpočet 10 %) | 0.9831 ± 0.0015 | 0.9864 ± 0.0074 | 0.0038 ± 0.0002 | 0.0058 ± 0.0022 |
| 5% | kaskáda V3 špecialista (hybrid) | 0.9891 ± 0.0033 | 0.9909 ± 0.0062 | 0.0051 ± 0.0006 | 0.0080 ± 0.0048 |
| 5% | kaskáda V3 špecialista (dynamika) | 0.9889 ± 0.0028 | 0.9898 ± 0.0084 | 0.0047 ± 0.0009 | 0.0073 ± 0.0035 |
| 20% | statický LightGBM | 0.9843 ± 0.0004 | 0.9934 ± 0.0020 | 0.0047 ± 0.0004 | 0.0090 ± 0.0020 |
| 20% | dynamický LightGBM | 0.6572 ± 0.0057 | 0.5764 ± 0.0195 | 0.0197 ± 0.0039 | 0.0095 ± 0.0022 |
| 20% | hybrid LightGBM | 0.9842 ± 0.0030 | 0.9903 ± 0.0031 | 0.0046 ± 0.0005 | 0.0094 ± 0.0028 |
| 20% | hybrid dvojvetvová sieť | 0.9767 ± 0.0043 | 0.9874 ± 0.0053 | 0.0057 ± 0.0009 | 0.0097 ± 0.0036 |
| 20% | kaskáda A-main | 0.9579 ± 0.0039 | 0.9713 ± 0.0162 | 0.0025 ± 0.0004 | 0.0039 ± 0.0015 |
| 20% | kaskáda A-baselines | 0.9831 ± 0.0015 | 0.9898 ± 0.0027 | 0.0039 ± 0.0004 | 0.0068 ± 0.0016 |
| 20% | kaskáda B-main | 0.9587 ± 0.0050 | 0.9649 ± 0.0118 | 0.0034 ± 0.0005 | 0.0043 ± 0.0011 |
| 20% | kaskáda B-baselines (rozpočet 10 %) | 0.9831 ± 0.0015 | 0.9898 ± 0.0027 | 0.0039 ± 0.0004 | 0.0068 ± 0.0016 |
| 20% | kaskáda V3 špecialista (hybrid) | 0.9891 ± 0.0033 | 0.9940 ± 0.0022 | 0.0051 ± 0.0007 | 0.0092 ± 0.0024 |
| 20% | kaskáda V3 špecialista (dynamika) | 0.9889 ± 0.0028 | 0.9944 ± 0.0012 | 0.0048 ± 0.0010 | 0.0097 ± 0.0027 |

## 2. Zero-day – TPR vynechanej rodiny (priemer cez 7 rodín: backdoor, coinminer, dropper, keylogger, ransomware, rat, trojan)

| kalibrácia (podiel neškodných) | prístup | TPR pôvodný | TPR prekalibrovaný | FPR pôvodný | FPR prekalibrovaný |
|---|---|---|---|---|---|
| 1% | statický LightGBM | 0.7922 ± 0.0019 | 0.7905 ± 0.1127 | 0.0047 ± 0.0002 | 0.0150 ± 0.0145 |
| 1% | dynamický LightGBM | 0.5094 ± 0.0046 | 0.4062 ± 0.1515 | 0.0184 ± 0.0006 | 0.0142 ± 0.0130 |
| 1% | hybrid LightGBM | 0.7870 ± 0.0027 | 0.7872 ± 0.1117 | 0.0045 ± 0.0002 | 0.0149 ± 0.0151 |
| 1% | hybrid dvojvetvová sieť | 0.7614 ± 0.0076 | 0.7247 ± 0.1585 | 0.0068 ± 0.0004 | 0.0135 ± 0.0086 |
| 1% | kaskáda A-main | 0.7392 ± 0.0044 | 0.7177 ± 0.1669 | 0.0023 ± 0.0001 | 0.0066 ± 0.0057 |
| 1% | kaskáda A-baselines | 0.7797 ± 0.0011 | 0.7825 ± 0.1075 | 0.0036 ± 0.0001 | 0.0114 ± 0.0119 |
| 1% | kaskáda B-main | 0.7309 ± 0.0058 | 0.7109 ± 0.0727 | 0.0030 ± 0.0002 | 0.0035 ± 0.0014 |
| 1% | kaskáda B-baselines (rozpočet 10 %) | 0.7797 ± 0.0011 | 0.7835 ± 0.1051 | 0.0036 ± 0.0001 | 0.0114 ± 0.0119 |
| 1% | kaskáda V3 špecialista (hybrid) | 0.7903 ± 0.0032 | 0.7978 ± 0.0807 | 0.0055 ± 0.0002 | 0.0118 ± 0.0108 |
| 1% | kaskáda V3 špecialista (dynamika) | 0.7799 ± 0.0091 | 0.7808 ± 0.0703 | 0.0049 ± 0.0005 | 0.0080 ± 0.0084 |
| 5% | statický LightGBM | 0.7922 ± 0.0019 | 0.8167 ± 0.0300 | 0.0046 ± 0.0002 | 0.0072 ± 0.0028 |
| 5% | dynamický LightGBM | 0.5094 ± 0.0046 | 0.3953 ± 0.0891 | 0.0183 ± 0.0006 | 0.0081 ± 0.0040 |
| 5% | hybrid LightGBM | 0.7870 ± 0.0027 | 0.8075 ± 0.0210 | 0.0044 ± 0.0003 | 0.0085 ± 0.0032 |
| 5% | hybrid dvojvetvová sieť | 0.7614 ± 0.0076 | 0.7720 ± 0.0149 | 0.0068 ± 0.0004 | 0.0088 ± 0.0024 |
| 5% | kaskáda A-main | 0.7392 ± 0.0044 | 0.7501 ± 0.0142 | 0.0023 ± 0.0001 | 0.0033 ± 0.0011 |
| 5% | kaskáda A-baselines | 0.7797 ± 0.0011 | 0.7980 ± 0.0202 | 0.0035 ± 0.0001 | 0.0056 ± 0.0021 |
| 5% | kaskáda B-main | 0.7309 ± 0.0058 | 0.7373 ± 0.0112 | 0.0030 ± 0.0002 | 0.0035 ± 0.0006 |
| 5% | kaskáda B-baselines (rozpočet 10 %) | 0.7797 ± 0.0011 | 0.7980 ± 0.0202 | 0.0035 ± 0.0001 | 0.0056 ± 0.0021 |
| 5% | kaskáda V3 špecialista (hybrid) | 0.7903 ± 0.0032 | 0.8100 ± 0.0304 | 0.0055 ± 0.0002 | 0.0076 ± 0.0028 |
| 5% | kaskáda V3 špecialista (dynamika) | 0.7799 ± 0.0091 | 0.8094 ± 0.0304 | 0.0048 ± 0.0005 | 0.0077 ± 0.0024 |
| 20% | statický LightGBM | 0.7922 ± 0.0019 | 0.8280 ± 0.0216 | 0.0045 ± 0.0003 | 0.0089 ± 0.0020 |
| 20% | dynamický LightGBM | 0.5094 ± 0.0046 | 0.4105 ± 0.0390 | 0.0184 ± 0.0009 | 0.0089 ± 0.0020 |
| 20% | hybrid LightGBM | 0.7870 ± 0.0027 | 0.8105 ± 0.0112 | 0.0043 ± 0.0004 | 0.0093 ± 0.0023 |
| 20% | hybrid dvojvetvová sieť | 0.7614 ± 0.0076 | 0.7776 ± 0.0124 | 0.0068 ± 0.0006 | 0.0099 ± 0.0030 |
| 20% | kaskáda A-main | 0.7392 ± 0.0044 | 0.7610 ± 0.0160 | 0.0022 ± 0.0003 | 0.0040 ± 0.0015 |
| 20% | kaskáda A-baselines | 0.7797 ± 0.0011 | 0.8044 ± 0.0111 | 0.0035 ± 0.0003 | 0.0067 ± 0.0017 |
| 20% | kaskáda B-main | 0.7309 ± 0.0058 | 0.7426 ± 0.0090 | 0.0030 ± 0.0005 | 0.0037 ± 0.0009 |
| 20% | kaskáda B-baselines (rozpočet 10 %) | 0.7797 ± 0.0011 | 0.8044 ± 0.0111 | 0.0035 ± 0.0003 | 0.0067 ± 0.0017 |
| 20% | kaskáda V3 špecialista (hybrid) | 0.7903 ± 0.0032 | 0.8307 ± 0.0227 | 0.0054 ± 0.0004 | 0.0092 ± 0.0019 |
| 20% | kaskáda V3 špecialista (dynamika) | 0.7799 ± 0.0091 | 0.8364 ± 0.0225 | 0.0049 ± 0.0006 | 0.0097 ± 0.0026 |

## 3. Téza 2 v scenári C (FPR < statický aj dynamický, TPR všetkého malvéru ≥ statický − 1 p. b.)

| kalibrácia | test | kaskáda | FPR | TPR | FPR statický | FPR dynamický | TPR statický | spĺňa |
|---|---|---|---|---|---|---|---|---|
| 1% | časový | kaskáda A-main | 0.0069 | 0.9094 | 0.0152 | 0.0158 | 0.9761 | nie |
| 1% | časový | kaskáda A-baselines | 0.0125 | 0.9636 | 0.0152 | 0.0158 | 0.9761 | nie |
| 1% | časový | kaskáda B-main | 0.0040 | 0.9441 | 0.0152 | 0.0158 | 0.9761 | nie |
| 1% | časový | kaskáda B-baselines (rozpočet 10 %) | 0.0125 | 0.9713 | 0.0152 | 0.0158 | 0.9761 | áno |
| 1% | časový | kaskáda V3 špecialista (hybrid) | 0.0119 | 0.9785 | 0.0152 | 0.0158 | 0.9761 | áno |
| 1% | časový | kaskáda V3 špecialista (dynamika) | 0.0071 | 0.9754 | 0.0152 | 0.0158 | 0.9761 | áno |
| 5% | časový | kaskáda A-main | 0.0031 | 0.9586 | 0.0076 | 0.0089 | 0.9902 | nie |
| 5% | časový | kaskáda A-baselines | 0.0058 | 0.9864 | 0.0076 | 0.0089 | 0.9902 | áno |
| 5% | časový | kaskáda B-main | 0.0038 | 0.9550 | 0.0076 | 0.0089 | 0.9902 | nie |
| 5% | časový | kaskáda B-baselines (rozpočet 10 %) | 0.0058 | 0.9864 | 0.0076 | 0.0089 | 0.9902 | áno |
| 5% | časový | kaskáda V3 špecialista (hybrid) | 0.0080 | 0.9909 | 0.0076 | 0.0089 | 0.9902 | nie |
| 5% | časový | kaskáda V3 špecialista (dynamika) | 0.0073 | 0.9898 | 0.0076 | 0.0089 | 0.9902 | áno |
| 20% | časový | kaskáda A-main | 0.0039 | 0.9713 | 0.0090 | 0.0095 | 0.9934 | nie |
| 20% | časový | kaskáda A-baselines | 0.0068 | 0.9898 | 0.0090 | 0.0095 | 0.9934 | áno |
| 20% | časový | kaskáda B-main | 0.0043 | 0.9649 | 0.0090 | 0.0095 | 0.9934 | nie |
| 20% | časový | kaskáda B-baselines (rozpočet 10 %) | 0.0068 | 0.9898 | 0.0090 | 0.0095 | 0.9934 | áno |
| 20% | časový | kaskáda V3 špecialista (hybrid) | 0.0092 | 0.9940 | 0.0090 | 0.0095 | 0.9934 | nie |
| 20% | časový | kaskáda V3 špecialista (dynamika) | 0.0097 | 0.9944 | 0.0090 | 0.0095 | 0.9934 | nie |
| 1% | zero-day | kaskáda A-main | 0.0066 | 0.8900 | 0.0150 | 0.0142 | 0.9494 | nie |
| 1% | zero-day | kaskáda A-baselines | 0.0114 | 0.9405 | 0.0150 | 0.0142 | 0.9494 | áno |
| 1% | zero-day | kaskáda B-main | 0.0035 | 0.9074 | 0.0150 | 0.0142 | 0.9494 | nie |
| 1% | zero-day | kaskáda B-baselines (rozpočet 10 %) | 0.0114 | 0.9448 | 0.0150 | 0.0142 | 0.9494 | áno |
| 1% | zero-day | kaskáda V3 špecialista (hybrid) | 0.0118 | 0.9563 | 0.0150 | 0.0142 | 0.9494 | áno |
| 1% | zero-day | kaskáda V3 špecialista (dynamika) | 0.0080 | 0.9447 | 0.0150 | 0.0142 | 0.9494 | áno |
| 5% | zero-day | kaskáda A-main | 0.0033 | 0.9383 | 0.0072 | 0.0081 | 0.9653 | nie |
| 5% | zero-day | kaskáda A-baselines | 0.0056 | 0.9602 | 0.0072 | 0.0081 | 0.9653 | áno |
| 5% | zero-day | kaskáda B-main | 0.0035 | 0.9277 | 0.0072 | 0.0081 | 0.9653 | nie |
| 5% | zero-day | kaskáda B-baselines (rozpočet 10 %) | 0.0056 | 0.9602 | 0.0072 | 0.0081 | 0.9653 | áno |
| 5% | zero-day | kaskáda V3 špecialista (hybrid) | 0.0076 | 0.9664 | 0.0072 | 0.0081 | 0.9653 | nie |
| 5% | zero-day | kaskáda V3 špecialista (dynamika) | 0.0077 | 0.9593 | 0.0072 | 0.0081 | 0.9653 | nie |
| 20% | zero-day | kaskáda A-main | 0.0040 | 0.9469 | 0.0089 | 0.0089 | 0.9708 | nie |
| 20% | zero-day | kaskáda A-baselines | 0.0067 | 0.9645 | 0.0089 | 0.0089 | 0.9708 | áno |
| 20% | zero-day | kaskáda B-main | 0.0037 | 0.9322 | 0.0089 | 0.0089 | 0.9708 | nie |
| 20% | zero-day | kaskáda B-baselines (rozpočet 10 %) | 0.0067 | 0.9645 | 0.0089 | 0.0089 | 0.9708 | áno |
| 20% | zero-day | kaskáda V3 špecialista (hybrid) | 0.0092 | 0.9725 | 0.0089 | 0.0089 | 0.9708 | nie |
| 20% | zero-day | kaskáda V3 špecialista (dynamika) | 0.0097 | 0.9681 | 0.0089 | 0.0089 | 0.9708 | nie |
