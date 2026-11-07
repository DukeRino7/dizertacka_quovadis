# 13 – Výsledky V3 (špecialista pre neisté súbory, prekalibrovanie prahu)

Stav k 2026-11-07. Zdroj: `runs_v3/`, beh kódu značky `v3` (ZIP) na pracovnom notebooku DCATLOCH,
v samostatnom priečinku `dizertacka_quovadis-3`, 2026-11-07 17:30 – 17:42 (`runs_v3/RUN_INFO.txt`).
Všetky kroky skončili (časový test 4/4, každá zo 7 rodín 4/4, súhrny 2/2), v logu nie je chyba. Pred ním prešla
technická kontrola (`runs_v3_smoke`, rodina rat).

Plán a kritériá boli určené vopred v `docs/12_plan_v3.md` (commit 1799a71, pred akýmkoľvek výsledkom) a podľa
výsledkov sa nemenili. Súhrny: `runs_v3/comparison/v3/README.md` (B), `RECALIBRATION.md` (C) a csv súbory.
Prahy sú z validácie a hodnoty sú priemer cez seedy 0–2. Body označené **Interpretácia** sú môj návrh výkladu.

## 1. B – kaskáda so špecialistom
Statický LightGBM rozhodne isté súbory. Sporné súbory (rozpočet emulácie 10 % z validácie; na teste 21,5 %,
v zero-day 22,8 %) rozhodne špecialista: LightGBM učený iba na tréningových súboroch blízko prahu.

### 1.1 Časový test
| prístup | TPR | FPR | F1 | emulované | CPU ms/vz. |
|---|---|---|---|---|---|
| statický LightGBM | 0,9843 | 0,0048 | 0,9900 | 0 % | 0,68 |
| hybrid LightGBM | 0,9842 | 0,0047 | 0,9901 | 100 % | 0,09 |
| kaskáda B-baselines (V2, rozpočet 10 %) | 0,9831 | 0,0039 | 0,9898 | 21,5 % | 0,68 |
| **špecialista (hybrid) – hlavný** | **0,9891** | 0,0052 | 0,9923 | 21,5 % | 0,70 |
| špecialista (iba dynamika) | 0,9889 | 0,0048 | 0,9924 | 21,5 % | 0,69 |
| špecialista, tréning 10 % (citlivosť) | 0,9908 | 0,0060 | 0,9928 | 21,5 % | 0,70 |
| špecialista, tréning 40 % (citlivosť) | 0,9896 | 0,0058 | 0,9924 | 21,5 % | 0,70 |

Špecialista sám stojí 0,087 ms na súbor (benchmark na pracovnom notebooku). Kaskáda ≈ statický model
+ 21,5 % × špecialista ≈ 0,70 ms.

### 1.2 Zero-day (priemer cez 7 rodín)
| prístup | TPR vynech. rodiny | sm. odch. | najhoršia | január | FPR | TPR všetok malvér |
|---|---|---|---|---|---|---|
| statický LightGBM | 0,7922 | 0,277 | 0,241 | 0,879 | 0,0047 | 0,9598 |
| hybrid LightGBM | 0,7870 | 0,305 | 0,168 | 0,876 | 0,0045 | 0,9557 |
| kaskáda B-baselines (V2) | 0,7797 | 0,300 | 0,168 | 0,875 | 0,0036 | 0,9536 |
| **špecialista (hybrid) – hlavný** | 0,7903 | 0,293 | 0,196 | 0,879 | 0,0055 | 0,9623 |
| špecialista (iba dynamika) | 0,7799 | 0,281 | 0,211 | 0,876 | 0,0049 | 0,9490 |
| špecialista, tréning 10 % (citlivosť) | 0,8176 | 0,275 | 0,216 | 0,883 | 0,0059 | 0,9669 |
| špecialista, tréning 40 % (citlivosť) | 0,7922 | 0,294 | 0,193 | 0,880 | 0,0055 | 0,9618 |

TPR vynechanej rodiny podľa rodiny (test):

| prístup | backdoor | coinminer | dropper | keylogger | ransomware | rat | trojan |
|---|---|---|---|---|---|---|---|
| statický LightGBM | 0,984 | 0,601 | 0,943 | 0,241 | 0,982 | 0,923 | 0,872 |
| špecialista (hybrid) | 0,984 | 0,604 | 0,950 | 0,196 | 0,978 | 0,936 | 0,885 |
| špecialista (iba dynamika) | 0,905 | 0,596 | 0,946 | 0,211 | 0,960 | 0,944 | 0,898 |
| špecialista, tréning 10 % | 0,983 | **0,778** | 0,946 | 0,216 | 0,979 | 0,938 | 0,885 |

