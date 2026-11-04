# V2 – krivka rozpočtu emulácie kaskád B (doplnok)

> Generované `src/evaluation/v2_budget.py`. Hlavný pracovný bod = pásmo neistoty (docs/09); rozpočty 10–40 %
> sú doplnková krivka – hranica sa určí na validácii, na teste je podiel emulovaných súborov vyšší (časový posun).
> Stĺpec „téza 2“ = kritérium z docs/09 (FPR < statický aj dynamický LightGBM, TPR ≥ statický − 1 p. b.).

## časový
Referencia: statický LightGBM TPR 0.9843, FPR 0.0048; dynamický LightGBM FPR 0.0198.

| variant | bod | emulované súbory | TPR | FPR | téza 2 |
|---|---|---|---|---|---|
| b_main | pásmo neistoty | 0.1065 | 0.9587 | 0.0034 | nie |
| b_main | rozpočet 10% | 0.1881 | 0.9597 | 0.0037 | nie |
| b_main | rozpočet 20% | 0.3259 | 0.9579 | 0.0035 | nie |
| b_main | rozpočet 30% | 0.4514 | 0.9579 | 0.0034 | nie |
| b_main | rozpočet 40% | 0.5285 | 0.9579 | 0.0033 | nie |
| b_direct | pásmo neistoty | 0.1065 | 0.9674 | 0.0032 | nie |
| b_direct | rozpočet 10% | 0.1881 | 0.9856 | 0.0056 | nie |
| b_direct | rozpočet 20% | 0.3259 | 0.9842 | 0.0054 | nie |
| b_direct | rozpočet 30% | 0.4514 | 0.9842 | 0.0055 | nie |
| b_direct | rozpočet 40% | 0.5285 | 0.9842 | 0.0054 | nie |
| b_heavy | pásmo neistoty | 0.1065 | 0.9528 | 0.0031 | nie |
| b_heavy | rozpočet 10% | 0.1881 | 0.9540 | 0.0032 | nie |
| b_heavy | rozpočet 20% | 0.3259 | 0.9539 | 0.0031 | nie |
| b_heavy | rozpočet 30% | 0.4514 | 0.9537 | 0.0030 | nie |
| b_heavy | rozpočet 40% | 0.5285 | 0.9537 | 0.0029 | nie |
| b_baselines | pásmo neistoty | 0.0035 | 0.9241 | 0.0004 | nie |
| b_baselines | rozpočet 10% | 0.2150 | 0.9831 | 0.0039 | áno |
| b_baselines | rozpočet 20% | 0.3977 | 0.9831 | 0.0039 | áno |
| b_baselines | rozpočet 30% | 0.5522 | 0.9831 | 0.0039 | áno |
| b_baselines | rozpočet 40% | 0.6938 | 0.9831 | 0.0039 | áno |
| b_nokd | pásmo neistoty | 0.0906 | 0.9601 | 0.0035 | nie |
| b_nokd | rozpočet 10% | 0.1768 | 0.9625 | 0.0037 | nie |
| b_nokd | rozpočet 20% | 0.3088 | 0.9608 | 0.0037 | nie |
| b_nokd | rozpočet 30% | 0.3765 | 0.9608 | 0.0036 | nie |
| b_nokd | rozpočet 40% | 0.4285 | 0.9607 | 0.0035 | nie |
| b_twobranch | pásmo neistoty | 0.0853 | 0.9679 | 0.0038 | nie |
| b_twobranch | rozpočet 10% | 0.2017 | 0.9712 | 0.0035 | nie |
| b_twobranch | rozpočet 20% | 0.3009 | 0.9704 | 0.0034 | nie |
| b_twobranch | rozpočet 30% | 0.3986 | 0.9691 | 0.0034 | nie |
| b_twobranch | rozpočet 40% | 0.4718 | 0.9691 | 0.0034 | nie |

## zero-day (priemer cez rodiny)
Referencia: statický LightGBM TPR 0.9598, FPR 0.0047; dynamický LightGBM FPR 0.0184.

| variant | bod | emulované súbory | TPR | FPR | téza 2 |
|---|---|---|---|---|---|
| b_main | pásmo neistoty | 0.1216 | 0.9248 | 0.0030 | nie |
| b_main | rozpočet 10% | 0.2357 | 0.9308 | 0.0031 | nie |
| b_main | rozpočet 20% | 0.3647 | 0.9295 | 0.0030 | nie |
| b_main | rozpočet 30% | 0.4679 | 0.9294 | 0.0029 | nie |
| b_main | rozpočet 40% | 0.5471 | 0.9294 | 0.0029 | nie |
| b_direct | pásmo neistoty | 0.1216 | 0.9321 | 0.0029 | nie |
| b_direct | rozpočet 10% | 0.2357 | 0.9571 | 0.0051 | nie |
| b_direct | rozpočet 20% | 0.3647 | 0.9559 | 0.0051 | nie |
| b_direct | rozpočet 30% | 0.4679 | 0.9557 | 0.0050 | nie |
| b_direct | rozpočet 40% | 0.5471 | 0.9557 | 0.0050 | nie |
| b_heavy | pásmo neistoty | 0.1216 | 0.9203 | 0.0032 | nie |
| b_heavy | rozpočet 10% | 0.2357 | 0.9277 | 0.0034 | nie |
| b_heavy | rozpočet 20% | 0.3647 | 0.9275 | 0.0033 | nie |
| b_heavy | rozpočet 30% | 0.4679 | 0.9273 | 0.0033 | nie |
| b_heavy | rozpočet 40% | 0.5471 | 0.9272 | 0.0033 | nie |
| b_baselines | pásmo neistoty | 0.0086 | 0.8758 | 0.0004 | nie |
| b_baselines | rozpočet 10% | 0.2281 | 0.9536 | 0.0036 | áno |
| b_baselines | rozpočet 20% | 0.4009 | 0.9536 | 0.0036 | áno |
| b_baselines | rozpočet 30% | 0.5922 | 0.9536 | 0.0036 | áno |
| b_baselines | rozpočet 40% | 0.7197 | 0.9536 | 0.0036 | áno |
| b_nokd | pásmo neistoty | 0.1053 | 0.9213 | 0.0031 | nie |
| b_nokd | rozpočet 10% | 0.2057 | 0.9290 | 0.0033 | nie |
| b_nokd | rozpočet 20% | 0.3137 | 0.9282 | 0.0032 | nie |
| b_nokd | rozpočet 30% | 0.3743 | 0.9281 | 0.0032 | nie |
| b_nokd | rozpočet 40% | 0.4339 | 0.9281 | 0.0032 | nie |
| b_twobranch | pásmo neistoty | 0.0884 | 0.9250 | 0.0032 | nie |
| b_twobranch | rozpočet 10% | 0.2081 | 0.9315 | 0.0032 | nie |
| b_twobranch | rozpočet 20% | 0.3244 | 0.9305 | 0.0030 | nie |
| b_twobranch | rozpočet 30% | 0.4265 | 0.9301 | 0.0029 | nie |
| b_twobranch | rozpočet 40% | 0.5007 | 0.9302 | 0.0029 | nie |
