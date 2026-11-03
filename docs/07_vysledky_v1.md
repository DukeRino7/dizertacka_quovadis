# 07 – Výsledky V1 (finálny beh)

Stav k 2026-11-03. Zdroj: `runs_final/` – finálny beh kódu značky `v1` (ZIP, `VERSION.txt` = v1) na pracovnom
notebooku DCATLOCH (16/24 jadier, RTX 4060 Laptop), 2026-11-01 21:28 – 2026-11-02 21:37 (`runs_final/RUN_INFO.txt`).
Všetkých 35 krokov skončilo (`runs_final/_state/`). Všetky merania nárokov sú z jedného počítača.

Pravidlá výberu a vykazovania podľa `docs/00` (dohodnuté vopred). Všetky čísla sú na **teste**
(apríl 2022, 17 339 vzoriek: 9 399 malvér, 7 940 neškodné), prahy sú z validácie (FPR ≤ 1 %), priemer cez seedy 0–2.
CPU čas = oficiálny benchmark (ms na vzorku, dávka, iba inferencia vrátane úpravy vstupu). Čísla sú prevzaté
z výstupov skriptov; odkazy na zdroj sú pri každej časti. Body označené **Interpretácia** sú môj návrh výkladu,
nie odsúhlasený záver.

## 1. Vybrané modely (iba validácia, `runs_final/selection/`)
| skupina | vybraný | rozhodlo | poznámka |
|---|---|---|---|
| static | `lightgbm` | 1. krok (TPR@FPR 1 % val 0,9978) | jednoznačne |
| dynamic | `lightgbm` | 2. krok (ROC-AUC), remíza s `rf` v TPR | |
| hybrid | `lightgbm` | 3. krok (CPU čas), remíza s `rf` v TPR aj ROC-AUC | stal sa učiteľom aj veľkým modelom kaskády |

Hybridný LightGBM je **najlacnejší** z vybraných modelov (0,086 ms/vz. oproti statickému LightGBM 0,679 ms).
Overené: nejde o chybu merania. Pri ladení dostal vyššiu rýchlosť učenia (0,134 vs. 0,017) a menej listov
(127 vs. 461) → 29 103 uzlov oproti 648 856 pri statickom (1,6 MB vs. 38 MB). Rozdiel v cene teda spôsobili
hyperparametre z ladenia, nie modalita.

## 2. Hlavná tabuľka (test)
Zdroj: `runs_final/comparison/final/README.md`.

| prístup | TPR | FPR | F1 | TPR@FPR 1 % | TPR@FPR 0,1 % | ROC-AUC | CPU ms/vz. | eskalácie | falošné na 1 skutočný @ 0,1 % prevalencie |
|---|---|---|---|---|---|---|---|---|---|
| statický (lightgbm) | 0,9843 | 0,0048 | 0,9900 | 0,9943 | **0,9699** | **0,9995** | 0,679 | – | 4,90 |
| dynamický (lightgbm) | 0,6572 | 0,0198 | 0,7852 | 0,5849 | 0,3139 | 0,9560 | 0,427 | – | 30,12 |
| hybrid (lightgbm) | 0,9842 | 0,0047 | **0,9901** | 0,9915 | 0,9329 | 0,9994 | **0,086** | – | 4,77 |
| hybrid two_branch | 0,9767 | 0,0058 | 0,9857 | 0,9893 | 0,8173 | 0,9985 | 32,45 | – | 5,97 |
| študent statický (KD) | 0,9581 | 0,0059 | 0,9761 | 0,9815 | 0,5483 | 0,9978 | 0,304 | – | 6,17 |
| študent statický (bez KD) | 0,9613 | 0,0076 | 0,9771 | 0,9754 | 0,3684 | 0,9973 | 0,304 | – | 7,85 |
| študent dynamický (KD) | 0,5214 | 0,0171 | 0,6790 | 0,4164 | 0,2898 | 0,8972 | 0,296 | – | 32,82 |
| študent dynamický (bez KD) | 0,5391 | 0,0177 | 0,6938 | 0,4484 | 0,3130 | 0,9112 | 0,296 | – | 32,75 |
| **kaskáda main** | 0,9579 | **0,0026** | 0,9774 | – | – | – | 0,621 | 25,3 % | **2,76** |
| kaskáda nokd | 0,9605 | 0,0027 | 0,9787 | – | – | – | 0,621 | 24,9 % | 2,79 |
| kaskáda modal (variant A) | 0,9635 | 0,0025 | 0,9804 | – | – | – | 0,625 | 26,3 % | 2,57 |
| kaskáda heavy (two_branch) | 0,9534 | 0,0027 | 0,9750 | – | – | – | 8,79 | 25,3 % | 2,86 |
| kaskáda baselines (veľké modely) | 0,9831 | 0,0039 | 0,9898 | – | – | – | 1,12 | 19,1 % | 3,97 |
| neskorá fúzia (stacking) | 0,9472 | 0,0056 | 0,9705 | – | – | – | 0,599 | – | 5,93 |

