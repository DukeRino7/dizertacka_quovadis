# 00 – Výskumné otázky a postup výberu modelov

Stav k 2026-11-01. Otázky sformuloval autor práce; pravidlá výberu sú **NÁVRH** (treba potvrdiť pred vyhodnotením).

## Výskumné otázky
1. **Najlepší hybridný model:** ktorý hybridný model (rebríček s rannou fúziou, dvojvetvová sieť, neskorá fúzia)
   dosahuje najlepšiu detekčnú kvalitu? Stane sa učiteľom študentov a veľkým modelom v kaskáde.
2. **Študenti:** ľahký statický a ľahký dynamický študent vytvorení destiláciou z hybridného učiteľa – sú lepší
   ako rovnako veľké modely bez destilácie a ako statické/dynamické baseline modely?
3. **Samostatné prístupy vs. hybrid:** sú samostatný statický a samostatný dynamický prístup horšie ako hybridný?
4. **Kaskáda:** (a) je kaskáda (dvaja lacní študenti, pri nezhode hybrid) rýchlejšia / menej náročná než hybrid
   na každej vzorke pri zachovaní kvality? (b) je pri podobných nárokoch spoľahlivejšia než samostatný statický
   alebo dynamický model?

## Pravidlá výberu (NÁVRH – určiť VOPRED, aby výber nebol prispôsobený výsledkom)
- Výber sa robí **iba na validácii**; test sa vyhodnotí až pre vybrané modely.
- **Najlepší model skupiny** = najvyššie ROC-AUC na validácii (priemer cez seedy). Ak je rozdiel medzi kandidátmi
  menší ako ich smerodajná odchýlka, rozhodne vyššie TPR pri FPR 1 % na validácii; ak aj to je zhodné, lacnejší model
  (nižší CPU čas na vzorku).
- **Učiteľ a veľký model kaskády** = najlepší hybridný model podľa pravidla vyššie.
- **Študent** = malá sieť s aspoň 10× nižším CPU časom na vzorku než učiteľ (docs/05).
- Variant s učiteľom z rovnakej modality (docs/05, variant A) je doplnkové porovnanie.

## Poznámka k nárokom
Kaskáda ušetrí výpočet iba vtedy, keď je hybrid výrazne drahší než dvojica študentov a podiel eskalácií je malý:
náklady kaskády ≈ študent statický + študent dynamický + podiel eskalácií × hybrid. Ak by najlepší hybrid bol
lacný (napr. LightGBM nad spojeným vektorom), úspora môže byť malá – aj to je výsledok, ktorý sa uvedie.
