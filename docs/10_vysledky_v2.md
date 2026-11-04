# 10 – Výsledky V2 (zero-day a kaskáda B)

Stav k 2026-11-04. Zdroj: `runs_v2/`, beh kódu značky `v2` (ZIP, `VERSION.txt` = v2) na pracovnom notebooku DCATLOCH.
Beh trval 2026-11-03 20:29 – 2026-11-04 20:47, prerušený ráno cez Ctrl+C a potom pokračoval; čistý výpočet ≈ 15,5 h
(`runs_v2/RUN_INFO.txt`). Všetkých 13 krokov časti `full` a 24 krokov každej zo 7 rodín skončilo (`_state/`).
Beh bol plný, nie skúšobný (`smoke: False`, časy tréningu zodpovedajú V1).

Plán a kritériá boli určené vopred v `docs/09_plan_v2.md` a podľa výsledkov sa nemenili.
- Prahy sú z validácie (FPR ≤ 1 %), hodnoty sú priemer cez seedy 0–2.
- Zero-day: v každom behu je jedna rodina vynechaná z tréningu aj validácie a hodnoty sú priemer cez 7 rodín.
- **TPR vynechanej rodiny** = podiel jej vzoriek v aprílovom teste, ktoré model zachytí. „Január“ = jej vzorky
  z tréningu a validácie, ktoré model nevidel (nová rodina bez časového posunu).
- **Emulované súbory** = podiel súborov, ktoré treba spustiť v emulátore. Emulácia sa nemeria, 60 s na súbor je **predpoklad**.

Súhrny: `runs_v2/comparison/v2/README.md` (tabuľky, tézy), `BUDGET.md` (krivka rozpočtu emulácie),
`temporal_test.csv`, `zero_day_per_family.csv`. Body označené **Interpretácia** sú môj návrh výkladu, nie odsúhlasený záver.

Prečo beh trval kratšie ako V1 (2–3 dni): vo V2 sa hyperparametre preberajú z V1 (ladili sa iba dvaja noví študenti)
a dynamická cache sa nevytvára nanovo. Na jednu rodinu pripadli ~2 h.

## 1. Časový test (rozdelenie V1, test apríl 2022)
Modely V1 a kaskády A pochádzajú z `runs_final`, nové modely a kaskády B z `runs_v2/full`.

| prístup | TPR | FPR | F1 | emulované súbory | CPU ms/vz. |
|---|---|---|---|---|---|
| statický LightGBM | 0,9843 | 0,0048 | 0,9900 | 0 % | 0,68 |
| dynamický LightGBM | 0,6572 | 0,0198 | 0,7852 | 100 % | 0,43 |
| hybrid LightGBM | 0,9842 | 0,0047 | 0,9901 | 100 % | 0,09 |
| hybrid dvojvetvová sieť (komplexný) | 0,9767 | 0,0058 | 0,9857 | 100 % | 32,45 |
| študent statický (KD z hybridu LightGBM) | 0,9581 | 0,0059 | 0,9761 | 0 % | 0,30 |
| **študent statický (KD z dvojvetvovej siete, nový)** | 0,9701 | 0,0083 | 0,9813 | 0 % | 0,30 |
| študent dynamický (KD z dvojvetvovej siete, nový) | 0,5182 | 0,0135 | 0,6775 | 100 % | 0,28 |
| kaskáda A-main | 0,9579 | 0,0026 | 0,9774 | 100 % | 0,62 |
| kaskáda A-baselines | 0,9831 | 0,0039 | 0,9898 | 100 % | 1,12 |
| kaskáda A-twobranch (nová) | 0,9683 | 0,0025 | 0,9828 | 100 % | 0,60 |
| **kaskáda B-main** | 0,9587 | 0,0034 | 0,9775 | **10,7 %** | 0,34 |
| kaskáda B-direct | 0,9674 | 0,0032 | 0,9821 | 10,7 % | 0,31 |
| kaskáda B-heavy | 0,9528 | 0,0031 | 0,9745 | 10,7 % | 2,45 |
| kaskáda B-baselines | 0,9241 | 0,0004 | 0,9604 | 0,4 % | 0,68 |
| kaskáda B-nokd | 0,9601 | 0,0035 | 0,9782 | 9,1 % | 0,34 |
| kaskáda B-twobranch | 0,9679 | 0,0038 | 0,9821 | 8,5 % | 0,33 |