## 3. Odpovede na výskumné otázky (docs/00)

### Otázka 1 – najlepší hybrid
`hybrid/lightgbm` (ranná fúzia). Dvojvetvová sieť je na teste horšia (TPR@FPR 0,1 % 0,817 vs. 0,933) a 380× drahšia.
Neskorá fúzia (stacking) je horšia než ranná fúzia (F1 0,9705 vs. 0,9901).

### Otázka 3 – samostatné prístupy vs. hybrid
- **Statický vs. hybrid: prakticky zhodné.** Rozdiely sú v rozsahu šumu: F1 0,9900 vs. 0,9901, FPR 0,0048 vs. 0,0047.
  Pri FPR 0,1 % je statický lepší (0,970 vs. 0,933).
- **Dynamický je výrazne horší** (F1 0,785) a na teste sa veľmi zhoršil: ROC-AUC val 0,997 → test 0,956.
- Hybrid dynamickú časť takmer nevyužíva. Permutácia skupín `dynamic:*` znižuje ROC-AUC hybridného LightGBM
  o ≤ 0,0001, kým `static:imports` o 0,0024 (`runs_final/comparison/hybrid/IMPORTANCE.md`).
- **Komplementarita** (nová analýza, `runs_final/comparison/complementarity/`, priemer cez seedy):
  hybrid opraví ~37 chýb statického modelu a ~37 jeho správnych rozhodnutí pokazí, čistý prínos je teda ≈ 0.
  Dynamický model je však správne pri **32 z 38** falošných poplachov statického modelu. Pri chybách na malvéri
  je správne iba pri 23 zo 148. Dynamické príznaky teda nesú doplnkovú informáciu najmä o neškodných súboroch,
  ktoré statický model mylne označí. Ranná fúzia v LightGBM ju nevyužije, kaskáda áno (pozri otázku 4).
- **Interpretácia:** Pri tomto datasete a časovom teste hybrid nepredčí statický prístup v kvalite. Podľa
  `docs/00` je to platná odpoveď. Výhodou hybridu je tu iba nižšia cena, ktorú však spôsobili hyperparametre.

### Otázka 2 – študenti a destilácia
- **Destilácia neprinesla zlepšenie.** Statický študent s KD a bez KD: F1 0,9761 vs. 0,9771, TPR@FPR 1 % 0,9815 vs. 0,9754.
  Dynamický študent s KD a bez KD: F1 0,6790 vs. 0,6938, ROC-AUC 0,897 vs. 0,911. Rozdiely sú malé a v oboch smeroch,
  pri TPR@FPR 0,1 % a FPR je KD statického študenta lepší (0,548 vs. 0,368; FPR 0,0059 vs. 0,0076).
- Variant A (učiteľ z rovnakej modality) nie je systematicky lepší ani horší.
- **Možné vysvetlenie (hypotéza):** mäkké označenia hybridného učiteľa sú takmer binárne – 97,6 % tréningových
  vzoriek má p < 0,01 alebo > 0,99 (`runs_final/teachers/hybrid_lightgbm/*/README.md`). Študent ich síce zmäkčuje
  teplotou v log-odds (T ladené v [1; 8]), no ladenie zvolilo vysokú váhu skutočných označení
  (α = 0,60 – 0,88; statický `mlp_kd` α = 0,60, T = 6,5; dynamický `mlp_kd` α = 0,71, T = 1,3). Učiteľ teda
  pravdepodobne nesie málo informácie navyše oproti skutočným označeniam. Dynamický študent sa navyše učí
  napodobniť učiteľa, ktorého rozhodnutia stoja na statických príznakoch, a tie dynamický vstup nemá.
  (Oprava 2026-11-03: pôvodná verzia neuvádzala zmäkčenie teplotou.)
- **Pravidlo „študent aspoň 10× lacnejší ako učiteľ“ (docs/05, NÁVRH) nie je splnené**, a to ani približne.
  Študenti (MLP, 74 tis. parametrov) stoja 0,30 ms/vz., učiteľ (hybridný LightGBM) 0,086 ms/vz. Študent je teda
  **3,5× drahší než učiteľ**. Pravidlo kód nekontroluje. Tento prípad `docs/00` predvídal („ak by najlepší hybrid
  bol lacný…“). Treba ho uviesť ako výsledok a s vedúcou dohodnúť, ako ho formulovať.
