# 20 – Výsledky V4 (KronoDroid)

Stav k 2026-11-24. Plán a kritériá: `docs/19_plan_v4.md` (rozhodnuté 2026-11-22, pred tréningom).
Beh: pracovný notebook (DCATLOCH), 2026-11-22 až 2026-11-23, kód značky `v4` (ZIP), `runs_v4/` (bez uložených modelov).
Súhrn: `runs_v4/comparison/v4/README.md` (`python -m src.evaluation.v4_report --root runs_v4`, bootstrap 2 000 opakovaní),
počítaný na súkromnom notebooku iba z uložených predikcií a meraní. Rozdiely sú v percentuálnych bodoch (p. b.),
v zátvorke 95 % interval spoľahlivosti (IS) z párového bootstrapu testu.

Hlavná miera O1/O2: TPR pri FPR 1 % z ROC krivky testu (metrika vyhodnotenia, nie ladenie). Tézy: prahy z validácie.

## 1. Odpovede na otázky O1 a O2 (docs/19, oddiel 4)
| | čo | rozdiel (IS) | kritérium |
|---|---|---|---|
| **O1** | real_full: hybrid − statický | **+1,78** (+1,15 až +2,38) | **splnené** |
| **O1-Z** | real_full, zero-day (priemer 5 rodín) | **+11,38** (+9,70 až +13,00) | **splnené** |
| Δ real_P | real_P: hybrid − statický | +2,76 (+2,01 až +3,46) | – |
| Δ emu_P | emu_P: hybrid − statický | +2,00 (+1,32 až +2,63) | – |
| **O2** | Δ real_P − Δ emu_P | +0,76 (+0,30 až +1,28) | **nesplnené** (< 1 p. b.) |
| **O2-Z** | to isté, zero-day | **+9,60** (+8,33 až +10,82) | **splnené** |
| D-norm | hybrid s podielmi volaní − statický (real_full / real_P / emu_P) | +1,74 / +2,33 / +1,57 (dolné hranice > +0,88) | prínos **nezmizol** |
| časový posun | real_time (malvér 2015–2020 v teste): hybrid − statický | +5,40 (+3,98 až +7,20) | doplnkovo |

**Záver podľa vopred určenej interpretácie (docs/19, 4.3):** O1 platí, O2 na hlavnom rozdelení neplatí →
„dynamika pomáha na KronoDroid aj z emulátora; rozdiel oproti Quo Vadis je skôr vo vlastnostiach datasetu“.

**Otázka 2 je potvrdená pre nové rodiny.** O2-Z bolo vopred stanovené kritérium (docs/19, 4.2) a je splnené
s veľkou rezervou (+9,6 p. b., dolná hranica IS +8,3). Na hlavnom (náhodnom) rozdelení je rozdiel štatisticky
nenulový (IS +0,30 až +1,28), ale pod vopred stanovenou hranicou 1 p. b., takže O2 v tomto zmysle splnené nie je.
Vopred určená tabuľka 4.3 bola napísaná iba pre O2; nasledujúce spresnenie je popis výsledku, nie zmena kritéria:
- Na **známych rodinách** je rozdiel medzi zariadením a emulátorom malý (+0,76 p. b.) – štatisticky nenulový, ale pod
  vopred stanovenou hranicou 1 p. b.
- Na **nových rodinách** je rozdiel veľký (+9,6 p. b.). Dynamický model zo zariadenia zachytí vynechanú rodinu
  v priemere v 67 % prípadov, z emulátora v 48 %; hybrid 88 % oproti 79 % (statický 74 %). Najväčší rozdiel je pri
  Airpush/StopSMS (hybrid 0,88 vs. 0,67) a Locker/SLocker (0,63 vs. 0,41).
- Zdroj dynamiky teda rozhoduje najmä tam, kde statika nestačí: pri nevidenej rodine.

**D-norm:** prínos hybridu ostal aj po prevode počtov volaní na podiely (bez celkového počtu). Nestojí teda na
celkovom množstve aktivity, ktoré by mohlo byť artefaktom zberu.

