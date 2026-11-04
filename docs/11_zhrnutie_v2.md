# Zhrnutie druhého experimentu (V2) – podklad pre konzultáciu

Dušan Čatloch, 4. 11. 2026. Podrobné výsledky sú v `docs/10_vysledky_v2.md`, plán a kritériá (určené pred behom)
v `docs/09_plan_v2.md`, surové výstupy v `runs_v2/`. Zhrnutie V1: `docs/08_zhrnutie_v1.md`.

## 1. Čo V2 pridáva oproti V1
- **Zero-day:** v 7 behoch sa vždy jedna rodina malvéru vynechá z tréningu aj validácie a meria sa, koľko z nej
  modely zachytia v teste (apríl 2022). Doplnkovo sa meria aj na jej januárových vzorkách (bez časového posunu).
  V každom behu sa znova natrénovali všetky modely (25 modelov × 3 seedy), učitelia, študenti a kaskády.
  Hyperparametre sa prevzali z V1.
- **Kaskáda B:** najprv rýchly statický model. Iba pri neistom skóre sa súbor emuluje a rozhodne dynamický model;
  pri nezhode rozhoduje hybrid. Šetrí počet súborov, ktoré treba spustiť v emulátore.
- **Nový študent** s učiteľom dvojvetvová sieť (komplexný hybrid), podľa znenia tézy 3.
- **Spresnenie téz po konzultácii:** „hybridný prístup“ v tézach 1 a 2 = kaskáda. Kritériá boli zapísané pred behom
  a nemenili sa.

## 2. Súhrnná tabuľka
Prahy z validácie (FPR ≤ 1 %), priemer 3 seedov. Zero-day = priemer cez 7 vynechaných rodín.
„Emulované“ = podiel súborov, ktoré treba spustiť v emulátore.

| prístup | časový test TPR | časový test FPR | zero-day: TPR vynechanej rodiny | zero-day FPR | emulované | CPU ms/vz. |
|---|---|---|---|---|---|---|
| statický LightGBM | **0,984** | 0,0048 | **0,792** | 0,0047 | **0 %** | 0,68 |
| dynamický LightGBM | 0,657 | 0,0198 | 0,509 | 0,0184 | 100 % | 0,43 |
| hybrid LightGBM | **0,984** | 0,0047 | 0,787 | 0,0045 | 100 % | **0,09** |
| hybrid dvojvetvová sieť | 0,977 | 0,0058 | 0,761 | 0,0068 | 100 % | 32,45 |
| študent statický (učiteľ dvojvetvová sieť) | 0,970 | 0,0083 | 0,762 | 0,0074 | 0 % | 0,30 |
| kaskáda A (študenti + hybrid) | 0,958 | **0,0026** | 0,739 | **0,0023** | 100 % | 0,62 |
| kaskáda A z LightGBM | 0,983 | 0,0039 | 0,780 | 0,0036 | 100 % | 1,12 |
| kaskáda B (študenti + hybrid) | 0,959 | 0,0034 | 0,731 | 0,0030 | **10,7 %** / 12,2 % | 0,34 |
| **kaskáda B z LightGBM, rozpočet 10 %** | **0,983** | 0,0039 | – ¹ | 0,0036 | 21,5 % / 22,8 % | 0,68 |

¹ Pri bodoch krivky rozpočtu sa TPR vynechanej rodiny neukladá. Celkové TPR v zero-day je 0,954
(statický LightGBM 0,960) a kritérium tézy 2 je splnené v 6 zo 7 rodín.

## 3. Hlavné zistenia
1. **V zero-day je najlepší statický model.** Zachytí v priemere 79 % vzoriek nevidenej rodiny; hybrid je
   rovnaký (79 %) a dynamický model iba 51 %. Bez časového posunu (január) je to 88 % oproti 47 %.
   Behaviorálne príznaky z emulácie sa na nové rodiny nezovšeobecňujú lepšie ako statické.
2. **Rodiny sa veľmi líšia.** Backdoor, ransomware a dropper zachytí statický model na 94–98 %, keylogger iba
   na 24 % (aj bez časového posunu na 43 %). Coinminer klesne z 87 % (január) na 60 % (apríl).
3. **Kaskády zhruba polovičia falošné poplachy** (FPR 0,0021–0,0036 oproti 0,0047) v časovom teste aj v zero-day.
   Kaskády so študentmi však strácajú 2–3 percentuálne body TPR, lebo statický študent je slabší ako LightGBM.
4. **Kaskáda B výrazne znižuje emuláciu.** So študentmi emuluje 11–12 % súborov namiesto 100 % (s predpokladom
   60 s na emuláciu ≈ 6–7 s na súbor), za cenu 2,6 p. b. TPR. Z LightGBM s rozpočtom 10 % emuluje ~22 % súborov
   a dosahuje rovnakú kvalitu ako kaskáda, ktorá emuluje všetko (TPR 0,983, FPR 0,0039).
5. **Destilácia z komplexného učiteľa funguje.** Statický študent s učiteľom dvojvetvová sieť je rovnako dobrý
   ako jeho učiteľ (zero-day 0,762 oproti 0,761) a 107× rýchlejší. Destilácia mu pridala 2,2 p. b. oproti študentovi
   bez nej (vo V1 bez prínosu). Lacný hybrid LightGBM je však ešte lepší aj rýchlejší.