Ostatní študenti a kaskády sú v `runs_v2/comparison/v2/README.md`. Kaskáda B-main na validácii emuluje 3,9 % súborov,
na teste 10,7 %.

## 2. Zero-day – vynechaná rodina (priemer cez 7 rodín)
| prístup | TPR vynech. rodiny (test) | sm. odch. | najhoršia rodina | TPR vynech. rodiny (január) | FPR | TPR všetok malvér | emulované |
|---|---|---|---|---|---|---|---|
| statický LightGBM | **0,792** | 0,277 | 0,241 | **0,879** | 0,0047 | **0,960** | 0 % |
| dynamický LightGBM | 0,509 | 0,243 | 0,124 | 0,471 | 0,0184 | 0,649 | 100 % |
| hybrid LightGBM | 0,787 | 0,305 | 0,168 | 0,876 | 0,0045 | 0,956 | 100 % |
| hybrid dvojvetvová sieť | 0,761 | 0,291 | 0,186 | 0,801 | 0,0068 | 0,944 | 100 % |
| študent statický (KD z dvojvetvovej siete) | 0,762 | 0,283 | 0,202 | 0,806 | 0,0074 | 0,936 | 0 % |
| kaskáda A-main | 0,739 | 0,290 | 0,144 | 0,817 | 0,0023 | 0,929 | 100 % |
| kaskáda A-baselines | 0,780 | 0,300 | 0,168 | 0,875 | 0,0036 | 0,954 | 100 % |
| kaskáda B-main | 0,731 | 0,304 | 0,103 | 0,808 | 0,0030 | 0,925 | 12,2 % |
| kaskáda B-direct | 0,737 | 0,309 | 0,103 | 0,827 | 0,0029 | 0,932 | 12,2 % |
| kaskáda B-twobranch | 0,746 | 0,300 | 0,146 | 0,792 | 0,0032 | 0,925 | 8,8 % |

TPR vynechanej rodiny podľa rodiny (test):

| prístup | backdoor | coinminer | dropper | keylogger | ransomware | rat | trojan |
|---|---|---|---|---|---|---|---|
| statický LightGBM | 0,984 | 0,601 | 0,943 | 0,241 | 0,982 | 0,923 | 0,872 |
| dynamický LightGBM | 0,422 | 0,499 | 0,680 | 0,124 | 0,313 | 0,785 | 0,743 |
| hybrid LightGBM | 0,986 | 0,597 | 0,947 | 0,168 | 0,985 | 0,947 | 0,879 |
| kaskáda A-main | 0,890 | 0,574 | 0,896 | 0,144 | 0,943 | 0,902 | 0,826 |
| kaskáda B-main | 0,884 | 0,565 | 0,893 | 0,103 | 0,942 | 0,907 | 0,822 |

TPR vynechanej rodiny v januári (bez časového posunu):

| prístup | backdoor | coinminer | dropper | keylogger | ransomware | rat | trojan |
|---|---|---|---|---|---|---|---|
| statický LightGBM | 0,993 | 0,865 | 0,979 | 0,429 | 0,995 | 0,964 | 0,930 |
| dynamický LightGBM | 0,498 | 0,256 | 0,646 | 0,367 | 0,083 | 0,774 | 0,671 |
| hybrid LightGBM | 0,992 | 0,871 | 0,980 | 0,395 | 0,997 | 0,968 | 0,932 |

