# 04 – Dynamické (Speakeasy) dáta

Stav k 2026-11-01 (večer): **dataset stiahnutý, audit hotový, dynamické dáta pripravené** (`processed/dynamic/`).
Revízia datasetu: `fc2e98fac0b4d43a5557ccab70c877af6cce9f4d` (`configs/data/dynamic.yaml`).

## Výsledky auditu tréningu (processed/dynamic/audit/AUDIT.md)
- Stiahnutých 92 406 / 92 406 súborov (veľkosti zhodné so zoznamom HF); **každá z 91 596 vzoriek indexu má report**
  s rovnakým SHA-256 a rodinou; všetky reporty sa načítali (žiadny poškodený).
- **Test bol pravdepodobne emulovaný inou verziou/nastavením Speakeasy** (odhad z dát, autori to neuvádzajú):
  ukončenie emulácie `unsupported_api` 0,0 % train / 0,0 % val / **54,6 % test**; iné názvy chýb
  („Invalid memory read (UC_ERR_READ_UNMAPPED)“ v train vs. „invalid_read“ v teste); vzorky s udalosťami: benign
  59 % train vs. 11 % test, malware 50 % vs. 32 % (v tréningu má udalosti častejšie benign, v teste malware).
- Malé reporty (≤ 5 volaní): ransomware 42 % train vs. 1,9 % test, dropper 22,6 % vs. 0,4 %; krátke postupnosti
  sú takmer výlučne pre jednu rodinu (riziko skratky).
- Slovník API na tréningu: 2 722 rôznych API, 1 099 v aspoň 5 vzorkách.

## Rozhodnutia (DOHODNUTÉ 2026-11-01, z princípu – nie podľa výsledkov)
1. **Hlavná reprezentácia = iba API volania** (n-gramy / postupnosti); udalosti a súhrnné počty (chyby emulácie,
   počty volaní, vlákien) sa vynechávajú – nesú stopu inej verzie emulátora. Výber podľa validácie by bol pasca
   (validácia je z rovnakej verzie emulátora ako tréning, artefakt v nej nevidno).
2. **Kontrolný experiment** `configs/dynamic_ablations/*_full` (reprezentácia vrátane udalostí a súhrnu,
   `processed/dynamic/tabular_full`, hyperparametre z hlavného modelu) – kvantifikuje vplyv artefaktu (iba popisne).
3. **Malé reporty sa ponechávajú** (skutočný výsledok emulácie; vyradenie by zmenilo spoločné rozdelenie);
   vo výsledkoch sa vyhodnotia zvlášť.
4. Vyhodnocuje sa validácia (bez posunu) aj test (časový posun + zmena nástroja) – kapitola obmedzení;
   úplne sa artefaktu zbaviť nedá (pri `unsupported_api` je postupnosť v teste kratšia).

## Pripravené dáta
- cache: 91 596 vzoriek, ~19 mil. API volaní (dĺžky zhodné s auditom),
- `tabular`: 2 000 n-gramov API (449 jednotlivých volaní, 1 551 dvojíc); `tabular_full`: + 15 typov udalostí + 9 súhrnných počtov,
- `sequence`: slovník 1 101 API, max. 1 024 volaní (orezaných iba 0,13 % vzoriek).

## Overený formát reportu (kontrola na testovacej časti)
- Súbor = JSON **zoznam vstupných bodov**; README datasetu opisuje iný tvar (`{"sha256", "entry_points"}`), ten v dátach nie je.
  SHA-256 je iba v názve súboru.
- Typy vstupných bodov: `module_entry`, `thread`, `tls_callback_N`; jedna vzorka môže mať aj vyše 100 vstupných bodov.
- API volanie: `pc`, `api_name`, `args` (vždy reťazce), `ret_val`. Názvy modulov majú rôznu veľkosť písmen
  (`kernel32` aj `KERNEL32`) → normalizácia na malé písmená.
- Voliteľné udalosti: `registry_access`, `file_access`, `network_events`, `process_events`, `dropped_files`, `handled_exceptions`.
- `error` = `{}` alebo popis ukončenia emulácie (`unsupported_api`, `max_api_count`, neplatný prístup do pamäte, ...).

## Popisné pozorovania na teste (nie podklad pre rozhodnutia)
- Emulácia `module_entry` končí chybou/limitom v 63–82 % vzoriek každej rodiny; najčastejšie `unsupported_api`
  (emulátor nepozná volanú funkciu) a `max_api_count` (limit 500 volaní).
- Limit 500 volaní dosiahne 42 % backdoorov, ale iba ~4 % benígnych súborov → **možný artefakt** (sledovať na tréningu).
- Malé reporty (≤ 5 volaní) sú v teste zriedkavé (0,4–6 % podľa rodiny); typicky jediné `VirtualAlloc(PAGE_EXECUTE_READWRITE)`
  – zbalená vzorka, emulácia skončila na začiatku. Na tréningu bolo zo zoznamu súborov podozrenie na 25 % malých
  ransomware reportov → **overiť auditom tréningu**.

## Postup spracovania (kód v `src/data/`)
| Krok | Modul | Výstup | Učí sa? |
|---|---|---|---|
| 1. audit | `audit_dynamic.py` | `processed/dynamic/audit/` (AUDIT.md, súhrn reportov, slovník API z tréningu, grafy) | nie |
| 2. normalizovaná cache | `build_dynamic.py` | `processed/dynamic/cache/<časť>.parquet` (+ `_args`) | nie |
| 3. pevný vektor pre rebríček | `build_dynamic_tabular.py` + `dynamic_features.py` | `processed/dynamic/tabular/` | slovník n-gramov iba z tréningu |

Reprezentácia pre spoločný rebríček (**NÁVRH**, `configs/data/dynamic.yaml`, potvrdiť po audite tréningu):
1- a 2-gramy postupnosti API volaní celej vzorky (top 2000 podľa dokumentovej frekvencie na tréningu, min. 5 vzoriek),
počty udalostí podľa typu, súhrnné príznaky reportu; surové počty (log a škálovanie robí model).
Argumenty volaní sa v rebríčku nepoužívajú; sú v cache pre sekvenčný model vrstvy B.

Hybrid (spoločný rebríček) = spojenie statického a dynamického vektora (ranná fúzia), `src/data/providers.py`.

## Otvorené rozhodnutia (po audite tréningu)
- čo s neúspešnými/malými reportmi (ponechať ako reálny výsledok emulácie, označiť príznakom, alebo vylúčiť –
  vylúčenie by zmenilo spoločné rozdelenie, preto by platilo pre všetky prístupy),
- veľkosť slovníka a rozsah n-gramov,
- či zahrnúť súhrnné príznaky, ktoré môžu niesť artefakty emulácie (počet volaní, chyby, dosiahnutý limit) –
  návrh: ponechať a overiť kontrolným experimentom ako pri statických dátach.

## Spustenie
`scriptsun_dynamic.ps1` (overenie dát, audit, príprava, dynamické modely, kontrolné experimenty) a
`scriptsun_hybrid.ps1` (hybridné modely). Všetky typy modelov boli na skutočných dátach overené v skúšobnom režime.