- Študent oproti najlepšiemu modelu svojej modality: statický je 2,2× lacnejší a horší (F1 −0,014, pri FPR 0,1 %
  výrazne). Dynamický je 1,4× lacnejší a horší (F1 −0,106).

### Otázka 4 – kaskáda
**(a) Kaskáda vs. hybrid na každej vzorke:** kaskáda main **nie je lacnejšia** (0,621 vs. 0,086 ms/vz., 7,2× drahšia)
a má nižšie TPR (0,958 vs. 0,984). Má však **o 45 % nižšie FPR** (0,0026 vs. 0,0047) a najlepšiu precision pri nízkej
prevalencii (2,76 vs. 4,77 falošného na 1 skutočný poplach pri 0,1 % malvéru).

S ťažkým hybridom (`heavy`, dvojvetvová sieť, doplnková analýza podľa docs/00) platí očakávaný vzťah. Kaskáda stojí
8,79 ms/vz. oproti 32,45 ms (**3,7× menej**) pri F1 0,9750 vs. 0,9857 a FPR 0,0027 vs. 0,0058.
Téza 4 sa teda potvrdzuje iba pri drahom veľkom modeli. Pri lacnom LightGBM sa nepotvrdzuje.

**(b) Kaskáda vs. samostatné modely pri podobných nárokoch:** v porovnaní s najlepším statickým modelom (0,679 ms)
má kaskáda podobnú cenu (0,621 ms), nižšie FPR (0,0026 vs. 0,0048) a nižšie TPR (0,958 vs. 0,984).
Oproti dynamickému je jednoznačne lepšia. Oproti neskorej fúzii pri rovnakej cene je lepšia (F1 0,9774 vs. 0,9705).

**Správanie kaskády** (`runs_final/cascade/main/*/README.md`, metrics.json):
- **Eskalácie: validácia 5,6 % → test 25,3 %.** Podiel eskalácií sa pri časovom posune zvýšil 4,5-násobne, lebo
  dynamický študent na teste zlyháva (TPR 0,52). Najviac sa eskaluje pri rodinách keylogger (73 %), coinminer (66 %)
  a ransomware (56 %), pri neškodných iba 2,4 %.
- **Na eskalovaných vzorkách rozhoduje v skutočnosti statická informácia.** Úspešnosť je: hybrid 0,984,
  statický študent 0,983, dynamický študent 0,017. Pri nezhode má takmer vždy pravdu statický študent.
  Hybrid prináša oproti statickému študentovi iba +0,1 b. Pri `heavy` je hybrid na eskaláciách dokonca horší (0,971).
- **Chyby pri zhode** (kaskáda ich nemôže opraviť): 325 (2,5 % zhôd), z toho FP 5 a FN 320. Hlavnou príčinou
  straty TPR je teda malvér, ktorý oba študenti zhodne pustia. Najviac pri rodine keylogger (108 chýb, 12,9 % rodiny).
- **Interpretácia:** Kaskáda A sa správa ako statický študent s „vetom“ dynamického: falošný poplach statického
  študenta sa pri nezhode pošle hybridu, ktorý ho často zamietne. Tým klesá FPR. To zodpovedá komplementarite
  z otázky 3: dynamická informácia pomáha pri neškodných súboroch, nie pri malvéri.

## 4. Nízka prevalencia (téza 2)
Prepočet z TPR/FPR, falošné poplachy na 1 skutočný pri 0,1 % malvéru: statický 4,90, hybrid 4,77, dynamický 30,1,
**kaskády 2,57 – 2,86**, kaskáda baselines 3,97.
**Interpretácia:** Samotný hybrid nemá výrazne menej falošných poplachov ako statický model (−3 %). Najnižšiu mieru
majú kaskády, ale za cenu nižšieho TPR (0,953 – 0,964 oproti 0,984).

## 5. Kontrolné experimenty a podskupiny
- **Statické artefakty** (bez podpisu, tabuľky certifikátov a času zostavenia; `comparison/static_ablations/`):
  LightGBM −0,4 b. TPR@FPR 1 % na teste, takže sa o artefakty neopiera. LR −2,5 b., pri FPR 0,1 % klesá zo 7,9 % na 1,1 %.
  Výsledky predbežného behu sa potvrdili.