## 2. Porovnanie s Quo Vadis (popisne, iba relatívne veličiny – docs/19, oddiel 5)
| | Quo Vadis (V1–V3, Speakeasy) | KronoDroid real_full (zariadenie) |
|---|---|---|
| hybrid − statický, hlavný test | ≈ 0 (−0,01; −0,11 až +0,09) | **+1,78** |
| hybrid − statický, zero-day | −0,51 (−0,83 až −0,22) | **+11,38** |
| strop „statický ALEBO dynamický správne“ nad statickým (prah z val.) | +0,6 p. b. (zero-day) | +3,6 p. b. (0,9820 vs. 0,9459, hlavné) |
| dynamický samostatne, TPR novej rodiny | 0,51 | 0,65 |
| hybrid oproti statickému pri novej rodine | horší | lepší v 4 z 5 rodín (výnimka Locker/SLocker) |

Pri časovom posune ide o iný typ testu (Quo Vadis: 3 mesiace; KronoDroid: malvér 2015–2020 oproti 2008–2014), preto
sa porovnáva iba smer: na Quo Vadis hybrid ≈ statický, na KronoDroid hybrid +5,4 p. b.

**Čo z toho vyplýva:** na KronoDroid dynamika prináša informáciu nad statiku, na Quo Vadis nie. Medzi emulátorom
a zariadením na tých istých APK je rozdiel hlavne pri nových rodinách. Výsledok preto **podporuje**, že slabinou
Quo Vadis boli dáta. Kvalita zdroja dynamiky je jednou z príčin (O2-Z), nie však jedinou: aj z emulátora pomáha
dynamika na KronoDroid viac ako Speakeasy na Quo Vadis (Δ emu_P = +2,0). Zostávajúci rozdiel môže byť v platforme,
type príznakov (systémové volania jadra vs. API volania Windows) a v tom, že emulátor Android spúšťa skutočný
systém, kým Speakeasy iba emuluje API. Toto sa jedným experimentom oddeliť nedá (obmedzenie, oddiel 7).

## 3. Modely na hlavnom rozdelení (priemer cez 3 seedy, test)
Vo všetkých vetvách vybral dohodnutý postup (docs/00) LightGBM pre statický, dynamický aj hybridný prístup.

| vetva | statický | dynamický | hybrid LightGBM | hybrid mlp_large | statický študent `mlp_kd` | dynamický študent `mlp_kd` |
|---|---|---|---|---|---|---|
| real_full | 0,9603 | 0,8730 | **0,9781** | 0,9663 | 0,9020 | 0,7549 |
| real_P | 0,9507 | 0,8586 | **0,9783** | 0,9555 | 0,8717 | 0,7339 |
| emu_P | 0,9507 | 0,8488 | **0,9707** | 0,9566 | 0,8812 | 0,6220 |

(TPR pri FPR 1 % z ROC testu.) Dynamický model zo zariadenia je na hlavnom rozdelení len o ~1 p. b. lepší ako
z emulátora; jeho **študent** však o 11 p. b. (0,73 vs. 0,62).

## 4. Kaskády (prahy z validácie)
Referencia real_full: statický TPR 0,9459 / FPR 0,0062, dynamický 0,8688 / 0,0090.

| kaskáda (real_full) | TPR | FPR | dyn. analýza | téza 2 | TPR novej rodiny | téza 1 |
|---|---|---|---|---|---|---|
| A-baselines (LightGBM) | 0,9687 | 0,0040 | 100 % | **áno** | 0,7902 | **áno** |
| B-baselines (LightGBM) | 0,9656 | 0,0042 | 16,6 % | **áno** | 0,7723 | **áno** |
| B-baselines, rozpočet 10 % | 0,9617 | 0,0038 | 10,3 % | **áno** | 0,7574 | **áno** |
| A-main (študenti) | 0,9397 | 0,0030 | 100 % | **áno** | 0,7619 | **áno** |
| B-main (študenti) | 0,9369 | 0,0029 | 38,3 % | **áno** | 0,7439 | **áno** |
| B-direct | 0,9692 | 0,0068 | 38,3 % | nie (FPR) | 0,8174 | nie (FPR) |
| špecialista B-spec (10 %) | 0,9740 | 0,0094 | 10,3 % | nie (FPR) | 0,8132 | nie (FPR) |

Statický model pri prahu z validácie zachytí novú rodinu v priemere v 0,678 (oddiel 6); hodnota 0,735 v oddiele 1
je TPR pri FPR 1 % z ROC testu, teda iná miera.