Celý rebríček modelov (LR, RF, MLP, seq_cnn) je v `runs_v2/comparison/v2/README.md`. V zero-day je statický LightGBM
najlepší samostatný model a všetky statické modely sú výrazne lepšie ako všetky dynamické.

## 3. Krivka rozpočtu emulácie (doplnok z docs/09, `BUDGET.md`)
Pri rozpočte sa emulujú súbory, ktorých skóre statického modelu je najbližšie jeho prahu. Hranicu určuje rozpočet
na validácii; na teste je podiel emulovaných súborov vyšší, lebo dáta sú posunuté.

| kaskáda | bod | test | emulované | TPR | FPR | kritérium tézy 2 |
|---|---|---|---|---|---|---|
| B-main | pásmo neistoty | časový | 10,7 % | 0,9587 | 0,0034 | nie |
| B-main | rozpočet 10 % | časový | 18,8 % | 0,9597 | 0,0037 | nie |
| B-direct | rozpočet 10 % | časový | 18,8 % | 0,9856 | 0,0056 | nie (FPR) |
| **B-baselines** | pásmo neistoty | časový | 0,4 % | 0,9241 | 0,0004 | nie (TPR) |
| **B-baselines** | **rozpočet 10 %** | časový | **21,5 %** | **0,9831** | **0,0039** | **áno** |
| **B-baselines** | **rozpočet 10 %** | zero-day | **22,8 %** | **0,9536** | **0,0036** | **áno** (6 zo 7 rodín, nie keylogger) |

- B-baselines pri rozpočte 10 % dosahuje **rovnaké TPR a FPR ako kaskáda A-baselines** (0,9831 / 0,0039, v zero-day
  0,9536 / 0,0036), hoci emuluje iba 21–23 % súborov namiesto 100 %. Väčší rozpočet už nič nemení.
- Pri kaskádach so študentom väčší rozpočet TPR nezvyšuje (B-main ostáva 0,958 – 0,960). Ak sa statický študent
  a dynamický študent zhodnú na „neškodný“, hybrid súbor nedostane, a dynamický model je na teste slabý.

## 4. Tézy (kritériá z docs/09)
| téza | výsledok | stručne |
|---|---|---|
| 1. kaskáda presnejšia a stabilnejšia v zero-day | **nepotvrdená** | TPR vynechanej rodiny: kaskády 0,73–0,78, statický LightGBM 0,79; kaskády sú horšie v 7 zo 7 rodín, sm. odchýlka nie je menšia; FPR je nižšie (0,0023–0,0036 oproti 0,0047) |
| 2. kaskáda menej falošných poplachov pri zachovaní citlivosti | **potvrdená pre kaskády z LightGBM**, nie pre kaskády so študentmi | A-baselines (časový aj zero-day) a B-baselines pri rozpočte 10 %; hlavný variant (A-main, B-main) stráca 2,5–3,5 p. b. TPR |
| 3. destilovaný model rýchlejší, porovnateľne presný ako komplexný hybrid | **čiastočne potvrdená** | statický študent s učiteľom dvojvetvová sieť: TPR vynech. rodiny 0,762 oproti 0,761, 107× rýchlejší; ostatní statickí študenti −1,4 až −2,1 p. b.; dynamickí študenti nie; oproti lacnému hybridu LightGBM nie |
| 4. viacstupňová architektúra zníži náročnosť | **potvrdená v hlavnej miere** (podiel emulácie) | B-main emuluje 10,7 % (zero-day 12,2 %) súborov namiesto 100 %, ale stráca 2,6 p. b. TPR oproti hybridu; B-baselines s rozpočtom 10 % emuluje 21,5 % a kvalitu nestráca |