6. **Neistota určená na validácii sa pri posune dát podhodnocuje.** Na teste je neistých 2–3× viac súborov ako na
   validácii; pri LightGBM je pásmo neistoty také úzke, že kaskáda B s pásmom stratí 6 p. b. TPR. Pevný rozpočet
   emulácie je odolnejší.

## 4. Prečo to tak dopadlo – analýza príčin
Z uložených predikcií, bez nového tréningu (podrobne `docs/10`, oddiel 6). Hodnoty označené ako horná hranica
používajú test a slúžia iba na vysvetlenie.
1. **Dynamická časť nemá čo pridať.** Aj keby sa súbor označil ako malvér vždy, keď ho označí statický *alebo*
   dynamický model, TPR nevidenej rodiny stúpne iba z 0,792 na 0,798. Dynamický model zachytí len 9 % vzoriek,
   ktoré statický minie. Žiadna kombinácia týchto dvoch modelov preto nemôže výrazne prekonať statický model.
2. **Statický model nové rodiny rozpozná, ale prah sa pri posune dát sprísni.** ROC-AUC je pri 6 zo 7 rodín ≥ 0,99.
   Prah z validácie (FPR 1 %) dáva na aprílovom teste FPR iba 0,5 %; pri plánovanom 1 % by TPR bolo 0,84 namiesto
   0,79. Skutočne novou rodinou je iba keylogger (AUC 0,84).
3. **Kaskáda B posiela na emuláciu správne súbory.** Pri rozpočte 10 % sa eskaluje 95 % chýb statického modelu.
   Keby druhý stupeň rozhodol eskalované súbory dokonale, TPR by bolo 0,96. Súčasný hybrid však v tejto oblasti
   opakuje chyby statického modelu.
4. **Chyby sa sústreďujú vo vzorkách, ktorých emulácia skončila `unsupported_api`, aj pri statickom modeli.**
   Zrejme ide o novú podskupinu vzoriek v apríli, nielen o chybu emulátora.

## 5. Súvis s tézami (kritériá z docs/09)
| téza | výsledok | vysvetlenie |
|---|---|---|
| 1. Kaskáda dosahuje vyššiu presnosť a stabilitu v zero-day | **nepotvrdená** | Kaskády sú lepšie ako dynamický model, ale horšie ako statický vo všetkých 7 rodinách. Príčina nie je v návrhu kaskády: aj najlepšia možná kombinácia statického a dynamického rozhodnutia by pridala najviac 0,6 p. b. (oddiel 4). Prínosom kaskády je nižšie FPR, nie vyššia detekcia. |
| 2. Kaskáda má menej falošných poplachov pri zachovaní citlivosti | **potvrdená pre kaskádu z LightGBM** | FPR 0,0039 oproti 0,0048 (časový), 0,0036 oproti 0,0047 (zero-day), TPR v tolerancii 1 p. b. Platí pre kaskádu A aj kaskádu B s rozpočtom 10 %. S destilovanými študentmi nie (TPR −2 až −3 p. b.). |
| 3. Destilácia vytvorí rýchlejší model s porovnateľnou presnosťou ako komplexný hybrid | **čiastočne potvrdená** | Platí pre statického študenta s učiteľom dvojvetvová sieť (rovnaké TPR, 107× rýchlejší). Neplatí pre dynamických študentov ani oproti lacnému hybridu LightGBM. |
| 4. Viacstupňová architektúra zníži náročnosť | **potvrdená v hlavnej miere** | Kaskáda B emuluje 11–12 % súborov (so študentmi) alebo ~22 % (z LightGBM, bez straty kvality) namiesto 100 %. Čas emulácie je predpoklad, nie meranie. |

## 6. Ďalší postup – V3 (rozhodnuté 2026-11-04, plán `docs/12_plan_v3.md`)
Na základe analýzy príčin (oddiel 4) sa V3 zameria na dve miesta, kde je merateľný priestor na zlepšenie:
- **Druhý stupeň učený iba na neistých súboroch.** Eskalácia trafí 95 % chýb, ale súčasný hybrid ich nevyrieši
  (0,79 oproti hornej hranici 0,96). Model učený len na tréningových súboroch blízko prahu statického modelu sa môže
  naučiť rozlišovať práve v tejto oblasti.
- **Prekalibrovanie prahu na nových neškodných súboroch** (samostatný scenár). Strata v zero-day vzniká hlavne
  sprísnením prahu pri posune dát. Nový legitímny softvér sa v praxi zbiera ľahko, malvér sa na kalibráciu nepoužije.
- Lepšie dynamické príznaky sa nerobia: obmedzuje ich chyba emulátora v dátach a pomohli by najmä jednej rodine.

## 7. Otázky na konzultáciu (návrhy, nerozhodnuté)
1. **Téza 1** – ponechať ako nepotvrdenú s vysvetlením (strop kombinácie +0,6 p. b.), alebo ju preformulovať na
   „kaskáda znižuje falošné poplachy aj pri nových rodinách“, čo výsledky podporujú? Výsledok V3 môže odpoveď zmeniť.
2. **Téza 2 a 4** – je prijateľné, že ich potvrdzuje kaskáda zložená z LightGBM modelov (bez destilácie),
   a nie hlavný variant so študentmi?
3. **Téza 3** – stačí potvrdenie pre statického študenta voči komplexnému hybridu (dvojvetvová sieť)?
4. **Scenár s prekalibrovaním prahu** (V3, C) – je prijateľný ako doplnkový scenár, ak sa vykáže oddelene
   od hlavných výsledkov?
