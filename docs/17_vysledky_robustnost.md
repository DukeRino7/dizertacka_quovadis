# 17 – Výsledky overenia robustnosti

Stav k 2026-11-07. Plán a kritériá: `docs/16_plan_robustnost.md` (commit 8ea2883, pred výpočtom). Zdroj:
`runs_v3/comparison/robustness/ROBUSTNESS.md` a csv súbory (`src/evaluation/robustness.py`). Počítané na súkromnom
notebooku iba z uložených predikcií: nič sa netrénovalo a nemeral sa výkon. Rozdiely sú v percentuálnych bodoch (p. b.),
v zátvorke je 95 % interval spoľahlivosti (IS) z párového bootstrapu testu (2 000 opakovaní).

## 1. R1 – štatistická významnosť hlavných tvrdení
| # | tvrdenie | časový test | zero-day | záver |
|---|---|---|---|---|
| 1, 2 | kaskáda z LightGBM (A aj B 10 %) má nižšie FPR ako statický | −0,09 (−0,17 až −0,02) | −0,11 (−0,16 až −0,06) | **potvrdené** |
| 1, 2 | … a TPR všetkého malvéru nie je horšie o viac ako 1 p. b. | −0,12 (−0,20 až −0,05) | −0,62 (−0,70 až −0,54) | **potvrdené** |
| 3 | B-baselines (10 %) oproti hybridu: TPR nie horšie | −0,11 (−0,18 až −0,05) | −0,21 (−0,26 až −0,16) | **potvrdené** |
| 3 | B-baselines (10 %) oproti hybridu: FPR nižšie | −0,08 (−0,14 až −0,03) | −0,09 (−0,12 až −0,06) | **potvrdené** |
| 4 | kaskády so študentmi zachytia menej novej rodiny ako statický | – | A-main −5,3 (−5,9 až −4,8); B-main −6,1 (−6,7 až −5,6) | **potvrdené** |
| 5 | hybrid = statický (±1 p. b.) | TPR −0,01 (−0,11 až +0,09) | nová rodina −0,51 (−0,83 až −0,22) | **potvrdené** |
| 6 | študent z dvojvetvovej siete = učiteľ (±1 p. b.) | – | nová rodina +0,06 (−0,34 až +0,45) | **potvrdené** |

**Doplnkové zistenie:** kaskáda B z LightGBM (rozpočet 10 %) robí na každom testovacom súbore **presne to isté rozhodnutie**
ako kaskáda A z LightGBM (overené pre všetky seedy v časovom teste aj pri rodine rat: 0 rozdielnych rozhodnutí). Nezhody
statického a dynamického modelu mimo eskalovaných súborov existujú (~2 500), ale hybrid v nich vždy rozhodne ako statický
model. Kaskáda B tak dosahuje výsledok kaskády A s emuláciou iba 22 % súborov namiesto 100 %.

### Body 7 a 8 – scenár C (párovo cez 10 rozdelení × 3 seedy)
Interval tu vyjadruje neistotu z výberu kalibračných súborov.

| # | tvrdenie | kalibrácia | zero-day | časový test | záver |
|---|---|---|---|---|---|
| 7 | špecialista − statický pri rovnakom (prekalibrovanom) prahu, TPR | 5 % | −0,67 (−4,20 až +3,04) | +0,07 (−0,41 až +0,64) | **rozdiel nepreukázaný** |
| 7 | to isté | 20 % | +0,27 (−1,63 až +3,84) | +0,06 (−0,29 až +0,35) | **rozdiel nepreukázaný** |
| 8 | statický: prekalibrovaný − pôvodný, TPR | 5 % (~400 súborov) | +2,45 (−2,49 až +6,04) | +0,59 (−0,63 až +1,13) | v priemere zlepšenie, **nie spoľahlivo** |
| 8 | to isté | 20 % (~1 600 súborov) | **+3,58 (+0,76 až +6,14)** | **+0,91 (+0,40 až +1,10)** | **spoľahlivé zlepšenie** |

Spresnenie oproti docs/13: prekalibrovanie zvyšuje detekciu **spoľahlivo pri ~1 600** nových neškodných súboroch
(FPR pritom stúpne o +0,44 p. b. na ~0,9 %, teda k plánovanému 1 %). Pri ~400 súboroch je zlepšenie v priemere +2,5 p. b.,
ale nie v každom výbere.

