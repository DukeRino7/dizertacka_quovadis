# 19 – Plán V4 (overenie na datasete KronoDroid)

Stav k 2026-11-22: **ROZHODNUTÉ autorom práce** (2026-11-22, po konzultácii s vedúcou). Zapísané **pred** akýmkoľvek
tréningom na KronoDroid; pravidlá sa podľa výsledkov nemenia. Výsledky V1–V3 (`docs/07`, `10`, `13`, `17`) ostávajú
v platnosti a uvádzajú sa celé. Fakty o dátach: `docs/18_audit_kronodroid.md`. Cieľ termínu: do Vianoc 2026.

## 1. Prečo V4 a na čo odpovedá
Po V1–V3 platí: na Quo Vadis je najlepší samotný statický model a dynamika z emulácie Speakeasy takmer nič nepridáva
(strop kombinácie +0,65 p. b., pri úspešnej emulácii dynamika novú rodinu zhoršuje; `docs/17`). Na Quo Vadis sa však
nedá oddeliť vplyv emulácie od vplyvu inej verzie emulátora v teste (docs/04). Vedúca (konzultácia, november 2026)
súhlasí so stavom a žiada overiť na inom datasete, **či je primárnou slabinou dataset**.

Dataset rovnaký ako Quo Vadis s opravenou emuláciou verejne neexistuje. KronoDroid je najbližšia dostupná možnosť:
ten istý súbor má statické príznaky raz a dynamiku dvakrát, z **emulátora** aj zo **skutočného zariadenia**.

**V4 odpovedá na dve otázky:**
1. **Dosiahne sa s kvalitnejšou dynamikou (skutočné zariadenie) lepší výsledok než so samotnou statikou?**
   Postup je čo najbližšie Quo Vadis: rovnaké modely, destilácia, kaskády A a B, zero-day a nízka prevalencia.
2. **Je rozdiel medzi emuláciou a skutočným zariadením?** Na rovnakých súboroch, s rovnakou statikou a rovnakým
   rozdelením; líši sa iba zdroj dynamiky.

Závery sa formulujú ako **podpora alebo oslabenie** vysvetlenia z V1–V3, nie ako dôkaz. Ide o iný emulátor, inú
platformu a iné príznaky; porovnanie dvoch datasetov je popisné.

## 2. Dáta
### 2.1 Vetvy (spoločné rozdelenie)
| vetva | vzorky | dynamika | účel |
|---|---|---|---|
| **real_full** (hlavná) | celé skutočné zariadenie: 78 133 APK (po vyradení 4 SHA-256) | zariadenie | otázka 1, tézy 1–4, celý postup ako na Quo Vadis |
| **real_P** | prekrytie: 63 316 APK (34 977 benign, 28 339 malware) | zariadenie | otázka 2 (párovo s emu_P) |
| **emu_P** | to isté prekrytie | emulátor | otázka 2 |

- Rozdelenie sa urobí raz na celom zariadení (78 133). real_P a emu_P sú jeho podmnožina, takže každý súbor patrí
  vo všetkých vetvách do tej istej časti. 667 súborov iba z emulátora sa nepoužije.
- real_P oproti real_full doplnkovo ukáže vplyv veľkosti tréningu.
- Vyradené: 4 SHA-256, ktoré sú v oboch triedach (v každej podmnožine tie isté, všetky v prekrytí).
- Benígne súbory s `Detection_Ratio` > 0 a benígne s vyplnenou rodinou **ostávajú** s označením autorov.
  Prepisovať ich podľa VirusTotal by znamenalo použiť stĺpec vyradený ako prezrádzajúci triedu. FPR na tejto
  podskupine sa vykáže zvlášť.

