# Komplementarita statického, dynamického a hybridného modelu (test)

> Generované `src/evaluation/complementarity.py`. Vybrané modely z `selection/`; prah z validácie (FPR ≤ 1%), test sa na nič nenastavuje. Počty vzoriek, priemer cez seedy 0–2.

Modely: static = `runs_final/static/lightgbm/20261101-215345`, dynamic = `runs_final/dynamic/lightgbm/20261102-003953`, hybrid = `runs_final/hybrid/lightgbm/20261102-052826`

## Súhrn (priemer cez seedy)

| trieda | n | chyby statický | chyby dynamický | chyby hybrid | hybrid opraví chybu statického | hybrid pokazí správne statického | dynamický správne pri chybe statického | chyba všetkých troch |
|---|---|---|---|---|---|---|---|---|
| benign | 7940.0 | 38.3 | 157.3 | 37.3 | 11.3 | 10.3 | 32.3 | 5.0 |
| malware | 9399.0 | 147.7 | 3222.0 | 148.3 | 25.7 | 26.3 | 23.3 | 106.7 |

## Podľa rodiny (seed 0)

| rodina | n | chyby statický | chyby dynamický | chyby hybrid | dynamický správne pri chybe statického |
|---|---|---|---|---|---|
| backdoor | 1940 | 3 | 289 | 11 | 3 |
| benign | 7940 | 37 | 181 | 37 | 32 |
| coinminer | 1684 | 34 | 694 | 44 | 9 |
| dropper | 252 | 2 | 76 | 1 | 0 |
| keylogger | 1041 | 30 | 838 | 33 | 1 |
| ransomware | 2139 | 14 | 927 | 14 | 3 |
| rat | 1258 | 12 | 165 | 13 | 1 |
| trojan | 1085 | 48 | 196 | 47 | 2 |
