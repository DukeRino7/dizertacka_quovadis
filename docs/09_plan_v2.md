# 09 – Plán V2 (zero-day a kaskáda B)

Stav k 2026-11-03: **DOHODNUTÉ** (autor práce potvrdil 2026-11-03 po konzultácii s vedúcou). Zapísané **pred**
akýmkoľvek výsledkom V2; pravidlá sa podľa výsledkov nemenia. Výsledky V1 (`docs/07`) ostávajú v platnosti
a uvádzajú sa celé.

## 1. Spresnenie téz (po konzultácii s vedúcou, 2026-11-03)
Pôvodné znenie téz v `docs/00` ostáva. Vedúca súhlasila, že tézy sa môžu mierne prispôsobiť a nemusia sa všetky
potvrdiť; nepotvrdenú tézu treba vysvetliť. Spresnenie podľa pôvodného zámeru autora:
- **„Hybridný prístup“ v tézach 1 a 2 = kaskáda** (viacstupňová kombinácia statického a dynamického modelu
  s hybridným modelom pri neistote/nezhode), nie samostatný hybridný model.
- **Téza 4** opisuje kaskádu B: najprv rýchly statický model, pri neistom skóre dynamická analýza, pri nezhode
  hybridný model.

## 2. Mapovanie téz na merania V2
| téza | porovnanie | kritérium (určené vopred) |
|---|---|---|
| 1. kaskáda presnejšia a stabilnejšia v zero-day | kaskády vs. samostatný statický, dynamický a hybridný model; vynechanie rodiny | TPR na vynechanej rodine (test), FPR na neškodných; stabilita = sm. odchýlka TPR cez 7 rodín |
| 2. kaskáda menej falošných poplachov pri zachovaní citlivosti | kaskády vs. samostatný statický a dynamický model | **spĺňa**, ak FPR kaskády < FPR statického aj dynamického **a** TPR kaskády ≥ TPR statického − 1 p. b. (test, prahy z validácie); vyhodnotí sa v časovom teste aj priemerne v zero-day |
| 3. destilovaný model rýchlejší s porovnateľnou presnosťou ako komplexný hybrid | študenti vs. dvojvetvová sieť (komplexný hybrid; doplnkovo vs. LightGBM hybrid) | CPU čas na vzorku (benchmark) a TPR na vynechanej rodine; „porovnateľná“ = rozdiel TPR ≤ 1 p. b. (rovnaká tolerancia ako pri téze 2) |
| 4. viacstupňová architektúra zníži náročnosť | kaskáda B vs. dynamický/hybridný model na každej vzorke a vs. kaskáda A | **hlavná miera: podiel súborov, ktoré treba emulovať**; doplnkovo CPU čas modelov; celkový čas s **predpokladom** 60 s emulácie na súbor (limit z `speakeasy-config.json`, nie meranie) |

## 3. Zero-day: vynechanie rodiny (leave-one-family-out)
- 7 behov, v každom sa jedna rodina malvéru odstráni z **tréningu aj validácie**; neškodné súbory ostávajú.
- Učené reprezentácie sa fitujú bez vynechanej rodiny: slovník n-gramov API a slovník sekvencií
  (`processed/dynamic/lofo/<rodina>/`), štandardizácia vstupu a mäkké označenia učiteľov v každom behu znova.
- **Hyperparametre sa preberajú z V1** (bez ladenia). Obmedzenie: ladenie vo V1 videlo validáciu so všetkými
  rodinami – uvedie sa v kapitole obmedzení.
- **Architektúry v kaskádach podľa výberu V1** (static/dynamic/hybrid = LightGBM); výber sa v behoch neopakuje,
  aby boli behy porovnateľné. Celý rebríček modelov sa vykáže ako doplnok.