### Téza 1 podrobnejšie
Kritérium: TPR vynechanej rodiny a stabilita (sm. odchýlka cez rodiny) oproti samostatným modelom.
- Kaskády A-main a B-main sú lepšie ako dynamický LightGBM (7 zo 7, resp. 6 zo 7 rodín), ale horšie ako statický
  aj hybridný LightGBM v každej rodine. Oproti dvojvetvovej sieti sú lepšie v 3 zo 7 rodín.
- **Interpretácia:** kaskáda sa v zero-day nemá od čoho „odraziť“. Dynamické príznaky (API volania zo Speakeasy)
  sa na novú rodinu zovšeobecňujú horšie ako statické (január 0,47 oproti 0,88), takže dynamický stupeň pri nezhode
  pridá menej, ako pokazí. Najväčšie straty kaskády sú pri keyloggeri (statický 0,24, B-main 0,10).
- Keylogger je ťažký pre všetky modely aj bez časového posunu (január: statický 0,43). Coinminer klesá z 0,87
  (január) na 0,60 (apríl), teda pri ňom pôsobí hlavne časový posun.

### Téza 2 podrobnejšie
Kritérium: FPR kaskády < FPR statického aj dynamického modelu **a** TPR ≥ TPR statického − 1 p. b.
- A-baselines: časový test FPR 0,0039 < 0,0048, TPR 0,9831 ≥ 0,9743; zero-day FPR 0,0036 < 0,0047, TPR 0,9536 ≥ 0,9498.
- B-baselines s rozpočtom 10 %: rovnaké čísla pri 21–23 % emulovaných súborov. Je to doplnkový bod krivky,
  ktorý bol v docs/09 určený vopred, nie hlavný pracovný bod.
- Kaskády so študentmi znižujú FPR viac (0,0025–0,0038), ale TPR klesne o 1,6–3,1 p. b., pretože statický študent
  je slabší ako statický LightGBM (0,958 – 0,970 oproti 0,984).
- **Upozornenie:** variant, ktorý spĺňa kritérium, je zároveň jediný bez destilácie. Pri písaní treba uviesť, že
  téza platí pre kaskádu ako princíp (viac stupňov znižuje FPR), nie pre destilovaných študentov.

### Téza 3 podrobnejšie
- Nový variant `mlp_kd_twobranch` (statický študent, učiteľ = dvojvetvová sieť): zero-day TPR vynechanej rodiny
  0,7620 oproti 0,7614 (rozdiel +0,06 p. b.), CPU 0,30 ms oproti 32,45 ms. Časový test: TPR 0,970 oproti 0,977
  (−0,7 p. b.), FPR však vyššie (0,0083 oproti 0,0058).
- Statický študent sa učí iba zo statického vstupu, takže porovnateľnosť znamená, že dvojvetvová sieť
  z dynamickej vetvy v zero-day takmer nič nezíska. Nie je to dôkaz, že destilácia preniesla „dynamické“ znalosti.
- Prínos destilácie: študent s KD z dvojvetvovej siete 0,762, bez KD 0,740 (+2,2 p. b.). Je to jediný prípad,
  kde destilácia pomohla viac ako o 1 p. b.; vo V1 nepomohla.
- Oproti lacnému hybridu LightGBM (0,09 ms, TPR 0,787) sú študenti pomalší aj horší. Tento výsledok sa uvedie
  rovnako ako vo V1.

### Téza 4 podrobnejšie
- Hlavná miera (docs/09) je podiel súborov, ktoré treba emulovať: kaskáda B-main 10,7 % (časový) a 12,2 % (zero-day),
  oproti 100 % pri dynamickom alebo hybridnom modeli a kaskáde A. S predpokladom 60 s emulácie to je ≈ 6,4 s na súbor
  oproti 60 s.
- Cena: TPR B-main 0,959 oproti 0,984 (hybrid LightGBM). Kritérium tézy 4 kvalitu nestanovuje, pri písaní ju však treba uviesť.
- Najlepší kompromis: B-baselines s rozpočtom 10 % emuluje 21,5 % súborov (≈ 13 s na súbor) pri kvalite
  kaskády A-baselines a hybridu (TPR 0,983, FPR 0,0039 – nižšie ako hybrid 0,0047).
