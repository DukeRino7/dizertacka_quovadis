# Zhrnutie prvého experimentu (V1) – podklad pre konzultáciu

Dušan Čatloch, 3. 11. 2026. Podrobné výsledky sú v `docs/07_vysledky_v1.md`, surové výstupy v `runs_final/`.

## 1. Čo bolo cieľom V1
Laboratórne porovnať statickú, dynamickú a hybridnú detekciu malvéru a overiť kaskádu. Kaskáda funguje takto:
dva ľahké destilované modely (statický a dynamický) rozhodnú, a ak sa nezhodnú, rozhodne veľký hybridný model.
V1 testuje **časový posun** (tréning január 2022 → test apríl 2022). Scenár zero-day (vynechané rodiny)
a kaskáda B sú plánované vo V2.

Pravidlá výberu modelov a vykazovania boli dohodnuté **pred** behom a podľa výsledkov sa nemenili:
- najlepší model skupiny = najvyššie TPR pri FPR 1 % na validácii;
- prahy sa určujú na validácii;
- test sa použil iba na finálne vyhodnotenie.

## 2. Dáta
| | |
|---|---|
| Dataset | Quo Vadis (Trizna, 2022): statické príznaky EMBER + reporty emulácie Speakeasy, spárované podľa SHA-256 |
| Triedy | neškodné súbory + 7 rodín malvéru (backdoor, coinminer, dropper, keylogger, ransomware, rat, trojan) |
| Rozdelenie | tréning 66 831 / validácia 7 426 (január 2022) / **test 17 339** (apríl 2022, pôvodný test datasetu) |
| Podiel malvéru | tréning 67 %, test 54 % |
| Statický vstup | vektor príznakov EMBER |
| Dynamický vstup | 1- a 2-gramy API volaní zo Speakeasy (2 000 najčastejších z tréningu) |
| Hybridný vstup | spojenie oboch vektorov (ranná fúzia); ďalej dvojvetvová sieť a neskorá fúzia |

Dôležité obmedzenie: dynamické dáta pochádzajú z **emulácie** (Speakeasy), nie z behu v sandboxe Windows.
V teste skončila emulácia chybou `unsupported_api` pri 52 % vzoriek (stopa inej verzie emulátora).

## 3. Použité modely
Každý model: ladenie Optuna (30 pokusov, cieľ ROC-AUC na validácii), 3 seedy, rovnaký protokol pre všetky prístupy.

| skupina | modely |
|---|---|
| statické, dynamické, hybridné | logistická regresia, Random Forest, LightGBM, MLP malá, MLP veľká |
| špecifické | sekvenčná CNN nad API volaniami (dynamické), dvojvetvová sieť (hybridná), neskorá fúzia (priemer, stacking) |
| študenti | MLP s 1 skrytou vrstvou: s destiláciou od hybridného učiteľa, bez destilácie, s učiteľom z rovnakej modality |
| kaskády | `main` (destilovaní študenti + hybrid), `nokd`, `modal`, `heavy` (veľký model = dvojvetvová sieť), `baselines` (najlepšie samostatné modely) |

**Vybrané podľa pravidla:** statický LightGBM, dynamický LightGBM, hybridný LightGBM. Hybridný LightGBM sa
stal učiteľom študentov aj veľkým modelom kaskády.

Merania výpočtových nárokov:
- všetky na jednom počítači (Lenovo Legion, RTX 4060);
- CPU čas na vzorku zahŕňa iba inferenciu modelu;
- extrakcia príznakov a emulácia sa zmerať nedajú, lebo dataset neobsahuje samotné súbory.

## 4. Súhrnná tabuľka (test, prah z validácie pri FPR ≤ 1 %, priemer 3 seedov)
| prístup | TPR | FPR | F1 | TPR @ FPR 0,1 % | ROC-AUC | CPU ms/vzorku | eskalácie | falošné poplachy na 1 skutočný pri 0,1 % malvéru |
|---|---|---|---|---|---|---|---|---|
| statický (LightGBM) | **0,984** | 0,0048 | 0,990 | **0,970** | **0,9995** | 0,68 | – | 4,9 |
| dynamický (LightGBM) | 0,657 | 0,0198 | 0,785 | 0,314 | 0,956 | 0,43 | – | 30,1 |
| hybrid (LightGBM) | **0,984** | 0,0047 | **0,990** | 0,933 | 0,9994 | **0,09** | – | 4,8 |
| hybrid – dvojvetvová sieť | 0,977 | 0,0058 | 0,986 | 0,817 | 0,9985 | 32,45 | – | 6,0 |
| neskorá fúzia (stacking) | 0,947 | 0,0056 | 0,971 | – | – | 0,60 | – | 5,9 |
| študent statický (destilácia) | 0,958 | 0,0059 | 0,976 | 0,548 | 0,9978 | 0,30 | – | 6,2 |
| študent statický (bez destilácie) | 0,961 | 0,0076 | 0,977 | 0,368 | 0,9973 | 0,30 | – | 7,9 |
| študent dynamický (destilácia) | 0,521 | 0,0171 | 0,679 | 0,290 | 0,897 | 0,30 | – | 32,8 |
| študent dynamický (bez destilácie) | 0,539 | 0,0177 | 0,694 | 0,313 | 0,911 | 0,30 | – | 32,7 |
| **kaskáda main** | 0,958 | 0,0026 | 0,977 | – | – | 0,62 | 25 % | 2,8 |
| kaskáda modal | 0,964 | **0,0025** | 0,980 | – | – | 0,63 | 26 % | **2,6** |
| kaskáda heavy (dvojvetvová sieť) | 0,953 | 0,0027 | 0,975 | – | – | 8,79 | 25 % | 2,9 |
| kaskáda baselines | 0,983 | 0,0039 | 0,990 | – | – | 1,12 | **19 %** | 4,0 |

