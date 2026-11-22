# 18 – Audit datasetu KronoDroid (V4)

Stav k 2026-11-22. Účel V4: overiť na inom datasete, či slabý prínos dynamiky v Quo Vadis (docs/07, 10, 13, 17)
spôsobuje kvalita dynamických dát (emulácia Speakeasy), alebo či ide o všeobecnejší jav (požiadavka vedúcej po
konzultácii). Tento dokument obsahuje **iba overené fakty a návrhy**; plán V4 s kritériami sa zapíše samostatne
(docs/19) pred trénovaním.

Zdroj: https://github.com/aleguma/kronodroid, commit `c6ec342` (stiahnuté 2026-11-22, hash ZIP v
`configs/kronodroid/data.yaml`). Článok: Guerra-Manzanares, Bahsi, Nõmm, *KronoDroid: Time-based Hybrid-featured
Dataset for Effective Android Malware Detection and Characterization*, Computers & Security 110 (2021) 102399
(podmienka použitia = citácia). Overené skriptom `src/data/kronodroid/audit_kronodroid.py` →
`processed/kronodroid/audit/AUDIT.md` (všetky čísla nižšie sú odtiaľ).

## 1. Formát
- 4 CSV (emulátor / skutočné zariadenie × benign / malware), jeden riadok = jedna APK, SHA-256 v stĺpci `sha256`.
- Raw logy a APK sú iba na vyžiadanie u autora; máme iba hotové príznaky (žiadne postupnosti).
- **Dynamické príznaky:** 288 počtov systémových volaní + `nr_syscalls` (= ich súčet, overené na všetkých riadkoch).
  Názvy stĺpcov sú v oboch podmnožinách rovnaké.
- **Statické príznaky:** 173 stĺpcov oprávnení (binárne + súčty podľa úrovne) a 12 metadát (veľkosť APK,
  počty aktivít, služieb, prijímačov, intent filtrov). Žiadna analýza kódu (na rozdiel od EMBER).
- **Ostatné stĺpce:** `Package`, `MalFamily`, dva dátumy, `Scanners`, `Detection_Ratio`, `TimesSubmitted`,
  `NrContactedIps` (údaje z VirusTotal).

| | emulátor | skutočné zariadenie |
|---|---|---|
| benign / malware | 35 246 / 28 745 | 36 755 / 41 382 |
| rodiny malvéru | 209 | 240 |
| rodiny s ≥ 100 / ≥ 500 vzorkami | 27 / 11 | 36 / 14 |
| nr_syscalls = 0 | 94 | 471 |

Počty zodpovedajú README datasetu.

## 2. Párovanie a označenia
- Označenie `Malware` vždy zodpovedá súboru, z ktorého riadok pochádza.
- V každej podmnožine sú **4 SHA-256 v oboch triedach** (rovnaký súbor raz ako benign, raz ako malware).
- **Prekrytie podmnožín: 63 320 APK je v oboch** (34 981 benign, 28 339 malware); iba v emulátore 667, iba na
  zariadení 14 813. Na prekrytí sa zhoduje označenie (100 %) a dátum (100 %), rodina v 61 443 prípadoch.
  Oprávnenia sú zhodné vždy; metadáta sa líšia iba chýbajúcimi hodnotami (nižšie).
- Dynamické vektory toho istého súboru sú v emulátore a na zariadení **takmer vždy iné** (zhodných 38).
  Medián `nr_syscalls` na prekrytí: emulátor 2 740, zariadenie 1 407 (Spearman 0,62).
- **Medián `nr_syscalls` podľa triedy sa medzi podmnožinami obracia:** emulátor benign 2 958 / malware 2 363,
  zariadenie benign 1 148 / malware 3 258.

## 3. Problémy a riziká
1. **Benígne súbory s rodinou malvéru:** 2 765 (emulátor) a 2 959 (zariadenie) benígnych riadkov má vyplnenú
   `MalFamily`; 12,6 % / 13,2 % benígnych má `Detection_Ratio` > 0 (max. 0,54). Benígna trieda teda nie je
   „0 detekcií na VirusTotal“, ale podľa nejakého prahu autorov (v CSV nie je uvedený). Riziko šumu v označeniach.