### 2.2 Príznaky
| vstup | stĺpce | poznámka |
|---|---|---|
| **statický** (rovnaký vo všetkých vetvách) | 173 oprávnení a ich súčtov + 11 metadát (bez `FilesInsideAPK`) + príznak „metadáta chýbajú“ | `FilesInsideAPK` v emulátore chýba pre všetok malvér → vynechaný všade. Metadáta sa berú zo zariadenia, ak chýbajú, z emulátora (podľa SHA-256). Zvyšné NaN: stromy ich spracujú priamo, LR a MLP dostanú 0 a príznak chýbania. |
| **dynamický** | 288 počtov systémových volaní + `nr_syscalls` (zariadenie alebo emulátor podľa vetvy) | rovnaká transformácia ako pri Quo Vadis (signed log1p, štandardizácia pre LR a MLP) |
| **hybridný** | statický + dynamický príslušnej vetvy | ranná fúzia ako na Quo Vadis |

Nepoužijú sa: `sha256`, `Package`, `MalFamily`, dátumy, `Scanners`, `Detection_Ratio`, `TimesSubmitted`,
`NrContactedIps` (identifikátory, označenia a údaje z VirusTotal; docs/18, bod 3.2).

**Kontrolný experiment D-norm** (obdoba `dynamic_ablations` vo V1):
- vstup: dynamika ako podiely volaní (počet / `nr_syscalls`), bez `nr_syscalls`;
- hyperparametre z hlavného modelu, vykazuje sa popisne;
- účel: overiť, či prínos dynamiky nestojí iba na celkovom množstve aktivity. Medián `nr_syscalls` podľa triedy sa
  medzi emulátorom a zariadením obracia (docs/18), čo môže byť aj artefakt zberu.

### 2.3 Rozdelenie
- **Hlavné – náhodné:** train 70 % / validation 10 % / test 20 %, seed 42.
  - Stratifikované podľa triedy a rodiny; rodiny s < 50 vzorkami sa spoja do „ostatné“.
  - Súbory s identickým statickým vektorom idú spolu do jednej časti (ako validácia vo V1).
  - Časový test ako vo V1 nie je možný: dataset nemá neskoršie obdobie zberu ani dátum objavenia. Neškodné súbory
    sú prevažne z rokov 2010–2011, malvér z 2012–2018, takže rozdelenie podľa dátumu by meralo hlavne zmenu pomeru
    tried (docs/18, bod 3.4). Výsledky sú preto bez časového posunu a optimistickejšie ako časový test V1.
- **Zero-day – vynechanie rodiny (ako V2):**
  - **Pravidlo:** rodina s ≥ 1 000 vzorkami v prekrytí P, ktorá nie je všeobecným názvom antivírusu.
  - **5 rodín:** Airpush/StopSMS (6 507), Boxer (3 538), FakeInst (2 121), Locker/SLocker Ransomware (1 697),
    BankBot (1 230).
  - Vyradené z vynechávania: `Agent` (1 907) a `Malap` (2 484) sú všeobecné označenia antivírusov, pod ktorými sú
    rôzne rodiny, takže test by nebol zero-day. V tréningu ostávajú ako bežný malvér.
  - Rodina sa odstráni z tréningu aj validácie vo všetkých vetvách. Hodnotí sa TPR na **všetkých** jej vzorkách
    (žiadnu model nevidel) a FPR na neškodných súboroch testu.
  - Učené transformácie sa fitujú bez vynechanej rodiny (ako V2).
- **Doplnkové – časový posun malvéru:**
  - malvér s rokom (`date_last`) 2008–2014 → train/validation, 2015–2020 → test; neškodné podľa hlavného rozdelenia;
  - oddeľuje posun malvéru od zmeny pomeru tried; malvér s neplatným rokom sa vynechá;
  - iba pre real_full, hyperparametre z hlavného rozdelenia.

## 3. Modely, destilácia a kaskády (čo najbližšie V1/V2)
Protokol `docs/03` a `configs/protocol.yaml` bez zmeny: ladenie Optuna 30 pokusov s cieľom ROC-AUC na validácii,
3 seedy (0, 1, 2), váhy tried, prahy (0,5 a FPR ≤ 1 % z validácie), metriky, nízka prevalencia (1 % a 0,1 %),
benchmark CPU času.