TPR = podiel zachyteného malvéru, FPR = podiel neškodných súborov označených ako malvér.
Prepočet na nízku prevalenciu vychádza z TPR a FPR (v teste je 54 % malvéru, v praxi ~1 % a menej).

## 5. Najlepší prístup podľa jednotlivých parametrov
| parameter | najlepší | hodnota | ďalší v poradí |
|---|---|---|---|
| zachytený malvér (TPR) | statický LightGBM | 0,984 | hybrid LightGBM 0,984, kaskáda baselines 0,983 |
| najmenej falošných poplachov (FPR) | kaskáda modal | 0,0025 | kaskáda main 0,0026 (statický 0,0048, hybrid 0,0047) |
| F1 | hybrid LightGBM | 0,990 | statický LightGBM 0,990 (rozdiel 0,0001) |
| TPR pri prísnom FPR 0,1 % | statický LightGBM | 0,970 | hybrid LightGBM 0,933 |
| ROC-AUC | statický LightGBM | 0,9995 | hybrid LightGBM 0,9994 |
| nízka prevalencia (falošné na 1 skutočný) | kaskády | 2,6 – 2,9 | hybrid 4,8, statický 4,9 |
| výpočtové nároky (CPU čas) | hybrid LightGBM | 0,09 ms | študenti 0,30 ms, kaskáda main 0,62 ms |
| najmenej eskalácií | kaskáda baselines | 19 % | ostatné kaskády 25 – 26 % |
| odolnosť voči časovému posunu | statický LightGBM | ROC-AUC 0,9998 → 0,9995 | dynamický: 0,997 → 0,956 |

## 6. Hlavné zistenia
1. **Statický a hybridný model sú prakticky rovnako dobré.** Hybrid dynamické príznaky takmer nevyužíva.
   Statické príznaky sú na tomto datasete takmer nasýtené (ROC-AUC 0,9995).
2. **Dynamický prístup pri časovom posune zlyháva** (ROC-AUC z 0,997 na 0,956). Zlyhanie súvisí najmä
   s výsledkom emulácie v testovacom období.
3. **Dynamická informácia je predsa užitočná, ale iba na odhalenie falošných poplachov.** Pri 32 z 38 falošných
   poplachov statického modelu má dynamický model pravdu. Pri chýbajúcom malvéri pomáha málo.
4. **Kaskáda znižuje falošné poplachy o ~45 %** (FPR 0,0026 vs. 0,0047) za cenu nižšieho TPR (0,958 vs. 0,984).
   Na teste eskaluje 25 % vzoriek, na validácii 6 %. Nárast spôsobuje zlyhávanie dynamického študenta.
5. **Destilácia nepriniesla zlepšenie.** Študenti s destiláciou a bez nej sú rovnakí. Možný dôvod (hypotéza):
   učiteľ dáva takmer binárne odpovede (97,6 % pravdepodobností je < 0,01 alebo > 0,99); ani zmäkčenie teplotou
   a ladenie váhy učiteľa nepriniesli zlepšenie.
6. **Vybraný hybrid je veľmi lacný** (0,09 ms). Študenti (0,30 ms) sú preto 3,5× drahší než učiteľ a kaskáda
   je 7× drahšia než samotný hybrid. Pri drahom hybride (dvojvetvová sieť) je kaskáda 3,7× lacnejšia.

## 7. Súvis s tézami
| téza | výsledok V1 | poznámka |
|---|---|---|
| 1. Hybrid dosahuje vyššiu presnosť a stabilitu v zero-day scenároch | **zatiaľ neoverená** | V1 testuje iba časový posun (rovnaké rodiny); tu je hybrid rovnaký ako statický model. Zero-day (vynechané rodiny) je vo V2. |
| 2. Hybrid má pri nízkej prevalencii menej falošných poplachov pri zachovaní citlivosti | **čiastočne** | Samotný hybrid nie (4,8 vs. 4,9). Kaskáda áno (2,6 – 2,9, o ~45 % menej), ale citlivosť klesá o 2 – 3 body. |
| 3. Destilácia vytvorí rýchlejší model s porovnateľnou presnosťou | **nepotvrdená** | Destilácia bez prínosu; študent nie je rýchlejší ako vybraný (lacný) hybrid. |
| 4. Viacstupňová architektúra zníži výpočtovú náročnosť | **podmienene** | Platí voči drahému hybridu (3,7× úspora), neplatí voči lacnému LightGBM. Náklady emulácie, ktoré sú v praxi rozhodujúce, sa nedajú zmerať. |

## 8. Otázky na konzultáciu (návrhy, nerozhodnuté)
1. **Téza 4 – čo sa má šetriť?** Výpočet modelov (kaskáda A, V1), alebo počet súborov, ktoré treba emulovať
   (kaskáda B vo V2: najprv statický model, emulácia iba pri neistých súboroch)? Výsledky V1 naznačujú, že
   zmysel má skôr kaskáda B.
2. **Téza 3 – pravidlo pre študenta** („aspoň 10× lacnejší než učiteľ“) sa nedá splniť, keď je učiteľ lacný
   LightGBM. Ponechať výsledok ako negatívny, alebo vo V2 doplniť (vopred ohlásené) porovnanie s drahým učiteľom
   (dvojvetvová sieť)?
3. **Téza 2** – prijateľná formulácia „viacstupňová hybridná architektúra znižuje falošné poplachy“ namiesto
   „hybridný model“?
4. Pokračovať V2 (zero-day = vynechanie jednej z 7 rodín z tréningu aj validácie) podľa plánu.
