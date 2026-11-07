# Zhrnutie experimentov V1 – V3 – podklad pre konzultáciu

Dušan Čatloch, 7. 11. 2026. Podrobnosti: V1 `docs/07`, V2 `docs/10`, V3 `docs/13`; plány s kritériami určenými
pred behom: `docs/09` (V2), `docs/12` (V3). Predchádzajúce zhrnutia: `docs/08` (V1), `docs/11` (V2).

## 1. Čo sa robilo
| verzia | otázka | test |
|---|---|---|
| **V1** | statická vs. dynamická vs. hybridná detekcia; destilácia; kaskáda A (dvaja študenti, pri nezhode hybrid) | časový posun (tréning január → test apríl 2022) |
| **V2** | to isté pre **nové rodiny** (zero-day: 7 behov, vždy jedna rodina vynechaná z tréningu aj validácie); kaskáda B (najprv statický model, emulácia iba pri neistom skóre) | časový posun + nevidená rodina |
| **V3** | podľa analýzy príčin V2: (B) druhý stupeň učený iba na sporných súboroch, (C) prekalibrovanie prahu na nových neškodných súboroch | ako V2 |

Dataset Quo Vadis: statické príznaky EMBER + reporty z emulácie Speakeasy. Hlavné modely: LightGBM (vybraný pravidlom
TPR pri FPR 1 % na validácii). Prahy vždy z validácie, test nikdy na ladenie, 3 seedy.

## 2. Stav téz
| téza | stav | stručne |
|---|---|---|
| 1. Kaskáda dosahuje vyššiu presnosť a stabilitu v zero-day | **nepotvrdená, s vysvetlením** | Na nevidených rodinách je najlepší samotný statický model (zachytí 79 %, dynamický 51 %). Dva nezávislé dôkazy, že príčinou sú dáta, nie návrh kaskády: (1) aj najlepšia kombinácia statického a dynamického rozhodnutia pridá najviac 0,6 p. b.; (2) model učený len na sporných súboroch je pri rovnakom FPR rovnaký ako statický. Dynamické príznaky z emulácie nenesú doplnkovú informáciu o nových rodinách. |
| 2. Kaskáda má menej falošných poplachov pri zachovaní citlivosti | **potvrdená pre kaskády z LightGBM** | FPR o ~20–25 % nižšie pri TPR v tolerancii 1 p. b., v časovom teste aj v zero-day, aj po prekalibrovaní prahu. Neplatí pre kaskády s destilovanými študentmi (TPR −2 až −4 p. b.). |
| 3. Destilácia vytvorí rýchlejší model s porovnateľnou presnosťou ako komplexný hybrid | **čiastočne** | Statický študent s učiteľom dvojvetvová sieť má rovnakú presnosť ako učiteľ a je 107× rýchlejší. Lacný hybrid LightGBM je však ešte rýchlejší aj presnejší. |
| 4. Viacstupňová architektúra zníži náročnosť | **potvrdená v podiele emulácie** | Kaskáda B potrebuje emulovať iba 21,5 % súborov bez straty kvality (z LightGBM) alebo 10,7 % so stratou 2,6 p. b. (so študentmi); ostatné prístupy emulujú 100 %. Čas emulácie nemožno zmerať: dataset nemá PE súbory a reporty neobsahujú čas; 60 s je iba horný limit z konfigurácie. |

## 3. Hlavné zistenia
1. **Statické príznaky dominujú.** Hybridný model je rovnaký ako statický (V1, V2). Dynamický model je slabší a pri
   časovom posune aj pri nových rodinách zlyháva výraznejšie.
2. **Prínosom kaskády je menej falošných poplachov**, nie vyššia detekcia. Pri nízkej prevalencii malvéru je to
   podstatné (V1: falošné poplachy na 1 skutočný pri prevalencii 0,1 % klesnú zo 4,9 na 4,0 – 2,6).
3. **Kaskáda B šetrí emuláciu:** sporných je ~10 – 23 % súborov a iba tie treba emulovať.
4. **Najväčšiu stratu pri nových rodinách spôsobuje posun prahu, nie chýbajúca informácia.** Statický model nové
   rodiny zoraďuje správne (ROC-AUC ≥ 0,99 pri 6 zo 7 rodín), ale prah z validácie je v apríli príliš prísny
   (FPR 0,5 % namiesto 1 %). Prekalibrovanie na **~400 – 1 600 nových neškodných súboroch** (bez malvéru) zvýši
   zachytenie nevidenej rodiny z 79 % na 82 – 83 % pri FPR do 1 %. 79 súborov na to nestačí.
5. **Keylogger** je jediná skutočne nová rodina: zachytí sa len 24 % aj bez časového posunu 43 %.
6. **Destilácia** pomohla iba s komplexným učiteľom (dvojvetvová sieť, +2,2 p. b.); s lacným učiteľom (LightGBM) nie.

## 4. Obmedzenia
- Jeden dataset, 7 rodín, iba 32-bitové PE súbory; dynamické dáta sú z emulácie (Speakeasy), nie zo sandboxu.
- V testovacom období skončilo 52 % emulácií chybou `unsupported_api` (iná verzia emulátora). Dynamický prístup to
  znevýhodňuje, preto sa v práci uvádza ako obmedzenie dát.
- Čas emulácie a extrakcie príznakov sa nedá zmerať; CPU čas sa meria iba pre modely.
- V3 vychádzala z analýzy testu V2 (nie je nezávislým potvrdením); kritériá boli zapísané vopred.
- Scenár s prekalibrovaním používa neškodné súbory z testovacieho obdobia, preto sa vykazuje oddelene.

## 5. Otázky na konzultáciu (návrhy, nerozhodnuté)
1. **Téza 1:** ponechať ako nepotvrdenú s vysvetlením (dva dôkazy, že dynamické príznaky z emulácie nepridávajú
   informáciu o nových rodinách), alebo ju preformulovať na „kaskáda znižuje falošné poplachy aj pri nových rodinách“?
2. **Téza 2 a 4:** je prijateľné, že ich potvrdzuje kaskáda z LightGBM modelov (bez destilácie)?
3. **Téza 3:** stačí čiastočné potvrdenie (statický študent oproti komplexnému hybridu)?
4. **Posun prahu a prekalibrovanie** – zaradiť do práce ako samostatné zistenie (praktický význam: koľko nových
   neškodných súborov treba na udržanie pracovného bodu)?
5. **Ďalšie experimenty** – podľa výsledkov už nie sú potrebné na zodpovedanie téz. Ostáva prípadné overenie na
   reálnych súboroch (najmä falošné poplachy na legitímnom softvéri), ak to vedúca bude považovať za potrebné.
