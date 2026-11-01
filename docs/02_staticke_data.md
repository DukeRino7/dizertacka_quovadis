# 02 – Spoločné rozdelenie a predspracovanie statických dát

Stav k 2026-11-01. Čísla sú prevzaté z generovaných výstupov `processed/index/README.md`
a `processed/static/STATISTICS.md`. Pri zmene konfigurácie sa tieto súbory vytvoria znova; tento
dokument treba potom aktualizovať podľa nich.

## Spoločné rozdelenie (pre všetky modely)
Postup (`src/data/build_index.py`, `configs/data/index.yaml`):
1. Katalóg EMBER s kontrolou integrity; vynechaných 366 súborov so zlyhanou extrakciou EMBER.
2. Prekryv pôvodného train/test podľa SHA-256 (446 keyloggerov): vyradené z tréningu, test ostáva pôvodný. **NÁVRH.**
3. Validácia vyčlenená z pôvodného tréningu: 10 % (**NÁVRH**), `StratifiedGroupKFold` – stratifikácia
   podľa rodiny, vzorky s identickým EMBER vektorom (131 skupín, 268 vzoriek) vždy v rovnakej časti, seed 42.
4. Pôvodný časový test (apríl 2022) bez zmeny; tréning a validácia z januára 2022.
5. Každá vzorka v indexe má v zozname súborov Speakeasy report s rovnakým SHA-256 a rovnakou rodinou.

| Časť | Vzorky | Benign | Malware | Podiel malvéru |
|---|---:|---:|---:|---:|
| train | 66 831 | 21 974 | 44 857 | 0,671 |
| validácia | 7 426 | 2 442 | 4 984 | 0,671 |
| test | 17 339 | 7 940 | 9 399 | 0,542 |

## Predspracovanie statických dát
Postup (`src/data/build_static.py`, `configs/data/static.yaml`):
- Riadky pôvodných matíc mapované podľa indexu z `hashes.txt`; uložené po častiach ako float32 `.npy`
  s metadátami (SHA-256, rodina, označenie) v rovnakom poradí.
- Kontroly: žiadne NaN ani ±Inf; zhoda s pôvodnými dátami overená na 600 náhodných riadkoch (odchýlka 0).
- Uložené sú **pôvodné hodnoty** príznakov. Učené transformácie (odstránenie konštantných stĺpcov,
  signed log1p, štandardizácia) sú pripravené v `src/data/static_transforms.py` a fitujú sa až v experimente
  iba na tréningu. Stromové modely ich nepotrebujú.
- Bez výberu príznakov, bez vyvažovania tried, bez úprav testu.

## Hlavné zistenia o dátach (popisné)
- 2381 príznakov v 9 skupinách (EMBER v2). Na tréningu je 62 príznakov konštantných a 172 takmer
  konštantných (najčastejšia hodnota ≥ 99,9 % vzoriek).
- Mnohé skupiny majú ťažké chvosty (napr. veľkosti, adresy) → pre lineárne modely a neurónové siete log-transformácia.
- **Posun train → test je zreteľný**: medián KS štatistiky po skupinách 0,07–0,11 pri histogramoch,
  reťazcoch, všeobecných príznakoch a dátových adresároch, oproti ≈ 0,01 pri náhodnej validácii.
  Najväčší posun má `header_coff_timestamp` (čas zostavenia, KS 0,24).
- Zloženie tried sa medzi tréningom a testom mení (podiel malvéru 0,671 → 0,542; napr. dropper 11 % → 1,5 %,
  rat 2,3 % → 7,3 %). Metriky na teste treba interpretovať s ohľadom na tento posun; vhodné sú metriky
  necitlivé na pomer tried (ROC-AUC, TPR pri pevnom FPR) popri accuracy/F1.

## Obmedzenie dôležité pre porovnanie výpočtových nárokov
Pôvodné PE súbory nie sú k dispozícii, preto nemožno zmerať čas extrakcie EMBER príznakov ani čas
emulácie Speakeasy. Merania inferencie v projekte pokrývajú iba časť od hotových vstupov po rozhodnutie.
Pozri otvorenú otázku v `docs/01_audit_dat.md`.