2. **Stĺpce z VirusTotal prezrádzajú triedu:** `Detection_Ratio` má medián 0 pri benign a 0,47 pri malware.
   Spolu so `Scanners`, `TimesSubmitted`, `MalFamily` nie sú vlastnosťou súboru.
3. **Dátumy sú dátumy súborov vnútri APK, nie dátum objavenia:** ~1 200–1 350 neplatných, `date_first` má
   5 285 / 6 945 hodnôt z roku 1980 (predvolený dátum v ZIP), niekoľko dátumov po roku 2020 (až 2107).
   README spomína 4 časové údaje; v CSV sú iba 2.
4. **Čas silno súvisí s triedou:** benígne súbory sú hlavne z rokov 2010–2011 (emulátor 27 130 z 35 246),
   malvér hlavne 2012–2014 a 2016–2018. Časové rozdelenie by meralo aj zmenu pomeru tried, nie iba posun správania.
5. **Statika je chudobná:** v oprávneniach je iba ~10 800 / ~13 700 unikátnych vektorov (duplicitných 53 128 /
   64 424 riadkov); s metadátami 61 446 / 74 300 unikátnych.
6. **Chýbajúce hodnoty:** `FilesInsideAPK` v emulátore chýba celý pre malvér (28 745) → v emulátore ho nepoužiť
   (alebo prevziať zo zariadenia podľa SHA-256); 9 metadát chýba v 309 / 642 riadkoch.
7. **Duplicity všetkých príznakov:** 167 / 171 riadkov, žiadna skupina rovnakých príznakov s oboma triedami.

## 4. Návrhy na rozhodnutie (NÁVRH, rozhodnúť v docs/19 pred trénovaním)
1. **Hlavné porovnanie na prekrytí 63 320 APK:** ten istý súbor, rovnaká statika, rovnaké označenie, rovnaké
   rozdelenie; líši sa iba zdroj dynamiky (emulátor vs. skutočné zariadenie). To je priamy test otázky vedúcej.
   Celé podmnožiny ako doplnok.
2. **Vyradiť z príznakov:** `sha256`, `Package`, `MalFamily`, dátumy, `Scanners`, `Detection_Ratio`,
   `TimesSubmitted`, `NrContactedIps`; `FilesInsideAPK` vyradiť pre obe podmnožiny (rovnaká statika).
3. **Vyradiť 4 SHA-256 s oboma označeniami** (v oboch podmnožinách).
4. **Benígne s `Detection_Ratio` > 0 ponechať** podľa označenia autorov; vyhodnotiť zvlášť ako podskupinu
   (citlivosť na šum v označení). Alternatíva: vyradiť – rozhodnúť z princípu, nie podľa výsledkov.
5. **Rozdelenie:** (a) náhodné stratifikované podľa rodiny s identickými vektormi spolu (ako vo V1 validácia),
   (b) zero-day vynechaním rodiny (rodiny s ≥ 500 vzorkami, ako vo V2). Časové rozdelenie iba doplnkovo,
   kvôli bodu 3.4 (iba platné roky 2008–2020, s upozornením na zmenu pomeru tried).
6. **Modely:** dynamika sú počty, nie postupnosti → iba tabulárne modely (LR, RF, LightGBM, MLP) a kaskády A/B;
   sekvenčné modely z V1 sa nepoužijú.

## 5. Obmedzenia, ktoré treba uvádzať
- Android, nie Windows PE: výsledok overuje vplyv kvality dynamických dát, nie je to replikácia na PE súboroch.
- Statika je slabšia než EMBER (iba oprávnenia a metadáta) → prínos dynamiky môže byť vyšší aj preto.
  Porovnanie emulátor vs. zariadenie má statiku rovnakú, takže tento vplyv vylučuje.
- Dynamika je agregovaná (počty volaní), bez poradia; dĺžka a nastavenie behu nie sú v CSV uvedené.