- **Dynamická reprezentácia** (`comparison/dynamic_ablations/`): variant s udalosťami a súhrnom (`*_full`) je
  na validácii mierne lepší, na teste pri LightGBM horší (ROC-AUC 0,9415 vs. 0,9560). To potvrdzuje rozhodnutie
  z docs/04 používať iba API volania (artefakt emulátora v teste).
- **Podskupiny emulácie** (`comparison/subsets/`): na vzorkách s ukončením `unsupported_api` (9 094 z 17 339 testových)
  má dynamický LightGBM TPR iba 0,51. Na ostatných 0,83. Pri malých reportoch (≤ 5 volaní) 0,37. Statické
  a hybridné modely majú pri malých reportoch vyššie FPR (hybrid 0,012, statický 0,016 vs. ~0,005 inde).
  Zlyhanie dynamického prístupu na teste je teda z veľkej časti viazané na výsledok emulácie v testovacom období.
  Podiel časového posunu správania a posunu emulátora sa z týchto dát nedá oddeliť.

## 6. Výpočtové nároky – čo čísla zahŕňajú
- Merané je iba **inferencia modelu vrátane úpravy vstupu**, nie extrakcia príznakov. Dataset neobsahuje PE súbory,
  preto sa čas extrakcie EMBER a čas emulácie Speakeasy nedá zmerať (docs/00). V praxi by emulácia (až 60 s podľa
  `speakeasy-config.json`, iba predpoklad) prevýšila všetky časy modelov o niekoľko rádov. Kaskáda A emuluje každý súbor.
- Pri meraní MLP a študentov bol počítač pred meraním zaťažený na 16 – 24 % (⚠ v tabuľkách). Rozdiely študentov
  sú voči hybridu veľké (3,5×), preto to na závery nemá vplyv, ale v práci treba ⚠ uviesť.
- Náklady kaskády sú odhad (statický + dynamický študent + podiel eskalácií × hybrid), nie meranie celej kaskády.

## 7. Zhrnutie
| téza (docs/00) | výsledok V1 |
|---|---|
| 1 – hybrid presnejší a stabilnejší (zero-day) | **nepotvrdená v časovom teste**: hybrid ≈ statický; zero-day (vynechané rodiny) príde vo V2 |
| 2 – hybrid menej falošných poplachov pri nízkej prevalencii | **samotný hybrid nie** (4,77 vs. 4,90); kaskády áno (2,6 – 2,9), ale s nižším TPR |
| 3 – destilácia → rýchlejší model s porovnateľnou presnosťou | **nepotvrdená**: KD bez prínosu, študent nie je rýchlejší než (lacný) učiteľ |
| 4 – viacstupňová architektúra zníži náročnosť | **iba voči drahému hybridu** (two_branch: 3,7× menej); voči LightGBM hybridu nie |

## 8. Zistené nedostatky výstupov (bez vplyvu na čísla)
- `comparison/students_*/README.md` boli vygenerované pred benchmarkom študentov. Dnes boli pregenerované
  (`src.evaluation.compare --runs-root runs_final`) a tabuľka spotreby je doplnená.
- `comparison/final/README.md` odkazuje pri otázke 1 na `runs/comparison/hybrid/` namiesto `runs_final/…`.
  Graf `quality_vs_cost.png` má prekrývajúce sa popisy. Oprava v kóde je potrebná pre V2.
- Podrobnosti kaskády (eskalácie, rodiny) sú v README iba pre seed 0. Metriky kvality sú priemerom cez seedy.

## 9. Návrhy na ďalší postup (NÁVRH, nerozhodnuté)
1. **Kaskáda B** (vo V2 už plánovaná podľa docs/00: najprv statický študent, pri neistom skóre emulácia a hybrid).
   Výsledky V1 ju podporujú ako vhodnejšiu formuláciu tézy 4: emulácia by sa robila iba pre časť súborov, čím sa
   ušetrí najdrahší krok. Z uložených predikcií V1 by sa dala vyhodnotiť takmer bez výpočtu, vo V1 sa však podľa
   rozhodnutia autora nerobí. Prah neistoty treba určiť na validácii.
2. S vedúcou prekonzultovať pravidlo 10× pre študenta (učiteľ je lacný LightGBM) a to, či vo V2 ponechať pravidlo
   výberu (pri remíze rozhoduje CPU čas), alebo uviesť ako doplnok RF/two_branch ako učiteľa.
3. Vo V2 (vynechané rodiny) sledovať najmä keylogger a coinminer: tu kaskáda najviac eskaluje a robí najviac
   spoločných chýb.