Oproti statickému modelu (bootstrap, všetky varianty v README):
- kaskády z LightGBM (A-baselines, B-baselines aj B-baselines 10 %) majú **vyššie TPR** (+1,6 až +2,3 p. b.)
  **a nižšie FPR** (−0,2 p. b.) vo všetkých troch vetvách, s IS mimo nuly;
- kaskády so študentmi majú nižšie FPR, ale aj nižšie TPR (real_full −0,4 až −1,3; emu_P −3,7 až −5,8 p. b.),
  lebo dynamický študent je slabý.

## 5. Tézy (kritériá docs/09; hlavná vetva real_full, doplnkovo real_P a emu_P)
| téza | real_full | real_P | emu_P | Quo Vadis (docs/14) |
|---|---|---|---|---|
| 1. zero-day: kaskáda ≥ statický + 1 p. b., FPR ≤ | **áno** (všetky kaskády okrem B-direct a špecialistov) | **áno** pre väčšinu (nie A-main, B-main, B-heavy) | **áno** iba z LightGBM a B-direct | nie |
| 2. FPR nižšie než statický aj dynamický, TPR v tolerancii 1 p. b. | **áno** pre 9 z 13 kaskád | áno pre LightGBM a nokd | áno iba z LightGBM a B-direct | áno (z LightGBM) |
| 3. študent ≈ `mlp_large` hybrid (±1 p. b.), rýchlejší | **nie** (−8 až −34 p. b.) | nie | nie | čiastočne |
| 4. podiel dynamickej analýzy pri splnení tézy 2 | **10,3 %** (B-baselines 10 %) | 10,6 % | 10,6 % | 21,5 % |

**Téza 1 sa na KronoDroid potvrdzuje,** na Quo Vadis nie. Najlepšia kaskáda splňujúca kritérium na real_full
(A-baselines) zachytí novú rodinu v 79,0 % oproti 67,8 % statického modelu (obe pri prahu z validácie) pri nižšom FPR.

**Téza 3 sa nepotvrdzuje vo všetkých vetvách.** Nie je to chyba destilácie: študent bez učiteľa (`mlp_nokd`) je rovnako
dobrý (real_full statický 0,910 vs. 0,902 s učiteľom). Malá sieť (~10 tis. parametrov) na binárnych oprávneniach a počtoch
volaní nedosiahne LightGBM ani `mlp_large`. Študenti sú pritom 2–7× rýchlejší (CPU 0,03–0,05 ms/vzorku oproti
0,11–0,24 ms pre `mlp_large`).

## 6. Špecialista V3 (kritériá B1–B3, docs/19, 3.4)
| vetva | TPR novej rodiny: špecialista / statický | rodiny spec ≥ stat | FPR spec / stat (hlavné) | B1 | B2 | B3 |
|---|---|---|---|---|---|---|
| real_full | 0,813 / 0,678 | 5 z 5 | 0,0094 / 0,0062 | nie | nie | nie |
| real_P | 0,809 / 0,711 | 5 z 5 | 0,0083 / 0,0080 | nie | nie | nie |
| emu_P | 0,753 / 0,711 | 5 z 5 | 0,0076 / 0,0080 | nie | **áno** | nie |

Špecialista zachytí novú rodinu výrazne lepšie (+10 až +14 p. b. pri zariadení, +4 p. b. pri emulátore) a je lepší
vo všetkých 5 rodinách vo všetkých vetvách. Platí to však **za cenu vyššieho FPR** (real_full 0,94 % oproti 0,62 %),
preto B1 a B3 nie sú splnené (vyžadujú FPR nanajvýš ako statický, resp. +0,1 p. b.); B2 je splnené iba v emu_P.

**Prečo to uviesť:** na Quo Vadis špecialista nepriniesol nič (pri rovnakom FPR rovnaký ako statický, docs/13, 17).
Na KronoDroid sa v neistej oblasti naučil niečo, čo statika nemá – zisk je väčší pri dynamike zo zariadenia
(real_P +9,8 p. b.) než z emulátora (emu_P +4,2 p. b., tie isté APK), čo je v súlade s O2-Z. FPR celej kaskády ostáva pod 1 %, ktoré bolo
cieľom prahu (docs/19, 3.4, bod 5). Podľa vopred určeného kritéria to však nie je zlepšenie pri rovnakom FPR;
v práci uviesť ako pozitívne pozorovanie s výhradou, nie ako splnené kritérium.