### 1.3 Kritériá (docs/12, bod 2)
| variant | B1 – téza 1 (+1 p. b. oproti statickému, FPR ≤, ≥ 5 zo 7 rodín) | B2 – téza 2 | B3 – oproti V2 (+1 p. b., FPR ≤ +0,1 p. b.) |
|---|---|---|---|
| **špecialista (hybrid) – hlavný** | **nesplnené** (0,790 vs. 0,792; FPR 0,0055 vs. 0,0047; 5 zo 7) | nesplnené (časový aj zero-day) | nesplnené (FPR 0,0055 vs. 0,0036) |
| špecialista (iba dynamika) | nesplnené (0,780; 3 zo 7) | zero-day nie; časový test **áno**, FPR 0,0048 oproti 0,0048 sa líši až na 4. desatinnom mieste | nesplnené |
| tréning 10 % (citlivosť) | nesplnené (0,818, ale FPR 0,0059 > 0,0047; 4 zo 7) | nesplnené | nesplnené (FPR) |
| tréning 40 % (citlivosť) | nesplnené | nesplnené | nesplnené |

**Žiadny variant nesplnil kritérium tézy 1 ani prínosu oproti V2.**

### 1.4 Čo znamenajú výsledky B
- Špecialista mení hlavne **pracovný bod**, nie schopnosť rozlišovať. Pri prahoch z validácie zvyšuje TPR
  (časový test +0,5 p. b.) aj FPR (0,0052 oproti 0,0048; v zero-day 0,0055 oproti 0,0047).
- Porovnanie pri **rovnakom FPR** dáva scenár C (oddiel 2), kde sa prah všetkých modelov nastaví na rovnaké FPR na
  nových neškodných súboroch. Pri kalibrácii na 20 % neškodných:

  | | statický | špecialista (hybrid) | špecialista (dynamika) |
  |---|---|---|---|
  | zero-day TPR vynech. rodiny | 0,828 ± 0,022 | 0,831 ± 0,023 | 0,836 ± 0,023 |
  | zero-day FPR | 0,0089 | 0,0092 | 0,0097 |
  | časový test TPR | 0,9934 | 0,9940 | 0,9944 |

  Rozdiely sú menšie ako rozptyl a FPR špecialistov je mierne vyššie. **Pri rovnakom FPR špecialista nerozlišuje
  lepšie ako samotný statický model.**
- Variant s tréningom na 10 % (citlivosť) má priemer 0,818 len vďaka rodine coinminer (0,60 → 0,78). Jeho seedy dávajú
  0,61 / 0,88 / 0,85, výsledok je teda nestabilný. Ide o citlivostný variant, nie hlavný, preto sa neuvádza ako úspech.
- **Interpretácia:** je to druhý nezávislý dôkaz k analýze príčin V2 (docs/10, oddiel 6.1). Prvým bol strop
  kombinácie rozhodnutí (+0,6 p. b.). Teraz ani model učený výlučne na sporných súboroch, s prístupom k statickým aj
  dynamickým príznakom, nenájde v dynamických príznakoch informáciu, ktorú statický model nemá. Téza 1 sa nepotvrdzuje
  pre vlastnosti dát (dynamické príznaky z emulácie Speakeasy), nie pre spôsob, akým kaskáda kombinuje modely.

## 2. C – prekalibrovanie prahu na nových neškodných súboroch (samostatný scenár)
Prah každého modelu sa nastaví na FPR 1 % na kalibračnej časti aprílových **neškodných** súborov. Malvér kalibrácia
nevidí. Hodnotí sa na zvyšku testu, 10 náhodných rozdelení × 3 seedy (priemer ± sm. odchýlka).

### 2.1 Statický LightGBM
| kalibrácia | počet neškodných | zero-day TPR vynech. rodiny | zero-day FPR | časový TPR | časový FPR |
|---|---|---|---|---|---|
| bez (prah z validácie) | – | 0,792 | 0,0047 | 0,9843 | 0,0048 |
| 1 % | ~79 | 0,791 ± 0,113 | 0,0150 ± 0,0145 | 0,976 ± 0,043 | 0,0152 ± 0,0153 |
| 5 % | ~397 | **0,817 ± 0,030** | 0,0072 | 0,9902 | 0,0076 |
| 20 % | ~1 588 | **0,828 ± 0,022** | 0,0089 | 0,9934 | 0,0090 |

- Prekalibrovanie vracia pracovný bod k plánovanému FPR (≤ 1 %) a TPR vynechanej rodiny stúpne o **+2,5 p. b.**
  (~400 súborov) až **+3,6 p. b.** (~1 600 súborov). Orákulum v docs/10 (6.2) odhadlo +4,6 p. b.; skutočný výsledok je
  o 1 p. b. nižší, lebo prah sa určuje na menšej vzorke.
- **~79 neškodných súborov nestačí:** prah pre FPR 1 % určuje jediný súbor, FPR je 1,5 % ± 1,5 p. b.
  a výsledok je horší ako bez kalibrácie.
- Prekalibrovanie pomáha všetkým modelom podobne (hybrid LightGBM pri 20 %: 0,811; kaskády z LightGBM: 0,804).
  Poradie prístupov sa nemení. Dynamický model sa zhoršuje (0,51 → 0,41), lebo jeho prah z validácie bol na teste voľnejší
  (FPR 1,8 %) a kalibrácia ho sprísni.

