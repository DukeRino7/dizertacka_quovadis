# Komplementarita statického, dynamického a hybridného modelu (test)

> Generované `src/evaluation/complementarity.py`. Vybrané modely z `selection/`; prah z validácie (FPR ≤ 1%), test sa na nič nenastavuje. Počty vzoriek, priemer cez seedy 0–2.

Modely: static = `runs_v4/emu_p/full/static/lightgbm/20261122-231010`, dynamic = `runs_v4/emu_p/full/dynamic/lightgbm/20261123-191933`, hybrid = `runs_v4/emu_p/full/hybrid/lightgbm/20261123-195420`

## Súhrn (priemer cez seedy)

| trieda | n | chyby statický | chyby dynamický | chyby hybrid | hybrid opraví chybu statického | hybrid pokazí správne statického | dynamický správne pri chybe statického | chyba všetkých troch |
|---|---|---|---|---|---|---|---|---|
| benign | 6983.0 | 56.0 | 55.7 | 42.0 | 33.7 | 19.7 | 52.3 | 3.0 |
| malware | 5673.0 | 315.7 | 918.7 | 209.0 | 155.3 | 48.7 | 137.0 | 134.3 |

## Podľa rodiny (seed 0)

| rodina | n | chyby statický | chyby dynamický | chyby hybrid | dynamický správne pri chybe statického |
|---|---|---|---|---|---|
| Adwo | 6 | 0 | 4 | 0 | 0 |
| Agent | 393 | 14 | 77 | 16 | 3 |
| Airpush/StopSMS | 1308 | 84 | 116 | 40 | 54 |
| AnServer/Answerbot | 7 | 1 | 1 | 1 | 0 |
| BankBot | 245 | 0 | 12 | 1 | 0 |
| Booster | 11 | 0 | 3 | 0 | 0 |
| Boxer | 709 | 1 | 15 | 1 | 1 |
| Coogos | 23 | 2 | 11 | 2 | 0 |
| Cosha | 9 | 2 | 2 | 2 | 2 |
| Counterclank | 15 | 5 | 7 | 5 | 1 |
| Dialer | 12 | 0 | 2 | 1 | 0 |
| Dnotua | 20 | 0 | 13 | 0 | 0 |
| Dowgin | 171 | 1 | 28 | 2 | 0 |
| DroidDream | 11 | 4 | 7 | 3 | 1 |
| DroidJack/SandoRAT | 11 | 0 | 1 | 0 | 0 |
| DroidKungFu | 58 | 9 | 23 | 6 | 3 |
| FakeAngry | 11 | 4 | 6 | 3 | 2 |
| FakeApp | 190 | 21 | 37 | 3 | 18 |
| FakeBank | 60 | 0 | 1 | 1 | 0 |
| FakeDoc | 30 | 0 | 1 | 0 | 0 |
| FakeFlash | 10 | 0 | 1 | 0 | 0 |
| FakeInst | 426 | 8 | 76 | 7 | 0 |
| Gamex | 11 | 1 | 3 | 2 | 1 |
| Gappusin | 12 | 4 | 8 | 2 | 3 |
| GinMaster | 112 | 3 | 25 | 3 | 0 |
| GoldDream | 15 | 1 | 9 | 1 | 0 |
| HiddenAds | 27 | 0 | 1 | 0 | 0 |
| HongTouTou/Adrd | 17 | 0 | 12 | 1 | 0 |
| Iconosys | 30 | 2 | 5 | 2 | 1 |
| Kmin | 16 | 0 | 3 | 0 | 0 |
| Ksapp | 11 | 0 | 9 | 0 | 0 |
| Kuguo | 98 | 5 | 31 | 6 | 1 |
| LinuxLotoor | 8 | 2 | 6 | 4 | 0 |
| Locker/SLocker Ransomware | 325 | 13 | 74 | 9 | 9 |
| Lovetrap/Luvrtrap | 8 | 0 | 2 | 0 | 0 |
| Malap | 501 | 19 | 36 | 1 | 1 |
| MimobSMS | 20 | 0 | 1 | 0 | 0 |
| MobiDash | 29 | 0 | 2 | 0 | 0 |
| MobileSpy/Godwon | 44 | 3 | 14 | 4 | 0 |
| Mseg | 17 | 0 | 15 | 0 | 0 |
| Nandrobox | 13 | 0 | 7 | 1 | 0 |
| OpFake | 23 | 1 | 4 | 1 | 0 |
| Plankton | 8 | 2 | 4 | 1 | 1 |
| Robtes | 29 | 1 | 12 | 0 | 1 |
| RuFraud | 11 | 1 | 2 | 1 | 1 |
| SMSSend | 42 | 1 | 9 | 1 | 1 |
| SMSreg | 82 | 6 | 19 | 4 | 1 |
| SMSspy | 10 | 0 | 3 | 0 | 0 |
| SmForw | 7 | 0 | 2 | 0 | 0 |
| SmsPay | 5 | 0 | 1 | 0 | 0 |
| TrojanSMS.Stealer | 16 | 0 | 1 | 2 | 0 |
| Vdloader | 5 | 0 | 2 | 0 | 0 |
| Waps/Simhosy | 41 | 7 | 15 | 4 | 5 |
| Wooboo | 28 | 2 | 14 | 3 | 0 |
| Youmi | 93 | 26 | 64 | 32 | 2 |
| benign | 6983 | 63 | 54 | 41 | 58 |
| other | 204 | 27 | 62 | 24 | 6 |
| unknown | 19 | 7 | 8 | 6 | 3 |
