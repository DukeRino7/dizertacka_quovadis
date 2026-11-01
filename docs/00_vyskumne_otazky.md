# 00 – Výskumné otázky a postup výberu modelov

Stav k 2026-11-01. Otázky sformuloval autor práce; pravidlá výberu a vykazovania sú **dohodnuté**.

## Tézy dizertačnej práce (znenie autora, 2026-11-01)
1. Hybridný prístup kombinujúci statické a dynamické príznaky dosahuje vyššiu presnosť a stabilitu v zero-day scenároch.
2. Hybridný prístup pri nízkej prevalencii malvéru dosahuje nižšiu mieru falošných poplachov pri zachovaní vysokej
   citlivosti v porovnaní so samostatným statickým alebo dynamickým modelom.
3. Destilácia vedomostí umožňuje vytvoriť rýchlejší model, ktorý si zachová porovnateľnú presnosť detekcie zero-day
   malvéru ako komplexný hybridný model.
4. Viacstupňová architektúra detekcie, v ktorej rýchle statické a destilované modely slúžia ako prvotný filter
   a komplexný dynamický/hybridný model je aplikovaný iba na neisté prípady, zníži celkovú výpočtovú náročnosť systému.

**Mapovanie téz na experimenty (NÁVRH, na dohodnutie):** zero-day = časový test (už teraz) + vynechanie rodiny
z tréningu (leave-one-family-out, plánované); nízka prevalencia = metriky prepočítané na nízky podiel malvéru
(plánované); stabilita = rozptyl cez seedy, rodiny a čas; „neisté prípady“ = eskalácia pri nezhode (teraz)
a doplnkovo pri neistom skóre (plánované).

## Verzie experimentu (DOHODNUTÉ 2026-11-01)
Jeden kód; verzia = značka v gite (`v1`, `v2`), výsledky v samostatných priečinkoch (`runs_v1/`, `runs_v2/`,
`scripts/run_all.ps1 -RunsDir ...`). V2 kód iba rozširuje, V1 ostáva reprodukovateľná zo svojej značky.

| | V1 | V2 (zero-day) |
|---|---|---|
| test | časový (tréning január 2022 → test apríl 2022) | časový + vynechaná rodina (leave-one-family-out, 7 rodín; rodina vynechaná aj z validácie; hyperparametre prevzaté z V1) |
| kaskáda A (statický + dynamický študent, pri nezhode hybrid; emulácia sa robí pre každý súbor, šetrí sa výpočet modelov) | áno | áno |
| kaskáda B (najprv statický študent, pri neistom skóre emulácia + hybrid; šetrí počet súborov v sandboxe) | nie (rozhodnutie autora) – pozn.: z uložených predikcií by bola takmer bez výpočtu | áno |
| nízka prevalencia (metriky prepočítané z TPR/FPR na prevalenciu napr. 1 %, 0,1 %) | áno (iba prepočet) | áno |

Formulácia tézy 4 sa prekonzultuje s vedúcou: „výpočtová náročnosť klasifikácie“ (kaskáda A) vs. „počet vzoriek
vyžadujúcich dynamickú analýzu“ (kaskáda B). Čas emulácie sa nemeria (dataset neobsahuje PE súbory); 60 s
z `speakeasy-config.json` možno použiť iba ako jasne označený predpoklad.

## Výskumné otázky
1. **Najlepší hybridný model:** ktorý hybridný model (rebríček s rannou fúziou, dvojvetvová sieť, neskorá fúzia)
   dosahuje najlepšiu detekčnú kvalitu? Stane sa učiteľom študentov a veľkým modelom v kaskáde.
2. **Študenti:** ľahký statický a ľahký dynamický študent vytvorení destiláciou z hybridného učiteľa – sú lepší
   ako rovnako veľké modely bez destilácie a ako statické/dynamické baseline modely?