### 3.1 Rebríček (samostatne pre každú vetvu; statika je spoločná)
| vstup | modely |
|---|---|
| statický | `lr`, `rf`, `lightgbm`, `mlp_small`, `mlp_large` |
| dynamický | to isté |
| hybridný | to isté + **neskorá fúzia** (priemer a stacking skóre statického a dynamického modelu) |

- **Sekvenčné modely (`seq_cnn`, `two_branch`) sa nepoužijú**, lebo dynamika sú počty bez poradia (docs/18).
  Úlohu „komplexného hybridu“ (dvojvetvová sieť vo V1/V2) prevezme **`mlp_large` na hybridnom vstupe**,
  najdrahší model rebríčka.
- **Výber** podľa `docs/00`: najlepší model skupiny = TPR pri FPR 1 % na validácii (priemer cez seedy), ďalej
  ROC-AUC, potom CPU čas. Výber sa robí zvlášť pre každú vetvu.

### 3.2 Destilácia (ako docs/05 a V2)
| študent | učiteľ | obdoba z Quo Vadis |
|---|---|---|
| `mlp_kd` (statický aj dynamický) | vybraný hybrid vetvy | `mlp_kd` |
| `mlp_nokd` | bez učiteľa | `mlp_nokd` |
| `mlp_kd_modal` | najlepší model rovnakej modality | `mlp_kd_modal` |
| `mlp_kd_heavy` | `mlp_large` hybrid (komplexný hybrid) | `mlp_kd_twobranch` |

Mäkké označenia out-of-fold (5 častí), strata a priestor hyperparametrov (α, T) ako vo V1. Pravidlo „aspoň 10× nižší
CPU čas než učiteľ“ sa overí benchmarkom.

### 3.3 Kaskády (všetky varianty V1/V2; prahy z validácie, vyhodnotenie z uložených predikcií)
| variant | 1. stupeň | pri nezhode / neistote | obdoba |
|---|---|---|---|
| A-main | `mlp_kd` statický + dynamický | vybraný hybrid | main |
| A-nokd | `mlp_nokd` | vybraný hybrid | nokd |
| A-modal | `mlp_kd_modal` | vybraný hybrid | modal |
| A-heavy | `mlp_kd` | `mlp_large` hybrid | heavy |
| A-baselines | najlepší statický + dynamický | vybraný hybrid | baselines |
| B-main | statický `mlp_kd` | dynamický `mlp_kd` → pri nezhode hybrid | b_main |
| B-direct | statický `mlp_kd` | rovno hybrid | b_direct |
| B-heavy | statický `mlp_kd` | dynamický `mlp_kd` → `mlp_large` hybrid | b_heavy |
| B-baselines | najlepší statický | najlepší dynamický → hybrid | b_baselines |
| B-nokd | statický `mlp_nokd` | ako B-main | b_nokd |
| B-heavyteacher | študent `mlp_kd_heavy` | ako B-main | b_twobranch |

- Kaskáda B: pásmo neistoty ako v docs/09 a krivka pevných rozpočtov 10 / 20 / 30 / 40 % (vzdialenosť od prahu
  v log-odds, hranica z validácie). „Emulácia“ tu znamená dynamickú analýzu v prostredí danej vetvy.
- Zero-day behy: hyperparametre z hlavného rozdelenia (ako V2), architektúry podľa výberu na hlavnom rozdelení.
- **Nepoužije sa:** špecialista V3 (nepreukázal prínos) a prekalibrovanie prahu z V3 (nie sú neškodné súbory
  z neskoršieho obdobia).

### 3.4 Analýzy ako na Quo Vadis
Komplementarita (ktoré chyby statického modelu opraví dynamika), strop „statický alebo dynamický správne“,
dôležitosť príznakov (skupiny: oprávnenia, metadáta, systémové volania), robustnosť bootstrapom (docs/16).

