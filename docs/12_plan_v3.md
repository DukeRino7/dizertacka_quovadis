# 12 – Plán V3 (druhý stupeň pre neisté súbory, prekalibrovanie prahu)

Stav k 2026-11-04: **ROZHODNUTÉ autorom práce** (2026-11-04), s vedúcou sa ešte neprerokovalo. Zapísané **pred**
akýmkoľvek výsledkom V3; pravidlá sa podľa výsledkov nemenia. Výsledky V1 (`docs/07`) a V2 (`docs/10`) ostávajú
v platnosti a uvádzajú sa celé. V3 ich nenahrádza, ale dopĺňa.

## 1. Na základe čoho sa V3 navrhla
V2 potvrdila tézy 2 a 4 iba pre kaskády z LightGBM, tézu 3 čiastočne a tézu 1 nepotvrdila (`docs/10`, oddiel 4).
Aby sa ďalší krok neurčoval odhadom, urobila sa analýza príčin z uložených predikcií V2 (`docs/10`, oddiel 6;
`runs_v2/comparison/v2/ANALYSIS.md`). Zistenia, ktoré rozhodli o obsahu V3:

| zistenie (zero-day, priemer cez 7 rodín) | číslo | dôsledok pre V3 |
|---|---|---|
| strop každej kombinácie statického a dynamického **rozhodnutia** („S alebo D“) | TPR 0,792 → 0,798 | kombinovať hotové rozhodnutia nemá zmysel → nové kaskádové pravidlá nad súčasnými modelmi sa nerobia |
| statický model nové rodiny zoraďuje správne | ROC-AUC 0,974 (6 zo 7 rodín ≥ 0,99) | informácia v statických príznakoch je, chýba správne rozhodnutie |
| prah z validácie dáva na teste FPR iba 0,5 % namiesto 1 % | orákulum pri FPR 1 % na teste: TPR 0,838 | **C:** obnoviť pracovný bod bez malvéru z nového obdobia |
| rozpočet 10 % eskaluje takmer všetky chyby statického modelu | 94,6 % chýb eskalovaných | eskalácia funguje, nemení sa |
| druhý stupeň v eskalovanej oblasti chyby nevyrieši | 0,792 oproti hornej hranici 0,963 | **B:** druhý stupeň učený práve pre túto oblasť |
| hybrid LightGBM (učený na všetkom) sa v eskalovanej oblasti správa ako statický model | ROC-AUC 0,902 oproti 0,914 | špecialista sa učí **iba** na súboroch blízko prahu, aby sa nemohol oprieť len o statické príznaky „ľahkých“ súborov |
| pri keyloggeri je v eskalovanej oblasti dynamický model lepší | 0,727 oproti 0,539 | variant špecialistu, ktorý musí použiť dynamické príznaky |

Zvážené a **zamietnuté** možnosti:
- **Nová téza:** netreba. Analýza vysvetľuje, prečo téza 1 nevyšla (strop +0,6 p. b.); zmenu znenia téz rieši autor
  s vedúcou (`docs/11`, oddiel 7), nie experiment.
- **Lepšie dynamické príznaky** (udalosti, súhrn reportu): obmedzuje ich chyba emulátora v dátach (`unsupported_api`
  v 52 % testu, docs/04) a podľa analýzy by pomohli najmä keyloggeru. Prínos je neistý a nesúvisí s hlavnou stratou.
- **Ladenie pásma neistoty alebo rozpočtu podľa testu:** porušilo by pravidlá (test sa nepoužíva na ladenie).
- **Lepší statický študent ako 1. stupeň:** V2 ukázala, že LightGBM ako 1. stupeň je lepší a študent je 3,5× drahší
  než lacný LightGBM (docs/07); vylepšovanie študenta neodpovedá na zistené príčiny.

**Riziko, ktoré treba uviesť v práci:** návrh V3 vychádza z analýzy testu V2, takže V3 nie je nezávislým potvrdením.
Zmierňuje sa to takto:
- kritériá sú zapísané vopred;
- počet variantov je malý a pevný, beh je jeden bez opakovania;
- výsledky sa vykazujú vždy;
- doplnkovo sa hodnotí na januárových vzorkách vynechanej rodiny, ktoré pri analýze nerozhodovali.