Pri bode 7 je interval široký (zero-day −1,6 až +3,8), takže nemožno tvrdiť presnú rovnocennosť v ±1 p. b. Možno však
tvrdiť, že **zlepšenie špecialistu sa nepreukázalo**.

## 2. R2 – iba súbory s úspešnou emuláciou
V teste má úspešnú emuláciu 4 407 z 9 399 súborov malvéru a 3 174 zo 7 940 neškodných. Podľa rodiny (úspešné / všetky):
backdoor 1 613 / 1 940, coinminer 678 / 1 684, dropper 178 / 252, keylogger 225 / 1 041, ransomware 1 007 / 2 139,
rat 320 / 1 258, trojan 386 / 1 085.

| zero-day, priemer cez rodiny | všetky súbory | iba úspešná emulácia |
|---|---|---|
| statický LightGBM – TPR novej rodiny | 0,792 | **0,918** |
| dynamický LightGBM | 0,509 | 0,635 |
| hybrid LightGBM | 0,787 | 0,876 |
| špecialista V3 | 0,790 | 0,890 |
| horná hranica „statický alebo dynamický“ | 0,798 | 0,924 |
| ROC-AUC statický / dynamický | 0,974 / 0,918 | 0,996 / 0,917 |

Rozdiely oproti statickému modelu (iba úspešná emulácia):
- horná hranica kombinácie: **+0,65 p. b.** (+0,39 až +0,92);
- hybrid: **−4,21 p. b.** (−5,10 až −3,28);
- špecialista: **−2,78 p. b.** (−3,63 až −1,88).

**Kritérium R2 (docs/16) je splnené:** zistenie D („správanie z emulácie nepridáva informáciu o nových rodinách“)
**platí aj tam, kde emulácia funguje**.

Je to dokonca silnejšie: na súboroch s úspešnou emuláciou dynamické príznaky detekciu novej rodiny **zhoršujú**. Hybrid aj
špecialista sú o 3 – 4 p. b. horší ako samotný statický model. Chybou emulácie sa teda nedá vysvetliť, prečo dynamika
nepomáha.

**Interpretácia:** dynamický model sa naučil správanie známych rodín a pri novej rodine ho aj jeho kombinácia so
statickým modelom zavádza. Na všetkých súboroch sa to neprejaví, lebo pri polovici súborov emulácia zlyhala a dynamické
príznaky sú tam takmer prázdne.

Ďalšie pozorovanie: statický model zachytí novú rodinu na súboroch s úspešnou emuláciou v 92 % prípadov, na všetkých
súboroch v 79 %. Ťažké súbory sú teda práve tie, ktorých emulácia skončila `unsupported_api` (docs/10, 6.4). Zrejme ide
o odlišnú podskupinu vzoriek v apríli.

## 3. Čo z toho vyplýva pre tézy
- **Téza 2 / alternatívna A:** štatisticky významná v časovom teste aj v zero-day (FPR nižšie, TPR v tolerancii).
- **Téza 4 / alternatívna B:** kaskáda B z LightGBM rozhoduje identicky s kaskádou A pri 22 % emulácií; oproti hybridu
  je TPR nie horšie a FPR významne nižšie.
- **Téza 1 / alternatívna D:** posilnená. Platí aj na súboroch s úspešnou emuláciou a dynamika tam dokonca škodí.
- **Alternatívna C (posun prahu):** platí spoľahlivo pri ~1 600 nových neškodných súboroch; pri ~400 iba v priemere.
- **Téza 3 / alternatívna E:** rovnocennosť študenta a učiteľa (±1 p. b.) je štatisticky potvrdená na všetkých súboroch.

## 4. Obmedzenia
- Bootstrap zachytáva neistotu z výberu testovacích súborov, nie variabilitu tréningu. Tú vyjadruje sm. odchýlka cez seedy
  v docs/10 a docs/13.
- Na podskupine s úspešnou emuláciou je menej súborov (najmä neškodných: 3 174), preto sú intervaly širšie. Pri dvoch
  tvrdeniach (FPR v časovom teste, nie horšie TPR v zero-day) preto na podskupine neprejde hranica významnosti, hoci
  smer je rovnaký.
