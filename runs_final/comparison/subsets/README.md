# Výsledky podľa výsledku emulácie (test)

> Generované `src/evaluation/subset_analysis.py` (2026-11-02T21:37:30+01:00), výsledky z `runs_final`.
> Prah z validácie (FPR ≤ 1 %), priemer cez seedy. TPR = zachytený malvér, FPR = falošné poplachy na neškodných.
> Podskupiny podľa auditu dynamických dát (docs/04): malé reporty, emulácia ukončená `unsupported_api`
> (stopa inej verzie emulátora v teste), ostatné.

## Veľkosti podskupín
| podskupina | n_malware | n_benign |
|---|---|---|
| malý report (≤5 volaní) | 186 | 478 |
| ostatné | 4407 | 3174 |
| ukončené unsupported_api | 4806 | 4288 |

## Výsledky
| model | FPR – malý report (≤5 volaní) | FPR – ostatné | FPR – ukončené unsupported_api | TPR – malý report (≤5 volaní) | TPR – ostatné | TPR – ukončené unsupported_api |
|---|---|---|---|---|---|---|
| dynamic/lightgbm | 0.0021 | 0.0243 | 0.0185 | 0.3746 | 0.8291 | 0.5105 |
| dynamic/lr | 0.0021 | 0.0334 | 0.1495 | 0.2312 | 0.5759 | 0.4299 |
| dynamic/mlp_large | 0.0028 | 0.0261 | 0.0072 | 0.3244 | 0.6482 | 0.4268 |
| dynamic/mlp_small | 0.0021 | 0.0272 | 0.0051 | 0.3208 | 0.6611 | 0.4173 |
| dynamic/rf | 0.0021 | 0.0212 | 0.0187 | 0.3280 | 0.7899 | 0.3876 |
| dynamic/seq_cnn | 0.0028 | 0.0527 | 0.0047 | 0.5394 | 0.7857 | 0.4907 |
| hybrid/lightgbm | 0.0119 | 0.0057 | 0.0032 | 0.9319 | 0.9928 | 0.9784 |
| hybrid/lr | 0.0251 | 0.0047 | 0.0047 | 0.8871 | 0.9331 | 0.9043 |
| hybrid/mlp_large | 0.0153 | 0.0047 | 0.0083 | 0.8925 | 0.9533 | 0.9408 |
| hybrid/mlp_small | 0.0258 | 0.0038 | 0.0071 | 0.8817 | 0.9418 | 0.8251 |
| hybrid/rf | 0.0174 | 0.0112 | 0.0061 | 0.9480 | 0.9794 | 0.9202 |
| hybrid/two_branch | 0.0174 | 0.0030 | 0.0066 | 0.8871 | 0.9862 | 0.9714 |
| static/lightgbm | 0.0160 | 0.0054 | 0.0032 | 0.9516 | 0.9927 | 0.9778 |
| static/lr | 0.0418 | 0.0072 | 0.0063 | 0.9194 | 0.9664 | 0.9336 |
| static/mlp_large | 0.0272 | 0.0049 | 0.0054 | 0.9552 | 0.9799 | 0.9804 |
| static/mlp_small | 0.0314 | 0.0050 | 0.0051 | 0.9373 | 0.9756 | 0.9613 |
| static/rf | 0.0146 | 0.0063 | 0.0044 | 0.8978 | 0.9489 | 0.9757 |
| students_dynamic/mlp_kd | 0.0021 | 0.0291 | 0.0100 | 0.3369 | 0.6629 | 0.3989 |
| students_dynamic/mlp_kd_modal | 0.0021 | 0.0269 | 0.0090 | 0.2975 | 0.6510 | 0.3791 |
| students_dynamic/mlp_nokd | 0.0035 | 0.0308 | 0.0096 | 0.4355 | 0.6776 | 0.4161 |
| students_static/mlp_kd | 0.0181 | 0.0047 | 0.0054 | 0.8817 | 0.9696 | 0.9505 |
| students_static/mlp_kd_modal | 0.0258 | 0.0054 | 0.0058 | 0.9194 | 0.9851 | 0.9516 |
| students_static/mlp_nokd | 0.0349 | 0.0064 | 0.0054 | 0.9391 | 0.9734 | 0.9510 |