## 2. B – druhý stupeň učený iba na neistých súboroch („špecialista“)
### Postup
1. **1. stupeň:** statický LightGBM (vybraný vo V1). Prah z validácie (FPR 1 %).
2. **Eskalácia:** rozpočet 10 % ako v docs/09. Emulujú sa súbory, ktorých skóre statického modelu je najbližšie prahu
   (vzdialenosť v log-odds). Hranica vzdialenosti je kvantil 10 % na validácii a na teste sa nemení.
   Pásmo z prahov sa nepoužije: V2 ukázala, že pri LightGBM je príliš úzke (docs/10, oddiel 5).
3. **Tréningové dáta špecialistu:** tréningové súbory daného behu (bez vynechanej rodiny), ktorých **OOF skóre**
   statického LightGBM (`teachers/static_lightgbm/*/train_oof.parquet`, model súbor pri tréningu nevidel) leží
   najbližšie prahu.
   - Vyberie sa **20 % tréningu**. Je to širšie ako 10 %, lebo na teste sa pri rozpočte 10 % eskaluje ~22 % súborov.
   - Citlivostne sa vyhodnotí aj 10 % a 40 %. Uvedie sa to ako citlivosť, nie ako výber.
4. **Špecialista:** LightGBM s hyperparametrami hybridného LightGBM z V1 (bez ladenia), 3 seedy, váhy tried ako v protokole.
   Early stopping na validačných súboroch v tej istej oblasti (skóre finálneho statického modelu, rovnaká hranica).
   - **B-spec (hlavný):** vstup = statické + dynamické príznaky + log-odds skóre statického modelu.
   - **B-spec-dyn:** vstup = dynamické príznaky + log-odds skóre statického modelu. Model musí použiť dynamiku;
     odpovedá na to, či sa správanie oplatí pri neistých súboroch.
5. **Rozhodnutie:** neeskalované súbory rozhodne statický model svojím prahom, eskalované rozhodne špecialista.
   Prah špecialistu sa určí na validácii tak, aby mala **celá kaskáda na validácii FPR ≤ 1 %** (rovnaké pravidlo ako
   pri všetkých modeloch).
6. Doplnkovo sa vykáže celá krivka rozpočtu 10 / 20 / 30 / 40 % (s tým istým špecialistom).

### Rozsah
- **Časový test** (rozdelenie V1): komponenty a OOF skóre z `runs_final`.
- **Zero-day:** 7 rodín, komponenty a OOF skóre z `runs_v2/lofo/<rodina>`; dynamické príznaky bez vynechanej rodiny
  (`processed/dynamic/lofo/<rodina>`).
- **Referencie na rovnakých dátach:** statický LightGBM, hybrid LightGBM, B-baselines s rozpočtom 10 % (najlepšia
  kaskáda V2). TPR vynechanej rodiny pre B-baselines s rozpočtom 10 % sa dopočíta z uložených predikcií
  (vo V2 sa neukladalo).

### Kritériá (určené vopred)
| | kritérium | test |
|---|---|---|
| **B1 – téza 1** | priemerné TPR vynechanej rodiny ≥ statický LightGBM **+ 1 p. b.**, FPR ≤ FPR statického a B-spec ≥ statický aspoň v 5 zo 7 rodín | zero-day, apríl |
| **B2 – téza 2** | FPR < FPR statického aj dynamického **a** TPR ≥ TPR statického − 1 p. b. (ako docs/09) | časový aj zero-day |
| **B3 – prínos oproti V2** | TPR vynechanej rodiny ≥ B-baselines (rozpočet 10 %) + 1 p. b. pri FPR nie vyššom o viac ako 0,1 p. b. | zero-day, apríl |
| doplnkovo | TPR vynechanej rodiny na januárových vzorkách; stabilita = sm. odchýlka cez rodiny; podiel emulovaných súborov; CPU čas | – |