- Hodnotenie:
  - **hlavné – aprílový test** (celý pôvodný test): TPR na vynechanej rodine, FPR na neškodných, celkové metriky;
    meria novú rodinu aj časový posun;
  - **doplnkové – januárové vzorky vynechanej rodiny** (jej vzorky z tréningu a validácie, ktoré model nevidel):
    iba TPR pri prahoch z validácie; meria novú rodinu bez časového posunu.

## 4. Kaskády vo V2
Všetky prahy z validácie (FPR ≤ 1 %), vyhodnotenie z uložených predikcií.

| variant | 1. stupeň | neisté / nezhoda | účel |
|---|---|---|---|
| A-main, A-nokd, A-modal, A-heavy, A-baselines | ako vo V1 | ako vo V1 | porovnateľnosť s V1 |
| **B-main** | statický študent (`mlp_kd`) | emulácia → dynamický študent; ak sa nezhodne so statickým → hybrid LightGBM | **hlavný variant (téza 4)** |
| B-direct | statický študent | rovno hybrid LightGBM | treba dynamický stupeň? |
| B-heavy | statický študent | dynamický študent → dvojvetvová sieť | s komplexným hybridom |
| B-baselines | statický LightGBM | dynamický LightGBM → hybrid LightGBM | treba študenta? |
| B-nokd | študent bez destilácie | ako B-main | prínos destilácie v kaskáde |
| B-twobranch | študent s učiteľom = dvojvetvová sieť | ako B-main | destilácia z komplexného učiteľa |

**Pásmo neistoty (hlavný pracovný bod, určené na validácii):**
- isto malvér: skóre statického modelu ≥ prah, pri ktorom má na validácii FPR ≤ 0,1 %,
- isto neškodný: skóre ≤ prah, pod ktorým leží najviac 1 % malvéru validácie,
- inak neisté → emulácia a druhý stupeň.

**Doplnková krivka:** pevné rozpočty emulácie 10 / 20 / 30 / 40 % – emulujú sa vzorky najbližšie prahu statického
modelu (vzdialenosť v log-odds), hranica vzdialenosti sa určí na validácii a použije na teste.

## 5. Destilácia – nový variant
Kontrola kódu V1: študent sa už vo V1 učil z log-odds učiteľa zmäkčených teplotou T (T ∈ [1; 8], ladené), takže
variant „destilácia z logitov“ netreba. Nový variant vychádza zo znenia tézy 3 („komplexný hybridný model“):
- `mlp_kd_twobranch` (statický aj dynamický študent): učiteľ = dvojvetvová sieť; mäkké označenia out-of-fold
  ako vo V1; hyperparametre študenta sa ladia raz na rozdelení V1 (30 pokusov, rovnaký priestor ako `mlp_kd`),
  v zero-day behoch sa preberajú.

## 6. Rozsah behu a výstupy
- `runs_v2/full/` – rozdelenie V1 (časový test): učiteľ dvojvetvová sieť, študenti `mlp_kd_twobranch`, ich benchmark,
  kaskády B na modeloch V1 (predikcie z `runs_final/`).
- `runs_v2/lofo/<rodina>/` – 7 zero-day behov: celý rebríček (static, dynamic, hybrid vrátane seq_cnn a two_branch),
  3 seedy, učitelia (hybrid, static, dynamic, two_branch), študenti (`mlp_kd`, `mlp_nokd`, `mlp_kd_modal`,
  `mlp_kd_twobranch`), kaskády A aj B.
- `runs_v2/comparison/v2/` – súhrn cez rodiny a vyhodnotenie téz podľa kritérií z bodu 2.
- Výpočtové nároky sa merajú raz (`runs_final/` a `runs_v2/full/`), v zero-day behoch nie (rovnaké modely).
- Odhad trvania (podľa časov V1): ~2,5–3 h na rodinu → 2–3 večery na pracovnom notebooku.

## 7. Otvorené (nie je súčasťou V2, iba ak zostane čas)
- Skutočné meranie času celej kaskády (spustenie modelov za sebou) namiesto súčtu benchmarkov komponentov.