## 4. Kritériá (určené vopred)
Rozdiely v p. b., 95 % interval spoľahlivosti (IS) z párového bootstrapu testu (2 000 opakovaní, ako docs/16).
**Hlavná miera:** TPR pri FPR 1 % odčítané z ROC krivky testu. Ide o metriku vyhodnotenia, nie o ladenie.
Doplnkovo sa uvedie TPR a FPR pri prahu z validácie.

### 4.1 Otázka 1 – prínos kvalitnejšej dynamiky (real_full)
**Δ = TPR(najlepší hybrid) − TPR(najlepší statický)**, rovnako pre najlepšiu kaskádu.

| | kritérium |
|---|---|
| **O1** | Δ ≥ +1 p. b. a dolná hranica IS > 0 (náhodné rozdelenie) → dynamika zo zariadenia pridáva informáciu nad statiku |
| **O1-Z** | to isté pre TPR vynechanej rodiny, priemer cez 5 rodín (zero-day) |
| popisne | strop „statický alebo dynamický správne“; ROC-AUC dynamického modelu; D-norm |

### 4.2 Otázka 2 – emulácia vs. skutočné zariadenie (real_P a emu_P)
**Δ_v = TPR(najlepší hybrid vetvy v) − TPR(najlepší statický)**, statický model je v oboch vetvách ten istý.

| | kritérium |
|---|---|
| **O2** | Δ_real_P − Δ_emu_P ≥ +1 p. b. a dolná hranica IS > 0 → kvalitnejší zdroj dynamiky pomáha |
| **O2-Z** | to isté pre zero-day (priemer cez 5 rodín) |
| popisne | dynamický model samostatne (ROC-AUC, TPR pri FPR 1 %): zariadenie vs. emulátor; D-norm v oboch vetvách |

### 4.3 Interpretácia (určená vopred)
| výsledok | záver |
|---|---|
| O1 platí, O2 platí | kvalitnejšia dynamika pomáha a emulácia ju zhoršuje → **podporuje** vysvetlenie, že slabinou Quo Vadis bola emulácia |
| O1 platí, O2 neplatí | dynamika pomáha na KronoDroid aj z emulátora → rozdiel oproti Quo Vadis je skôr vo vlastnostiach datasetu (statika, platforma, verzia emulátora v teste) než v emulácii ako takej |
| O1 neplatí | ani kvalitnejšia dynamika nepridáva informáciu nad statiku → záver V1–V3 platí na dvoch datasetoch, **oslabuje** vysvetlenie „slabinou bola emulácia“ |
| D-norm | ak prínos v D-norm zmizne (Δ < +1 p. b.), uvedie sa, že stojí na celkovom množstve aktivity, ktoré môže byť artefaktom zberu |

### 4.4 Tézy (rovnaké kritériá ako docs/09, na real_full; doplnkovo real_P a emu_P)
| téza | kritérium |
|---|---|
| 1 | zero-day: TPR vynechanej rodiny kaskády ≥ statický + 1 p. b. a FPR ≤ FPR statického; stabilita = sm. odchýlka cez rodiny |
| 2 | FPR kaskády < FPR statického aj dynamického **a** TPR ≥ TPR statického − 1 p. b. (prahy z validácie; náhodné rozdelenie aj priemer zero-day) |
| 3 | študent vs. `mlp_large` hybrid: rozdiel TPR ≤ 1 p. b. pri nižšom CPU čase na vzorku |
| 4 | kaskáda B: podiel súborov s dynamickou analýzou pri splnení kritéria tézy 2 |

