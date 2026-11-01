# 05 – Destilácia vedomostí a kaskáda

Stav k 2026-11-01: **dohodnutý postup** (autor práce súhlasil s bodmi 1, 3, 4, 5; bod 2 sa určí podľa výsledkov
baseline modelov). Implementácia destilácie nasleduje po výsledkoch učiteľov.

## Dohodnuté rozhodnutia
1. **Učiteľ – obe varianty sa porovnajú:**
   - A: učiteľ z rovnakej modality (najlepší statický → statický študent, najlepší dynamický → dynamický študent),
   - B: hybridný učiteľ pre oboch študentov (krížovo-modálna destilácia; hypotéza: študenti sa viac zhodnú
     s hybridom a kaskáda bude menej často eskalovať).
2. **Študent:** malá neurónová sieť; konkrétna veľkosť sa vyberie **podľa nameraných nárokov učiteľov**.
   Pravidlo (NÁVRH): študent má aspoň **10× nižší CPU čas na vzorku** (benchmark) než jeho učiteľ.
   Pozn.: ak je statický učiteľ už sám lacný (napr. LightGBM), rozdiel bude výrazný hlavne pri dynamických/hybridných modeloch.
3. **Strata:** α · BCE(skutočné označenie) + (1 − α) · T² · BCE(mäkké pravdepodobnosti učiteľa pri teplote T);
   α a T sa ladia na validácii s rovnakým rozpočtom ako ostatné modely (Optuna, 30 pokusov).
4. **Mäkké označenia na tréningu krížovo (out-of-fold):** tréning sa rozdelí na 5 častí (stratifikovane, so skupinami
   identických vektorov) a každú časť predpovedá učiteľ natrénovaný na zvyšných štyroch. Dôvod: učiteľ je na vlastných
   tréningových dátach príliš istý (napr. RF má na tréningu ROC-AUC 1,0), mäkké označenia by nič neniesli.
5. **Kontrola:** rovnaký študent natrénovaný bez destilácie (iba skutočné označenia) – dôkaz prínosu destilácie.

## Kaskáda (podľa zadania práce)
Statický a dynamický študent ohodnotia vzorku; ak sa zhodnú (oba malware alebo oba benign pri svojich prahoch
z validácie), rozhodnutie je konečné; inak rozhodne veľký hybridný model.

Vyhodnotenie (`src/cascade/`): kvalita kaskády, podiel eskalácií, spoločné chyby pri zhode študentov (chyby,
ktoré kaskáda nemôže opraviť), prínos hybridu na eskalovaných vzorkách, porovnanie s hybridom na každej vzorke,
so samostatnými študentmi a s neskorou fúziou; výpočtové nároky z benchmarku (CPU čas, latencia, GPU energia).