## 7. Výpočtové nároky (real_full, benchmark seed 0, CPU ms na vzorku v dávke)
| model | CPU ms/vz. | parametre / uzly | tréning s (seed) | ladenie s |
|---|---|---|---|---|
| statický LightGBM | 0,205 | 498 553 | 13,4 | 725 |
| dynamický LightGBM | 0,241 | 434 868 | 17,2 | 713 |
| hybrid LightGBM | 0,179 | 357 120 | 19,1 | 949 |
| hybrid `mlp_large` | 0,115 | 317 697 | 13,7 | 279 |
| statický študent `mlp_kd` | 0,048 | 10 753 | 5,2 | 243 |
| dynamický študent `mlp_kd` | 0,035 | 8 641 | 13,2 | 334 |

- Odhad kaskády B-baselines (10 %): 0,236 ms/vzorku – drahšia na CPU ako samostatný statický model (0,205), ale
  dynamickú analýzu potrebuje iba 10,3 % súborov.
- **Čas dynamickej analýzy (behu APK na zariadení / v emulátore) KronoDroid neuvádza**, preto ju nemožno do nákladov
  započítať (ako pri Quo Vadis). Úspora kaskády B je vyjadrená iba podielom súborov.
- Absolútne časy sú porovnateľné iba v rámci V4 (iná veľkosť dát ako Quo Vadis); merané na tom istom notebooku ako V1–V3.

## 8. Obmedzenia
1. **Jeden dataset, jedna platforma:** rozdiel Quo Vadis vs. KronoDroid zahŕňa platformu (Windows PE vs. Android),
   typ príznakov aj zdroj dynamiky. O2 oddeľuje iba zdroj dynamiky na tých istých APK.
2. **Náhodné rozdelenie** na hlavnom teste (Quo Vadis: časový test). Časový posun je iba doplnkový a týka sa len
   malvéru (neškodné súbory nemajú spoľahlivé dátumy, docs/18).
3. **Dynamika = počty systémových volaní** (288 + celkový počet), bez sekvencií; sekvenčné modely z V1 sa nepoužili.
4. **Emulátor v KronoDroid** je emulátor Android (skutočný systém vo virtuálnom stroji), nie emulácia API ako Speakeasy –
   „emulátor“ v O2 preto nie je rovnaký typ prostredia ako na Quo Vadis.
5. **Rodiny zero-day:** 5 rodín (Quo Vadis 7); Locker/SLocker je jediná, kde hybrid nie je lepší ako dynamický model.
6. Interpretácia O2 vs. O2-Z: vopred určená tabuľka (docs/19, 4.3) pokrýva iba O2; spresnenie v oddiele 1 je
   popis výsledku, nie zmena kritéria.

## 9. Čo to znamená pre prácu
- Na kvalitnejšom datasete s dynamikou zo zariadenia **dynamika pomáha** (O1 aj O1-Z), najmä pri nových rodinách
  (+11 p. b.), a nestojí iba na množstve aktivity (D-norm).
- **Téza 1 (zero-day) sa potvrdzuje na KronoDroid**, na Quo Vadis nie → záver V1–V3 „dynamika nepridáva informáciu“
  je vlastnosť datasetu Quo Vadis, nie návrhu kaskády.
- **Téza 2 a 4 platia na oboch datasetoch** pre kaskády z LightGBM; na KronoDroid stačí dynamická analýza 10 % súborov
  a kaskáda je navyše citlivejšia ako statický model.
- **Téza 3 neplatí** na KronoDroid (malí študenti sú výrazne slabší); na Quo Vadis platila čiastočne.
- **Zariadenie vs. emulátor (O2):** potvrdené pre nové rodiny (O2-Z +9,6 p. b., vopred určené kritérium splnené);
  na známych rodinách malý rozdiel (+0,76 p. b.), pod hranicou 1 p. b.
- **Špecialista V3:** kritériá B1 a B3 nesplnené (vyšší FPR), ale na rozdiel od Quo Vadis zlepšuje detekciu nových
  rodín vo všetkých rodinách, viac pri dynamike zo zariadenia – uviesť ako pozorovanie s výhradou.