### 2.2 Téza 2 v scenári C
Rovnaké kritérium ako docs/09 (FPR < statický aj dynamický, TPR všetkého malvéru ≥ statický − 1 p. b.); referencie
sú tiež prekalibrované.

| kalibrácia | test | A-baselines / B-baselines (rozpočet 10 %) | A-main, B-main (študenti) | špecialisti V3 |
|---|---|---|---|---|
| 1 % | časový | B áno, A nie | nie | áno (nestabilné) |
| 1 % | zero-day | áno | nie | áno (nestabilné) |
| 5 % | časový | **áno** (FPR 0,0058 vs. 0,0076; TPR 0,986 vs. 0,990) | nie | dynamika áno, hybrid nie |
| 5 % | zero-day | **áno** (FPR 0,0056 vs. 0,0072; TPR 0,960 vs. 0,965) | nie | nie |
| 20 % | časový | **áno** (FPR 0,0068 vs. 0,0090; TPR 0,990 vs. 0,993) | nie | nie |
| 20 % | zero-day | **áno** (FPR 0,0067 vs. 0,0089; TPR 0,965 vs. 0,971) | nie | nie |

**Téza 2 pre kaskády z LightGBM platí aj po prekalibrovaní**, vo všetkých stabilných nastaveniach (5 % a 20 %),
v časovom teste aj v zero-day. Kaskáda znižuje FPR o ~25 % pri strate TPR do 0,6 p. b. Kaskády so študentmi kritérium
nesplnia ani tu (TPR −2 až −4 p. b.).

## 3. Výpočtové nároky – čo sa dá a čo nedá merať
- **CPU čas modelov** (benchmark, pracovný notebook): statický LightGBM 0,68 ms, hybrid LightGBM 0,09 ms, špecialista
  0,087 ms, študenti 0,30 ms, dvojvetvová sieť 32,45 ms na súbor.
- **Emulácia sa nemeria.** Overené 2026-11-07: reporty Speakeasy v datasete neobsahujú údaj o čase emulácie (iba
  vstupné body, API volania, chyby). `speakeasy-config.json` z datasetu určuje limit `timeout: 60` s a
  `max_api_count: 500`. **60 s je teda horná hranica, nie skutočný čas**. Skutočný čas môže byť výrazne kratší, lebo
  veľa emulácií končí po 500 API volaniach (`max_api_count`, docs/04).
- Preto hlavná miera tézy 4 ostáva **podiel súborov, ktoré treba emulovať** (B-main 10,7 %, B-baselines aj
  špecialista 21,5 %, ostatné 100 %). Čas sa uvádza iba ako horná hranica: ≤ podiel × 60 s.

## 4. Stav téz po V1–V3
| téza | stav | hlavný dôkaz |
|---|---|---|
| 1. kaskáda presnejšia a stabilnejšia v zero-day | **nepotvrdená, s vysvetlením** | strop kombinácie +0,6 p. b. (V2); špecialista pri rovnakom FPR = statický (V3); dynamické príznaky z emulácie nenesú doplnkovú informáciu o nových rodinách |
| 2. kaskáda menej falošných poplachov pri zachovaní citlivosti | **potvrdená pre kaskády z LightGBM** | V2: časový test aj zero-day; V3: aj po prekalibrovaní prahu (5 %, 20 %); neplatí pre kaskády so študentmi |
| 3. destilácia: rýchlejší model s porovnateľnou presnosťou ako komplexný hybrid | **čiastočne** | V2: statický študent s učiteľom dvojvetvová sieť = učiteľ, 107× rýchlejší; neplatí oproti lacnému hybridu LightGBM |
| 4. viacstupňová architektúra zníži náročnosť | **potvrdená v podiele emulácie** | V2: 21,5 % emulovaných súborov bez straty kvality (B-baselines), 10,7 % so stratou 2,6 p. b. (B-main); čas emulácie iba horná hranica |

Ďalšie zistenie (nie téza): **najväčšiu časť straty v zero-day spôsobuje posun prahu** pri časovom posune. Dá sa
z väčšej časti vrátiť prekalibrovaním na ~400 – 1 600 nových neškodných súboroch (+2,5 až +3,6 p. b.), bez akéhokoľvek
malvéru z nového obdobia.

## 5. Obmedzenia V3
- Návrh V3 vychádzal z analýzy testu V2, nie je to nezávislé potvrdenie (docs/12). Kritériá boli zapísané vopred,
  variantov bolo málo a vykazujú sa všetky.
- Scenár C používa časť testovacieho obdobia (iba neškodné súbory) na kalibráciu. Je to iný scenár ako hlavné
  výsledky a vykazuje sa oddelene.
- Rodina = označenie datasetu (docs/10, oddiel 8). Čas emulácie sa nemeria (oddiel 3).