- CPU čas modelov je pri všetkých kaskádach rádovo menší ako emulácia (desatiny ms); v skutočnej prevádzke rozhoduje emulácia.

## 5. Pásmo neistoty pri posune dát
Pásmo neistoty je určené na validácii: nad hornou hranicou je FPR ≤ 0,1 %, pod dolnou je ≤ 1 % malvéru.
- Pre študentov je pásmo široké (lo ≈ 0,56–0,63, hi ≈ 0,998). Na validácii emuluje 3,9 % súborov, na teste 10,7 %.
- Pre LightGBM je pásmo veľmi úzke (lo ≈ 0,974–0,979, hi ≈ 0,979–0,982), lebo jeho skóre na validácii je takmer
  dokonale rozdelené. Na teste potom pod dolnú hranicu spadne ~7 % malvéru (TPR 0,924) a emuluje sa iba 0,4 % súborov.
- **Interpretácia:** neistota určená na dátach z rovnakého obdobia ako tréning sa pri časovom posune podhodnocuje.
  Je to ten istý jav ako vo V1 (eskalácie 5,6 % na validácii, 25 % na teste). Pevný rozpočet emulácie je voči posunu
  odolnejší ako pásmo z prahov. Nastaviť pásmo podľa testu by porušilo pravidlá, preto sa to nerobí.

## 6. Zhrnutie
1. V zero-day je najlepší **statický LightGBM** (TPR vynechanej rodiny 0,79). Hybridný model je rovnaký (0,79)
   a dynamický výrazne horší (0,51). Behaviorálne príznaky z emulácie Speakeasy na nové rodiny nepomáhajú.
2. Kaskády zhruba **polovičia falošné poplachy** (FPR 0,0021–0,0036 oproti 0,0047). Bez straty TPR to však dokážu
   iba kaskády zložené z LightGBM.
3. Kaskáda B potrebuje emuláciu iba pre **9–12 %** súborov (so študentmi) alebo **21–23 %** (LightGBM s rozpočtom 10 %,
   bez straty kvality).
4. Destilovaný statický študent dosahuje kvalitu komplexného hybridu (dvojvetvová sieť) pri 107× nižšom CPU čase;
   lacný hybrid LightGBM je však ešte lacnejší aj lepší.
5. Slabým miestom kaskád so študentmi je prvý stupeň, teda statický študent (o 1,4–2,6 p. b. horší ako LightGBM).

## 7. Obmedzenia V2
- Hyperparametre sú z V1, kde ladenie videlo validáciu so všetkými rodinami (docs/09).
- Rodina = označenie datasetu; rodiny môžu zdieľať kód (napr. dropper a trojan), takže „nevidená rodina“ nie je
  nutne nevidený kód.
- Emulácia je iba predpoklad 60 s na súbor; skutočný čas emulácie ani celej kaskády sa nemeral.
- Krivka rozpočtu je doplnková analýza. Bod 10 % nebol vybraný podľa testu, ale je jediný, kde to funguje,
  a preto sa uvádza celá krivka.

## 8. Návrhy na ďalší postup (NÁVRH, nerozhodnuté)
- Prerokovať s vedúcou spresnenie téz podľa výsledkov:
  - téza 2: „kaskáda“ ako princíp (LightGBM);
  - téza 4: rozpočet emulácie;
  - téza 1: nepotvrdená, vysvetliť slabou zovšeobecniteľnosťou dynamických príznakov.
- Analýza komplementarity pre zero-day (ktoré chyby statického modelu kaskáda opraví a ktoré pokazí podľa rodín) –
  z uložených predikcií, bez nového tréningu.
- Ak by bol čas: skutočné meranie celej kaskády (docs/09, bod 7) a overenie na reálnych súboroch (docs/00).