## 5. Porovnanie s Quo Vadis (popisné)
| porovnateľné (relatívne veličiny) | neporovnateľné |
|---|---|
| prínos dynamiky a hybridu nad statikou (Δ), strop kombinácie | absolútne TPR, FPR, ROC-AUC |
| nezhoda statického a dynamického modelu, opravené chyby | časový posun (Quo Vadis: test o 3 mesiace neskôr; KronoDroid: náhodné rozdelenie) |
| podiel eskalácií a podiel súborov s dynamickou analýzou (kaskáda B) | rodiny malvéru (iná platforma) |
| prínos destilácie (kd vs. nokd) | čas dynamickej analýzy (ani jeden dataset ho neobsahuje) |
| pomery CPU času (študent/učiteľ, kaskáda/hybrid), rovnaký počítač | sekvenčné modely (iba Quo Vadis) |
| pokles v zero-day oproti známym rodinám | príčina rozdielov medzi datasetmi (mení sa viac vecí naraz) |
| verdikty téz 1–4 | |

Doplnkový beh Quo Vadis s náhodným rozdelením sa **nerobí** (rozhodnutie autora). Uvedie sa v obmedzeniach.

## 6. Implementácia
Bez zmeny správania V1–V3: predvolený dataset ostáva Quo Vadis, staré skripty bežia rovnako.
1. `src/data/kronodroid/build_kronodroid.py` →
   `processed/kronodroid/{index, static, dynamic_real, dynamic_emu, dynamic_*_norm}`.
   Rovnaký formát ako `processed/static` (`X_*.npy`, `y_*.npy`, `meta_*.parquet` so `sha256`, `family`,
   `feature_names.csv`) a manifest. Rozdelenie sa uloží do indexu a verzuje.
2. Premenná prostredia `DIZERTACKA_DATASET` (`kronodroid_real_full` / `kronodroid_real_p` / `kronodroid_emu_p`)
   v `src/common/paths.py` a `src/data/providers.py` presmeruje priečinky dát. Bez nej sa nič nemení.
   - Overenie: načítanie Quo Vadis dá bitovo rovnaké polia ako pred zmenou.
   - Vynechané rodiny cez existujúci mechanizmus `DIZERTACKA_HOLDOUT_FAMILY`.
3. Konfigurácie `configs/kronodroid/` (rebríček, študenti, kaskády podľa bodu 3).
4. `scripts/run_v4.ps1` →
   - `runs_v4/{real_full,real_p,emu_p}/{full,lofo/<rodina>}` a `runs_v4/real_full/time`;
   - `runs_v4/comparison/v4/`: súhrn, kritériá O1, O2, tézy, bootstrap, porovnanie s Quo Vadis.
5. Postup behu:
   - technická kontrola na súkromnom notebooku (jedna rodina, skrátené ladenie);
   - značka `v4`;
   - plný beh na pracovnom notebooku v priečinku `dizertacka_quovadis-4` (CPU čas na rovnakom počítači ako V1–V3),
     prenos výsledkov bez modelov;
   - odhad: 1–2 večery, spresní sa po technickej kontrole.
6. Výsledky: `docs/20_vysledky_v4.md` a zhrnutie pre vedúcu.

## 7. Obmedzenia (uviesť v práci)
- Iná platforma (Android): V4 overuje vplyv kvality dynamických dát, nie je replikáciou na Windows PE.
- Iný emulátor než Speakeasy; problém inej verzie emulátora v teste (Quo Vadis) sa na KronoDroid neopakuje.
- Statika KronoDroid je chudobnejšia než EMBER; otázka 2 sa preto opiera o rozdiel emulátor vs. zariadenie
  (statika rovnaká), nie o absolútne čísla.
- Dynamika sú agregované počty volaní bez poradia → bez sekvenčných modelov. Podmienky behu (dĺžka, interakcia,
  verzia Androidu) CSV neuvádza.
- Hlavné rozdelenie je náhodné (bez časového posunu); časový posun iba doplnkovo pre malvér.
- Šum v označeniach benígnej triedy (docs/18, bod 3.1); vykazuje sa podskupina.
- Porovnanie s Quo Vadis je popisné; doplnkový beh Quo Vadis s náhodným rozdelením sa nerobil.
