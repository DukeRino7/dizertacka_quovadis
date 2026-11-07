# 16 – Plán overenia robustnosti (štatistická významnosť, citlivosť na chybu emulácie)

Stav k 2026-11-07: **ROZHODNUTÉ autorom** (2026-11-07). Zapísané **pred** výpočtom. Nič sa netrénuje: všetko sa počíta
z uložených predikcií `runs_final`, `runs_v2`, `runs_v3`, s prahmi z validácie ako doteraz. Výsledky V1 – V3 sa nemenia;
tento krok overuje, či hlavné tvrdenia obstoja (a) štatisticky a (b) aj na súboroch s úspešnou emuláciou.

## R1 – štatistická významnosť hlavných tvrdení
**Metóda:** párový bootstrap testovacej množiny (apríl 2022), 2 000 opakovaní, stratifikovane podľa triedy (malvér /
neškodné). V každom opakovaní sa pre oba porovnávané prístupy na **tých istých** súboroch spočíta metrika (priemer cez
seedy 0 – 2, v zero-day aj cez 7 rodín) a ich rozdiel. Výsledok: rozdiel a jeho 95 % interval spoľahlivosti (percentilový).
Bootstrap zachytáva neistotu z výberu testovacích súborov, nie variabilitu tréningu (tá je v sm. odchýlke cez seedy).

**Pravidlá rozhodnutia (vopred):**
- *lepší / horší*: 95 % interval rozdielu neobsahuje 0;
- *nie horší* (tolerancia 1 p. b. ako v docs/09): dolná hranica intervalu rozdielu TPR > −1 p. b.;
- *rovnocenný*: celý interval rozdielu v ±1 p. b.

| # | tvrdenie | porovnanie | test (časový / zero-day) |
|---|---|---|---|
| 1 | kaskáda z LightGBM má menej falošných poplachov | A-baselines − statický: FPR *nižšie*, TPR všetkého malvéru *nie horšie* | oba |
| 2 | to isté pre kaskádu B s rozpočtom 10 % | B-baselines (10 %) − statický | oba |
| 3 | selektívna emulácia = kvalita hybridu (alt. téza B) | B-baselines (10 %) − hybrid LightGBM: TPR *nie horšie*, FPR *nižšie* | oba |
| 4 | kaskády so študentmi strácajú detekciu novej rodiny (téza 1) | A-main − statický, B-main − statický: TPR vynechanej rodiny *horšie* | zero-day |
| 5 | hybrid sa rovná statickému modelu | hybrid LightGBM − statický: TPR (časový) a TPR vynechanej rodiny *rovnocenné* | oba |
| 6 | študent z dvojvetvovej siete = učiteľ (alt. téza E) | `mlp_kd_twobranch` − dvojvetvová sieť: TPR vynechanej rodiny *rovnocenné* | zero-day |
| 7 | špecialista V3 pri rovnakom FPR = statický (alt. téza D) | z prekalibrovania (C): rozdiel TPR vynechanej rodiny a FPR, párovo cez rozdelenia × seedy, kalibrácia 5 % a 20 % | zero-day, časový |
| 8 | prekalibrovanie zvyšuje detekciu (alt. téza C) | statický prekalibrovaný − pôvodný: TPR vynechanej rodiny, párovo cez rozdelenia × seedy, 5 % a 20 % | zero-day, časový |

Body 7 a 8 používajú už vypočítané rozdelenia scenára C (`runs_v3/comparison/v3/recalibration.csv`). Interval je tu
2,5. – 97,5. percentil párových rozdielov cez 10 rozdelení × 3 seedy, teda neistota z výberu kalibračných súborov.

## R2 – citlivosť na chybu emulácie
**Námietka:** v teste skončilo 52 % emulácií chybou `unsupported_api` (v tréningu 0 %), takže záver „správanie nepridáva
informáciu o nových rodinách“ (alt. téza D, nepotvrdená téza 1) môže byť len dôsledkom pokazenej emulácie.

**Postup:** všetko z R1 a z analýzy príčin (docs/10, 6.1) sa vyhodnotí znova **iba na testovacích súboroch s úspešnou
emuláciou** (nie `unsupported_api`, nie malý report ≤ 5 API volaní; definícia ako v `v2_analysis.py`). Modely ani prahy
sa nemenia. Pre každú podskupinu sa uvedie počet súborov.
- TPR vynechanej rodiny a FPR: statický, dynamický, hybrid LightGBM, horná hranica „statický alebo dynamický“,
  kaskády A-baselines, B-baselines (10 %), špecialista V3;
- ROC-AUC statického a dynamického modelu (vynechaná rodina vs. neškodné).

**Kritérium (vopred):** zistenie D platí aj pri úspešnej emulácii, ak na tejto podskupine (zero-day, priemer cez rodiny)
horná hranica „statický alebo dynamický“ zvýši TPR vynechanej rodiny o ≤ 1 p. b. **a** ani hybrid, ani špecialista
nie sú lepší ako statický model o viac ako 1 p. b. Inak sa zistenie D zúži na „pri emulácii s chybami“ a v práci sa
uvedie, že dynamika pomáha tam, kde emulácia funguje.

## Výstupy
- `src/evaluation/robustness.py` → `runs_v3/comparison/robustness/ROBUSTNESS.md` (+ csv);
- `docs/17_vysledky_robustnost.md`; rozšírenie PDF pre vedúcu (`docs/15`) na najviac 3 strany.