3. **Samostatné prístupy vs. hybrid:** sú samostatný statický a samostatný dynamický prístup horšie ako hybridný?
4. **Kaskáda:** (a) je kaskáda (dvaja lacní študenti, pri nezhode hybrid) rýchlejšia / menej náročná než hybrid
   na každej vzorke pri zachovaní kvality? (b) je pri podobných nárokoch spoľahlivejšia než samostatný statický
   alebo dynamický model?

## Pravidlá výberu (DOHODNUTÉ 2026-11-01 – určené VOPRED, nemenia sa podľa výsledkov)
- Výber sa robí **iba na validácii**; test sa vyhodnotí až pre vybrané modely.
- **Najlepší model skupiny** = najvyššie **TPR pri FPR 1 % na validácii** (priemer cez seedy) – podiel zachyteného
  malvéru, keď smie byť najviac 1 % neškodných súborov chybne označených; je to pracovný bod, pri ktorom rozhodujú
  modely v kaskáde. ROC-AUC je pri hodnotách ~0,999 nasýtené a zle rozlišuje najlepšie modely.
- Ak je rozdiel menší ako smerodajná odchýlka cez seedy → rozhodne ROC-AUC na validácii → potom nižší CPU čas na vzorku.
- Ladenie hyperparametrov naďalej optimalizuje ROC-AUC (stabilná celková metrika); výber medzi modelmi podľa pravidla vyššie.
- **Učiteľ a veľký model kaskády** = najlepší hybridný model podľa tohto pravidla. Doplnková analýza: kaskáda aj s
  najlepším ťažkým hybridom (dvojvetvová sieť), ak by vyhral lacný model.
- **Študent** = malá sieť s aspoň 10× nižším CPU časom na vzorku než učiteľ (docs/05).
- Variant s učiteľom z rovnakej modality (docs/05, variant A) je doplnkové porovnanie.

## Interpretácia a vykazovanie výsledkov (DOHODNUTÉ)
- Hlavné výsledky sa uvádzajú na **teste** (zber o 3 mesiace neskôr → časový posun); validácia je takmer dokonalá,
  lebo pochádza z rovnakého obdobia ako tréning.
- Uvádzať aj prísnejší pracovný bod **FPR 0,1 %** – tam sú rozdiely medzi modelmi zreteľné
  (napr. LR: validácia 82,7 % → test 7,6 %; RF: 98,5 % → 92,0 %).
- Tvrdenia práce sú **porovnávacie** (kaskáda vs. hybrid vs. samostatné prístupy za rovnakých podmienok); absolútne
  čísla sú laboratórne a do prevádzky sa priamo neprenášajú → kapitola obmedzení (jeden dataset, 7 rodín, emulácia,
  32-bitové PE, artefakty zberu – kontrolné experimenty bez nich).
- Ak hybrid na teste neprinesie zlepšenie oproti statickému prístupu, je to platná odpoveď na otázku 3, nie zbytočná práca.
- **Analýza komplementarity (plánované):** ktoré chyby statického modelu (rodiny, zbalené vzorky, časový posun)
  opraví dynamický/hybridný model – argument, kde a prečo má hybrid zmysel.

## Overenie na reálnych súboroch (plánované na záver)
Súbory z počítača autora (prevažne legitímny softvér) → rovnaká extrakcia príznakov ako v datasete (EMBER s verziou
LIEF podľa autorov datasetu, Speakeasy s `speakeasy-config.json` z datasetu) → vyhodnotenie modelmi; meria sa hlavne
miera falošných poplachov. Malvér iba vo virtuálnom stroji. Pozor: dataset obsahuje iba 32-bitové PE.

## Poznámka k nárokom
Kaskáda ušetrí výpočet iba vtedy, keď je hybrid výrazne drahší než dvojica študentov a podiel eskalácií je malý:
náklady kaskády ≈ študent statický + študent dynamický + podiel eskalácií × hybrid. Ak by najlepší hybrid bol
lacný (napr. LightGBM nad spojeným vektorom), úspora môže byť malá – aj to je výsledok, ktorý sa uvedie.