Ak B1 nevyjde, téza 1 ostáva nepotvrdená a výsledok sa uvedie ako ďalší dôkaz, že rozhodnutie v neistej oblasti
sa z týchto dát nedá zlepšiť.

## 3. C – prekalibrovanie prahu na nových neškodných súboroch (samostatný scenár)
**Zdôvodnenie:** v praxi sa nový legitímny softvér zbiera ľahko, nový malvér a jeho označenie nie. Kalibrácia preto
používa **iba neškodné súbory** z testovacieho obdobia. O vynechanej rodine sa model nič nedozvie, takže zero-day
tvrdenie ostáva platné. Ide o **iný scenár** (prevádzka s priebežne zbieranými neškodnými súbormi) a vykazuje sa
**oddelene**; hlavné výsledky V1/V2/V3 sa nemenia.

### Postup
1. Neškodné súbory aprílového testu (7 940) sa náhodne rozdelia (podľa skupín identických EMBER vektorov) na
   **kalibračnú** a **hodnotiacu** časť. Všetok malvér ide do hodnotenia.
2. Veľkosť kalibračnej časti: **1 %, 5 %, 20 %** neškodných (≈ 79, 397, 1 588 súborov); **10 náhodných rozdelení**
   pre každú veľkosť. Výsledok = priemer ± sm. odchýlka.
3. Prah každého modelu (a každého komponentu kaskády) sa nastaví tak, aby mal na kalibračnej časti **FPR 1 %**
   (rovnaký cieľ ako pri validácii). **Eskalácia kaskády B (rozpočet) ostáva z validácie**, mení sa iba prah rozhodnutia.
4. Porovnanie na **tej istej hodnotiacej časti:** prahy z validácie oproti prekalibrovaným prahom.
5. Rozsah: statický, dynamický, hybrid LightGBM, dvojvetvová sieť, kaskády A-main a A-baselines, kaskády B-main,
   B-baselines (rozpočet 10 %) a kaskády V3 (B-spec, B-spec-dyn); časový test aj 7 zero-day behov.

### Kritériá a vykazovanie
- Hlavná veličina: zmena TPR vynechanej rodiny (zero-day) a TPR všetkého malvéru (časový test) a skutočné FPR na
  hodnotiacej časti, podľa veľkosti kalibračnej časti.
- Téza 2 sa v tomto scenári vyhodnotí znova rovnakým kritériom (referencie sú tiež prekalibrované).
- Očakávanie podľa orákula (docs/10, 6.2), **nie kritérium úspechu:** statický LightGBM TPR vynechanej rodiny ~0,84
  pri FPR ~1 %. Uvedie sa, o koľko sa skutočný výsledok od horného odhadu líši.
- Obmedzenie: pri 79 kalibračných súboroch je prah pre FPR 1 % určený ~1 súborom, preto sa očakáva veľký rozptyl.
  Práve to sa má ukázať (koľko neškodných súborov treba).

## 4. Výpočty a výstupy
- **B** vyžaduje tréning: špecialisti 2 varianty × 3 seedy × 8 behov (časový + 7 rodín), plus citlivosť 10 % a 40 %
  pre B-spec. Tréningové dáta tvorí ~20 % tréningu, odhad je ~1–2 h. Spustenie:
  - technická kontrola na súkromnom notebooku (rodina rat);
  - plný beh na pracovnom notebooku, aby boli merania CPU času z rovnakého počítača ako V1 a V2.
- **C** sa počíta iba z uložených predikcií (`runs_final`, `runs_v2`, `runs_v3`), bez tréningu.
- Výstupy:
  - `runs_v3/full/` a `runs_v3/lofo/<rodina>/` – špecialisti a kaskády;
  - `runs_v3/comparison/v3/` – súhrn B, scenár C a vyhodnotenie kritérií;
  - dokument `docs/13_vysledky_v3.md`.

## 5. Čo sa nemení
- Dáta, rozdelenie, modely V1/V2, ich hyperparametre a prahy z validácie.
- Pravidlo výberu (TPR pri FPR 1 % na validácii) a zákaz ladenia na teste.
- Výsledky V1 a V2 sa uvádzajú celé vrátane nepotvrdených téz.
